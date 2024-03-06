import cv2
import pytesseract
import pandas as pd
from datetime import datetime

def extract_text_from_video_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    text_data = []

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)
        timestamp_str = str(datetime.utcfromtimestamp(timestamp / 1000.0))

        text = pytesseract.image_to_string(frame)
        text_data.append([timestamp_str, text])

    cap.release()
    cv2.destroyAllWindows()

    return text_data

def save_text_to_csv(text_data, csv_path):
    df = pd.DataFrame(text_data, columns=['Timestamp', 'Text'])
    df.to_csv(csv_path, index=False)
    print("Text extracted from the video frames saved to CSV successfully!")

# Example usage
video_path = "PATH_TO_VIDEO_FILE"
csv_path = "OUTPUT_CSV_FILE_PATH"

text_data = extract_text_from_video_frames(video_path)
save_text_to_csv(text_data, csv_path)