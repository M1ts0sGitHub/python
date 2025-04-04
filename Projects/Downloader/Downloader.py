import os
import sys
import re
import subprocess
import logging
from datetime import datetime

# Try to import yt-dlp
try:
    import yt_dlp
except ImportError:
    print("yt-dlp is not installed. Installing now...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
    import yt_dlp

# Setup directories and files
def setup_environment():
    # Create directories if they don't exist
    os.makedirs("Downloads/audio", exist_ok=True)
    os.makedirs("Downloads/video", exist_ok=True)
    
    # Create text files if they don't exist
    if not os.path.exists("audio.txt"):
        with open("audio.txt", "w") as f:
            pass
    
    if not os.path.exists("video.txt"):
        with open("video.txt", "w") as f:
            pass
    
    # Setup logging
    logging.basicConfig(
        filename='download_log.txt',
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

# Function to extract cookies from browser
def get_cookies():
    cookies_file = "cookies.txt"
    try:
        # Try to extract cookies from Chrome browser
        subprocess.run(["yt-dlp", "--cookies-from-browser", "chrome", "--cookies", cookies_file], 
                       check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        print("Successfully extracted cookies from Chrome.")
        return cookies_file
    except Exception as e:
        print(f"Failed to extract cookies from Chrome: {e}")
        try:
            # Try Firefox as fallback
            subprocess.run(["yt-dlp", "--cookies-from-browser", "firefox", "--cookies", cookies_file], 
                           check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            print("Successfully extracted cookies from Firefox.")
            return cookies_file
        except Exception as e:
            print(f"Failed to extract cookies from Firefox: {e}")
            print("Proceeding without cookies. Some downloads might fail.")
            return None

# Function to extract video ID from URL
def extract_id(url):
    if "youtube.com" in url or "youtu.be" in url:
        # YouTube URL pattern
        if "youtube.com/watch?v=" in url:
            video_id = url.split("watch?v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            video_id = url.split("youtu.be/")[1].split("?")[0]
        else:
            return None
        return video_id
    elif "vimeo.com" in url:
        # Vimeo URL pattern
        match = re.search(r'vimeo\.com/(\d+)', url)
        if match:
            return match.group(1)
        else:
            return None
    else:
        # Try to use yt-dlp to extract the ID for other platforms
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                return info.get('id', None)
        except:
            return None

# Function to check if content has already been downloaded
def is_already_downloaded(video_id, content_type):
    try:
        with open("download_log.txt", "r") as log_file:
            log_content = log_file.read()
            search_pattern = f"{video_id} --> {content_type}"
            return search_pattern in log_content
    except FileNotFoundError:
        # If log file doesn't exist, create it
        with open("download_log.txt", "w") as f:
            pass
        return False

# Function to read URLs from file
def read_urls(file_path):
    try:
        with open(file_path, "r") as f:
            urls = [line.strip() for line in f if line.strip()]
        return urls
    except Exception as e:
        logging.error(f"Error reading {file_path}: {e}")
        return []

# Function to update URL file after download
def update_url_file(file_path, urls):
    try:
        with open(file_path, "w") as f:
            for url in urls:
                f.write(f"{url}\n")
    except Exception as e:
        logging.error(f"Error updating {file_path}: {e}")

# Function to determine platform from URL
def get_platform(url):
    if "youtube.com" in url or "youtu.be" in url:
        return "Youtube"
    elif "vimeo.com" in url:
        return "Vimeo"
    else:
        return "Other"

# Function to download audio
def download_audio(url, cookies_file):
    video_id = extract_id(url)
    if not video_id:
        logging.error(f"Could not extract ID from {url}")
        return False
    
    platform = get_platform(url)
    
    if is_already_downloaded(video_id, "audio"):
        print(f"This {video_id} is already downloaded as audio.")
        return True
    
    output_template = f"Downloads/audio/%(title)s-%(id)s.%(ext)s"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_template,
        'noplaylist': True,  # Only download single video, not playlist
    }
    
    if cookies_file:
        ydl_opts['cookiefile'] = cookies_file
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'Unknown Title')
            # Log the download
            logging.info(f"{platform}: {video_id} --> audio")
            print(f"Downloaded audio: {title}")
            return True
    except Exception as e:
        logging.error(f"Error downloading audio from {url}: {e}")
        print(f"Error downloading audio: {e}")
        return False

# Function to download video
def download_video(url, cookies_file):
    video_id = extract_id(url)
    if not video_id:
        logging.error(f"Could not extract ID from {url}")
        return False
    
    platform = get_platform(url)
    
    if is_already_downloaded(video_id, "video"):
        print(f"This {video_id} is already downloaded as video.")
        return True
    
    output_template = f"Downloads/video/%(title)s-%(id)s.%(ext)s"
    
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': output_template,
        'noplaylist': True,  # Only download single video, not playlist
    }
    
    if cookies_file:
        ydl_opts['cookiefile'] = cookies_file
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'Unknown Title')
            # Log the download
            logging.info(f"{platform}: {video_id} --> video")
            print(f"Downloaded video: {title}")
            return True
    except Exception as e:
        logging.error(f"Error downloading video from {url}: {e}")
        print(f"Error downloading video: {e}")
        return False

# Main function to process downloads
def process_downloads(content_type):
    # Setup required environment
    setup_environment()
    
    # Get cookies
    cookies_file = get_cookies()
    
    # Determine which file to read
    file_path = f"{content_type}.txt"
    
    # Read URLs
    urls = read_urls(file_path)
    if not urls:
        print(f"No URLs found in {file_path}. Please add URLs to the file.")
        return
    
    # Process each URL
    remaining_urls = []
    for i, url in enumerate(urls, 1):
        print(f"\nProcessing {i}/{len(urls)}: {url}...")
        if content_type == "audio":
            success = download_audio(url, cookies_file)
        else:
            success = download_video(url, cookies_file)
        
        if not success:
            remaining_urls.append(url)
    
    # Update the URL file with remaining URLs
    update_url_file(file_path, remaining_urls)
    
    print(f"\nDownload process completed.")
    print(f"Successfully downloaded: {len(urls) - len(remaining_urls)} items")
    print(f"Failed or skipped: {len(remaining_urls)} items")

# Main menu
def display_menu():
    print("\n===== YouTube & Vimeo Downloader =====")
    print("1. Download Audio")
    print("2. Download Video")
    print("3. Exit")
    choice = input("Enter your choice (1-3): ")
    return choice

# Main program
def main():
    # Initial setup
    setup_environment()
    
    while True:
        choice = display_menu()
        
        if choice == "1":
            process_downloads("audio")
        elif choice == "2":
            process_downloads("video")
        elif choice == "3":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
