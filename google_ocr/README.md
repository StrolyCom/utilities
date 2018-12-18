# Google OCR Utilities

###  Description 
 We use [Google Vision API](https://cloud.google.com/vision/) to extract the text
from images. This category includes several tools to visualize, process, or analyze the output of
the API, mainly of the OCR.

==============

#### 1. __visualize_google_ocr.py__

This script is used to create a visualization of the results of the Google Vision API 
[Optical Character Recognition](https://cloud.google.com/vision/docs/ocr). It can be done
in batch, with the content of a complete directory.

It creates two images, one contains only the texts in the same position and trying to approximate
the same size. The other one draws the detected polygons on top of the original image

![Texts](https://raw.githubusercontent.com/StrolyCom/utilities/master/google_ocr/images_example/output/_JTB_MyTokyo_EN_Zentaizu_text.jpg)
![Polygons](https://raw.githubusercontent.com/StrolyCom/utilities/master/google_ocr/images_example/output/_JTB_MyTokyo_EN_Zentaizu.jpg)

Usage:

```bash
$ python google_ocr/visualize_google_ocr.py -h
usage: visualize_google_ocr.py [-h] [-i /path/to/images/]
                               [-o /path/to/store/output] [-d]

Visualize the results of google OCR in two different ways. 1. A blank image
with only the detected text. 2. A copy of the original image, with the
detected polygons drawn. It is expected that the original images and a
correspondig .json file are in the same directory --images_path.

optional arguments:
  -h, --help            show this help message and exit
  -i /path/to/images/, --images_path /path/to/images/
                        Path to image files. Defaults to current directory,
  -o /path/to/store/output, --ouput_path /path/to/store/output
                        Path to store the results. Defaults to
                        <path/to/images>/output
  -d, --debug           Run in debug mode. Even more information is printed
```

For instance:

```bash
$ python google_ocr/visualize_google_ocr.py -i google_ocr/images_example/ -d
Welcome
Going to read from google_ocr/images_example/
Going to create annotated images on google_ocr/images_example/output/
There are 2 images to be processed
Checking if there is a json file for each of the images
  - Verified JSON file 'google_ocr/images_example/_JTB_MyTokyo_EN_Zentaizu.json'
  - Verified JSON file 'google_ocr/images_example/_JTB_MyTokyo_CN_asakusa.json'
Processing google_ocr/images_example/_JTB_MyTokyo_EN_Zentaizu.jpg
Processing google_ocr/images_example/_JTB_MyTokyo_CN_asakusa.jpg
```

__NOTE__: Naturally it is suposed that you already have the results of OCR as a .json file, and 
the images in the same directory. Like in the directory `google_ocr/images_example/`.

#### 2. TO-DO


