from ocr_handler import *
import tkinter as tk
import tkinter.font as tkFont
import requests
import os
from pytube import YouTube
from requests_html import HTMLSession
from datetime import datetime

class App:
    def __init__(self, root):
        #setting title
        root.title("Video Text Extract")
        #setting window size
        width=365
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
        GLabel_179.place(x=60,y=50,width=90,height=25)

        self.GLineEdit_797=tk.Entry(root)
        self.GLineEdit_797["borderwidth"] = "1px"
        self.ft = tkFont.Font(family='Times',size=10)
        self.GLineEdit_797["font"] = ft
        self.GLineEdit_797["fg"] = "#333333"
        self.GLineEdit_797["justify"] = "center"
        self.GLineEdit_797["text"] = "Entry"
        self.GLineEdit_797.place(x=60,y=90,width=219,height=30)

        GButton_578=tk.Button(root)    
        GButton_578["activebackground"] = "#ff5722"
        GButton_578["activeforeground"] = "#ff5722"
        GButton_578["bg"] = "#ff5722"
        ft = tkFont.Font(family='Times',size=10)
        GButton_578["font"] = ft
        GButton_578["fg"] = "#ffffff"
        GButton_578["justify"] = "center"
        GButton_578["text"] = "Start Extracting"
        GButton_578.place(x=60,y=140,width=220,height=37)
        GButton_578["command"] = self.GButton_578_command


    def GButton_578_command(self):
        #filename = input("ENTER FILENAME: ")
        # ocr_type = input("ENTER OCR_MODE (WORDS/LINES): ")
        filename = self.GLineEdit_797.get()
        ocr_type = "WORDS"
        
        save_path = ".\input"
        self.download_video(filename, save_path)
    
    def download_video(self, url, save_path):
        if "youtube.com" in url:
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            video_filename = f"{timestamp}.mp4"
            stream.download(output_path=save_path, filename=video_filename)
            print(f"YouTube video downloaded successfully! {video_filename}")
            scrapeText(video_filename)
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
        def scrapeText(self, filename):
            if os.path.isfile(filename):
                ocr_handler = OCR_HANDLER(filename, CV2_HELPER(),ocr_type)
                ocr_handler.process_frames()
                ocr_handler.assemble_video()
                print("OCR PROCESS FINISHED: OUTPUT FILE => " + ocr_handler.out_name)
            else:
                 print("FILE NOT FOUND: BYE")
    

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
