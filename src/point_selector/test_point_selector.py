from point_selector import PointSelector

if __name__ == "__main__":
    video_path = "./../data/videos/video_2/video.mp4"
    point_selector = PointSelector(video_path)
    point_selector.select_points()