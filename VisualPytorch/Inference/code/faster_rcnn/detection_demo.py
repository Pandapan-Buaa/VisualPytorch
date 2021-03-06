# -*- coding: utf-8 -*-
"""
# @file name  : detection_demo.py
# @author     : TingsongYu https://github.com/TingsongYu
# @date       : 2019-11-30
# @brief      : Faster rcnn实现目标检测
"""

import os
import time
import torch.nn as nn
import torch
import numpy as np
import torchvision.transforms as transforms
import torchvision
from PIL import Image
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# appendix
classes_pascal_voc = ['__background__',
                      'aeroplane', 'bicycle', 'bird', 'boat',
                      'bottle', 'bus', 'car', 'cat', 'chair',
                      'cow', 'diningtable', 'dog', 'horse',
                      'motorbike', 'person', 'pottedplant',
                      'sheep', 'sofa', 'train', 'tvmonitor']

# classes_coco
COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]


def faster_rcnn(pic_name, pkl_path):
    tic = time.time()
    # config
    preprocess = transforms.Compose([
        transforms.ToTensor(),
    ])

    # 1. load data & model
    input_image = Image.open(pic_name).convert("RGB")
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=False, pretrained_backbone=False)
    model.load_state_dict(torch.load(pkl_path + 'fasterrcnn_resnet50_fpn_coco-258fb6c6.pth'))
    model.eval()

    # 2. preprocess
    img_chw = preprocess(input_image)

    # 3. to device
    if torch.cuda.is_available():
        img_chw = img_chw.to('cuda')
        model.to('cuda')

    # 4. forward
    input_list = [img_chw]
    with torch.no_grad():

        print("input img tensor shape:{}".format(input_list[0].shape))
        output_list = model(input_list)
        output_dict = output_list[0]
        labels = "{}".format(list(map(lambda x: COCO_INSTANCE_CATEGORY_NAMES[int(x)], output_dict['labels'].numpy())))
        scores = "{}".format(list(map(lambda x: int(x * 1000) / 1000, output_dict['scores'].numpy())))

    # 5. visualization
    out_boxes = output_dict["boxes"].cpu()
    out_scores = output_dict["scores"].cpu()
    out_labels = output_dict["labels"].cpu()

    fig, ax = plt.subplots(figsize=(16, 12))
    ax.imshow(input_image, aspect='equal')

    num_boxes = out_boxes.shape[0]
    max_vis = 40
    thres = 0.5

    for idx in range(0, min(num_boxes, max_vis)):

        score = out_scores[idx].numpy()
        bbox = out_boxes[idx].numpy()
        class_name = COCO_INSTANCE_CATEGORY_NAMES[out_labels[idx]]

        if score < thres:
            continue

        ax.add_patch(plt.Rectangle((bbox[0], bbox[1]), bbox[2] - bbox[0], bbox[3] - bbox[1], fill=False,
                                   edgecolor='red', linewidth=3.5))
        ax.text(bbox[0], bbox[1] - 2, '{:s} {:.3f}'.format(class_name, score), bbox=dict(facecolor='blue', alpha=0.5),
                fontsize=14, color='white')
    # plt.show()
    pic_out = pic_name[:-4] + '_out.jpg'
    plt.savefig(pic_out)

    plt.close()

    return {"addr": pic_out, "input_shape": input_image.size, "time": round(time.time() - tic, 2), "labels": labels,
            "scores": scores}


if __name__ == "__main__":
    print(faster_rcnn("PennPed00016.png", './'))
