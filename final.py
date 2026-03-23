import subprocess
import os
from pathlib import Path

def concatenate_videos(video_paths, output_name="combined_rasters.mp4"):
    """
    Concatenate multiple video files using ffmpeg
    """
    # Check if all files exist
    valid_videos = []
    for video in video_paths:
        if os.path.exists(video):
            valid_videos.append(video)
            print(f"✓ Found: {os.path.basename(video)}")
        else:
            print(f"✗ Warning: {video} not found")
    
    if not valid_videos:
        print("No valid videos found!")
        return False
    
    # Create file list for ffmpeg
    with open('file_list.txt', 'w') as f:
        for video in valid_videos:
            f.write(f"file '{os.path.abspath(video)}'\n")
    
    # Run ffmpeg concatenation
    cmd = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', 'file_list.txt',
        '-c', 'copy',  # Copy without re-encoding (fast)
        '-y',  # Overwrite output if exists
        output_name
    ]
    
    print(f"\n🎬 Concatenating {len(valid_videos)} videos...")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ Successfully created: {output_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"Error output: {e.stderr}")
        return False
    finally:
        # Clean up temporary file
        if os.path.exists('file_list.txt'):
            os.remove('file_list.txt')

# Define the videos you want to concatenate (in order)
# Adjust paths based on your actual folder structure
videos_to_concat = [
    "media/videos/Boundary/1080p60/Boundary.mp4",
    "media/videos/Circle/1080p60/GridCircle.mp4",
    "media/videos/Ellipse/1080p60/GridEllipse.mp4",
    "media/videos/Line/1080p60/GridLine.mp4",
]

# Also check if dda_manim has a video
dda_video = "media/videos/dda_manim/1080p60/GridLine.mp4"
if os.path.exists(dda_video):
    videos_to_concat.append(dda_video)

# Run the concatenation
if __name__ == "__main__":
    print("=" * 50)
    print("Concatenating Raster Manim Videos")
    print("=" * 50)
    concatenate_videos(videos_to_concat, "all_rasters_combined.mp4")
