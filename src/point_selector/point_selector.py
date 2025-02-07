
import cv2

class PointSelector:
    def __init__(self, video_path):
        self.points = []
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        self.frame = self.cap.read()[1]
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.on_mouse)
    
    def on_mouse(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(self.frame,(x,y),10,(255,0,0),-1)
            print("Adding point...")
            self.points.append([x, y])
            for point in self.points:
                print(f"{point[0]},{point[1]}")

    def select_points(self):
        while(1):
            cv2.imshow('image',self.frame)
            k = cv2.waitKey(25)
            if k == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()
