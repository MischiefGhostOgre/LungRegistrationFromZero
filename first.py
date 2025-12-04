import os
from pathlib import Path

# ================== 配置区 ==================
ROOT_DIR = r"D:\LungRegistrationFromZero\DirLab"  # 修改为你的实际路径
# ============================================

def main():
    root = Path(ROOT_DIR)

    print("开始统一文件命名，并将 case10 重命名为 case0...\n")

    for case_folder in root.iterdir():
        if not case_folder.is_dir() or not case_folder.name.startswith('Case'):
            continue

        original_name = case_folder.name

        # 提取编号：Case10Pack -> 10, Case1Pack -> 1, Case8Deploy -> 8
        if 'Pack' in original_name:
            case_num = case_folder.name[4:-4]
        elif 'Deploy' in original_name:
            case_num = case_folder.name[4:-6]
        else:
            case_num = case_folder.name[4:]

        # === 特殊处理：case10 → case0 ===
        if case_num == '10':
            target_name = 'Case0Pack'
            new_case_num = '0'
        else:
            target_name = f"Case{case_num}Pack"
            new_case_num = case_num

        # 重命名主文件夹（如果需要）
        target_path = case_folder.parent / target_name
        if case_folder.name != target_name:
            if target_path.exists():
                print(f"⚠️  目标文件夹已存在: {target_name}，跳过重命名")
            else:
                case_folder.rename(target_path)
                print(f"📁 重命名文件夹: {original_name} → {target_name}")
            case_folder = target_path  # 更新路径
        # 如果原文件夹被重命名，case_folder 已指向新路径

        # 处理子目录和文件，使用 new_case_num（case10 → case0）
        process_extreme_phases(case_folder, new_case_num)
        process_images(case_folder, new_case_num)
        process_sampled_4d(case_folder, new_case_num)

    print("\n✅ 所有文件处理完成！case10 已改为 case0。")


# === 1. 处理 ExtremePhases 文件夹 ===
def process_extreme_phases(folder, num):
    sub = folder / "ExtremePhases"
    if not sub.exists():
        alt_names = [d for d in folder.iterdir() if d.is_dir() and 'extreme' in d.name.lower()]
        if alt_names:
            old_sub = alt_names[0]
            old_sub.rename(sub)
            print(f"🔧 重命名子目录: {old_sub.name} → ExtremePhases")
        else:
            return  # 没有该目录

    for file in sub.iterdir():
        if file.is_file() and file.suffix == '.txt':
            old_name = file.name

            # 确定是 T00 还是 T50
            phase = 'T00'
            if 'T50' in old_name:
                phase = 'T50'

            new_name = f"case{num}_300_{phase}_xyz.txt"
            new_file = sub / new_name

            if old_name != new_name:
                if new_file.exists():
                    print(f"❌ 冲突: {new_file} 已存在")
                else:
                    file.rename(new_file)
                    print(f"📄 ExtremePhases: {old_name} → {new_name}")


# === 2. 处理 Images 文件夹中的 .img 图像文件 ===
def process_images(folder, num):
    sub = folder / "Images"
    if not sub.exists():
        print(f"⚠️  缺少 Images 目录: {folder.name}")
        return

    for file in sub.iterdir():
        if file.is_file() and file.suffix == '.img':
            old_name = file.name

            # 提取 Txx 部分（如 T00, T10）
            phase = None
            for p in ['T00', 'T10', 'T20', 'T30', 'T40', 'T50', 'T60', 'T70', 'T80', 'T90']:
                if p in old_name:
                    phase = p
                    break
            if not phase:
                print(f"❓ 无法识别相位: {old_name}")
                continue

            # 统一命名为 caseN_TXX.img
            new_name = f"case{num}_{phase}.img"
            new_file = sub / new_name

            if old_name != new_name:
                if new_file.exists():
                    print(f"❌ 冲突: {new_file} 已存在")
                else:
                    file.rename(new_file)
                    print(f"🖼️  Images: {old_name} → {new_name}")


# === 3. 处理 Sampled4D 文件夹中的 .txt 文件 ===
def process_sampled_4d(folder, num):
    sub = folder / "Sampled4D"
    if not sub.exists():
        print(f"⚠️  缺少 Sampled4D 目录: {folder.name}")
        return

    for file in sub.iterdir():
        if file.is_file() and file.suffix == '.txt':
            old_name = file.name

            # 提取 Txx
            phase = None
            for p in ['T00', 'T10', 'T20', 'T30', 'T40', 'T50']:
                if p in old_name:
                    phase = p
                    break
            if not phase:
                continue

            # 统一命名为 caseN_4D75_TXX.txt
            new_name = f"case{num}_4D75_{phase}.txt"
            new_file = sub / new_name

            if old_name != new_name:
                if new_file.exists():
                    print(f"❌ 冲突: {new_file} 已存在")
                else:
                    file.rename(new_file)
                    print(f"📊 Sampled4D: {old_name} → {new_name}")


# =============== 运行 ===============
if __name__ == "__main__":
    main()
