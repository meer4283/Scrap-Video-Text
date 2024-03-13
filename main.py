from ocr_handler import *
import tkinter as tk
import tkinter.font as tkFont
import requests
import os
from pytube import YouTube
from requests_html import HTMLSession
from datetime import datetime
import cv2
import pytesseract
import pandas as pd
import threading
from tkinter import messagebox
from tkinter import filedialog

class App:
    def __init__(self, root):
        #setting title
        root.title("Video Text Extract")
        #setting window size
        width=400
        height=240
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GLabel_179=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_179["font"] = ft
        GLabel_179["fg"] = "#333333"
        GLabel_179["justify"] = "center"
        GLabel_179["text"] = "Enter Video Url"
        GLabel_179.place(x=80,y=50,width=90,height=25)

        self.GLineEdit_797=tk.Entry(root)
        self.GLineEdit_797["borderwidth"] = "1px"
        self.ft = tkFont.Font(family='Times',size=10)
        self.GLineEdit_797["font"] = ft
        self.GLineEdit_797["fg"] = "#333333"
        self.GLineEdit_797["justify"] = "center"
        self.GLineEdit_797["text"] = "Entry"
        self.GLineEdit_797.place(x=80,y=90,width=219,height=30)

        self.GButton_578=tk.Button(root)    
        self.GButton_578["activebackground"] = "#ff5722"
        self.GButton_578["activeforeground"] = "#ff5722"
        self.GButton_578["bg"] = "#ff5722"
        ft = tkFont.Font(family='Times',size=10)
        self.GButton_578["font"] = ft
        self.GButton_578["fg"] = "#ffffff"
        self.GButton_578["justify"] = "center"
        self.GButton_578["text"] = "Start Extracting"
        self.GButton_578.place(x=80,y=140,width=220,height=37)
        self.GButton_578["command"] = self.GButton_578_command

        self.isLocalPath = False
        self.GCheckBox_568=tk.Checkbutton(root)
        ft = tkFont.Font(family='Times',size=10)
        self.GCheckBox_568["font"] = ft
        self.GCheckBox_568["fg"] = "#333333"
        self.GCheckBox_568["justify"] = "center"
        self.GCheckBox_568["text"] = "Local Path"
        self.GCheckBox_568["relief"] = "flat"
        self.GCheckBox_568.place(x=200,y=50,width=126,height=30)
        self.GCheckBox_568["offvalue"] = "0"
        self.GCheckBox_568["onvalue"] = "1"
        self.GCheckBox_568["command"] = self.GCheckBox_568_command

    def GCheckBox_568_command(self):
        self.isLocalPath = not self.isLocalPath
        if self.isLocalPath == True:
            self.videoFilePath = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video files", "*.mp4;")])
            self.GLineEdit_797.insert(0, self.videoFilePath)




    def GButton_578_command(self):
        #filename = input("ENTER FILENAME: ")
        # ocr_type = input("ENTER OCR_MODE (WORDS/LINES): ")
        self.filename = self.GLineEdit_797.get()
        
        self.save_path = ".\input"
        # self.download_video(filename, save_path)

        if self.isLocalPath == True:
           if os.path.exists(self.filename):
                print("Video file exists.")
                loading_thread = threading.Thread(target=self.processVideo, args=(self.filename,))
                loading_thread.start()
                # self.processVideo(self.filename)
           else:
                print("Video file does not exist.")
                messagebox.showinfo("Error","Video file does not exist.")

        else:
            self.GButton_578["text"] = "Video Downloading"
            self.GButton_578["fg"] = "#ffffff"

            self.GButton_578["state"] = "disabled"
            self.GButton_578["activebackground"] = "#e8e8e8"
            self.GButton_578["activeforeground"] = "#e8e8e8"
            self.GButton_578["bg"] = "#e8e8e8"
            loading_thread = threading.Thread(target=self.download_video, args=(self.filename, self.save_path,))
            loading_thread.start()
        
        
    def processVideo(self, videoFilePath):
        self.GButton_578["text"] = "Processing. this may take a while ....."
        self.GButton_578["state"] = "disabled"
        self.GButton_578["activebackground"] = "#e8e8e8"
        self.GButton_578["activeforeground"] = "#e8e8e8"
        self.GButton_578["bg"] = "#e8e8e8"
        self.scrapeText(videoFilePath)

        messagebox.showinfo("Process Completed", "OCR process has been completed successfully.")
        self.GButton_578["state"] = "normal"
        self.GButton_578["activebackground"] = "#ff5722"
        self.GButton_578["activeforeground"] = "#ff5722"
        self.GButton_578["bg"] = "#ff5722"
        self.GButton_578["text"] = "Start Extracting"

    
    def download_video(self, url, save_path):
        if "youtube.com" in url:
            try:
                yt = YouTube(url)
                stream = yt.streams.get_highest_resolution()
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                video_filename = f"{timestamp}.mp4"
                stream.download(output_path=save_path, filename=video_filename)
                
                
                self.GButton_578["text"] = "Processing. this may take a while ....."

                videoFilePath = os.path.join(save_path, video_filename)
                self.scrapeText(videoFilePath)

                messagebox.showinfo("Process Completed", "OCR process has been completed successfully.")
                self.GButton_578["state"] = "normal"
                self.GButton_578["activebackground"] = "#ff5722"
                self.GButton_578["activeforeground"] = "#ff5722"
                self.GButton_578["bg"] = "#ff5722"
                self.GButton_578["text"] = "Start Extracting"
            except Exception as e:
                messagebox.showinfo("Error", f"An error occurred: {e}")
                self.GButton_578["state"] = "normal"
                self.GButton_578["activebackground"] = "#ff5722"
                self.GButton_578["activeforeground"] = "#ff5722"
                self.GButton_578["bg"] = "#ff5722"
                self.GButton_578["text"] = "Start Extracting"



            # loading_thread = threading.Thread(target=self.scrapeText(videoFilePath))
            # loading_thread.start()
            
        elif "tiktok.com" in url:
            session = HTMLSession()
            r = session.get(url)
            video_url = r.html.find('video', first=True).attrs['src']
            video_data = requests.get(video_url).content
            with open(os.path.join(save_path, "tiktok_video.mp4"), 'wb') as f:
                f.write(video_data)
            print("TikTok video downloaded successfully!")
        else:
            r = requests.head(url)
            if "video" in r.headers.get('content-type', ''):
                video_data = requests.get(url).content
                with open(os.path.join(save_path, "video_file.mp4"), 'wb') as f:
                    f.write(video_data)
                print("Video file downloaded successfully!")
            else:
                print("Unsupported video URL.")
                messagebox.showinfo("Error", "Unsupported video URL.")
    def scrapeText(self, filename):
        # Example usage
        # video_path = filename
        # csv_path = "./text.csv"

        # text_data = self.extract_text_from_video_frames(video_path)
        # print(text_data)
        # self.save_text_to_csv(text_data, csv_path)

        #Medthod 2
        ocr_type = "LINES"
        if os.path.isfile(filename):
            ocr_handler = OCR_HANDLER(filename, CV2_HELPER(),ocr_type)
            ocr_handler.process_frames()
            ocr_handler.assemble_video()
            # ocr_handler.assemble_video()
            # print("OCR PROCESS FINISHED: OUTPUT FILE => " + ocr_handler.out_name)
        else:
            print("FILE NOT FOUND: BYE")
    def extract_text_from_video_frames(self,video_path):
        frames_per_second=60
        cap = cv2.VideoCapture(video_path)
        text_data = []
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        #cap = cv2.VideoCapture(str(video_path))
        frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        target_frames = min(frames_per_second * 60, total_frames)
    
        df = pd.DataFrame(columns=['Timestamp', 'Text'])
        frame_count = 0

        while cap.isOpened() and frame_count < target_frames:
            ret, frame = cap.read()

            if not ret:
                break

            timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)
            timestamp_str = str(datetime.utcfromtimestamp(timestamp / 1000.0))

            text = pytesseract.image_to_string(frame)
            print(f"this  {text}")
            text_data.append([timestamp_str, text])
            frame_count += 1
        cap.release()
        cv2.destroyAllWindows()

        return text_data

    def save_text_to_csv(self, text_data, csv_path):
        df = pd.DataFrame(text_data, columns=['Timestamp', 'Text'])
        df.to_csv(csv_path, index=False)
        print("Text extracted from the video frames saved to CSV successfully!")
    
    

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()





