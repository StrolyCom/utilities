from PIL import Image, ImageDraw, ImageFont
import os
import glob
import random
import json
import argparse
from progressbar import ProgressBar, Percentage, Bar, ETA, FileTransferSpeed


def check_or_create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_image_files(path):
    extensions = ("*.jpg", "*.jpeg", "*.JPG", "*.JPEG")
    file_list = []
    for extension in extensions:
        file_list.extend(glob.glob(os.path.join(path, extension)))
    return file_list


def get_json_for_image(image_path):
    parent = os.path.dirname(image_path)
    no_ext = os.path.basename(image_path).split(".")[0]
    return os.path.join(parent, no_ext+".json")


def check_json_files(file_list, debug=False):
    for f in file_list:
        json_file = get_json_for_image(f)
        if not os.path.isfile(json_file):
            print("\033[91m ERROR: Cannot find json file '%s'\033[0m" % json_file)
            exit(1)
        elif debug:
            print("  - Verified JSON file '%s'" % json_file)


def process(file_list, output, debug=False):
    images_done = 0
    total_images = len(file_list)

    if not debug:
        widgets = ['Progress: ', Percentage(), ' ', Bar(marker='=', left='[', right=']'),
                   ' ', ETA(), ' ', FileTransferSpeed()]
        pbar = ProgressBar(widgets=widgets, maxval=total_images)
        pbar.start()

    random.shuffle(file_list)
    for (i, f) in enumerate(file_list):
        if debug:
            print("Processing "+f)
        im = Image.open(f)
        file_name = os.path.basename(f)
        base, extension = file_name.split(".")
        width, height = im.size
        texts = Image.new('RGB', (width, height), (255, 255, 255))
        output_file = os.path.join(output, file_name)
        output_file_texts = os.path.join(output, base+"_text."+extension)

        pdraw = ImageDraw.Draw(im)
        ptext = ImageDraw.Draw(texts)

        json_file = get_json_for_image(f)
        data = json.load(open(json_file))
        if 'textAnnotations' not in data['responses'][0]:
            continue

        for p in data['responses'][0]['textAnnotations'][1:]:
            points = []
            vertices = p['boundingPoly']['vertices']
            for v in vertices:
                if 'x' not in v:
                    x = 0
                else:
                    x = int(v['x'])
                if 'y' not in v:
                    y = 0
                else:
                    y = int(v['y'])
                points.append((x, y))
            pdraw.polygon(points, fill=None, outline=(255, 0, 255, 0))
            height = abs(points[0][1] - points[3][1])
            if height < 5:
                height = abs(points[0][1] - points[1][1])

            font = ImageFont.truetype("Arial Unicode.ttf", height)
            ptext.text(points[0], p['description'], fill=(0, 0, 0, 0), font=font)
            ptext.polygon(points, fill=None, outline=(0, 0, 0, 0))
        im.save(output_file)
        texts.save(output_file_texts)
        images_done += 1
        if not debug:
            pbar.update(images_done)

    if not debug:
        pbar.finish()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Visualize the results of google OCR in two different ways.\n"
                    "1. A blank image with only the detected text.\n"
                    "2. A copy of the original image, with the detected polygons drawn.\n"
                    "It is expected that the original images and a correspondig .json "
                    "file are in the same directory --images_path."
    )
    parser.add_argument("-i", "--images_path",
                        metavar="/path/to/images/",
                        help="Path to image files. Defaults to current directory,",
                        default="."
                        )
    parser.add_argument("-o", "--ouput_path",
                        metavar="/path/to/store/output",
                        help="Path to store the results. Defaults to <path/to/images>/output",
                        default=None)
    parser.add_argument("-d", "--debug",
                        help="Run in debug mode. Even more information is printed",
                        action="store_true",
                        default=False)
    args = parser.parse_args()

    images_path = args.images_path
    if not os.path.isdir(images_path):
        print("\033[91m ERROR: Images path '%s' is not a directory\033[0m "
              % images_path)
        exit(1)

    ouput_path = args.ouput_path or os.path.join(images_path, "output/")
    debug = args.debug

    check_or_create_dir(ouput_path)
    file_list = get_image_files(images_path)

    print("Welcome")
    print("Going to read from %s" % images_path)
    print("Going to create annotated images on %s" % ouput_path)

    if debug:
        print("There are "+str(len(file_list))+" images to be processed")

    print("Checking if there is a json file for each of the images")
    check_json_files(file_list, debug=debug)

    process(file_list, ouput_path, debug)
