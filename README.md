# <a name="overview"/>Foreign Object Debris in Airports (FOD-A) Dataset Overview
The FOD-A dataset consists of images of common Foreign Object Debris (FOD) with a runway or taxiway background. While the main annotation style consists of bounding boxes, FOD-A also includes seperate light-level and weather categorization annotations. FOD-A is designed to be easily expanded using a command-line tool developed alongside the dataset. The instructions for this process are contained in a pdf file included in this repository.

<p align="center">
  <img alt="AnnotationExamples" src="Examples/AnnotationExamples.png">
</p>

<p align="center">
  <img alt="Examples" src="Examples/manyEx.png">
</p>
  
<p align="center">
  <img alt="Instances" src="Examples/AnnotationInstancesV2.1.png">
</p>

# <a name="download_instructions"/>Download
It is recommended to use the Pascal VOC format for experimentation and the original format for dataset extension. A train and validation split is provided in the Pascal VOC version. Experiments in the original paper used Pascal VOC version 2.1 (300x300 resolution) with the splits provided in that version. Tools for resizing the annotations and converting the original format to the Pascal VOC format are included in the Tools folder of this repository. 

### Most Current Version Download
[FOD-A Version 2.1 original format (8.3 gb) 400x400 image size](https://drive.google.com/file/d/1lLBJXXaQCWaFa-1MeLAANPpSwMhCJqGh/view?usp=sharing).  
[FOD-A Version 2.1 Pascal VOC format (412 mb) 300x300 image size](https://drive.google.com/file/d/1RdErcq8PGRXZUOGauaACkQG44T-QyZ4x/view?usp=sharing).  

# <a name="citation"/>Citation
If you find this dataset beneficial to your work, consider citing the paper:

Travis Munyer, Pei-Chi Huang, Chenyu Huang, and Xin Zhong. 2021. FOD-A: A Dataset for Foreign Object Debris in Airports. https://arxiv.org/abs/2110.03072  

Travis Munyer, Daniel Brinkman, Chenyu Huang, and Xin Zhong. 2021. Integrative Use of Computer Vision and Unmanned Aircraft Technologies in Public Inspection: Foreign Object Debris Image Collection. arXiv: https://arxiv.org/abs/2106.00161
