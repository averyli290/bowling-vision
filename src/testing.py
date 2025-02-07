"""
File used to test functionality.
"""

from video_processor import VideoProcessor
from util.util import get_lane_points
import cv2
import sys

if __name__ == "__main__":
    window_name = "image"

    folder_path = "./../data/videos/video_2"
    
    video_processor = VideoProcessor(folder_path=folder_path)
    video_processor.process_video()