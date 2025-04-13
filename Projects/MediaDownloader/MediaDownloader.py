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

        self.audio_dir = os.path.join(self.script_dir, "Downloads", "audio")
        self.video_dir = os.path.join(self.script_dir, "Downloads", "video")
        self.bin_dir = os.path.join(self.script_dir, "bin")
        
        # Separate archive files for audio and video
        self.audio_archive_file = os.path.join(self.bin_dir, "audio_archive.txt")
        self.video_archive_file = os.path.join(self.bin_dir, "video_archive.txt")
        
        self.log_file = os.path.join(self.bin_dir, "_log.txt")
        self.cookies_file = os.path.join(self.bin_dir, "_cookies.txt")
        
        
        # Setup environment before anything else
        self.setup_environment()
        self.setup_logging()
        
        print(f"Script directory: {self.script_dir}")
        print(f"Audio file path: {self.audio_file}")
        print(f"Video file path: {self.video_file}")
    
    def setup_environment(self):
        """Create necessary directories and files if they don't exist"""
        print("Setting up environment...")
        
        # Create directories
        os.makedirs(self.bin_dir, exist_ok=True)
        os.makedirs(self.audio_dir, exist_ok=True)
        os.makedirs(self.video_dir, exist_ok=True)
        
        # Create text files if they don't exist
        for file_path in [self.audio_file, self.video_file, self.audio_archive_file, self.video_archive_file]:
            if not os.path.exists(file_path):
                print(f"Creating file: {file_path}")
                with open(file_path, "w") as f:
                    if file_path.endswith(".txt") and not file_path.endswith("_archive.txt"):
                        f.write("# Add URLs here, one per line\n")
                    
        print("Environment setup complete.")
    
    def setup_logging(self):
        """Configure logging"""
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        logging.info("Media Downloader started")
    
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
            if not os.path.exists(file_path):
                print(f"File does not exist: {file_path}")
                # Create the file if it doesn't exist
                with open(file_path, "w") as f:
                    f.write("# Add URLs here, one per line\n")
                return []
                
            with open(file_path, "r") as f:
                urls = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]
            
            if not urls:
                print(f"No URLs found in {file_path}. Please add URLs to this file.")
                # Add an option to add URLs directly
                choice = input("Would you like to add a URL now? (y/n): ")
                if choice.lower() == 'y':
                    return self.add_url(file_path)
            return urls
        except Exception as e:
            logging.error(f"Error reading {file_path}: {e}")
            print(f"Error reading {file_path}: {e}")
            return []
    
    def add_url(self, file_path):
        """Add a URL to the specified file"""
        url = input("Enter URL to add: ")
        if url:
            try:
                with open(file_path, "a") as f:
                    f.write(f"{url}\n")
                print(f"URL added to {os.path.basename(file_path)}")
                return [url]
            except Exception as e:
                logging.error(f"Error adding URL to {file_path}: {e}")
                print(f"Error adding URL: {e}")
        return []
    
    def remove_url_from_file(self, file_path, url_to_remove):
        """Remove a URL from the file after successful download"""
        try:
            urls = self.read_urls(file_path)
            # Filter out the URL to remove
            updated_urls = [url for url in urls if url != url_to_remove]
            
            # Write the updated list back to the file
            with open(file_path, "w") as f:
                f.write("# Add URLs here, one per line\n")
                for url in updated_urls:
                    f.write(f"{url}\n")
            
            logging.info(f"Removed {url_to_remove} from {os.path.basename(file_path)}")
        except Exception as e:
            logging.error(f"Error removing URL from {file_path}: {e}")
            print(f"Error removing URL: {e}")
    
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
            'download_archive': self.audio_archive_file,  # Use audio-specific archive
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
            'download_archive': self.video_archive_file,  # Use video-specific archive
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
        
        # Ensure the file exists
        if not os.path.exists(file_path):
            print(f"Creating {content_type} file at: {file_path}")
            with open(file_path, "w") as f:
                f.write("# Add URLs here, one per line\n")
        
        # Get cookies
        cookies_file = self.get_cookies()
        
        # Read URLs
        urls = self.read_urls(file_path)
        if not urls:
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
                # Remove the URL from the file after successful download
                self.remove_url_from_file(file_path, url)
        
        print(f"\nCompleted processing {len(urls)} URLs")
        print(f"Successfully downloaded: {len(successful_downloads)}")
        print(f"Failed downloads: {len(urls) - len(successful_downloads)}")
    
    def manage_urls(self, content_type):
        """Manage URLs in the specified file"""
        file_path = self.audio_file if content_type == "audio" else self.video_file
        
        # Ensure the file exists
        if not os.path.exists(file_path):
            print(f"Creating {content_type} file at: {file_path}")
            with open(file_path, "w") as f:
                f.write("# Add URLs here, one per line\n")
        
        while True:
            print(f"\n===== Manage {content_type.capitalize()} URLs =====")
            print("1. View current URLs")
            print("2. Add new URL")
            print("3. Remove URL")
            print("4. Back to main menu")
            
            choice = input("Enter your choice (1-4): ")
            
            if choice == "1":
                # View current URLs
                urls = self.read_urls(file_path)
                if urls:
                    print("\nCurrent URLs:")
                    for i, url in enumerate(urls, 1):
                        print(f"{i}. {url}")
                else:
                    print(f"No URLs found in {os.path.basename(file_path)}")
            
            elif choice == "2":
                # Add new URL
                self.add_url(file_path)
            
            elif choice == "3":
                # Remove URL
                urls = self.read_urls(file_path)
                if urls:
                    print("\nSelect URL to remove:")
                    for i, url in enumerate(urls, 1):
                        print(f"{i}. {url}")
                    
                    try:
                        idx = int(input("Enter number to remove (0 to cancel): "))
                        if 1 <= idx <= len(urls):
                            removed = urls.pop(idx - 1)
                            with open(file_path, "w") as f:
                                f.write("# Add URLs here, one per line\n")
                                for url in urls:
                                    f.write(f"{url}\n")
                            print(f"Removed: {removed}")
                        elif idx != 0:
                            print("Invalid number.")
                    except ValueError:
                        print("Please enter a valid number.")
                else:
                    print(f"No URLs found in {os.path.basename(file_path)}")
            
            elif choice == "4":
                # Back to main menu
                break
            
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")
    
    def clear_archive(self):
        """Clear archive files to allow re-downloading content"""
        print("\n===== Clear Download Archives =====")
        print("1. Clear audio archive only")
        print("2. Clear video archive only")
        print("3. Clear both archives")
        print("4. Back to main menu")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == "1":
            confirmation = input("Are you sure you want to clear the audio archive? This will allow re-downloading previously downloaded audio (y/n): ")
            if confirmation.lower() == 'y':
                with open(self.audio_archive_file, "w") as f:
                    pass  # Clear the file
                print("Audio archive cleared.")
        
        elif choice == "2":
            confirmation = input("Are you sure you want to clear the video archive? This will allow re-downloading previously downloaded videos (y/n): ")
            if confirmation.lower() == 'y':
                with open(self.video_archive_file, "w") as f:
                    pass  # Clear the file
                print("Video archive cleared.")
        
        elif choice == "3":
            confirmation = input("Are you sure you want to clear both archives? This will allow re-downloading all previously downloaded content (y/n): ")
            if confirmation.lower() == 'y':
                with open(self.audio_archive_file, "w") as f:
                    pass  # Clear the file
                with open(self.video_archive_file, "w") as f:
                    pass  # Clear the file
                print("Both archives cleared.")
        
        elif choice != "4":
            print("Invalid choice.")
    
    def display_menu(self):
        """Display the main menu"""
        print("\n===== Media Downloader =====")
        print("1. Download Audio")
        print("2. Download Video")
        print("3. Manage Audio URLs")
        print("4. Manage Video URLs")
        print("5. Show Available Formats for URL")
        print("6. Clear Download Archives")
        print("7. Exit")
        return input("Enter your choice (1-7): ")
    
    def run(self):
        """Main program loop"""
        print("=== Media Downloader Started ===")
        print(f"Script running from: {self.script_dir}")
        
        while True:
            choice = self.display_menu()
            if choice == "1":
                self.process_downloads("audio")
            elif choice == "2":
                self.process_downloads("video")
            elif choice == "3":
                self.manage_urls("audio")
            elif choice == "4":
                self.manage_urls("video")
            elif choice == "5":
                url = input("Enter URL to check formats: ")
                if url:
                    self.show_available_formats(url)
                else:
                    print("No URL entered.")
            elif choice == "6":
                self.clear_archive()
            elif choice == "7":
                print("Exiting program. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1-7.")

def main():
    downloader = MediaDownloader()
    downloader.run()

if __name__ == "__main__":
    main()