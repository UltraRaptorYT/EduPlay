import os
from moviepy.editor import VideoFileClip

def convert_videos_to_gifs(input_folder, output_folder):
    duration = 10  # Duration in seconds
    fps = 33  # Frames per second

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.mp4'):
            video_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.gif')

            # Convert the video to GIF
            clip = VideoFileClip(video_path).subclip(0, duration)
            clip.write_gif(output_path, fps=fps)

# Example usage
input_folder = r"C:/Users/Moham/Downloads/videos"
output_folder = r"C:/Users/Moham/OneDrive/Desktop/EduPlay/New_GIFs(use_this)"

convert_videos_to_gifs(input_folder, output_folder)
