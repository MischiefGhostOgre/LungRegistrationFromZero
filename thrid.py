import os
import nibabel as nib
import numpy as np
import scipy.ndimage
from lungmask import LMInferer
from nibabel.viewers import OrthoSlicer3D


def save_vol(data, data_name, affine=None):
    if affine is None:
        affine = np.array([[-1, 0, 0, 0], [0, 0, 1, 0], [0, -1, 0, 0], [0, 0, 0, 1]], dtype=float)

    nib.Nifti1Image(data, affine).to_filename(data_name)


def window_transform(ct_array, windowWidth, windowCenter, normal=False):
    """
    return: trucated image according to window center and window width
    and normalized to [0,1]
    """
    minWindow = float(windowCenter) - 0.5 * float(windowWidth)
    newimg = (ct_array - minWindow) / float(windowWidth)
    newimg[newimg < 0] = 0
    newimg[newimg > 1] = 1
    if not normal:
        newimg = (newimg * 255).astype('uint8')
    return newimg


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

for num in range(0, 10):
    current_dir = "./DirLab/Case" + str(num) + "Pack/Images/"
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            if file.endswith("nii.gz"):
                img_path = os.path.join(root, file)
                img = nib.load(img_path).get_fdata()

                if 0 < num < 6:
                    img = np.pad(img, [(16, 16), (0, 0), (0, 0)], mode='constant')
                else:
                    [[x_min, y_min, z_min, ], [x_max, y_max, z_max]] = crop_case_num[num]
                    img = img[x_min:-x_max, y_min:-y_max, z_min:-z_max]

                img = scipy.ndimage.zoom(img, [0.625, 0.625, 0.625], order=1)
                img_ = img - 1000
                img_ = np.transpose(img_, axes=(2, 1, 0))
                inferer = LMInferer(modelname="R231CovidWeb", modelpath="./unet_r231covid-0de78a7e.pth",
                                    volume_postprocessing=True)
                seg = inferer.apply(img_)
                seg = np.transpose(seg, axes=(2, 1, 0))

                img = window_transform(img, 1700, 1000, True)

                vol = img * np.where(seg > 0, 1, 0)
                vol /= vol.max()
                vol = vol * np.where(seg > 0, 1, 0)
                vol = np.pad(vol, [(6, 6), (0, 0), (0, 0)], mode='constant')
                # OrthoSlicer3D(vol).show()
                img_path = img_path.replace(".nii.gz", "_vol.nii.gz")
                save_vol(vol, img_path)
