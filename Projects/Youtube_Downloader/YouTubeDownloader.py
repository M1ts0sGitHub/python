# Install PyTube | pip install pytube==15.0.0


import os
from pytube import YouTube
import pytube.request

def cc_folder(download_folder): #Check or Create Folder
    if os.path.exists(download_folder) == False:
        os.makedirs(download_folder)
        print("Folder created")
    else:
        print("Folder already exists")
def download_youtube_videos(youtube_links, download_folder):
    for link in youtube_links:
        try:
            yt = YouTube(link)
            stream = yt.streams.filter(progressive=True).order_by('resolution').desc().first()
            stream.download(download_folder)
            print(f"Downloaded: {yt.title}")
        except Exception as e:
            print(f"Error downloading {link}: {e}")

download_folder = "./Projects/Youtube_Downloader/Downloads"
youtube_links = ["https://www.youtube.com/watch?v=7czhMCG-mtE",
                 "https://www.youtube.com/watch?v=TE6glBxnYuo"]
pytube.request.proxy = {"http": "http://your_proxy:port",
                        "https": "https://your_proxy:port"}
pytube.request.default_range_size = 1048576  # 1MB

cc_folder(download_folder)
download_youtube_videos(youtube_links, download_folder)