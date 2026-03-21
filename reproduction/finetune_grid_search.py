import json
import itertools
import subprocess
import os
import copy
import csv
import time
import logging
import re
import pandas as pd

cur_dir = os.getcwd()
father_dir = os.path.abspath(os.path.join(cur_dir, '..'))
os.chdir(father_dir)

def load_config(path):
    with open(path, "r") as f:
        return json.load(f)


def save_config(cfg, path):
    with open(path, "w") as f:
        json.dump(cfg, f, indent=4)


def generate_combinations(search_space):
    keys = list(search_space.keys())
    values = list(search_space.values())
    combos = list(itertools.product(*values))
    return keys, combos


def get_available_gpu(min_vram_mb, max_utilization, logger):
    try:
        cmd = "nvidia-smi --query-gpu=index,memory.free,utilization.gpu --format=csv,nounits,noheader"
        result = subprocess.check_output(cmd, shell=True).decode('utf-8').strip().split('\n')
        for line in result:
            idx, free_mem, util = line.split(', ')
            idx, free_mem, util = int(idx), int(free_mem), int(util)
            if free_mem >= min_vram_mb and util <= max_utilization:
                return idx
        return -1
    except Exception as e:
        logger.error(f"Failed to fetch GPU info via nvidia-smi: {e}")
        return 0


def wait_for_gpu(min_vram_mb, max_utilization, check_interval, logger):
    gpu_id = get_available_gpu(min_vram_mb, max_utilization, logger)
    if gpu_id != -1:
        return gpu_id
    logger.info(f"All GPUs are busy. Waiting for >{min_vram_mb}MB free VRAM...")
    while True:
        time.sleep(check_interval)
        gpu_id = get_available_gpu(min_vram_mb, max_utilization, logger)
        if gpu_id != -1:
            logger.info(f"GPU {gpu_id} is now available!")
            return gpu_id


def extract_metrics_from_log(log_path):

    test_mae, test_r2 = "N/A", "N/A"
    if not os.path.exists(log_path):
        return test_mae, test_r2

    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()

    test_match = re.search(r"Test MAE when got best validation result:\s*([0-9.]+),\s*R2:\s*([-0-9.]+)", content)
    if test_match:
        test_mae = test_match.group(1)
        test_r2 = test_match.group(2)

    return test_mae, test_r2




def run_grid_search(base_config, search_space, min_vram_mb=5000, max_utilization=30, check_interval=30):

    config_name = os.path.splitext(os.path.basename(base_config))[0]
    base_out_dir = f"./reproduction/7_finetune_results/{config_name}"
    output_dir = f"{base_out_dir}/grid_configs"
    exp_log_dir = f"{base_out_dir}/experiment_logs"
    model_save_base_dir = f"{base_out_dir}/model_path"
    results_file = f"{base_out_dir}/results.csv"
    main_log_file = f"{base_out_dir}/grid_search.log"

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(exp_log_dir, exist_ok=True)
    os.makedirs(model_save_base_dir, exist_ok=True)

    logger = logging.getLogger(config_name)
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    fh = logging.FileHandler(main_log_file, mode='a', encoding='utf-8')
    fh.setFormatter(formatter)
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(sh)

    base_cfg = load_config(base_config)
    keys, combos = generate_combinations(search_space)
    logger.info("==========================================================================")
    logger.info(f"Started Grid Search for '{config_name}'. Total experiments: {len(combos)}")
    logger.info("==========================================================================")

    if not os.path.exists(results_file):
        with open(results_file, mode="w", newline="") as f:
            writer = csv.writer(f)
            header = ["experiment_id", "gpu_used"] + keys + ["status", "test_mae", "test_r2", "timestamp"]
            writer.writerow(header)

    all_results = []

    for i, combo in enumerate(combos):
        cfg = copy.deepcopy(base_cfg)
        param_tags = []

        for k, v in zip(keys, combo):
            if k == "learning_rate":
                if "optimizer" not in cfg: cfg["optimizer"] = {}
                cfg["optimizer"]["learning_rate"] = v
                param_tags.append(f"lr{v}")
            elif k in ["batch_size", "train_ratio", "valid_ratio", "seed"]:
                if "data" not in cfg: cfg["data"] = {}
                cfg["data"][k] = v
                if k == "batch_size":
                    param_tags.append(f"bs{v}")
                elif k == "train_ratio":
                    param_tags.append(f"tr{v}")
                elif k == "valid_ratio":
                    param_tags.append(f"vr{v}")
                elif k == "seed":
                    param_tags.append(f"seed{v}")
            elif k == "warmup_step":
                if "scheduler" not in cfg: cfg["scheduler"] = {}
                cfg["scheduler"]["warmup_step"] = v
                param_tags.append(f"warmup{v}")
            elif k == "tag":
                if "others" not in cfg: cfg["others"] = {}
                cfg["others"]["tag"] = v
            else:
                cfg[k] = v
                param_tags.append(f"{k}{v}")

        param_str = dict(zip(keys, combo))
        logger.info(f"--- Preparing Experiment {i}/{len(combos) - 1} ---")
        logger.info(f"Parameters: {param_str}")

        target_gpu = wait_for_gpu(min_vram_mb, max_utilization, check_interval, logger)
        if "others" not in cfg: cfg["others"] = {}
        cfg["others"]["device"] = f"cuda:{target_gpu}"

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        param_prefix = "_".join(param_tags)

        unique_name_log = f"exp{i}_{param_prefix}_{timestamp}"
        unique_name_json = f"exp{i}_{timestamp}"

        cfg_path = os.path.join(output_dir, f"{unique_name_json}.json")
        exp_log_path = os.path.join(exp_log_dir, f"{unique_name_log}.log")

        current_model_save_dir = os.path.join(model_save_base_dir, unique_name_json)
        if "model" not in cfg:
            cfg["model"] = {}
        cfg["model"]["save_dir"] = current_model_save_dir

        save_config(cfg, cfg_path)

        cmd = f"python train_model.py --config_json {cfg_path}"

        logger.info(f"Allocated GPU {target_gpu} for experiment {i}.")
        logger.info(f"Config file saved at: {cfg_path}")
        # logger.info(f"Weights will be saved at: {current_model_save_dir}")
        logger.info(f"To reproduce this run manually, use:")
        logger.info(f"$  python train_model.py --config_json {cfg_path}")
        logger.info(f"To monitor training progress, run in new terminal:")
        logger.info(f"$  tail -f {exp_log_path}")

        status = "Failed"
        with open(exp_log_path, "w", encoding="utf-8") as exp_log_file:
            try:
                subprocess.run(cmd, shell=True, check=True, stdout=exp_log_file, stderr=subprocess.STDOUT)
                status = "Success"
                logger.info(f"Experiment {i} completed successfully.")
            except subprocess.CalledProcessError:
                logger.error(f"Experiment {i} FAILED. Check '{exp_log_path}' for details.")

        test_mae, test_r2 = extract_metrics_from_log(exp_log_path)

        if status == "Success" and test_mae != "N/A":
            logger.info(f"Test MAE when got best validation result: {test_mae}, R2: {test_r2}")

        with open(results_file, mode="a", newline="") as f:
            writer = csv.writer(f)
            row_data = [i, target_gpu] + list(combo) + [status, test_mae, test_r2, timestamp]
            writer.writerow(row_data)

        run_record = {
            "exp_id": i,
            "status": status,
            "test_mae": test_mae,
            "test_r2": test_r2,
            "timestamp": timestamp
        }

        run_record.update(param_str)

        all_results.append(run_record)

    logger.info("==========================================================================")
    logger.info(f"All experiments finished! Check '{results_file}' for summary.")

    df = pd.DataFrame(all_results)

    df['test_mae'] = pd.to_numeric(df['test_mae'], errors='coerce')
    df['test_r2'] = pd.to_numeric(df['test_r2'], errors='coerce')

    sorted_df = df.sort_values(by='test_mae', ascending=True, na_position='last').reset_index(drop=True)

    sorted_df = sorted_df.fillna("N/A")

    return sorted_df


if __name__ == "__main__":

    CONFIG = "./config/Test/sulfoxonium_seed68909_parameters.json"
    SPACE = {
        "train_ratio": [0.8], # 0.7
        "valid_ratio": [0.2], # 0.3
        "seed": [42],
        "tag": [f"seed{42}"],
        "learning_rate": [0.4, 0.5],
        "batch_size": [32, 64],
        "warmup_step": [3000],
    }

    min_vram_mb = 2000
    max_utilization = 100
    check_interval = 30

    best_results_df = run_grid_search(base_config=CONFIG, search_space=SPACE, min_vram_mb=min_vram_mb, max_utilization=max_utilization)

    print("\n\n" + "*" * 80)
    print("Grid Search Top Results (Sorted by Test MAE)")
    print("*" * 80)

    # pd.options.display.max_columns = None
    # pd.options.display.max_columns = None
    # pd.options.display.width = 1000

    print(best_results_df.to_string())
    print("*" * 80 + "\n")
