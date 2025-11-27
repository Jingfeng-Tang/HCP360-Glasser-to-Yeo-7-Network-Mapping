# HCP360-Glasser-atlas-mapping-Yeo-7-subnetwork

<table>
  <tr>
    <td align="center" width="25%"><img src="asset/hcp360.png" width="100%"></td>
    <td align="center" width="25%"><img src="asset/yeo7.png" width="100%"></td>
    <td align="center" width="25%"><img src="asset/hcp360_resample.png" width="100%"></td>
    <td align="center" width="25%"><img src="asset/hcp360_to_yeo7.png" width="100%"></td>
  </tr>
  <tr>
   <td align="center">hcp360</td>
    <td align="center">yeo7</td>
    <td align="center">hcp360_resample</td>
    <td align="center">hcp360_to_yeo7</td>
  </tr>
</table>


## You can download the [mapping file](https://github.com/Jingfeng-Tang/HCP360-Glasser-atlas-mapping-Yeo-7-subnetwork/blob/main/HCP360_to_Yeo7_Mapping.csv) directly, or generate it yourself using the script below.

### step1: get yeo
`python fetch_yeo.py` or [yeo file](https://github.com/Jingfeng-Tang/HCP360-Glasser-atlas-mapping-Yeo-7-subnetwork/blob/main/Yeo2011_7Networks_MNI152_FreeSurferConformed1mm_LiberalMask.nii.gz)

### step2: get hcp360
[hcp link](https://github.com/brainspaces/glasser360) or [hcp file](https://github.com/Jingfeng-Tang/HCP360-Glasser-atlas-mapping-Yeo-7-subnetwork/blob/main/glasser360MNI.nii.gz)

### step3: resample hcp360 to yeo size
`python resample_hcp2yeo.py`

### step4: mapping hcp360 to yeo
`python mapping_hcp2yeo.py`
