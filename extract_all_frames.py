import os
import imageio
from skimage import img_as_ubyte
from skimage.transform import resize, rotate
from skimage.util import img_as_ubyte
import numpy as np
from argparse import ArgumentParser
from tqdm import tqdm

def save_frame(frame, filename, format='.png'):
    """ Save a single frame as an image in the specified format. """
    imageio.imwrite(filename, img_as_ubyte(frame))  # Ensure frame is in the right data type

def process_frames(frames, output_path, image_shape=None, flip_horizontally=False, flip_vertically=False):
    """ Apply transformations to frames and save them. """
    for idx, frame in enumerate(frames):
        if image_shape is not None:
            frame = resize(frame, image_shape, anti_aliasing=True)
        if flip_horizontally:
            frame = np.fliplr(frame)
        if flip_vertically:
            frame = np.flipud(frame)
        filename = os.path.join(output_path, f"frame_{idx:05d}.png")
        save_frame(frame, filename)

def process_video(video_path, output_path, image_shape=None, flip_horizontally=False, flip_vertically=False):
    """ Process a video file to extract and transform frames, then save them. """
    try:
        reader = imageio.get_reader(video_path)
        frames = [frame for frame in reader]
        process_frames(frames, output_path, image_shape, flip_horizontally, flip_vertically)
    except Exception as e:
        print(f"Error processing video {video_path}: {e}")

def main():
    parser = ArgumentParser()
    parser.add_argument("--video_folder", help="Path to video files", default='./videos')
    parser.add_argument("--out_folder", help="Path to output", default='./output')
    parser.add_argument("--image_shape", type=lambda x: tuple(map(int, x.split(','))), default=None,
                        help="Image shape, None for no resize")
    parser.add_argument("--flip_horizontally", action='store_true', help="Flip frames horizontally")
    parser.add_argument("--flip_vertically", action='store_true', help="Flip frames vertically")
    args = parser.parse_args()

    if not os.path.exists(args.video_folder):
        os.makedirs(args.video_folder)
    if not os.path.exists(args.out_folder):
        os.makedirs(args.out_folder)

    video_files = [f for f in os.listdir(args.video_folder) if f.endswith('.mp4')]
    for video_file in tqdm(video_files):
        video_path = os.path.join(args.video_folder, video_file)
        output_path = os.path.join(args.out_folder, os.path.splitext(video_file)[0])
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        process_video(video_path, output_path, args.image_shape, args.flip_horizontally, args.flip_vertically)

if __name__ == "__main__":
    main()

