import os
import sys
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

class MediaDownloader:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.audio_file = os.path.join(self.script_dir, "audio.txt")
        self.video_file = os.path.join(self.script_dir, "video.txt")
        self.archive_file = os.path.join(self.script_dir, "downloads_archive.txt")
        self.log_file = os.path.join(self.script_dir, "download_log.txt")
        self.cookies_file = os.path.join(self.script_dir, "cookies.txt")
        
        self.audio_dir = os.path.join(self.script_dir, "Downloads", "audio")
        self.video_dir = os.path.join(self.script_dir, "Downloads", "video")
        
        self.setup_environment()
        self.setup_logging()
    
    def setup_environment(self):
        """Create necessary directories and files if they don't exist"""
        # Create directories
        os.makedirs(self.audio_dir, exist_ok=True)
        os.makedirs(self.video_dir, exist_ok=True)
        
        # Create text files if they don't exist
        for file_path in [self.audio_file, self.video_file, self.archive_file]:
            if not os.path.exists(file_path):
                with open(file_path, "w") as f:
                    pass
    
    def setup_logging(self):
        """Configure logging"""
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    def get_cookies(self):
        """Extract cookies from browser"""
        try:
            # Try Chrome first
            subprocess.run(
                ["yt-dlp", "--cookies-from-browser", "chrome", "--cookies", self.cookies_file],
                check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE
            )
            print("Successfully extracted cookies from Chrome.")
            return self.cookies_file
        except Exception as e:
            print(f"Failed to extract cookies from Chrome: {e}")
            try:
                # Try Firefox as fallback
                subprocess.run(
                    ["yt-dlp", "--cookies-from-browser", "firefox", "--cookies", self.cookies_file],
                    check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE
                )
                print("Successfully extracted cookies from Firefox.")
                return self.cookies_file
            except Exception as e:
                print(f"Failed to extract cookies from Firefox: {e}")
                print("Proceeding without cookies. Some downloads might fail.")
                return None
    
    def get_platform(self, url):
        """Determine platform from URL"""
        if "youtube.com" in url or "youtu.be" in url:
            return "YouTube"
        elif "vimeo.com" in url:
            return "Vimeo"
        else:
            return "Other"
    
    def read_urls(self, file_path):
        """Read URLs from file"""
        try:
            with open(file_path, "r") as f:
                urls = [line.strip() for line in f if line.strip()]
            return urls
        except Exception as e:
            logging.error(f"Error reading {file_path}: {e}")
            print(f"Error reading {file_path}: {e}")
            return []
    
    def download_audio(self, url, cookies_file):
        """Download audio from URL"""
        def log_hook(d):
            if d['status'] == 'downloading':
                try:
                    percent = d['_percent_str']
                    print(f"Downloading: {percent}", end='\r')
                except:
                    pass
            elif d['status'] == 'finished':
                info = d.get('info_dict', {})
                video_id = info.get('id', 'unknown_id')
                platform = self.get_platform(info.get('webpage_url', ''))
                logging.info(f"{platform}: {video_id} --> audio")
                print(f"\nSuccessfully downloaded audio: {info.get('title', 'Unknown Title')}")
        
        output_template = os.path.join(self.audio_dir, "%(title)s-%(id)s.%(ext)s")
        
        # Modified audio options with more flexible format selection
        ydl_opts = {
            'format': 'bestaudio/best',  # More flexible format selection
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': output_template,
            'download_archive': self.archive_file,
            'progress_hooks': [log_hook],
            'cookiefile': cookies_file,
            'ignoreerrors': True,
            'noplaylist': True,
            'quiet': False,
            'no_warnings': False
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return True
        except Exception as e:
            logging.error(f"Error downloading audio from {url}: {e}")
            print(f"Error downloading audio: {e}")
            return False
    
    def download_video(self, url, cookies_file):
        """Download video from URL"""
        def log_hook(d):
            if d['status'] == 'downloading':
                try:
                    percent = d['_percent_str']
                    print(f"Downloading: {percent}", end='\r')
                except:
                    pass
            elif d['status'] == 'finished':
                info = d.get('info_dict', {})
                video_id = info.get('id', 'unknown_id')
                platform = self.get_platform(info.get('webpage_url', ''))
                logging.info(f"{platform}: {video_id} --> video")
                print(f"\nSuccessfully downloaded video: {info.get('title', 'Unknown Title')}")
        
        output_template = os.path.join(self.video_dir, "%(title)s-%(id)s.%(ext)s")
        
        # Modified video options with more flexible format selection
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',  # More flexible format selection
            'merge_output_format': 'mp4',  # Try to merge to mp4 if possible
            'outtmpl': output_template,
            'download_archive': self.archive_file,
            'progress_hooks': [log_hook],
            'cookiefile': cookies_file,
            'ignoreerrors': True,
            'noplaylist': True,
            'quiet': False,
            'no_warnings': False
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return True
        except Exception as e:
            logging.error(f"Error downloading video from {url}: {e}")
            print(f"Error downloading video: {e}")
            return False
    
    def show_available_formats(self, url):
        """Show available formats for a URL"""
        print(f"\nListing available formats for {url}...")
        
        ydl_opts = {
            'listformats': True,
            'quiet': False,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            print(f"Error listing formats: {e}")
    
    def process_downloads(self, content_type):
        """Process downloads based on content type"""
        file_path = self.audio_file if content_type == "audio" else self.video_file
        cookies_file = self.get_cookies()
        
        urls = self.read_urls(file_path)
        if not urls:
            print(f"No URLs found in {file_path}")
            return
        
        print(f"\nProcessing {len(urls)} URLs for {content_type} download...")
        
        successful_downloads = []
        for url in urls:
            print(f"\nProcessing {url}...")
            
            if content_type == "audio":
                success = self.download_audio(url, cookies_file)
            else:
                success = self.download_video(url, cookies_file)
            
            # If download failed, offer to show available formats
            if not success:
                print(f"Download failed for {url}")
                choice = input("Would you like to see available formats? (y/n): ")
                if choice.lower() == 'y':
                    self.show_available_formats(url)
            else:
                successful_downloads.append(url)
        
        # Per your requirement, we don't remove failed URLs from the text files
        print(f"\nCompleted processing {len(urls)} URLs")
        print(f"Successfully downloaded: {len(successful_downloads)}")
        print(f"Failed downloads: {len(urls) - len(successful_downloads)}")
    
    def display_menu(self):
        """Display the main menu"""
        print("\n===== Media Downloader =====")
        print("1. Download Audio")
        print("2. Download Video")
        print("3. Show Available Formats for URL")
        print("4. Exit")
        return input("Enter your choice (1-4): ")
    
    def run(self):
        """Main program loop"""
        while True:
            choice = self.display_menu()
            if choice == "1":
                self.process_downloads("audio")
            elif choice == "2":
                self.process_downloads("video")
            elif choice == "3":
                url = input("Enter URL to check formats: ")
                if url:
                    self.show_available_formats(url)
                else:
                    print("No URL entered.")
            elif choice == "4":
                print("Exiting program. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")

def main():
    downloader = MediaDownloader()
    downloader.run()

if __name__ == "__main__":
    main()
