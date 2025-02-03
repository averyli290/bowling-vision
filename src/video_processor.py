"""
This module contains the VideoProcessor class which is responsible for
processing individual frames of a video.
"""

import cv2
import numpy as np
from util.util import get_lane_points
import os
import time

class VideoProcessor:
    """
    """
    ALLEY_WITDH = 42
    ALLEY_LENGTH = 720

    def __init__(self, folder_path):
        self.folder_path = folder_path 
        self.lane_points = get_lane_points(f"{folder_path}/points")
        self.projective_matrix = None
        self.scale = 2
        self.generate_transform_matrix()
    
    def generate_transform_matrix(self):
        print("Generating transform matrix...")


        alley_coords = [
            [self.ALLEY_WITDH, 0],
            [self.ALLEY_WITDH, self.ALLEY_LENGTH],
            [0, 0],
            [0, self.ALLEY_LENGTH] ]
        src_points = np.float32(self.lane_points)
        dest_points = np.float32([[p[1] * self.scale, p[0] * self.scale] for p in alley_coords])
        self.projective_matrix = cv2.getPerspectiveTransform(src_points, dest_points)
        print("Done generating transform matrix.")
    
    def transform_frame(self, frame):

        colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 255, 0)]
        # red, green, blue, cyan

        transformed_frame = cv2.warpPerspective(frame, self.projective_matrix, (self.ALLEY_LENGTH * self.scale, self.ALLEY_WITDH * self.scale))

        # Annotating original frame
        # for p in range(4):
        #     point = self.lane_points[p]
        #     color = colors[p]
        #     cv2.circle(frame, (int(point[0]), int(point[1])), 5, color, -1)
        # cv2.imshow("original", frame)

        # Annotating transformed frame
        # dest_points = [[42,0],[42,720],[0,0],[0,720]]
        # for p in range(4):
        #     point = dest_points[p]
        #     color = colors[p]
        #     cv2.circle(transformed_frame, (int(point[0]), int(point[1])), 10, color, -1)
        # cv2.imshow("original", frame)

        return transformed_frame

    def pre_process_frame(self):
        print(f"Processing single frame of video {self.folder_path}...")
        transformed_frame = self.transform_frame(cv2.imread('./../data/images/image_1.jpg'))

        return transformed_frame
    
    def process_video(self):
        # load video capture from file
        cap = cv2.VideoCapture(os.path.join(f"{self.folder_path}", "video.mp4"))
        # window name and size
        cv2.namedWindow("video", cv2.WINDOW_AUTOSIZE)
        while cap.isOpened():
            ret, frame = cap.read()

            transformed_frame = self.transform_frame(frame)
            if not ret:
                break

            # Display the frame
            #cv2.imshow('Frame', transformed_frame)
            cv2.imshow('Frame', transformed_frame)

            # Wait for 25ms and check if the user pressed 'q' to exit
            if cv2.waitKey(25) == ord('q'):
                break
        
            time.sleep(0.025)

        cap.release()
        cv2.destroyAllWindows()