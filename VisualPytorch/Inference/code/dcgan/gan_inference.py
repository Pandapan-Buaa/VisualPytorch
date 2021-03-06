# -*- coding: utf-8 -*-
"""
# @file name  : gan_inference.py
# @author     : TingsongYu https://github.com/TingsongYu
# @date       : 2019-12-05
# @brief      : gan inference
"""
import os
import time

import torch.nn as nn
import torch.optim as optim
import torch.utils.data
# import imageio
import torchvision.transforms as transforms
import torchvision.utils as vutils
import numpy as np
import matplotlib

matplotlib.use('Agg')
from matplotlib import pyplot as plt
# from tools.common_tools import set_seed
# from torch.utils.data import DataLoader
# from tools.my_dataset import CelebADataset
from ..tools.dcgan import Discriminator, Generator


def remove_module(state_dict_g):
    # remove module.
    from collections import OrderedDict

    new_state_dict = OrderedDict()
    for k, v in state_dict_g.items():
        namekey = k[7:] if k.startswith('module.') else k
        new_state_dict[namekey] = v

    return new_state_dict


def gcgan(pic_name, pkl_path, num_img, nrow, noise):
    # config
    if (noise == 1):
        noise_continue = True
    else:
        noise_continue = False

    tic = time.time()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    path_checkpoint = pkl_path + "dcgan.pkl"
    time_tic = time.time()
    nz = 100

    # step 1: data
    fixed_noise = torch.randn(num_img, nz, 1, 1, device=device)

    if noise_continue:
        fixed_noise[0, ...] = torch.randn(1, nz, 1, 1, device=device)
        delta = torch.randn(1, nz, 1, 1, device=device) - fixed_noise[0, ...]
        delta /= num_img

        for i in range(1, num_img):
            fixed_noise[i, ...] = fixed_noise[i - 1, ...] + delta

    # step 2: model
    net_g = Generator(nz=nz, ngf=128, nc=3)
    # net_d = Discriminator(nc=nc, ndf=ndf)
    checkpoint = torch.load(path_checkpoint, map_location="cpu")

    state_dict_g = checkpoint["g_model_state_dict"]
    state_dict_g = remove_module(state_dict_g)
    net_g.load_state_dict(state_dict_g)
    net_g.to(device)
    # net_d.load_state_dict(checkpoint["d_model_state_dict"])
    # net_d.to(device)

    # step3: inference
    with torch.no_grad():
        fake_data = net_g(fixed_noise).detach().cpu()
    img_grid = vutils.make_grid(fake_data, padding=2, normalize=True, nrow=nrow).numpy()
    img_grid = np.transpose(img_grid, (1, 2, 0))
    plt.imshow(img_grid)
    pic_out = pic_name
    plt.savefig(pic_out)

    plt.close()

    return {"addr": pic_out, "time": round(time.time() - tic, 2)}


if __name__ == "__main__":
    print(gcgan("test.jpg", './'))
