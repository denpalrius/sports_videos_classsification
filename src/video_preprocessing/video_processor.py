import cv2
import numpy as np
from config import VideoClassificationConfig


class VideoProcessor:
    def __init__(self, config: VideoClassificationConfig):
        self.config = config

    def load_video(self, video_path: str) -> cv2.VideoCapture:
        return cv2.VideoCapture(video_path)

    def load_and_preprocess_video(self, video_path: str) -> np.ndarray:
        cap = self.load_video(video_path)
        frames = []
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame = self.crop_center_square(frame)
                frame = self.resize_frame(frame, (self.config.image_size, self.config.image_size))
                frame = frame[:, :, [2, 1, 0]]  # BGR to RGB
                frame = self.normalize_frame(frame)
                frames.append(frame)
                
                if len(frames) == self.config.max_sequence_length:
                    break
        finally:
            cap.release()
        
        return np.array(frames)

    def crop_center_square(self, frame: np.ndarray) -> np.ndarray:
        y, x = frame.shape[0:2]
        min_dim = min(y, x)
        start_x = (x // 2) - (min_dim // 2)
        start_y = (y // 2) - (min_dim // 2)
        return frame[start_y:start_y + min_dim, start_x:start_x + min_dim]

    def resize_frame(self, frame: np.ndarray, size: tuple) -> np.ndarray:
        return cv2.resize(frame, size)

    def normalize_frame(self, frame: np.ndarray) -> np.ndarray:
        return frame / 255.0


# Test the VideoProcessor class
# if __name__ == "__main__":
#     config = VideoClassificationConfig()
#     # TODO: Use secrets to store the video path
#     video_path = "/Users/mzitoh/.cache/kagglehub/datasets/matthewjansen/ucf101-action-recognition/versions/4/train/Basketball/v_Basketball_g23_c01.avi"
#     processor = VideoProcessor(config)
#     frames = processor.load_and_preprocess_video(video_path)
    
#     print(frames)
#     print(frames.shape)