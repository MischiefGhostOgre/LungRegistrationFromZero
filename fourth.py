import os
import nibabel as nib
import numpy as np

case_vxl_space_list = [(2.5, 0.97, 0.97),
                       (2.5, 0.97, 0.97),
                       (2.5, 1.16, 1.16),
                       (2.5, 1.15, 1.15),
                       (2.5, 1.13, 1.13),
                       (2.5, 1.10, 1.10),
                       (2.5, 0.97, 0.97),
                       (2.5, 0.97, 0.97),
                       (2.5, 0.97, 0.97),
                       (2.5, 0.97, 0.97),
                       ]

crop_case_num = [
    [[108, 98, 0], [116, 158, 128]],  # 0
    [[None, None, None], [None, None, None]],  # 1
    [[None, None, None], [None, None, None]],  # 2
    [[None, None, None], [None, None, None]],  # 3
    [[None, None, None], [None, None, None]],  # 4
    [[None, None, None], [None, None, None]],  # 5
    [[128, 128, 44], [96, 128, 84]],  # 6
    [[124, 128, 44], [100, 128, 84]],  # 7
    [[108, 68, 64], [116, 188, 64]],  # 8
    [[108, 128, 0], [116, 128, 128]],  # 9
    [[108, 98, 0], [116, 158, 128]],  # 10
]


def save_point(point_name, p_x, p_y, p_z):
    with open(point_name, 'w') as file:
        for i in range(300):
            line = f"{p_x[i]} {p_y[i]} {p_z[i]}\n"
            file.write(line)


for num in range(0, 10):
    current_dir = "./DirLab/Case" + str(num) + "Pack/ExtremePhases/"
    vxl_shape = case_vxl_space_list[num]
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            if file.endswith("_xyz.txt"):
                point_path = os.path.join(root, file)
                print(point_path)
                point = np.loadtxt(point_path)
                p_x, p_y, p_z = point[:, 0], point[:, 1], point[:, 2]

                case_vxl_space = case_vxl_space_list[num]
                alpha = max(case_vxl_space) / min(case_vxl_space)
                p_z *= alpha

                if 0 < num < 6:
                    p_x += 16
                else:
                    [[x_min, y_min, z_min], [x_max, y_max, z_max]] = crop_case_num[num]
                    p_x -= x_min
                    p_y -= y_min
                    p_z -= z_min

                p_x *= 0.625
                p_y *= 0.625
                p_z *= 0.625

                p_x += 6

                point_path = point_path.replace("_xyz.txt", ".txt")
                save_point(point_path, p_x, p_y, p_z)
