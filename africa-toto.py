import cv2
import argparse
import numpy
import glob
import os
from PIL import Image, ImageDraw
from multiprocessing import Process, Queue
import time


def extract_images(videosrc, imagedest, timeint=1):
    vidcap = cv2.VideoCapture(videosrc)
    print("Total video frames: ", vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    print("Video FPS: {:.2f}".format(vidcap.get(cv2.CAP_PROP_FPS), 3))
    print("Total video time: {:.2f} minutes".format(int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT) /
                                                        vidcap.get(cv2.CAP_PROP_FPS)) / 60, 2))
    success, image = vidcap.read()
    count = 0

    # Save all frames to folder.
    print("Extracting frames...")
    while success:
        if args.time_interval:
            vidcap.set(cv2.CAP_PROP_POS_MSEC, (count * 1000))  # Capture frame every x seconds
        cv2.imwrite(imagedest + "\\%d.jpg" % count, image)  # save frame as JPEG file
        success, image = vidcap.read()
        count += timeint
    print("Finished extracting frames...")


def create_queue(imagedest):
    for image in sorted(glob.glob(imagedest + "\\*"), key=os.path.getmtime):
        q.put(image)
    return q


def get_color(q):
    color_array = []
    while not q.empty():
        myimg = cv2.imread(q.get())  # read frame
        avg_color_per_row = numpy.average(myimg, axis=0)  # get average per row
        avg_color = numpy.average(avg_color_per_row, axis=0)  # get average for whole image
        color_array.append(reversed(avg_color.astype(int)))
    return color_array


def create_final_image(colors, imgheight):
    print("Processing final image...")
    finalimage = Image.new("RGB", (len(colors), imgheight))  # create blank canvas
    finalimagedraw = ImageDraw.Draw(finalimage)
    count = 0
    print("Drawing %d colors" % len(colors))
    for i in colors:
        finalimagedraw.line([(count, 0), (count, 1000)], fill=tuple(i))  # draw colors onto canvas
        count = count + 1
        finalimage.save(os.path.splitext(args.path_in)[0] + "_avgcolor_spectrum.PNG")
    print("Final image processed!")


def clean_up(imagedest):
    if not args.no_clean_up:
        pass
    else:
        print("Cleaning up generated frames...")
        generated_frames = os.listdir(imagedest)
        for frame in generated_frames:
            if frame.endswith(".jpg"):
                os.remove(os.path.join(imagedest, frame))
        print("Cleanup Complete")


if __name__ == '__main__':
    a = argparse.ArgumentParser(description="Taken a given video file, output an image of average frame colors.")
    a.add_argument("--path-in", help="path to src video", required=True, type=str)
    a.add_argument("--path-out", help="path to dest image folder", required=True, type=str)
    a.add_argument("--time-interval", help="time interval to take frame capture. this will affect final image size",
                   type=int)
    a.add_argument("--img-height", help="image height of output file. default 650px. this will affect final image size",
                   type=int, nargs='?', const=650, default=650)
    a.add_argument("--no-clean-up", help="removes all captured frames to save space. default 'yes'",
                   action="store_false")
    args = a.parse_args()
    q = Queue()
    if not args.time_interval:
        s = time.perf_counter()
        extract_images(args.path_in, args.path_out)
        p = Process(target=get_color, args=(q,))
        create_final_image(get_color(create_queue(args.path_out)), args.img_height)
        clean_up(args.path_out)
        e = time.perf_counter() - s
        print(f"Executed in {e:0.2f} seconds.")
    else:
        s = time.perf_counter()
        extract_images(args.path_in, args.path_out, args.time_interval)
        p = Process(target=get_color, args=(q,))
        create_final_image(get_color(create_queue(args.path_out)), args.img_height)
        clean_up(args.path_out)
        e = time.perf_counter() - s
        print(f"Executed in {e:0.2f} seconds.")
