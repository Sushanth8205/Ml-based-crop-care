import torch
import torch.nn as nn
from torchvision import models

class AttentionBlock(nn.Module):
    def __init__(self, in_features):
        super(AttentionBlock, self).__init__()
        self.attention = nn.Sequential(
            nn.Conv2d(in_features, in_features // 8, kernel_size=1),
            nn.BatchNorm2d(in_features // 8),
            nn.ReLU(),
            nn.Conv2d(in_features // 8, in_features, kernel_size=1),
            nn.BatchNorm2d(in_features),
            nn.Sigmoid()
        )

    def forward(self, x):
        attn_weights = self.attention(x)
        return x * attn_weights

class CropDiseaseModel(nn.Module):
    def __init__(self, num_classes=38):
        super(CropDiseaseModel, self).__init__()
        # Load pre-trained VGG16
        vgg16 = models.vgg16(weights='DEFAULT')
        self.features = vgg16.features
        
        # Add Attention Mechanism after features
        self.attention = AttentionBlock(512)
        
        self.avgpool = vgg16.avgpool
        
        # Replace classifier
        self.classifier = nn.Sequential(
            nn.Linear(512 * 7 * 7, 4096),
            nn.ReLU(True),
            nn.Dropout(p=0.5),
            nn.Linear(4096, 1024),
            nn.ReLU(True),
            nn.Dropout(p=0.5),
            nn.Linear(1024, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.attention(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x
