import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import cv2
import numpy as np
from fvcore.nn import FlopCountAnalysis, flop_count_table
import torch
import os, sys, time, shutil
from PIL import Image
from torchvision.transforms import transforms
to_pil_image = transforms.ToPILImage()
import torchvision.transforms.functional as F
# from DataLoader.custom_data_class import CustomDataset
# from utils.utils import *
# from utils.checkpoint import *


"""import your models here!"""
from models.Model_0_unet import UNet as My_model



class CustomDataset(torch.utils.data.Dataset):
    def __init__(self, root_dir="./testset", transform=transforms.ToTensor()):
        super(CustomDataset, self).__init__()
        self.root_dir = root_dir
        self.transform = transform

        # Load your dataset files or directories here
        self.files = os.listdir(root_dir)  # List all files in the directory
        print(f"Loaded {len(self.files)} tif files.")  # Replace this with actual file loading logic

    def __len__(self):
        return len(self.files) // 9  # each input consists 9 frames per scene

    def __getitem__(self, idx):
        """
        Returns:
            inputs (Tensor): A batch of 9 input images.
        """
        # Load the input and target images from disk or memory
        input_images = []
        names = os.listdir(self.root_dir)
        # import pdb; pdb.set_trace()
        for i in range(9):  # Assuming you have 8 input images per sample
            img_path = f"{self.root_dir}{names[9*idx + i]}"  # Adjust path according to your naming convention
            img_tensor = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
            if self.transform:
                img_tensor = self.transform(img_tensor)
            input_images.append(img_tensor)
        inputs = torch.stack(input_images)  # Stack the input images into a single tensor
        return inputs

def test(cuda=True, mGPU=True):
    print('Results on the test set ......')

    # the path for saving eval images
    test_dir = './test_img_results'
    if not os.path.exists(test_dir):
        os.mkdir(test_dir)

    # dataset and dataloader
    data_set = CustomDataset(root_dir="./testset/")
    data_loader = torch.utils.data.DataLoader(data_set, batch_size=1, shuffle=False)
    print("Length of the data_loader :", len(data_loader))



    """ Your model will be loaded here, via submitted pytorch code and trained parameters."""
    model = My_model()
    if cuda:
        model = model.cuda()
        device = torch.device("cuda:0")
    else:
        device = torch.device("cpu")

    # load trained model parameters
    if mGPU:
        model = nn.DataParallel(model)
    model.load_state_dict(torch.load('./model_zoo/Ckpt_0_Organizer_team.pth', weights_only=True))
    print('The model has been completely loaded from the user submission.')

    # print parameters and flops
    flops = FlopCountAnalysis(model, torch.ones(1, 9, 768, 1536).to(device))
    print(flop_count_table(flops))

    num_params = sum(p.numel() for p in model.parameters())
    print("\n" + "="*20 +" Model params and FLOPs " + "="*20)
    print(f"\tTotal # of model parameters : {num_params / (1000**2) :.3f} M")
    print(f"\tTotal FLOPs of the model : {flops.total() / (1000**4) :.3f} T")
    print("=" * 64)
    print('\n------- Fusion started -------\n')


    model.eval()

    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)
    timings=[]
    with torch.no_grad():
        for i, burst_noise in enumerate(data_loader):
            
            if cuda:
                burst_noise = burst_noise.cuda()

            burst_noise = burst_noise.squeeze(2)
             
            start.record()
            pred = model(burst_noise)
            end.record()
            torch.cuda.synchronize()
            timei=start.elapsed_time(end)
            timings.append(timei)
                
            pred = torch.clamp(pred, 0.0, 1.0)
            
            
            
            if cuda:
                pred = pred.cpu()
                burst_noise = burst_noise.cpu()


            # to save the output image
            names = os.listdir("./testset")
            ii = i * 9
            out_file_name = test_dir + f'/' + names[ii][:-9] + f'-out.tif'
            cv2.imwrite(out_file_name, (pred[0]*255).permute(1,2,0).cpu().numpy().astype(np.uint8))
            print(f'{i+1}-th image is completed.\t| {out_file_name} \t| time: {timei:.2f} ms.')


            
    mean_time=np.mean(timings)
    print(f'Total Validation time : {mean_time: .2f} ms.')

if __name__ == '__main__':
    test()