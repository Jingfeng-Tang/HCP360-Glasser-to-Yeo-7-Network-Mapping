
import os
import argparse
import logging
import numpy as np
import pandas as pd
import nibabel as nib
import torch



def get_logger(log_file):
    """配置日志"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # 清除旧handler
    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    fh = logging.FileHandler(log_file, mode='w')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def load_and_squeeze(nii_path, logger):
    """加载Nifti并确保它是3D的"""
    if not os.path.exists(nii_path):
        raise FileNotFoundError(f"找不到文件: {nii_path}")

    img = nib.load(nii_path)
    # 自动去除多余的维度 (比如 (256,256,256,1) -> (256,256,256))
    img = nib.squeeze_image(img)

    if len(img.shape) != 3:
        raise ValueError(f"文件 {nii_path} 在去除维度后仍不是3D图像，当前形状: {img.shape}")

    logger.info(f"加载成功: {os.path.basename(nii_path)} | 形状: {img.shape}")
    return img.get_fdata().astype(int)


# ================= 核心逻辑 =================

def main():
    parser = argparse.ArgumentParser(description="生成 HCP360 到 Yeo 网络的映射 CSV")
    # 输入文件路径
    # parser.add_argument('--hcp_path', type=str, default=r'E:\datasets\hcp_mmp_atlas\MNI_Glasser_HCP_v1.nii.gz', help='对齐后的 Glasser HCP360 Nifti 文件')
    # parser.add_argument('--hcp_path', type=str, default=r'E:\2_my_project\hcp2cab-np\Glasser_HCP360_FreeSurferConformed1mm.nii.gz', help='对齐后的 Glasser HCP360 Nifti 文件')
    parser.add_argument('--hcp_path', type=str, default=r'E:\2_my_project\hcp2cab-np\Glasser_HCP360_FreeSurferConformed1mm_FIXED.nii.gz', help='对齐后的 Glasser HCP360 Nifti 文件')
    parser.add_argument('--yeo_path', type=str, default=r'E:\2_my_project\hcp2cab-np\nilearn_data\yeo_2011\Yeo_JNeurophysiol11_MNI152\Yeo2011_7Networks_MNI152_FreeSurferConformed1mm_LiberalMask.nii.gz', help='Yeo 7 Networks Nifti 文件')
    parser.add_argument('--output_csv', type=str, default='HCP360_to_Yeo7_Mapping.csv', help='输出结果路径')

    args = parser.parse_args()

    # 初始化
    logger = get_logger('mapping_process.log')
    logger.info("开始执行映射计算任务")

    try:
        # 1. 加载数据
        hcp_data = load_and_squeeze(args.hcp_path, logger)
        yeo_data = load_and_squeeze(args.yeo_path, logger)

        # 2. 验证维度一致性
        if hcp_data.shape != yeo_data.shape:
            raise ValueError(f"维度不匹配! HCP: {hcp_data.shape} vs Yeo: {yeo_data.shape}。先检查重采样步骤。")

        # 3. 提取所有 HCP 脑区 ID
        # 排除 0 (背景)
        hcp_ids = np.unique(hcp_data)
        hcp_ids = hcp_ids[hcp_ids != 0]
        hcp_ids.sort()

        logger.info(f"在 HCP 图谱中检测到 {len(hcp_ids)} 个唯一脑区 ID")

        results = []

        # 4. 逐脑区计算 (Winner-Take-All)
        for roi_id in hcp_ids:
            # 创建当前 ROI 的掩码 (boolean mask)
            roi_mask = (hcp_data == roi_id)

            # 取出该 ROI 范围内对应的 Yeo 网络标签
            yeo_values_in_roi = yeo_data[roi_mask]

            # 过滤掉 Yeo 里的 0 (背景/无定义区域)
            # 如果你要强制归类即使落在背景上，可以不过滤，但通常建议过滤
            valid_yeo_values = yeo_values_in_roi[yeo_values_in_roi != 0]

            if len(valid_yeo_values) == 0:
                # 这种情况很少见，除非该脑区完全落在了 Yeo 的背景里
                mapped_net = 0
                confidence = 0.0
                logger.warning(f"HCP ID {roi_id} 与 Yeo 非零区域无重叠，归类为 0")
            else:
                # 计算众数 (出现次数最多的网络)
                counts = np.bincount(valid_yeo_values)
                mapped_net = counts.argmax()

                # 计算置信度 (最大票数 / 总有效票数)
                confidence = counts[mapped_net] / len(valid_yeo_values)

            results.append({
                'HCP_ID': roi_id,
                'Yeo_Network': mapped_net,
                'Confidence': round(confidence, 4)  # 保留4位小数
            })

        # 5. 保存结果
        df = pd.DataFrame(results)
        df.to_csv(args.output_csv, index=False)

        logger.info(f"映射完成！结果已保存至: {args.output_csv}")

        logger.info("-" * 40)
        logger.info("Yeo 7网络脑区分布统计:")

        # 定义网络名称映射
        yeo_labels = {
            1: 'Visual (视觉)',
            2: 'Somatomotor (体感运动)',
            3: 'Dorsal Attention (背侧注意)',
            4: 'Ventral Attention (腹侧注意)',
            5: 'Limbic (边缘系统)',
            6: 'Frontoparietal (额顶控制)',
            7: 'Default Mode (默认模式)',
            0: 'Unassigned (未分配)'
        }

        # 统计 Yeo_Network 列中每个值的出现次数
        network_counts = df['Yeo_Network'].value_counts().sort_index()

        for net_id, count in network_counts.items():
            net_name = yeo_labels.get(net_id, 'Unknown')
            logger.info(f"网络 {net_id} [{net_name}]: {count} 个脑区")

        logger.info(f"总计统计脑区数: {network_counts.sum()}")
        logger.info("-" * 40)
        # ==========================================

        # 简单预览
        print("\n映射结果预览 (前5行):")
        print(df.head())


    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")
        raise e


if __name__ == "__main__":
    main()