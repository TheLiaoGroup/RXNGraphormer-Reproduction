# RXNGraphormer Reproduction
This repository provides a **reproduction** of [🔗 RXNGraphormer](https://github.com/licheng-xu-echo/RXNGraphormer), a unified pre-trained framework for reaction performance prediction and synthesis planning. The original work is by Xu et al.

This reproduction focuses on validating core functionalities, reaction-type analysis, and extending evaluation to external literature datasets.

---

## 📁 Directory Structure

```
RXNGraphormer/reproduction/
├── 1_basic_usage.ipynb           # Basic model usage and embedding generation
├── 2_Reaction_Type_Visual.ipynb  # Reaction type clustering and visualization (HDBSCAN)
├── 3_regression.sh               # Script for regression task training (yield, selectivity)
├── 4_USPTO.sh                    # Script for USPTO-style sequence generation tasks
├── 5_SPR.ipynb                   # Structure-performance relationship analysis
├── 6_test.ipynb                  # External validation on real-world HTE and literature datasets
└── README.md
```

---

## 🗂️ Project Organization Update

For better reproducibility, the internal directory structures of `config`, `dataset`, and `model_path` have been reorganized compared to the original repository.

---

## ⚙️ Reproduction Setup

This reproduction uses the **original pre-trained model** weights; we only perform fine-tuning on downstream tasks (e.g., yield, selectivity prediction).  
For sequence generation tasks, models are fine-tuned on USPTO-50k and USPTO-480k, while the **USPTO-full model is evaluated without retraining**.  

All training logs and checkpoints are saved under corresponding subdirectories in `model_path/`.

```bash
# Install the additional dependency for reaction-type clustering
pip install hdbscan
```

> ✅ `hdbscan` is used in `2_Reaction_Type_Visual.ipynb` for unsupervised clustering of reaction embeddings.

---

## 📦 Datasets and Training Artifacts

- **For all datasets (`USPTO_STEREO`, `USPTO_full`, `USPTO_480k`, `USPTO_50k`, `OOS`, `external_validation_dataset`, and `50k_with_rxn_type`,`bechmark`)**:  
  Download from the [original model's Figshare repository](https://figshare.com/s/decc64a868ab64a93099).  
  These preprocessed datasets are part of the original RXNGraphormer release.

- **For `Test.zip`**:  
  Download from [our Figshare repository](https://doi.org/10.6084/m9.figshare.30498368.v2).  
  This test set contains **newly curated real-world reaction data** from literature and high-throughput experimentation (HTE) for external validation.

> **Note**:  
> - All **model checkpoints, training logs, and evaluation results** are available in **our Figshare repository** and correspond to our independent reproduction runs.  
> - Please follow the dataset directory structure outlined below after extraction.  
> - 💡 This ensures full reproducibility of all experiments presented in the `reproduction/` notebooks and scripts.

---

## 🧪 What This Reproduction Covers

- ✅ Basic inference and embedding generation  
- ✅ Reaction type classification and unsupervised clustering  
- ✅ Regression tasks (yield, regioselectivity, enantioselectivity)  
- ✅ Sequence generation (forward/retro-synthesis) on USPTO dataset   
- ✅ Structure-performance relationship (SPR) analysis  
- ✅ External validation on real-world HTE or literature datasets

---

## 📊 Experiment Results

### Regression Performance Comparison
The following table summarizes the performance comparison between the original **RXNGraphormer** and this **Reproduction** across benchmark, out-of-sample (OOS), and external datasets.

<table border="1" cellpadding="0" cellspacing="0">
  <tr>
    <td colspan="3" rowspan="2" align="center"><b>Data</b></td>
    <td colspan="4" align="center"><b>RXNGraphormer</b></td>
    <td colspan="4" align="center"><b>Reproduction</b></td>
  </tr>
  <tr>
    <td>R<sup>2</sup></td>
    <td>MAE</td>
    <td>Precision</td>
    <td>ACC</td>
    <td>R<sup>2</sup></td>
    <td>MAE</td>
    <td>Precision</td>
    <td>ACC</td>
  </tr>
  <tr>
    <td colspan="2" rowspan="4">Benchmark datasets</td>
    <td>Buchwald–Hartwig</td>
    <td>0.971</td>
    <td>2.980</td>
    <td>/</td>
    <td>/</td>
    <td>0.970±0.003</td>
    <td>3.079±0.144</td>
    <td>/</td>
    <td>/</td>
  </tr>
  <tr>
    <td>Suzuki–Miyaura</td>
    <td>0.876</td>
    <td>6.300</td>
    <td>/</td>
    <td>/</td>
    <td>0.871±0.009</td>
    <td>6.431±0.187</td>
    <td>/</td>
    <td>/</td>
  </tr>
  <tr>
    <td>C–H functionalization</td>
    <td>0.992</td>
    <td>0.266</td>
    <td>/</td>
    <td>/</td>
    <td>0.992±0.001</td>
    <td>0.273±0.007</td>
    <td>/</td>
    <td>/</td>
  </tr>
  <tr>
    <td>Asymmetric thiol</td>
    <td>0.915</td>
    <td>0.134</td>
    <td>/</td>
    <td>/</td>
    <td>0.916±0.010</td>
    <td>0.135±0.007</td>
    <td>/</td>
    <td>/</td>
  </tr>
  <tr>
    <td rowspan="11">OOS</td>
    <td rowspan="8">Buchwald Hartwig</td>
    <td>Additive 1</td>
    <td>0.883</td>
    <td>6.430</td>
    <td>/</td>
    <td>/</td>
    <td>0.815</td>
    <td>8.310</td>
    <td>/</td>
    <td>/</td>
  </tr>
  <tr>
    <td>Additive 2</td>
    <td>0.906</td>
    <td>6.000</td>
    <td>/</td>
    <td>/</td>
    <td>0.897</td>
    <td>6.280</td>
    <td>/</td>
    <td>/</td>
  </tr>
  <tr>
    <td>Additive 3</td>
    <td>0.792</td>
    <td>8.500</td>
    <td>/</td>
    <td>/</td>
    <td>0.651</td>
    <td>10.399</td>
    <td>/</td>
    <td>/</td>
  </tr>
  <tr>
    <td>Additive 4</td>
    <td>0.736</td>
    <td>9.940</td>
    <td>/</td>
    <td>/</td>
    <td>0.643</td>
    <td>10.966</td>
    <td>/</td>
    <td>/</td>
  </tr>
  <tr>
    <td>Bromide</td>
    <td>0.890</td>
    <td>5.810</td>
    <td>/</td>
    <td>/</td>
    <td>0.869</td>
    <td>5.934</td>
    <td>/</td>
    <td>/</td>
  </tr>
  <tr>
    <td>Chloride</td>
    <td>-0.053</td>
    <td>15.120</td>
    <td>/</td>
    <td>/</td>
    <td>-0.377</td>
    <td>18.879</td>
    <td>/</td>
    <td>/</td>
  </tr>
  <tr>
    <td>Iodide</td>
    <td>0.823</td>
    <td>7.540</td>
    <td>/</td>
    <td>/</td>
    <td>0.844</td>
    <td>7.186</td>
    <td>/</td>
    <td>/</td>
  </tr>
  <tr>
    <td>Component-combination</td>
    <td>0.725</td>
    <td>10.120</td>
    <td>/</td>
    <td>/</td>
    <td>0.732</td>
    <td>9.457</td>
    <td>/</td>
    <td>/</td>
  </tr>
  <tr>
    <td rowspan="3">Thiol addition</td>
    <td>Cat</td>
    <td>0.781</td>
    <td>0.236</td>
    <td>/</td>
    <td>/</td>
    <td>0.804</td>
    <td>0.230</td>
    <td>/</td>
    <td>/</td>
  </tr>
  <tr>
    <td>Sub</td>
    <td>0.923</td>
    <td>0.138</td>
    <td>/</td>
    <td>/</td>
    <td>0.915</td>
    <td>0.138</td>
    <td>/</td>
    <td>/</td>
  </tr>
  <tr>
    <td>Sub and Cat</td>
    <td>0.804</td>
    <td>0.248</td>
    <td>/</td>
    <td>/</td>
    <td>0.732</td>
    <td>0.257</td>
    <td>/</td>
    <td>/</td>
  </tr>
  <tr>
    <td rowspan="3">External</td>
    <td colspan="2">Nicolit Avg</td>
    <td>0.308</td>
    <td>21.760</td>
    <td>0.793</td>
    <td>0.732</td>
    <td>0.209</td>
    <td>37.199</td>
    <td>0.796</td>
    <td>0.730</td>
  </tr>
  <tr>
    <td colspan="2">Asymmetric hydrogenation of olefins</td>
    <td>0.832</td>
    <td>0.371</td>
    <td>/</td>
    <td>/</td>
    <td>0.739</td>
    <td>0.477</td>
    <td>/</td>
    <td>/</td>
  </tr>
  <tr>
    <td colspan="2">Pallada-electrocatalyzed C–H activation</td>
    <td>0.924</td>
    <td>0.211</td>
    <td>/</td>
    <td>/</td>
    <td>0.900</td>
    <td>0.196</td>
    <td>/</td>
    <td>/</td>
  </tr>
</table>

### Sequence Performance Comparison
This section evaluates synthesis planning performance via Top-n accuracy metrics on both **retrosynthetic** and **forward synthesis** tasks.

<table border="1" cellpadding="4" cellspacing="0">
  <tr>
    <td rowspan="3" align="center"><b>Task</b></td>
    <td rowspan="3" align="center"><b>Dataset</b></td>
    <td colspan="4" align="center"><b>RXNGraphormer</b></td>
    <td colspan="4" align="center"><b>Reproduction</b></td>
    <td rowspan="3" align="center"><b>note</b></td>
  </tr>
  <tr>
    <td colspan="4" align="center">top-n accuracy(%)</td>
    <td colspan="4" align="center">top-n accuracy(%)</td>
  </tr>
  <tr>
    <td align="center">1</td>
    <td align="center">3</td>
    <td align="center">5</td>
    <td align="center">10</td>
    <td align="center">1</td>
    <td align="center">3</td>
    <td align="center">5</td>
    <td align="center">10</td>
  </tr>
  <tr>
    <td rowspan="2" align="center">Retrosynthetic</td>
    <td align="center">USPTO-50k</td>
    <td align="center">51.0</td>
    <td align="center">69.0</td>
    <td align="center">74.2</td>
    <td align="center">79.2</td>
    <td align="center">50.3</td>
    <td align="center">69.3</td>
    <td align="center">73.7</td>
    <td align="center">78.0</td>
    <td align="center">fine-tuned</td>
  </tr>
  <tr>
    <td align="center">USPTO-full</td>
    <td align="center">47.4</td>
    <td align="center">63.0</td>
    <td align="center">67.4</td>
    <td align="center">71.6</td>
    <td align="center">47.3</td>
    <td align="center">62.9</td>
    <td align="center">67.5</td>
    <td align="center">71.6</td>
    <td align="center">inference-only</td>
  </tr>
  <tr>
    <td rowspan="2" align="center">Forward</td>
    <td align="center">USPTO-480k</td>
    <td align="center">90.6</td>
    <td align="center">94.3</td>
    <td align="center">94.9</td>
    <td align="center">95.5</td>
    <td align="center">90.5</td>
    <td align="center">94.4</td>
    <td align="center">95.1</td>
    <td align="center">95.7</td>
    <td align="center">fine-tuned</td>
  </tr>
  <tr>
    <td align="center">USPTO-STEREO</td>
    <td align="center">78.2</td>
    <td align="center">85.1</td>
    <td align="center">86.5</td>
    <td align="center">87.8</td>
    <td align="center">78.1</td>
    <td align="center">84.9</td>
    <td align="center">86.4</td>
    <td align="center">87.7</td>
    <td align="center">fine-tuned</td>
  </tr>
</table>

### External Validation Eval
Model generalization is validated on newly introduced real-world datasets (e.g., HTE or literature-derived reactions), with results compared to baseline methods.

<table border="1" cellpadding="4" cellspacing="0">
  <tr>
    <td colspan="3" rowspan="2" align="center"><b>DATA</b></td>
    <td colspan="2" align="center"><b>Origin Model</b></td>
    <td colspan="2" align="center"><b>Rxngraphormer</b></td>
  </tr>
  <tr>
    <td align="center">R<sup>2</sup></td>
    <td align="center">MAE(%)</td>
    <td align="center">R<sup>2</sup></td>
    <td align="center">MAE(%)</td>
  </tr>
  <tr>
    <td colspan="2" rowspan="2">Sulfoxonium</td>
    <td>Train Set</td>
    <td align="right">0.89</td>
    <td align="right">6.60</td>
    <td align="right">0.91</td>
    <td align="right">5.70</td>
  </tr>
  <tr>
    <td>Validation Set</td>
    <td align="right">0.77</td>
    <td align="right">8.00</td>
    <td align="right">0.60</td>
    <td align="right">9.46</td>
  </tr>
  <tr>
    <td colspan="2" rowspan="3">Meta_C_H</td>
    <td>Train Set</td>
    <td align="right">0.75</td>
    <td align="right">9.30</td>
    <td align="right">0.82</td>
    <td align="right">5.76</td>
  </tr>
  <tr>
    <td>Independt Test Set</td>
    <td align="right">0.74</td>
    <td align="right">9.10</td>
    <td align="right">0.78</td>
    <td align="right">6.49</td>
  </tr>
  <tr>
    <td>Strict Independt Test Set</td>
    <td align="right">0.71</td>
    <td align="right">11.60</td>
    <td align="right">-1.19</td>
    <td align="right">23.22</td>
  </tr>
  <tr>
    <td rowspan="24">Amide Coupling HTE</td>
    <td rowspan="3">Full HTE (with NATURE intermediate)</td>
    <td>Random split</td>
    <td align="right">0.66</td>
    <td align="right">10.00</td>
    <td align="right">0.58</td>
    <td align="right">14.14</td>
  </tr>
  <tr>
    <td>Partial Novelty</td>
    <td align="right">0.68</td>
    <td align="right">14.00</td>
    <td align="right">0.59</td>
    <td align="right">14.31</td>
  </tr>
  <tr>
    <td>Full Novelty</td>
    <td align="right">0.63</td>
    <td align="right">15.00</td>
    <td align="right">0.58</td>
    <td align="right">12.56</td>
  </tr>
  <tr>
    <td rowspan="3">Full HTE (without intermediate)</td>
    <td>Random split</td>
    <td align="right">0.66</td>
    <td align="right">10.00</td>
    <td align="right">0.58</td>
    <td align="right">14.31</td>
  </tr>
  <tr>
    <td>Partial Novelty</td>
    <td align="right">0.68</td>
    <td align="right">14.00</td>
    <td align="right">0.66</td>
    <td align="right">13.12</td>
  </tr>
  <tr>
    <td>Full Novelty</td>
    <td align="right">0.63</td>
    <td align="right">15.00</td>
    <td align="right">0.44</td>
    <td align="right">14.93</td>
  </tr>
  <tr>
    <td rowspan="3">DCC (with intermediate)</td>
    <td>Random split</td>
    <td align="right">0.86</td>
    <td align="right">8.00</td>
    <td align="right">0.37</td>
    <td align="right">16.63</td>
  </tr>
  <tr>
    <td>Partial Novelty</td>
    <td align="right">0.81</td>
    <td align="right">11.00</td>
    <td align="right">0.27</td>
    <td align="right">15.99</td>
  </tr>
  <tr>
    <td>Full Novelty</td>
    <td align="right">0.67</td>
    <td align="right">7.00</td>
    <td align="right">-0.41</td>
    <td align="right">13.05</td>
  </tr>
  <tr>
    <td rowspan="3">EDC (with intermediate)</td>
    <td>Random split</td>
    <td align="right">0.89</td>
    <td align="right">6.10</td>
    <td align="right">0.23</td>
    <td align="right">18.46</td>
  </tr>
  <tr>
    <td>Partial Novelty</td>
    <td align="right">0.88</td>
    <td align="right">9.00</td>
    <td align="right">0.20</td>
    <td align="right">18.32</td>
  </tr>
  <tr>
    <td>Full Novelty</td>
    <td align="right">0.75</td>
    <td align="right">14.00</td>
    <td align="right">-0.10</td>
    <td align="right">22.23</td>
  </tr>
  <tr>
    <td rowspan="3">HATU (with intermediate)</td>
    <td>Random split</td>
    <td align="right">0.86</td>
    <td align="right">6.00</td>
    <td align="right">0.08</td>
    <td align="right">19.08</td>
  </tr>
  <tr>
    <td>Partial Novelty</td>
    <td align="right">0.78</td>
    <td align="right">12.00</td>
    <td align="right">-0.09</td>
    <td align="right">20.57</td>
  </tr>
  <tr>
    <td>Full Novelty</td>
    <td align="right">0.84</td>
    <td align="right">7.00</td>
    <td align="right">-0.37</td>
    <td align="right">16.34</td>
  </tr>
  <tr>
    <td rowspan="3">PyBOP (with intermediate)</td>
    <td>Random split</td>
    <td align="right">0.90</td>
    <td align="right">5.00</td>
    <td align="right">0.35</td>
    <td align="right">15.54</td>
  </tr>
  <tr>
    <td>Partial Novelty</td>
    <td align="right">0.82</td>
    <td align="right">10.00</td>
    <td align="right">0.38</td>
    <td align="right">14.09</td>
  </tr>
  <tr>
    <td>Full Novelty</td>
    <td align="right">0.89</td>
    <td align="right">8.00</td>
    <td align="right">0.22</td>
    <td align="right">15.56</td>
  </tr>
  <tr>
    <td rowspan="3">TBTU (without intermediate)</td>
    <td>Random split</td>
    <td align="right">0.71</td>
    <td align="right">10.00</td>
    <td align="right">0.49</td>
    <td align="right">13.40</td>
  </tr>
  <tr>
    <td>Partial Novelty</td>
    <td align="right">0.57</td>
    <td align="right">16.00</td>
    <td align="right">0.31</td>
    <td align="right">11.70</td>
  </tr>
  <tr>
    <td>Full Novelty</td>
    <td align="right">0.66</td>
    <td align="right">13.00</td>
    <td align="right">0.64</td>
    <td align="right">5.96</td>
  </tr>
  <tr>
    <td rowspan="3">HBTU (without intermediate)</td>
    <td>Random split</td>
    <td align="right">0.83</td>
    <td align="right">8.00</td>
    <td align="right">0.23</td>
    <td align="right">18.02</td>
  </tr>
  <tr>
    <td>Partial Novelty</td>
    <td align="right">0.72</td>
    <td align="right">13.00</td>
    <td align="right">0.04</td>
    <td align="right">18.75</td>
  </tr>
  <tr>
    <td>Full Novelty</td>
    <td align="right">0.68</td>
    <td align="right">14.00</td>
    <td align="right">-0.11</td>
    <td align="right">17.88</td>
  </tr>
  <tr>
    <td colspan="3" align="center">Amide Coupling Literature</td>
    <td align="right">0.39</td>
    <td align="right">13.30</td>
    <td align="right">0.35</td>
    <td align="right">12.48</td>
  </tr>
</table>


### Non-USPTO Sequence Generation (External Comparison)

To further evaluate generalization in synthesis planning, we compare our reproduced results with those reported in the original paper on non-USPTO datasets.

#### Forward Synthesis

| Setting | Model | Invalid SMILES (%) | Top-1 Acc (with SC) (%) | Top-1 Acc (w/o SC) (%) |
|--------|--------|--------------------|------------------------|----------------------|
| Separated | Origin Model | **0.40** | 66.10                  | 66.92                |
| Separated (USPTO_480k) | RXNGraphormer | 0.75 | **83.34**              | 83.40                |
| Separated (USPTO_STEREO) | RXNGraphormer | 0.52 | 83.31                  | **85.64**            |
| Mixed | Origin Model | **0.27** | **84.12**              | 85.20                |
| Mixed (USPTO_480k) | RXNGraphormer | 0.77 | 83.29                  | 83.35                |
| Mixed (USPTO_STEREO) | RXNGraphormer | 0.48 | 83.30                  | **85.64**            |

#### Retrosynthesis

| Model                      | Invalid SMILES (%) | Top-1 Acc (with SC) (%) | Top-1 Acc (w/o SC) (%) |
|----------------------------|--------------------|-------------------------|------------------------|
| Origin Model               | **0.27**           | **37.22**               | **37.42**              |
| RXNGraphormer (USPTO_full) | 4.01               | 27.59                   | 28.03                  |
| RXNGraphormer (USPTO_50k)  | 3.05               | 16.52                   | 16.64                  |



## 📚 Acknowledgments

Thanks to the original authors for open-sourcing RXNGraphormer. This reproduction builds directly upon their codebase and methodology.
> 💡 **Note**: For full installation instructions and model details, please refer to the [original README](https://github.com/licheng-xu-echo/RXNGraphormer).


