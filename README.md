# HCP360 (Glasser) to Yeo-7 Network Mapping
<div align="center">

**English** | [简体中文](./README_zh-CN.md)

</div>

This project facilitates the mapping between the **HCP MMP 1.0 (Glasser 360)** atlas and the **Yeo 2011 (7 Networks)** functional parcellation. By resampling the atlases into a common space and calculating spatial overlap, this project assigns each of the 360 Glasser cortical regions to one of the 7 canonical Yeo functional networks.

<table>
  <tr>
    <td align="center" width="25%"><img src="asset/hcp360.png" width="100%" alt="HCP360 Original"></td>
    <td align="center" width="25%"><img src="asset/yeo7.png" width="100%" alt="Yeo 7 Networks"></td>
    <td align="center" width="25%"><img src="asset/hcp360_resample.png" width="100%" alt="HCP360 Resampled"></td>
    <td align="center" width="25%"><img src="asset/hcp360_to_yeo7.png" width="100%" alt="Mapping Result"></td>
  </tr>
  <tr>
   <td align="center"><b>HCP360 (Glasser)</b><br>Original Atlas</td>
    <td align="center"><b>Yeo-7</b><br>Functional Networks</td>
    <td align="center"><b>HCP360 Resampled</b><br>Aligned to Yeo space</td>
    <td align="center"><b>Mapping Result</b><br>HCP Regions Colored by Yeo Net</td>
  </tr>
</table>

## 📥 Quick Access

If you strictly require the final lookup table and do not need to run the processing pipeline, you can download the result directly:

* **Mapping File:** [HCP360_to_Yeo7_Mapping.csv](https://github.com/Jingfeng-Tang/HCP360-Glasser-atlas-mapping-Yeo-7-subnetwork/blob/main/HCP360_to_Yeo7_Mapping.csv)

This CSV contains the correspondence between Glasser ROI IDs ,Yeo network labels and confidence.
1: 'Visual (视觉)'
2: 'Somatomotor (体感运动)'
3: 'Dorsal Attention (背侧注意)'
4: 'Ventral Attention (腹侧注意)'
5: 'Limbic (边缘系统)'
6: 'Frontoparietal (额顶控制)'
7: 'Default Mode (默认模式)'
0: 'Unassigned (未分配)'
---

## 🚀 Usage

Follow these steps to reproduce the mapping process or generate the files from scratch.

### 0. Prerequisites
Ensure your Python environment has the necessary libraries installed for neuroimaging data manipulation (e.g., `nibabel`, `numpy`, `pandas`).

### 1. Acquire Yeo Atlas
Obtain the Yeo 2011 7-Network atlas in MNI152 space.
* **Run:**
    ```bash
    python fetch_yeo.py
    ```
* **Direct Download:** [Yeo2011_7Networks_MNI152.nii.gz](https://github.com/Jingfeng-Tang/HCP360-Glasser-atlas-mapping-Yeo-7-subnetwork/blob/main/Yeo2011_7Networks_MNI152_FreeSurferConformed1mm_LiberalMask.nii.gz)

### 2. Acquire HCP360 Atlas
Obtain the Glasser HCP 360 atlas.
* **Source:** [Glasser360 Github](https://github.com/brainspaces/glasser360)
* **Backup File:** [glasser360MNI.nii.gz](https://github.com/Jingfeng-Tang/HCP360-Glasser-atlas-mapping-Yeo-7-subnetwork/blob/main/glasser360MNI.nii.gz)

### 3. Resample HCP360 to Yeo Space
Resample the HCP360 atlas to match the resolution, affine matrix, and dimensions of the Yeo template to ensure voxel-wise alignment.
* **Run:**
    ```bash
    python resample_hcp2yeo.py
    ```

### 4. Generate Mapping
Calculate the overlap between the resampled HCP ROIs and the Yeo networks to generate the final CSV mapping file.
* **Run:**
    ```bash
    python mapping_hcp2yeo.py
    ```

---

## 📚 References

If you use these atlases in your research, please cite the original publications:

1.  **HCP MMP 1.0 (Glasser 360):**
    > Glasser, M. F., Coalson, T. S., Robinson, E. C., Hacker, C. D., Harwell, J., Yacoub, E., ... & Van Essen, D. C. (2016). A multi-modal parcellation of human cerebral cortex. *Nature*, 536(7615), 171-178.

2.  **Yeo 7 Networks:**
    > Yeo, B. T., Krienen, F. M., Sepulcre, J., Sabuncu, M. R., Lashkari, D., Hollinshead, M., ... & Buckner, R. L. (2011). The organization of the human cerebral cortex estimated by intrinsic functional connectivity. *Journal of neurophysiology*, 106(3), 1125-1165.
