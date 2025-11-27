from nilearn import datasets
import nibabel as nib
import os

# 配置下载路径 (可选，默认在 ~/nilearn_data)
output_dir = './nilearn_data'
os.makedirs(output_dir, exist_ok=True)

# 1. 下载/获取 Yeo 2011 图谱
# nilearn 会返回一个 Bunch 对象，包含不同版本图谱的文件路径
dataset_yeo = datasets.fetch_atlas_yeo_2011(data_dir=output_dir)

# 2. 获取 7网络 (Thick) 版本的路径
# thick_7: 包含皮层和皮层下的宽泛掩码 (Liberal mask)，适合做体积空间映射，因为它覆盖范围更广
# thin_7: 仅包含皮层的严格掩码 (Conservative mask)
yeo_7_nifti_path = dataset_yeo.thick_7

print(f"Yeo 7网络图谱文件路径: {yeo_7_nifti_path}")

# 3. 加载为 Nifti 对象以供后续使用
yeo_img = nib.load(yeo_7_nifti_path)
print(f"加载成功，图像维度: {yeo_img.shape}")
print(f"包含的标签值: {list(set(yeo_img.get_fdata().flatten().astype(int)))}")