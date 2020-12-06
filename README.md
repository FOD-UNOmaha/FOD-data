# FOD-data
A dataset of foreign object debris (FOD) designed for computer vision applications.

# Foreign Object Debris Dataset Overview
This foreign object debris (FOD) dataset is an image dataset with bounding box annotations. The intent is to utilize a model trained by this dataset to locate and categorize FOD in the airport environment. When FOD is allowed to remain in airport premises it can pierce vital components or become injested by jet engines, which can cause exhorbitant repair costs and/or injury to nearby personages. The initial goal is to utilize this model in stationary cameras or unmanned aerial vehicles (UAVs) to detect FOD and alert airport staff.

## Samples Images with Bounding Boxes
![alt text](Examples\ExampleImages.png)

# Dataset Specifications
The FOD dataset consists of thousands of images (currently 12,971 images) of common FOD objects and types of material with a typical runway or taxiway background. All images are stored with a resolution of 400x400. Soon, however, we will release our resizing tool tailored to this dataset to another github repository. This tool can resize the images and annotations of this dataset to any required resolution. During initial dataset preperation, images were stripped, frame by frame, from videos taken of object using our expansion tool. These videos were recorded in a local airport to ensure accuracy. Once the frames from these videos were stored indivudally as '.png' files, the videos were manually annotated using an open-source tool aptly named Computer Vision Annotation Tool (CVAT).

## Dataset Counts
| Object | Image Count |
|--------|-------|
| Bolts  | 3116  |
| Nuts | 520 |
| Metal sheet | 394 |
| Adjustable Clamp | 583 |
| Washers | 1797 |
| Luggage tag | 937 |
| Pliers | 1420 |
| Nail | 1005 |
| Hose | 295 |
| Bolt/Nut combination | 540 |
| Wrenches | 2364 |
| Total | 12971 |

## File Format
Each individual folder is a seperate annotated video. Within each of these folders, there is a folder of '.PNG' images labeled numberically from zero until the final frame and a separate folder containing the .XML which is also sequentially numbered from 0. At this time, we require the annotation file names to match the '.PNG' filenames. For example, frame_000440.PNG correlates to frame_000440.XML.

## Expansion Directions
This dataset was designed to be easily expanded (as needed) using a command-line tool developed specifically for this dataset. This tool and step-by-step directions will be released soon, alongside a detailed paper explaining this dataset and future theories for it's use. Instructions will be clearly explained in this section, and the open-source expansion tool will be located in a seperate github repository.

# Links
CVAT Link - https://github.com/openvinotoolkit/cvat

# Coming Soon
- expansion directions
- dataset resizing tool
- dataset expansion tool
