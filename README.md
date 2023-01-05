# Improved-reba-Deep-learning-based-rapid-entire-body-assessment

## Introduce

This is a ergonomic assessment tool based on the reba rule, which can precisely classify the behavior risk levle. In order to demonstrate the validity, some examples of gif file from different industries can be shown from following, more visual behavioral risk assessment videos have been released at https://youtu.be/CYp83d9IOSg.

![](gif/c-flooring.gif)
*<p align="center">**construction worker-laying floor**</p>*

![](gif/c-framing.gif)
*<p align="center">**Construction worker-building house frame**</p>*

![](gif/c-rooofing.gif)
*<p align="center">**Construction workers-repairing the roof**</p>*

![](gif/m-carrying.gif)
*<p align="center">**Manufacturing workers-carrying**</p>*

![](gif/m-liftinglowering.gif)
*<p align="center">**Manufacturing workers-lifting and lowering**</p>*

![](gif/m-pushpull.gif)
*<p align="center">**Manufacturing workers-pushing and pulling**</p>*

![](gif/a-planting_the_rice.gif)
*<p align="center">**Farmer-planting rice**</p>*

![](gif/a-land_clearing.gif)
*<p align="center">**Farmer-clearing land**</p>*

![](gif/a-giving_fertilizer.gif)
*<p align="center">**Farmer-giving fertilizer**</p>*

## Quick start 
You can test your custom video as the following preparation in your computer

### Hardware and software requirements
- Ubuntu 18.04  Cuda 10.1
- Anaconda3 Python3.7 Pytorch >= 0.4.0

### Dependencies
please open the terminal, installing the related dependencies by the following command
```sh
pip install -r requirement
```

### Download weight file
download the weight file from google cloud, and put it into the folder "checkpoint/"
``https://drive.google.com/file/d/1pLWtlenS0KOM89mqGDMnJLIvLEFLWhtA/view?usp=sharing``

### Assess the your video
```sh
cd Improved-reba-Deep-learning-based-rapid-entire-body-assessment

#processs the input video and obtain the 2d pose
scp -r input.mp4 /inference/input_directory  
cd inference    
python infer_video_d2.py  --cfg COCO-Keypoints/keypoint_rcnn_R_101_FPN_3x.yaml  --output-dir output_directory  --image-ext mp4  input_directory

#built custom dataset
cd ../data/
python prepare_data_2d_custom.py -i ../inference/output_directory -o myvideos

# obtain the 3d pose and visual, Replace the MP4 file with your own mp4 filename
cd ..
python run.py -d custom -k myvideos -arc 3,3,3,3,3 -c checkpoint \     
--evaluate reba_pose.bin --render --viz-subject input.mp4 --viz-action custom \
--viz-camera 0 --viz-video inference/input_directory/manu3_carrying.mp4 --viz-output input.mp4 --viz-export outputfile --viz-size 6 

# the input video has been induced
python evaluate.py
```




