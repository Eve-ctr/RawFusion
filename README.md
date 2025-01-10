# Efficient Burst HDR and Restoration
<p align="center">
    <img src="./figure.png" width="883px" height="618px" title="Figure"/>

## Overview
This is a competition held in CVPR 2025 New Trends in Image Restoration and Enhancement (NTIRE) workshop. The goal of
this competition is to develop an efficient algorithm for burst HDR and restoration. 

More precisely, this competition involves the following tasks:
* **Multi-frame RAW image fusion** : The inputs are given as multi-frame RAW images that follow Bayer patterns (GRBG).
* **HDR image synthesis** : The given nine frames have different brightness levels. The goal is to fuse these frames into a high dynamic range (HDR) image. 
* **Restoration** : The goal is to restore GT image from degraded RAW images, such as noise, translation, motion blur, and so on.
 
Overall, it is challenging to study an efficient algorithm for both multi-frame fusion and restoration.
The ultimate goal of this work is to develop an on-device model that can be deployed on mobile devices, so there are time and memory constraints.
For more details, see https://codalab.lisn.upsaclay.fr/competitions/21191#learn_the_details-overview .


## Dataset
The training, validation, and test datasets are constructed using the same method. 
Training and validation datasets can be downloaded via an external link in the competition homepage. 
Test dataset will be provided later. All images have the same size, 2000(H) x 3000(W). 

The specific configuration of datasets is as follows: 
* **Training** : Consists of 200 scenes, where each scene contains 9 RAW input frames and one GT RGB image. 
* **Validation** : Consists of 20 scenes, and GT images are hidden from participants, but PSNR and SSIM results are evaluated and will be announced on the leaderboard. 
* **Test** : Consists of 20 scenes, and both GT images and evaluation results are hidden from participants during the competition. The final ranking will be based on the
  PSNR results of the test set.

The downloaded training dataset contains 200 scenes, where each scene consists of nine input RAW frames ("Scene-xxx-in-0.tif" through "Scene-xxx-in-8.tif") and one ground
truth image ("Scene-xxx-gt.tif"). All training files (including GT images) are recommended to be stored in one folder, in the same level as the starting kit.
For example, the structure of the directory should look like this: 
```
# directory hierarchy
{root}/{dataset}/{trn}/{Scene-xxx-in-0.tif}
{root}/{dataset}/{trn}/{Scene-xxx-gt.tif}
{root}/{starting kit}/{README.md}
```

The provided nine input frames have three brightness levels (low, middle, and high), which induces three different level of noises. 
They further have the following characteristics: (We use the naming "Scene-xxx-in-0.tif" for convenience.)
1. **Scene-xxx-in-0.tif** : This is the *reference frame*, aligned with GT image. Other all frames may not be aligned with the GT image. 
This frame  is taken by a short exposure time, thus it has a high level noise.  
2. **Scene-xxx-in-1.tif** and **Scene-xxx-in-2.tif** : These two frames have the same exposure time with the reference frame.
3. **Scene-xxx-in-3.tif** to **Scene-xxx-in-5.tif** : These three frames have the middle exposure time, thus brighter than the reference frame, which means the level of noise is slightly decreased. 
4. **Scene-xxx-in-6.tif** to **Scene-xxx-in-8.tif** : These three frames are made through high exposure time which have the lowest noise level.

<p align="center">
<img src="./DB.png" width="1000px" height="562px" title="DB_example"/>
(Although the image appears saturated for visualization purposes, the actual data values are not clipped and maintain accurate values.)

Therefore, the key point of this competition is struggling *"how to effectively utilize the information of input frames while
considering the characteristics of each frame."* 

## Baseline model
The baseline model is given by a very simple U-net architecture. 
The shape of input of the network follows `(batch x 9 x 2000 x 3000)`, and the output shape follows `(batch x 
3 x 2000 x 3000)`.
The basic loss implemented in this starting kit is MSE loss.
Codes for computing PSNR and SSIM are provided in the utils folder.  



## Submissions
Participants can submit their trained models via code and trained parameters. 
Each submission should include a zip file containing the network architecture (`my_network.py`), and the trained
parameters (`my_parameters.pth`) saved by `model.state_dict()`. The submission system will evaluate the performance of the submitted model on the
validation set and provide the average PSNR, SSIM scores with inference time, FLOPs, and the number of all parameters.
Submission for each participant / team is limited up to 10 times per day. 


## Other competition rules
All training datasets and their images must not be shared with others or used for other purposes.
Regarding training processes and techniques, anything is possible as long as it does not violate 
the time and memory constraints we set in this challenge 
(e.g. using other public data for pre-training, importing pre-trained networks, using generative models, etc.).
In addition, it is not necessary to use all the input frames - to save memory and FLOPs, only a few frames may be selected and utilized. 

## Contacts
For any questions regarding this competition, please ask through forum of our competition site or contact to the organizers via email. 



















