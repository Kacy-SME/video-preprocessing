import os
from moviepy.editor import VideoFileClip
import pandas as pd

def extract_video_metadata(video_path):
    """ Extract metadata from a single video file. """
    with VideoFileClip(video_path) as clip:
        width, height = clip.size
        duration = clip.duration
    file_size = os.path.getsize(video_path)
    return {'Filename': os.path.basename(video_path),
            'Width': width,
            'Height': height,
            'Duration (seconds)': duration,
            'File Size (bytes)': file_size}

def process_videos(directory):
    """ Process all video files in the given directory and save metadata to CSV. """
    data = []
    for filename in os.listdir(directory):
        if filename.endswith(('.mp4', '.avi', '.mov', '.mkv')):  # Add other video formats as needed
            full_path = os.path.join(directory, filename)
            try:
                metadata = extract_video_metadata(full_path)
                data.append(metadata)
            except Exception as e:
                print(f"Failed to process {filename}: {str(e)}")

    # Convert list to DataFrame
    df = pd.DataFrame(data)
    # Save to CSV
    df.to_csv('video_metadata.csv', index=False)
    print("Metadata extraction complete and saved to 'video_metadata.csv'.")

# Replace 'path_to_your_video_directory' with the path to your video directory
process_videos('/Users/kacy/Desktop/Summer24/video-preprocessing/interaction-raw-data')
