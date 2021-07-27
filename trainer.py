import os
import time
from collections import OrderedDict

import torch
import torch.distributed as dist
import torch.optim
import torchvision.utils as vutils
from torch.utils.data import DataLoader

from data.CRN_dataset import CRNShapeNet
from data.ply_dataset import PlyDataset


from arguments import Arguments

from utils.pc_transform import voxelize
from utils.plot import draw_any_set
from utils.common_utils import *
from utils.inversion_dist import *
from loss import *

from shape_inversion import ShapeInversion

from model.treegan_network import Generator, Discriminator
from external.ChamferDistancePytorch.chamfer_python import distChamfer, distChamfer_raw

import random

class Trainer(object):

    def __init__(self, args):
        self.args = args
        
        if self.args.dist:
            self.rank = dist.get_rank()
            self.world_size = dist.get_world_size()
        else:
            self.rank, self.world_size = 0, 1

        self.inversion_mode = args.inversion_mode
        
        save_inversion_dirname = args.save_inversion_path.split('/')
        log_pathname = './logs/'+save_inversion_dirname[-1]+'.txt'
        args.log_pathname = log_pathname

        self.model = ShapeInversion(self.args)
        if self.inversion_mode == 'morphing':
            self.model2 = ShapeInversion(self.args)
            self.model_interp = ShapeInversion(self.args)
        
        if self.args.dataset in ['MatterPort','ScanNet','KITTI','PartNet']:
            dataset = PlyDataset(self.args)
        else: 
            dataset = CRNShapeNet(self.args)
        
        sampler = DistributedSampler(dataset) if self.args.dist else None

        if self.inversion_mode == 'morphing':
            self.dataloader = DataLoader(
                dataset,
                batch_size=2,
                shuffle=False,
                sampler=sampler,
                num_workers=1,
                pin_memory=False)
        else:
            self.dataloader = DataLoader(
                dataset,
                batch_size=1,
                shuffle=False,
                sampler=sampler,
                num_workers=1,
                pin_memory=False)

        # set generator parameter file path
        if self.args.GAN_save_every_n_data > 0:
            if not os.path.exists(self.args.GAN_ckpt_path):
                os.makedirs(self.args.GAN_ckpt_path)

    def train(self):
        pass

if __name__ == "__main__":
    args = Arguments(stage='inversion').parser().parse_args()
    args.device = torch.device('cuda:'+str(args.gpu) if torch.cuda.is_available() else 'cpu')
    torch.cuda.set_device(args.device)
    
    if not os.path.isdir('./logs/'):
        os.mkdir('./logs/')
    if not os.path.isdir('./saved_results'):
        os.mkdir('./saved_results')
    
    if args.dist:
        rank, world_size = dist_init(args.port)

    trainer = Trainer(args)
    trainer.run()
    
    