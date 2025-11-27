import os
import numpy as np
import nibabel as nib
from nilearn import image
from scipy.ndimage import center_of_mass


def robust_resample(source_path, target_ref_path, output_path):
    print(f"--- 开始处理 ---")

    # 1. 加载图像
    src_img = nib.load(source_path)
    ref_img = nib.load(target_ref_path)

    ref_img = nib.squeeze_image(ref_img)
    src_data = src_img.get_fdata().astype(int)

    # 检查 0 和 最大值
    unique_ids = np.unique(src_data)
    max_id = np.max(unique_ids)

    print(f"源文件 ID 范围: {np.min(unique_ids)} 到 {max_id}")

    # 检查 0 是否为背景
    if 0 in unique_ids:
        vol_0 = np.sum(src_data == 0)
        print(f"检测到 ID 0。体素数量: {vol_0}")
        if vol_0 > np.sum(src_data == 1) * 100:
            print("结论: 0 是背景 (Background)。")
    # 检查是否有 180
    if max_id < 180:
        print(f"警告: 源文件的最大 ID 只有 {max_id}，而 HCP 单侧通常有 180 个脑区。")
        print("可能原因: 文件本身缺失了最后几个脑区，或者这是 0-indexed 的文件(已尝试修复)。")
    # ==========================================

    # 2. 执行常规重采样 (Nearest Neighbor)
    print("正在执行初步重采样...")
    resampled_img = image.resample_to_img(
        source_img=src_img,
        target_img=ref_img,
        interpolation='nearest'
    )

    resampled_data = resampled_img.get_fdata().astype(int)

    # 3. 检测丢失的 ID
    # 重新从原始数据获取 IDs (确保此时 src_data 已修正)
    src_ids = set(np.unique(src_data))
    out_ids = set(np.unique(resampled_data))

    # 排除背景
    src_ids.discard(0)
    out_ids.discard(0)

    missing_ids = src_ids - out_ids

    if len(missing_ids) == 0:
        print("没有脑区丢失。")
        resampled_img.to_filename(output_path)
        return

    print(f"检测到 {len(missing_ids)} 个脑区在重采样后消失")
    print(f"丢失的 ID: {missing_ids}")
    print("强制找回")

    # 4. 强制找回
    src_affine = src_img.affine
    target_inv_affine = np.linalg.inv(resampled_img.affine)
    fixed_data = resampled_data.copy()
    recovered_count = 0

    for missing_id in missing_ids:
        roi_mask = (src_data == missing_id)
        if not np.any(roi_mask): continue

        src_vox_center = center_of_mass(roi_mask)
        src_world_point = src_affine @ np.array(list(src_vox_center) + [1])
        target_vox_point = target_inv_affine @ src_world_point
        i, j, k = np.round(target_vox_point[:3]).astype(int)

        dims = fixed_data.shape
        if 0 <= i < dims[0] and 0 <= j < dims[1] and 0 <= k < dims[2]:
            fixed_data[i, j, k] = missing_id
            recovered_count += 1
        else:
            print(f"  -> 无法恢复 ID {missing_id}: 超出边界")

    # 5. 保存结果
    final_img = nib.Nifti1Image(fixed_data, resampled_img.affine, resampled_img.header)
    final_img.to_filename(output_path)
    print(f"修复完成。共恢复 {recovered_count} 个丢失脑区。结果已保存至: {output_path}")


if __name__ == "__main__":
    # 配置你的路径
    source_file = r'E:\datasets\glasser360-master\glasser360-master\glasser360MNI.nii.gz'
    reference_file = r'E:\2_my_project\hcp2cab-np\nilearn_data\yeo_2011\Yeo_JNeurophysiol11_MNI152\Yeo2011_7Networks_MNI152_FreeSurferConformed1mm_LiberalMask.nii.gz'
    output_file = 'Glasser_HCP360_FreeSurferConformed1mm_FIXED.nii.gz'

    if os.path.exists(source_file) and os.path.exists(reference_file):
        robust_resample(source_file, reference_file, output_file)

