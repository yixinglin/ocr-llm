"""
Convolutional Neural Networks (CNN)

"""

import torch
import torchvision.models as models
import torchvision.transforms as transforms
import numpy as np

class FeatureExtractor:

    def __init__(self, checkpoint_path=None):
        if checkpoint_path is not None:
            # 从检查点文件中加载模型参数
            self.model = models.resnet50()
            self.model.load_state_dict(torch.load(checkpoint_path, weights_only=True))
        else:
            # 使用预训练的ResNet50模型
            self.model = models.resnet50(pretrained=True)

        # 修改模型最后一层
        self.model.fc = torch.nn.Identity()
        self.model.eval()
        self.model.cpu()
        # 定义图像预处理方式
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            # 使用ImageNet的均值和标准差进行标准化
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225]),
        ])

    def extract(self, img):
        # 预处理图像
        img_t = self.transform(img)
        # 增加一个批次维度 [C, H, W] -> [1, C, H, W]
        batch_t = torch.unsqueeze(img_t, 0)   # 增加batch维度，形状变为 [1, 3, 224, 224]
        # 提取特征
        with torch.no_grad():
            features = self.model(batch_t)   # features 的形状：[1, 2048, 1, 1]
        # 展平特征向量
        f_ = features.squeeze().numpy()
        # 对特征向量进行L2归一化，使得其范数为1
        f_ /= np.linalg.norm(f_)
        return f_  # 返回一个 NumPy 数组，形状为 [2048]

    @classmethod
    def from_checkpoint(cls, checkpoint_path):
        # 从检查点文件中加载模型参数
        return cls(checkpoint_path)

