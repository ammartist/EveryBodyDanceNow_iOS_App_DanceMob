import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

__weights_dict = dict()

def load_weights(weight_file):
    if weight_file == None:
        return

    try:
        weights_dict = np.load(weight_file).item()
    except:
        weights_dict = np.load(weight_file, encoding='bytes').item()

    return weights_dict

class KitModel(nn.Module):

    
    def __init__(self, weight_file):
        super(KitModel, self).__init__()
        global __weights_dict
        __weights_dict = load_weights(weight_file)

        self.conv1_1 = self.__conv(2, name='conv1_1', in_channels=3, out_channels=64, kernel_size=(3, 3), stride=(1, 1), groups=1, bias=True)
        self.conv1_2 = self.__conv(2, name='conv1_2', in_channels=64, out_channels=64, kernel_size=(3, 3), stride=(1, 1), groups=1, bias=True)
        self.conv2_1 = self.__conv(2, name='conv2_1', in_channels=64, out_channels=128, kernel_size=(3, 3), stride=(1, 1), groups=1, bias=True)
        self.conv2_2 = self.__conv(2, name='conv2_2', in_channels=128, out_channels=128, kernel_size=(3, 3), stride=(1, 1), groups=1, bias=True)
        self.conv3_1 = self.__conv(2, name='conv3_1', in_channels=128, out_channels=256, kernel_size=(3, 3), stride=(1, 1), groups=1, bias=True)
        self.conv3_2 = self.__conv(2, name='conv3_2', in_channels=256, out_channels=256, kernel_size=(3, 3), stride=(1, 1), groups=1, bias=True)
        self.conv3_3 = self.__conv(2, name='conv3_3', in_channels=256, out_channels=256, kernel_size=(3, 3), stride=(1, 1), groups=1, bias=True)
        self.conv3_4 = self.__conv(2, name='conv3_4', in_channels=256, out_channels=256, kernel_size=(3, 3), stride=(1, 1), groups=1, bias=True)
        self.conv4_1 = self.__conv(2, name='conv4_1', in_channels=256, out_channels=512, kernel_size=(3, 3), stride=(1, 1), groups=1, bias=True)
        self.conv4_2 = self.__conv(2, name='conv4_2', in_channels=512, out_channels=512, kernel_size=(3, 3), stride=(1, 1), groups=1, bias=True)
        self.conv4_3_CPM = self.__conv(2, name='conv4_3_CPM', in_channels=512, out_channels=256, kernel_size=(3, 3), stride=(1, 1), groups=1, bias=True)
        self.conv4_4_CPM = self.__conv(2, name='conv4_4_CPM', in_channels=256, out_channels=128, kernel_size=(3, 3), stride=(1, 1), groups=1, bias=True)
        self.conv5_1_CPM_L1 = self.__conv(2, name='conv5_1_CPM_L1', in_channels=128, out_channels=128, kernel_size=(3, 3), stride=(1, 1), groups=1, bias=True)
        self.conv5_1_CPM_L2 = self.__conv(2, name='conv5_1_CPM_L2', in_channels=128, out_channels=128, kernel_size=(3, 3), stride=(1, 1), groups=1, bias=True)
        self.conv5_2_CPM_L1 = self.__conv(2, name='conv5_2_CPM_L1', in_channels=128, out_channels=128, kernel_size=(3, 3), stride=(1, 1), groups=1, bias=True)
        self.conv5_2_CPM_L2 = self.__conv(2, name='conv5_2_CPM_L2', in_channels=128, out_channels=128, kernel_size=(3, 3), stride=(1, 1), groups=1, bias=True)
        self.conv5_3_CPM_L1 = self.__conv(2, name='conv5_3_CPM_L1', in_channels=128, out_channels=128, kernel_size=(3, 3), stride=(1, 1), groups=1, bias=True)
        self.conv5_3_CPM_L2 = self.__conv(2, name='conv5_3_CPM_L2', in_channels=128, out_channels=128, kernel_size=(3, 3), stride=(1, 1), groups=1, bias=True)
        self.conv5_4_CPM_L1 = self.__conv(2, name='conv5_4_CPM_L1', in_channels=128, out_channels=512, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.conv5_4_CPM_L2 = self.__conv(2, name='conv5_4_CPM_L2', in_channels=128, out_channels=512, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.conv5_5_CPM_L1 = self.__conv(2, name='conv5_5_CPM_L1', in_channels=512, out_channels=28, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.conv5_5_CPM_L2 = self.__conv(2, name='conv5_5_CPM_L2', in_channels=512, out_channels=16, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.Mconv1_stage2_L1 = self.__conv(2, name='Mconv1_stage2_L1', in_channels=172, out_channels=128, kernel_size=(7, 7), stride=(1, 1), groups=1, bias=True)
        self.Mconv1_stage2_L2 = self.__conv(2, name='Mconv1_stage2_L2', in_channels=172, out_channels=128, kernel_size=(7, 7), stride=(1, 1), groups=1, bias=True)
        self.Mconv2_stage2_L1 = self.__conv(2, name='Mconv2_stage2_L1', in_channels=128, out_channels=128, kernel_size=(7, 7), stride=(1, 1), groups=1, bias=True)
        self.Mconv2_stage2_L2 = self.__conv(2, name='Mconv2_stage2_L2', in_channels=128, out_channels=128, kernel_size=(7, 7), stride=(1, 1), groups=1, bias=True)
        self.Mconv3_stage2_L1 = self.__conv(2, name='Mconv3_stage2_L1', in_channels=128, out_channels=128, kernel_size=(7, 7), stride=(1, 1), groups=1, bias=True)
        self.Mconv3_stage2_L2 = self.__conv(2, name='Mconv3_stage2_L2', in_channels=128, out_channels=128, kernel_size=(7, 7), stride=(1, 1), groups=1, bias=True)
        self.Mconv4_stage2_L1 = self.__conv(2, name='Mconv4_stage2_L1', in_channels=128, out_channels=128, kernel_size=(7, 7), stride=(1, 1), groups=1, bias=True)
        self.Mconv4_stage2_L2 = self.__conv(2, name='Mconv4_stage2_L2', in_channels=128, out_channels=128, kernel_size=(7, 7), stride=(1, 1), groups=1, bias=True)
        self.Mconv5_stage2_L1 = self.__conv(2, name='Mconv5_stage2_L1', in_channels=128, out_channels=128, kernel_size=(7, 7), stride=(1, 1), groups=1, bias=True)
        self.Mconv5_stage2_L2 = self.__conv(2, name='Mconv5_stage2_L2', in_channels=128, out_channels=128, kernel_size=(7, 7), stride=(1, 1), groups=1, bias=True)
        self.Mconv6_stage2_L1 = self.__conv(2, name='Mconv6_stage2_L1', in_channels=128, out_channels=128, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.Mconv6_stage2_L2 = self.__conv(2, name='Mconv6_stage2_L2', in_channels=128, out_channels=128, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.Mconv7_stage2_L1 = self.__conv(2, name='Mconv7_stage2_L1', in_channels=128, out_channels=28, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.Mconv7_stage2_L2 = self.__conv(2, name='Mconv7_stage2_L2', in_channels=128, out_channels=16, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.Mconv1_stage3_L1 = self.__conv(2, name='Mconv1_stage3_L1', in_channels=172, out_channels=128, kernel_size=(7, 7), stride=(1, 1), groups=1, bias=True)
        self.Mconv1_stage3_L2 = self.__conv(2, name='Mconv1_stage3_L2', in_channels=172, out_channels=128, kernel_size=(7, 7), stride=(1, 1), groups=1, bias=True)
        self.Mconv2_stage3_L1 = self.__conv(2, name='Mconv2_stage3_L1', in_channels=128, out_channels=128, kernel_size=(7, 7), stride=(1, 1), groups=1, bias=True)
        self.Mconv2_stage3_L2 = self.__conv(2, name='Mconv2_stage3_L2', in_channels=128, out_channels=128, kernel_size=(7, 7), stride=(1, 1), groups=1, bias=True)
        self.Mconv3_stage3_L1 = self.__conv(2, name='Mconv3_stage3_L1', in_channels=128, out_channels=128, kernel_size=(7, 7), stride=(1, 1), groups=1, bias=True)
        self.Mconv3_stage3_L2 = self.__conv(2, name='Mconv3_stage3_L2', in_channels=128, out_channels=128, kernel_size=(7, 7), stride=(1, 1), groups=1, bias=True)
        self.Mconv4_stage3_L1 = self.__conv(2, name='Mconv4_stage3_L1', in_channels=128, out_channels=128, kernel_size=(7, 7), stride=(1, 1), groups=1, bias=True)
        self.Mconv4_stage3_L2 = self.__conv(2, name='Mconv4_stage3_L2', in_channels=128, out_channels=128, kernel_size=(7, 7), stride=(1, 1), groups=1, bias=True)
        self.Mconv5_stage3_L1 = self.__conv(2, name='Mconv5_stage3_L1', in_channels=128, out_channels=128, kernel_size=(7, 7), stride=(1, 1), groups=1, bias=True)
        self.Mconv5_stage3_L2 = self.__conv(2, name='Mconv5_stage3_L2', in_channels=128, out_channels=128, kernel_size=(7, 7), stride=(1, 1), groups=1, bias=True)
        self.Mconv6_stage3_L1 = self.__conv(2, name='Mconv6_stage3_L1', in_channels=128, out_channels=128, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.Mconv6_stage3_L2 = self.__conv(2, name='Mconv6_stage3_L2', in_channels=128, out_channels=128, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.Mconv7_stage3_L1 = self.__conv(2, name='Mconv7_stage3_L1', in_channels=128, out_channels=28, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.Mconv7_stage3_L2 = self.__conv(2, name='Mconv7_stage3_L2', in_channels=128, out_channels=16, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.Mconv1_stage4_L1 = self.__conv(2, name='Mconv1_stage4_L1', in_channels=172, out_channels=128, kernel_size=(7, 7), stride=(1, 1), groups=1, bias=True)
        self.Mconv1_stage4_L2 = self.__conv(2, name='Mconv1_stage4_L2', in_channels=172, out_channels=128, kernel_size=(7, 7), stride=(1, 1), groups=1, bias=True)
        self.Mconv2_stage4_L1 = self.__conv(2, name='Mconv2_stage4_L1', in_channels=128, out_channels=128, kernel_size=(7, 7), stride=(1, 1), groups=1, bias=True)
        self.Mconv2_stage4_L2 = self.__conv(2, name='Mconv2_stage4_L2', in_channels=128, out_channels=128, kernel_size=(7, 7), stride=(1, 1), groups=1, bias=True)
        self.Mconv3_stage4_L1 = self.__conv(2, name='Mconv3_stage4_L1', in_channels=128, out_channels=128, kernel_size=(7, 7), stride=(1, 1), groups=1, bias=True)
        self.Mconv3_stage4_L2 = self.__conv(2, name='Mconv3_stage4_L2', in_channels=128, out_channels=128, kernel_size=(7, 7), stride=(1, 1), groups=1, bias=True)
        self.Mconv4_stage4_L1 = self.__conv(2, name='Mconv4_stage4_L1', in_channels=128, out_channels=128, kernel_size=(7, 7), stride=(1, 1), groups=1, bias=True)
        self.Mconv4_stage4_L2 = self.__conv(2, name='Mconv4_stage4_L2', in_channels=128, out_channels=128, kernel_size=(7, 7), stride=(1, 1), groups=1, bias=True)
        self.Mconv5_stage4_L1 = self.__conv(2, name='Mconv5_stage4_L1', in_channels=128, out_channels=128, kernel_size=(7, 7), stride=(1, 1), groups=1, bias=True)
        self.Mconv5_stage4_L2 = self.__conv(2, name='Mconv5_stage4_L2', in_channels=128, out_channels=128, kernel_size=(7, 7), stride=(1, 1), groups=1, bias=True)
        self.Mconv6_stage4_L1 = self.__conv(2, name='Mconv6_stage4_L1', in_channels=128, out_channels=128, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.Mconv6_stage4_L2 = self.__conv(2, name='Mconv6_stage4_L2', in_channels=128, out_channels=128, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.Mconv7_stage4_L1 = self.__conv(2, name='Mconv7_stage4_L1', in_channels=128, out_channels=28, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.Mconv7_stage4_L2 = self.__conv(2, name='Mconv7_stage4_L2', in_channels=128, out_channels=16, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)

    def forward(self, x):
        conv1_1_pad     = F.pad(x, (1, 1, 1, 1))
        conv1_1         = self.conv1_1(conv1_1_pad)
        relu1_1         = F.relu(conv1_1)
        conv1_2_pad     = F.pad(relu1_1, (1, 1, 1, 1))
        conv1_2         = self.conv1_2(conv1_2_pad)
        relu1_2         = F.relu(conv1_2)
        pool1_stage1_pad = F.pad(relu1_2, (0, 1, 0, 1), value=float('-inf'))
        pool1_stage1    = F.max_pool2d(pool1_stage1_pad, kernel_size=(2, 2), stride=(2, 2), padding=0, ceil_mode=False)
        conv2_1_pad     = F.pad(pool1_stage1, (1, 1, 1, 1))
        conv2_1         = self.conv2_1(conv2_1_pad)
        relu2_1         = F.relu(conv2_1)
        conv2_2_pad     = F.pad(relu2_1, (1, 1, 1, 1))
        conv2_2         = self.conv2_2(conv2_2_pad)
        relu2_2         = F.relu(conv2_2)
        pool2_stage1_pad = F.pad(relu2_2, (0, 1, 0, 1), value=float('-inf'))
        pool2_stage1    = F.max_pool2d(pool2_stage1_pad, kernel_size=(2, 2), stride=(2, 2), padding=0, ceil_mode=False)
        conv3_1_pad     = F.pad(pool2_stage1, (1, 1, 1, 1))
        conv3_1         = self.conv3_1(conv3_1_pad)
        relu3_1         = F.relu(conv3_1)
        conv3_2_pad     = F.pad(relu3_1, (1, 1, 1, 1))
        conv3_2         = self.conv3_2(conv3_2_pad)
        relu3_2         = F.relu(conv3_2)
        conv3_3_pad     = F.pad(relu3_2, (1, 1, 1, 1))
        conv3_3         = self.conv3_3(conv3_3_pad)
        relu3_3         = F.relu(conv3_3)
        conv3_4_pad     = F.pad(relu3_3, (1, 1, 1, 1))
        conv3_4         = self.conv3_4(conv3_4_pad)
        relu3_4         = F.relu(conv3_4)
        pool3_stage1_pad = F.pad(relu3_4, (0, 1, 0, 1), value=float('-inf'))
        pool3_stage1    = F.max_pool2d(pool3_stage1_pad, kernel_size=(2, 2), stride=(2, 2), padding=0, ceil_mode=False)
        conv4_1_pad     = F.pad(pool3_stage1, (1, 1, 1, 1))
        conv4_1         = self.conv4_1(conv4_1_pad)
        relu4_1         = F.relu(conv4_1)
        conv4_2_pad     = F.pad(relu4_1, (1, 1, 1, 1))
        conv4_2         = self.conv4_2(conv4_2_pad)
        relu4_2         = F.relu(conv4_2)
        conv4_3_CPM_pad = F.pad(relu4_2, (1, 1, 1, 1))
        conv4_3_CPM     = self.conv4_3_CPM(conv4_3_CPM_pad)
        relu4_3_CPM     = F.relu(conv4_3_CPM)
        conv4_4_CPM_pad = F.pad(relu4_3_CPM, (1, 1, 1, 1))
        conv4_4_CPM     = self.conv4_4_CPM(conv4_4_CPM_pad)
        relu4_4_CPM     = F.relu(conv4_4_CPM)
        conv5_1_CPM_L1_pad = F.pad(relu4_4_CPM, (1, 1, 1, 1))
        conv5_1_CPM_L1  = self.conv5_1_CPM_L1(conv5_1_CPM_L1_pad)
        conv5_1_CPM_L2_pad = F.pad(relu4_4_CPM, (1, 1, 1, 1))
        conv5_1_CPM_L2  = self.conv5_1_CPM_L2(conv5_1_CPM_L2_pad)
        relu5_1_CPM_L1  = F.relu(conv5_1_CPM_L1)
        relu5_1_CPM_L2  = F.relu(conv5_1_CPM_L2)
        conv5_2_CPM_L1_pad = F.pad(relu5_1_CPM_L1, (1, 1, 1, 1))
        conv5_2_CPM_L1  = self.conv5_2_CPM_L1(conv5_2_CPM_L1_pad)
        conv5_2_CPM_L2_pad = F.pad(relu5_1_CPM_L2, (1, 1, 1, 1))
        conv5_2_CPM_L2  = self.conv5_2_CPM_L2(conv5_2_CPM_L2_pad)
        relu5_2_CPM_L1  = F.relu(conv5_2_CPM_L1)
        relu5_2_CPM_L2  = F.relu(conv5_2_CPM_L2)
        conv5_3_CPM_L1_pad = F.pad(relu5_2_CPM_L1, (1, 1, 1, 1))
        conv5_3_CPM_L1  = self.conv5_3_CPM_L1(conv5_3_CPM_L1_pad)
        conv5_3_CPM_L2_pad = F.pad(relu5_2_CPM_L2, (1, 1, 1, 1))
        conv5_3_CPM_L2  = self.conv5_3_CPM_L2(conv5_3_CPM_L2_pad)
        relu5_3_CPM_L1  = F.relu(conv5_3_CPM_L1)
        relu5_3_CPM_L2  = F.relu(conv5_3_CPM_L2)
        conv5_4_CPM_L1  = self.conv5_4_CPM_L1(relu5_3_CPM_L1)
        conv5_4_CPM_L2  = self.conv5_4_CPM_L2(relu5_3_CPM_L2)
        relu5_4_CPM_L1  = F.relu(conv5_4_CPM_L1)
        relu5_4_CPM_L2  = F.relu(conv5_4_CPM_L2)
        conv5_5_CPM_L1  = self.conv5_5_CPM_L1(relu5_4_CPM_L1)
        conv5_5_CPM_L2  = self.conv5_5_CPM_L2(relu5_4_CPM_L2)
        concat_stage2   = torch.cat((conv5_5_CPM_L1, conv5_5_CPM_L2, relu4_4_CPM), 1)
        Mconv1_stage2_L1_pad = F.pad(concat_stage2, (3, 3, 3, 3))
        Mconv1_stage2_L1 = self.Mconv1_stage2_L1(Mconv1_stage2_L1_pad)
        Mconv1_stage2_L2_pad = F.pad(concat_stage2, (3, 3, 3, 3))
        Mconv1_stage2_L2 = self.Mconv1_stage2_L2(Mconv1_stage2_L2_pad)
        Mrelu1_stage2_L1 = F.relu(Mconv1_stage2_L1)
        Mrelu1_stage2_L2 = F.relu(Mconv1_stage2_L2)
        Mconv2_stage2_L1_pad = F.pad(Mrelu1_stage2_L1, (3, 3, 3, 3))
        Mconv2_stage2_L1 = self.Mconv2_stage2_L1(Mconv2_stage2_L1_pad)
        Mconv2_stage2_L2_pad = F.pad(Mrelu1_stage2_L2, (3, 3, 3, 3))
        Mconv2_stage2_L2 = self.Mconv2_stage2_L2(Mconv2_stage2_L2_pad)
        Mrelu2_stage2_L1 = F.relu(Mconv2_stage2_L1)
        Mrelu2_stage2_L2 = F.relu(Mconv2_stage2_L2)
        Mconv3_stage2_L1_pad = F.pad(Mrelu2_stage2_L1, (3, 3, 3, 3))
        Mconv3_stage2_L1 = self.Mconv3_stage2_L1(Mconv3_stage2_L1_pad)
        Mconv3_stage2_L2_pad = F.pad(Mrelu2_stage2_L2, (3, 3, 3, 3))
        Mconv3_stage2_L2 = self.Mconv3_stage2_L2(Mconv3_stage2_L2_pad)
        Mrelu3_stage2_L1 = F.relu(Mconv3_stage2_L1)
        Mrelu3_stage2_L2 = F.relu(Mconv3_stage2_L2)
        Mconv4_stage2_L1_pad = F.pad(Mrelu3_stage2_L1, (3, 3, 3, 3))
        Mconv4_stage2_L1 = self.Mconv4_stage2_L1(Mconv4_stage2_L1_pad)
        Mconv4_stage2_L2_pad = F.pad(Mrelu3_stage2_L2, (3, 3, 3, 3))
        Mconv4_stage2_L2 = self.Mconv4_stage2_L2(Mconv4_stage2_L2_pad)
        Mrelu4_stage2_L1 = F.relu(Mconv4_stage2_L1)
        Mrelu4_stage2_L2 = F.relu(Mconv4_stage2_L2)
        Mconv5_stage2_L1_pad = F.pad(Mrelu4_stage2_L1, (3, 3, 3, 3))
        Mconv5_stage2_L1 = self.Mconv5_stage2_L1(Mconv5_stage2_L1_pad)
        Mconv5_stage2_L2_pad = F.pad(Mrelu4_stage2_L2, (3, 3, 3, 3))
        Mconv5_stage2_L2 = self.Mconv5_stage2_L2(Mconv5_stage2_L2_pad)
        Mrelu5_stage2_L1 = F.relu(Mconv5_stage2_L1)
        Mrelu5_stage2_L2 = F.relu(Mconv5_stage2_L2)
        Mconv6_stage2_L1 = self.Mconv6_stage2_L1(Mrelu5_stage2_L1)
        Mconv6_stage2_L2 = self.Mconv6_stage2_L2(Mrelu5_stage2_L2)
        Mrelu6_stage2_L1 = F.relu(Mconv6_stage2_L1)
        Mrelu6_stage2_L2 = F.relu(Mconv6_stage2_L2)
        Mconv7_stage2_L1 = self.Mconv7_stage2_L1(Mrelu6_stage2_L1)
        Mconv7_stage2_L2 = self.Mconv7_stage2_L2(Mrelu6_stage2_L2)
        concat_stage3   = torch.cat((Mconv7_stage2_L1, Mconv7_stage2_L2, relu4_4_CPM), 1)
        Mconv1_stage3_L1_pad = F.pad(concat_stage3, (3, 3, 3, 3))
        Mconv1_stage3_L1 = self.Mconv1_stage3_L1(Mconv1_stage3_L1_pad)
        Mconv1_stage3_L2_pad = F.pad(concat_stage3, (3, 3, 3, 3))
        Mconv1_stage3_L2 = self.Mconv1_stage3_L2(Mconv1_stage3_L2_pad)
        Mrelu1_stage3_L1 = F.relu(Mconv1_stage3_L1)
        Mrelu1_stage3_L2 = F.relu(Mconv1_stage3_L2)
        Mconv2_stage3_L1_pad = F.pad(Mrelu1_stage3_L1, (3, 3, 3, 3))
        Mconv2_stage3_L1 = self.Mconv2_stage3_L1(Mconv2_stage3_L1_pad)
        Mconv2_stage3_L2_pad = F.pad(Mrelu1_stage3_L2, (3, 3, 3, 3))
        Mconv2_stage3_L2 = self.Mconv2_stage3_L2(Mconv2_stage3_L2_pad)
        Mrelu2_stage3_L1 = F.relu(Mconv2_stage3_L1)
        Mrelu2_stage3_L2 = F.relu(Mconv2_stage3_L2)
        Mconv3_stage3_L1_pad = F.pad(Mrelu2_stage3_L1, (3, 3, 3, 3))
        Mconv3_stage3_L1 = self.Mconv3_stage3_L1(Mconv3_stage3_L1_pad)
        Mconv3_stage3_L2_pad = F.pad(Mrelu2_stage3_L2, (3, 3, 3, 3))
        Mconv3_stage3_L2 = self.Mconv3_stage3_L2(Mconv3_stage3_L2_pad)
        Mrelu3_stage3_L1 = F.relu(Mconv3_stage3_L1)
        Mrelu3_stage3_L2 = F.relu(Mconv3_stage3_L2)
        Mconv4_stage3_L1_pad = F.pad(Mrelu3_stage3_L1, (3, 3, 3, 3))
        Mconv4_stage3_L1 = self.Mconv4_stage3_L1(Mconv4_stage3_L1_pad)
        Mconv4_stage3_L2_pad = F.pad(Mrelu3_stage3_L2, (3, 3, 3, 3))
        Mconv4_stage3_L2 = self.Mconv4_stage3_L2(Mconv4_stage3_L2_pad)
        Mrelu4_stage3_L1 = F.relu(Mconv4_stage3_L1)
        Mrelu4_stage3_L2 = F.relu(Mconv4_stage3_L2)
        Mconv5_stage3_L1_pad = F.pad(Mrelu4_stage3_L1, (3, 3, 3, 3))
        Mconv5_stage3_L1 = self.Mconv5_stage3_L1(Mconv5_stage3_L1_pad)
        Mconv5_stage3_L2_pad = F.pad(Mrelu4_stage3_L2, (3, 3, 3, 3))
        Mconv5_stage3_L2 = self.Mconv5_stage3_L2(Mconv5_stage3_L2_pad)
        Mrelu5_stage3_L1 = F.relu(Mconv5_stage3_L1)
        Mrelu5_stage3_L2 = F.relu(Mconv5_stage3_L2)
        Mconv6_stage3_L1 = self.Mconv6_stage3_L1(Mrelu5_stage3_L1)
        Mconv6_stage3_L2 = self.Mconv6_stage3_L2(Mrelu5_stage3_L2)
        Mrelu6_stage3_L1 = F.relu(Mconv6_stage3_L1)
        Mrelu6_stage3_L2 = F.relu(Mconv6_stage3_L2)
        Mconv7_stage3_L1 = self.Mconv7_stage3_L1(Mrelu6_stage3_L1)
        Mconv7_stage3_L2 = self.Mconv7_stage3_L2(Mrelu6_stage3_L2)
        concat_stage4   = torch.cat((Mconv7_stage3_L1, Mconv7_stage3_L2, relu4_4_CPM), 1)
        Mconv1_stage4_L1_pad = F.pad(concat_stage4, (3, 3, 3, 3))
        Mconv1_stage4_L1 = self.Mconv1_stage4_L1(Mconv1_stage4_L1_pad)
        Mconv1_stage4_L2_pad = F.pad(concat_stage4, (3, 3, 3, 3))
        Mconv1_stage4_L2 = self.Mconv1_stage4_L2(Mconv1_stage4_L2_pad)
        Mrelu1_stage4_L1 = F.relu(Mconv1_stage4_L1)
        Mrelu1_stage4_L2 = F.relu(Mconv1_stage4_L2)
        Mconv2_stage4_L1_pad = F.pad(Mrelu1_stage4_L1, (3, 3, 3, 3))
        Mconv2_stage4_L1 = self.Mconv2_stage4_L1(Mconv2_stage4_L1_pad)
        Mconv2_stage4_L2_pad = F.pad(Mrelu1_stage4_L2, (3, 3, 3, 3))
        Mconv2_stage4_L2 = self.Mconv2_stage4_L2(Mconv2_stage4_L2_pad)
        Mrelu2_stage4_L1 = F.relu(Mconv2_stage4_L1)
        Mrelu2_stage4_L2 = F.relu(Mconv2_stage4_L2)
        Mconv3_stage4_L1_pad = F.pad(Mrelu2_stage4_L1, (3, 3, 3, 3))
        Mconv3_stage4_L1 = self.Mconv3_stage4_L1(Mconv3_stage4_L1_pad)
        Mconv3_stage4_L2_pad = F.pad(Mrelu2_stage4_L2, (3, 3, 3, 3))
        Mconv3_stage4_L2 = self.Mconv3_stage4_L2(Mconv3_stage4_L2_pad)
        Mrelu3_stage4_L1 = F.relu(Mconv3_stage4_L1)
        Mrelu3_stage4_L2 = F.relu(Mconv3_stage4_L2)
        Mconv4_stage4_L1_pad = F.pad(Mrelu3_stage4_L1, (3, 3, 3, 3))
        Mconv4_stage4_L1 = self.Mconv4_stage4_L1(Mconv4_stage4_L1_pad)
        Mconv4_stage4_L2_pad = F.pad(Mrelu3_stage4_L2, (3, 3, 3, 3))
        Mconv4_stage4_L2 = self.Mconv4_stage4_L2(Mconv4_stage4_L2_pad)
        Mrelu4_stage4_L1 = F.relu(Mconv4_stage4_L1)
        Mrelu4_stage4_L2 = F.relu(Mconv4_stage4_L2)
        Mconv5_stage4_L1_pad = F.pad(Mrelu4_stage4_L1, (3, 3, 3, 3))
        Mconv5_stage4_L1 = self.Mconv5_stage4_L1(Mconv5_stage4_L1_pad)
        Mconv5_stage4_L2_pad = F.pad(Mrelu4_stage4_L2, (3, 3, 3, 3))
        Mconv5_stage4_L2 = self.Mconv5_stage4_L2(Mconv5_stage4_L2_pad)
        Mrelu5_stage4_L1 = F.relu(Mconv5_stage4_L1)
        Mrelu5_stage4_L2 = F.relu(Mconv5_stage4_L2)
        Mconv6_stage4_L1 = self.Mconv6_stage4_L1(Mrelu5_stage4_L1)
        Mconv6_stage4_L2 = self.Mconv6_stage4_L2(Mrelu5_stage4_L2)
        Mrelu6_stage4_L1 = F.relu(Mconv6_stage4_L1)
        Mrelu6_stage4_L2 = F.relu(Mconv6_stage4_L2)
        Mconv7_stage4_L1 = self.Mconv7_stage4_L1(Mrelu6_stage4_L1)
        Mconv7_stage4_L2 = self.Mconv7_stage4_L2(Mrelu6_stage4_L2)
        concat_stage7   = torch.cat((Mconv7_stage4_L2, Mconv7_stage4_L1), 1)
        return concat_stage7


    @staticmethod
    def __conv(dim, name, **kwargs):
        if   dim == 1:  layer = nn.Conv1d(**kwargs)
        elif dim == 2:  layer = nn.Conv2d(**kwargs)
        elif dim == 3:  layer = nn.Conv3d(**kwargs)
        else:           raise NotImplementedError()

        layer.state_dict()['weight'].copy_(torch.from_numpy(__weights_dict[name]['weights']))
        if 'bias' in __weights_dict[name]:
            layer.state_dict()['bias'].copy_(torch.from_numpy(__weights_dict[name]['bias']))
        return layer

model = KitModel('pose_faster_pytorch.npy')
input_size = (1, 3, 224, 224)
