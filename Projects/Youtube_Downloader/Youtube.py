import yt_dlp, os

def download_video(url, download_folder, cookies_file):
    if url.startswith('https://www.pornhub'):
        ydl_opts = {'format': '720p'}
        ydl_opts['outtmpl'] = os.path.join(download_folder, 'video', 'pornhub', '%(channel)s', '%(title)s.%(ext)s')
    else:
        ydl_opts = {'format': 'bestvideo',
                    'outtmpl': '%(title)s.%(ext)s',  # Save file as title.extension
                    'cookiefile': cookies_file  # Add this line
                    }
        ydl_opts['outtmpl'] = os.path.join(download_folder, 'video', '%(channel)s', '%(title)s.%(ext)s')
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_audio(url, download_folder, cookies_file):
    ydl_opts = {'format': 'bestaudio/best',
                'cookiefile': cookies_file,  # Add this line
                'extractor-args': 'youtube:skip=authcheck',
                'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]}
    ydl_opts['outtmpl'] = os.path.join(download_folder,'audio',  '%(channel)s', '%(title)s.%(ext)s')
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def cc_folder(download_folder):  # Check or Create Folder
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
if __name__ == "__main__":
       
    root_folder = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_folder)
    download_folder = os.path.join(root_folder, 'Downloads')
    cookies_file = os.path.join(root_folder, 'cookies.txt')
    cc_folder(download_folder)
    
    choice = ''
    while choice not in ['v', 'a']:
        choice = input("Do you want to download video or audio? (v/a): ").strip().lower()
        if choice in ['v', 'a']:
            break
        print("Invalid input. Please enter 'v' for video or 'a' for audio.")
    
    os.system("notepad.exe 2Download.txt")
    
    with open("2Download.txt", "r") as f:
        urls = f.read().splitlines()    

    
    for url in urls:
        if choice == 'v':
            try:
                download_video(url, download_folder, cookies_file)
            except yt_dlp.utils.DownloadError as e:
                print(f"Error downloading video: {e}")
        elif choice == 'a':
            try:
                download_audio(url, download_folder, cookies_file)
            except yt_dlp.utils.DownloadError as e:
                print(f"Error downloading audio: {e}")
        else:
            print("Invalid choice. Please select 'v' for video or 'a' for audio.")
        
