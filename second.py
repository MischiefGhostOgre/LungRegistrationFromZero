import os

import numpy as np
import scipy.ndimage
import nibabel as nib
from nibabel.viewers import OrthoSlicer3D


def save_vol(data, data_name, affine=None):
    if affine is None:
        affine = np.array([[-1, 0, 0, 0], [0, 0, 1, 0], [0, -1, 0, 0], [0, 0, 0, 1]], dtype=float)

    nib.Nifti1Image(data, affine).to_filename(data_name)


def pad_to_256_depth(img):
    _, _, depth = img.shape
    if depth > 256:
        raise ValueError(f"深度 {depth} 已超过 256，无法填充")

    pad_width = [(0, 0), (0, 0), (0, 256 - depth)]
    padded_img = np.pad(img, pad_width, mode='constant', constant_values=0)

    return padded_img


def pad_to_256_depth(img):
    _, _, depth = img.shape
    if depth > 256:
        raise ValueError(f"深度 {depth} 已超过 256，无法填充")

    pad_width = [(0, 0), (0, 0), (0, 256 - depth)]
    padded_img = np.pad(img, pad_width, mode='constant', constant_values=0)

    return padded_img

def pad_to_384_depth(img):
    _, _, depth = img.shape
    if depth > 384:
        raise ValueError(f"深度 {depth} 已超过 384，无法填充")

    pad_width = [(0, 0), (0, 0), (0, 384 - depth)]
    padded_img = np.pad(img, pad_width, mode='constant', constant_values=0)

    return padded_img

case_shape_list = [(120, 512, 512),
                   (94, 256, 256),
                   (112, 256, 256),
                   (104, 256, 256),
                   (99, 256, 256),
                   (106, 256, 256),
                   (128, 512, 512,),
                   (136, 512, 512),
                   (128, 512, 512),
                   (128, 512, 512),
                   ]
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

for num in range(9, 10):
    current_dir = "./DirLab/Case" + str(num) + "Pack/Images/"
    vol_shape = case_shape_list[num]
    vxl_shape = case_vxl_space_list[num]
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            if file.endswith("img"):
                img_path = os.path.join(root, file)
                print(img_path)
                img = np.memmap(img_path, np.int16, mode='r', shape=vol_shape)
                vol = img
                vol = scipy.ndimage.zoom(vol, [vxl / min(vxl_shape) for vxl in vxl_shape], order=3)
                # OrthoSlicer3D(vol).show()
                img_name = img_path.replace(".img", ".nii.gz")
                vol = vol.transpose(2, 1, 0)  # 原始的维度是 z y x
                if 0 < num < 6:
                    vol = pad_to_256_depth(vol)
                else:
                    vol = pad_to_384_depth(vol)
                save_vol(vol, img_name)  # 保存的维度是 x y z
