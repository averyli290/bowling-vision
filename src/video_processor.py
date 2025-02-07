"""
This module contains the VideoProcessor class which is responsible for
processing individual frames of a video.
"""

import cv2
import numpy as np
from util.util import get_lane_points
import os

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

        # How can we warp the Perspective with a non-linear mapping?

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
        #fgbg = cv2.bgsegm.createBackgroundSubtractorMOG2()
        fgbg = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=25, detectShadows=False)
        fgbg2 = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=25, detectShadows=False)

        cap = cv2.VideoCapture(os.path.join(f"{self.folder_path}", "video.mp4"))
        # window name and size
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break


            fgmask = fgbg.apply(frame)
            _, fgmask = cv2.threshold(fgmask, 254, 255, cv2.THRESH_BINARY)
            #transformed_frame = self.transform_frame(fgmask)

            transformed_frame = self.transform_frame(frame)
            fgmask2 = fgbg2.apply(transformed_frame)
            _, fgmask2 = cv2.threshold(fgmask2, 254, 255, cv2.THRESH_BINARY)

            contours, _ = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 50:
                    cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 3)

            contours_2, _ = cv2.findContours(fgmask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours_2:
                area = cv2.contourArea(cnt)
                if area > 50:
                    cv2.drawContours(transformed_frame, [cnt], -1, (0, 255, 0), 3)
            
            # Display the frame
            cv2.imshow('Transformed', transformed_frame)
            cv2.imshow('Mask', fgmask)

            # Apply Gaussian blur to reduce noise
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)

            # Canny edge detection
            # edges = cv2.Canny(blurred, 100, 200)
            # transformed_frame_2 = self.transform_frame(edges)
            # cv2.imshow('Transformed Edges', transformed_frame_2)
            # Display the results
            # cv2.imshow('Edges', edges)

            # Display the original
            cv2.imshow('Original', frame)

            # Wait for 25ms and check if the user pressed 'q' to exit
            if cv2.waitKey(25) == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
