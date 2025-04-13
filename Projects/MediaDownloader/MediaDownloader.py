import os
import sys
import subprocess
import logging
from datetime import datetime
import re # Import regex for better URL matching

# Try to import yt-dlp
try:
    import yt_dlp
    from yt_dlp.utils import DownloadError # Import specific error for better handling
except ImportError:
    print("yt-dlp is not installed. Installing now...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "yt-dlp"])
        import yt_dlp
        from yt_dlp.utils import DownloadError
    except Exception as e:
        print(f"Failed to install yt-dlp: {e}")
        print("Please install it manually: pip install -U yt-dlp")
        sys.exit(1)

class MediaDownloader:
    def __init__(self):
        # Try to determine script directory robustly
        try:
             # If running as a script
            self.script_dir = os.path.dirname(os.path.abspath(__file__))
        except NameError:
             # If running interactively or packaged (e.g., pyinstaller)
            self.script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

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
        print("-" * 30) # Separator

    def setup_environment(self):
        """Create necessary directories and files if they don't exist"""
        print("Setting up environment...")

        # Create directories
        os.makedirs(self.bin_dir, exist_ok=True)
        os.makedirs(self.audio_dir, exist_ok=True)
        os.makedirs(self.video_dir, exist_ok=True)

        # Create text files if they don't exist
        for file_path in [self.audio_file, self.video_file, self.audio_archive_file, self.video_archive_file, self.cookies_file]:
             # Also ensure cookies file exists, even if empty initially
            if not os.path.exists(file_path):
                print(f"Creating file: {file_path}")
                with open(file_path, "w") as f:
                    if file_path.endswith(".txt") and not file_path.endswith("_archive.txt") and not file_path.endswith("_cookies.txt"):
                        f.write("# Add URLs here, one per line (lines starting with # are ignored)\n")
                    else:
                        pass # Create empty archive/cookie file

        print("Environment setup complete.")

    def setup_logging(self):
        """Configure logging"""
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s', # Added levelname
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler = logging.StreamHandler() # Log INFO to console as well
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        # Optional: Add console handler to root logger if desired
        # logging.getLogger('').addHandler(console_handler)

        logging.info("Media Downloader started")

    def get_cookies(self):
        """Extract cookies from browser, return path or None"""
        print("Attempting to extract browser cookies...")
        browsers_to_try = ["chrome", "firefox", "edge", "brave", "opera", "safari"] # Add more as needed
        for browser in browsers_to_try:
            try:
                # Use yt-dlp command to extract cookies
                # Run silently unless there's an error
                process = subprocess.run(
                    ["yt-dlp", "--cookies-from-browser", browser, "--cookies", self.cookies_file],
                    check=True, capture_output=True, text=True # Capture output
                )
                print(f"Successfully extracted cookies using {browser}.")
                logging.info(f"Successfully extracted cookies using {browser}.")
                # Check if the cookies file actually got content
                if os.path.exists(self.cookies_file) and os.path.getsize(self.cookies_file) > 0:
                   return self.cookies_file
                else:
                   print(f"Extracted cookie file from {browser} appears empty. Trying next browser.")
                   logging.warning(f"Extracted cookie file from {browser} appears empty.")
            except FileNotFoundError:
                print(f"yt-dlp command not found. Make sure it's in your PATH.")
                logging.error("yt-dlp command not found.")
                return None # Cannot proceed without yt-dlp
            except subprocess.CalledProcessError as e:
                # This is expected if the browser isn't installed or has no cookies
                # Log detailed error if needed: logging.debug(f"Cookie extraction from {browser} failed: {e.stderr}")
                print(f"Could not extract cookies from {browser}. Trying next...")
            except Exception as e:
                print(f"An unexpected error occurred extracting cookies from {browser}: {e}")
                logging.error(f"Unexpected cookie extraction error ({browser}): {e}")

        # If loop finishes without returning
        print("Failed to extract cookies from all supported browsers.")
        if os.path.exists(self.cookies_file) and os.path.getsize(self.cookies_file) > 0:
             print("Using previously existing cookies file (if any).")
             logging.warning("Failed cookie extraction, using existing file.")
             return self.cookies_file
        else:
             print("Proceeding without cookies. Downloads requiring login may fail.")
             logging.warning("Proceeding without cookies.")
             return None

    def get_platform(self, url):
        """Determine platform from URL (basic check)"""
        if not isinstance(url, str): return "Invalid URL"
        url_lower = url.lower()
        if "youtube.com" in url_lower or "youtu.be" in url_lower:
            return "YouTube"
        elif "vimeo.com" in url_lower:
            return "Vimeo"
        # Add more platform checks if needed
        else:
            # Try a generic check
            match = re.match(r'https?://(?:www\.)?([^/]+)', url_lower)
            return match.group(1) if match else "Other"

    def is_playlist_or_channel(self, url):
        """Check if URL is likely a playlist or channel using regex for better matching"""
        if not isinstance(url, str): return "single" # Handle non-string input

        # YouTube patterns
        # Playlist: /playlist?list=... or /watch?v=...&list=...
        # Channel: /channel/UC..., /user/..., /c/..., @handle
        if re.search(r'youtube\.com/(?:playlist|watch.*[&?]list=)', url, re.IGNORECASE):
            return "playlist"
        if re.search(r'youtube\.com/(?:channel/UC|user/|c/|@[\w-]+)', url, re.IGNORECASE):
            return "channel"

        # Vimeo patterns
        # Album (playlist): /album/...
        # Channel: /channels/...
        if re.search(r'vimeo\.com/album/\d+', url, re.IGNORECASE):
            return "playlist"
        if re.search(r'vimeo\.com/channels/[\w-]+', url, re.IGNORECASE):
            return "channel"

        # Add patterns for other sites if needed

        return "single"

    def read_urls(self, file_path):
        """Read URLs from file, skipping comments and empty lines"""
        urls = []
        try:
            if not os.path.exists(file_path):
                print(f"File does not exist: {file_path}. Creating it.")
                # Create the file if it doesn't exist
                with open(file_path, "w") as f:
                    f.write("# Add URLs here, one per line (lines starting with # are ignored)\n")
                return [] # Return empty list as the file was just created

            with open(file_path, "r", encoding='utf-8') as f: # Specify encoding
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line and not line.startswith("#"):
                        urls.append(line)

            if not urls:
                print(f"No URLs found in {os.path.basename(file_path)}. You can add some via the 'Manage URLs' menu.")
                # Removed automatic prompt to add URL here, handled by menu

            return urls
        except Exception as e:
            logging.error(f"Error reading {file_path}: {e}")
            print(f"Error reading {file_path}: {e}")
            return []

    def add_url(self, file_path):
        """Add a URL to the specified file"""
        url = input("Enter URL to add: ").strip()
        if url:
            # Basic validation: check if it looks like a URL
            if not (url.startswith("http://") or url.startswith("https://")):
                 print("Invalid URL format. Please include http:// or https://")
                 return []
            try:
                # Check if URL already exists
                current_urls = self.read_urls(file_path)
                if url in current_urls:
                    print(f"URL already exists in {os.path.basename(file_path)}.")
                    return [] # Don't add duplicate

                with open(file_path, "a", encoding='utf-8') as f: # Specify encoding
                    f.write(f"{url}\n")
                print(f"URL added to {os.path.basename(file_path)}")
                logging.info(f"Added URL {url} to {os.path.basename(file_path)}")
                return [url] # Return the added url in a list for consistency if needed elsewhere
            except Exception as e:
                logging.error(f"Error adding URL to {file_path}: {e}")
                print(f"Error adding URL: {e}")
        else:
             print("No URL entered.")
        return []

    def remove_url_from_file(self, file_path, url_to_remove):
        """Remove a specific URL from the file"""
        try:
            with open(file_path, "r", encoding='utf-8') as f:
                lines = f.readlines()

            updated_lines = []
            removed = False
            for line in lines:
                stripped_line = line.strip()
                # Keep comments and lines that don't match the URL to remove
                if stripped_line.startswith("#") or stripped_line != url_to_remove:
                    updated_lines.append(line)
                else:
                    removed = True # Mark that we found and skipped the URL

            if removed:
                with open(file_path, "w", encoding='utf-8') as f:
                    f.writelines(updated_lines)
                print(f"Removed {url_to_remove} from {os.path.basename(file_path)}")
                logging.info(f"Removed {url_to_remove} from {os.path.basename(file_path)}")
                return True
            else:
                 print(f"URL {url_to_remove} not found in the file.")
                 return False

        except Exception as e:
            logging.error(f"Error removing URL from {file_path}: {e}")
            print(f"Error removing URL: {e}")
            return False

    # --- Download Methods ---

    def _create_ydl_options(self, download_dir, archive_file, cookies_file, format_prefs, postprocessors=None):
        """Helper to create common yt-dlp options"""
        output_template = os.path.join(download_dir, "%(title)s [%(id)s].%(ext)s")
        # Use a more robust template: consider %(uploader)s or %(playlist_title)s if needed
        # output_template = os.path.join(download_dir, '%(playlist_title)s/%(playlist_index)s - %(title)s [%(id)s].%(ext)s' if is_playlist else ...)

        return {
            'format': format_prefs,
            'postprocessors': postprocessors if postprocessors else [],
            'outtmpl': output_template,
            'download_archive': archive_file,
            'cookiefile': cookies_file,
            'ignoreerrors': True, # Keep True to skip broken items in playlists
            'quiet': False,      # Show yt-dlp output
            'no_warnings': False,
            'verbose': False,     # Set True for debugging yt-dlp itself
            'noplaylist': False,  # Ensure playlists are handled
            'writethumbnail': True, # Optional: download thumbnail
            'postprocessor_args': { # Optional: Embed thumbnail if possible
                 'embedthumbnail': ['-metadata:s:v', 'title="Album cover"', '-metadata:s:v', 'comment="Cover (front)"']
            },
            # Removed 'extract_flat': 'in_playlist' - let yt-dlp get full info
        }

    def _download_with_ydl(self, url, ydl_opts, content_type_desc):
        """Core download logic using yt-dlp instance"""
        successful_items = 0
        total_items = 'unknown' # For playlists

        # Custom logger for yt-dlp
        class YtdlLogger:
             def debug(self, msg):
                  # Optional: Log verbose debug messages from yt-dlp if needed
                  # print(f"DEBUG: {msg}")
                  pass
             def info(self, msg):
                  # You can capture specific info messages if needed
                  # print(f"INFO: {msg}")
                  pass
             def warning(self, msg):
                  print(f"WARNING: {msg}")
                  logging.warning(f"YTDL Warning ({url}): {msg}")
             def error(self, msg):
                  print(f"ERROR: {msg}")
                  logging.error(f"YTDL Error ({url}): {msg}")

        ydl_opts['logger'] = YtdlLogger()

        # Progress hook
        def progress_hook(d):
            nonlocal successful_items, total_items
            if d['status'] == 'downloading':
                # Try to get filename, percentage, speed, eta
                filename = d.get('filename', 'N/A')
                percent_str = d.get('_percent_str', '---.-%')
                speed_str = d.get('_speed_str', '----.--B/s')
                eta_str = d.get('_eta_str', '--:--')
                # Truncate filename if too long for one line
                max_len = 60
                short_filename = os.path.basename(filename)
                if len(short_filename) > max_len:
                    short_filename = short_filename[:max_len-3] + "..."
                print(f"\rDownloading: {short_filename} | {percent_str.strip():>8} | {speed_str.strip():>12} | ETA: {eta_str.strip():<8}", end='')
            elif d['status'] == 'finished':
                successful_items += 1
                filename = d.get('filename', 'N/A')
                print(f"\nFinished: {os.path.basename(filename)}") # Newline after finish
                # Log success in main log file
                info = d.get('info_dict', {})
                video_id = info.get('id', 'unknown_id')
                platform = self.get_platform(info.get('webpage_url', url)) # Use original URL as fallback
                logging.info(f"Success ({platform}): {video_id} -> {content_type_desc} [{os.path.basename(filename)}]")
            elif d['status'] == 'error':
                 print(f"\nError downloading item in {url}. Check logs. Skipping...")
                 # Error already logged by YtdlLogger

            # Get total items if available (usually at the start of playlist download)
            if 'total_items' in d:
                 total_items = d['total_items']

            # Update progress summary for playlists
            if isinstance(total_items, int):
                 print(f"\rPlaylist Progress: {successful_items}/{total_items} items completed.", end='')


        ydl_opts['progress_hooks'] = [progress_hook]

        try:
            print(f"Starting {content_type_desc} download for: {url}")
            # Add limit if requested
            if 'playlistend' in ydl_opts:
                 print(f"Limiting download to {ydl_opts['playlistend']} items.")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                 ydl.download([url]) # Pass URL as a list
            # After download finishes (or errors out with ignoreerrors=True)
            print(f"\nFinished processing URL: {url}")
            if isinstance(total_items, int):
                 print(f"Successfully downloaded {successful_items}/{total_items} items from this URL.")
            elif successful_items > 0 :
                 print(f"Successfully downloaded {successful_items} item(s) from this URL.")
            else:
                 # This might happen if all items were already in archive or errors occurred
                 print("No new items downloaded (might be archived or errors occurred).")
            return True # Indicate the process ran, even if items were skipped/failed

        except DownloadError as e:
            # This catches errors if ignoreerrors=False, or fatal errors
            print(f"\nFATAL Download Error for {url}: {e}")
            logging.error(f"Fatal Download Error for {url}: {e}")
            return False
        except Exception as e:
            # Catch other unexpected errors during download attempt
            print(f"\nAn unexpected error occurred during download for {url}: {e}")
            logging.exception(f"Unexpected download error for {url}:") # Log full traceback
            return False

    def download_audio(self, url, cookies_file):
        """Download audio from URL"""
        postprocessors = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192', # Quality for mp3
        }]
        # Prefer opus or m4a for better quality if MP3 conversion isn't strictly needed
        # format_prefs = 'bestaudio[ext=opus]/bestaudio[ext=m4a]/bestaudio/best'
        format_prefs = 'bestaudio/best' # Let yt-dlp choose best audio format, then convert
        ydl_opts = self._create_ydl_options(self.audio_dir, self.audio_archive_file, cookies_file, format_prefs, postprocessors)

        # Handle playlists/channels - ask for limit
        content_type = self.is_playlist_or_channel(url)
        if content_type in ["playlist", "channel"]:
            print(f"Detected {content_type}. Will attempt to download all items.")
            try:
                limit_input = input("Enter max number of NEW items to download (leave blank for all, 0 for none): ")
                if limit_input.strip():
                    limit = int(limit_input)
                    if limit > 0:
                        ydl_opts['playlistend'] = limit
                        # Use 'playlist_items': f'1-{limit}' for more specific range if needed
                    elif limit == 0:
                         print("Skipping download as limit is 0.")
                         return True # Treat as "success" in terms of processing the URL line
            except ValueError:
                print("Invalid number. Will download all new items.")

        return self._download_with_ydl(url, ydl_opts, "audio")


    def download_video(self, url, cookies_file):
        """Download video from URL"""
        format_prefs = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best[ext=mp4]/best'
        # The above prefers MP4 directly if available, otherwise merges best video/audio, falling back to best overall MP4, then any best format.
        ydl_opts = self._create_ydl_options(self.video_dir, self.video_archive_file, cookies_file, format_prefs)
        ydl_opts['merge_output_format'] = 'mp4' # Ensure merged output is mp4

        # Handle playlists/channels - ask for limit
        content_type = self.is_playlist_or_channel(url)
        if content_type in ["playlist", "channel"]:
            print(f"Detected {content_type}. Will attempt to download all items.")
            try:
                limit_input = input("Enter max number of NEW items to download (leave blank for all, 0 for none): ")
                if limit_input.strip():
                    limit = int(limit_input)
                    if limit > 0:
                        ydl_opts['playlistend'] = limit
                    elif limit == 0:
                        print("Skipping download as limit is 0.")
                        return True # Treat as "success" in terms of processing the URL line
            except ValueError:
                print("Invalid number. Will download all new items.")

        return self._download_with_ydl(url, ydl_opts, "video")

    def show_available_formats(self, url):
        """Show available formats for a URL"""
        print(f"\nListing available formats for {url}...")
        cookies_file = self.get_cookies() # Get cookies for listing formats too
        ydl_opts = {
            'listformats': True,
            'quiet': False,
            'cookiefile': cookies_file,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
             # yt-dlp with listformats often exits non-zero even on success,
             # so we don't necessarily treat exceptions as errors here.
             # Check if it's a DownloadError we should report
             if isinstance(e, DownloadError):
                 print(f"Error listing formats: {e}")
                 logging.error(f"Error listing formats for {url}: {e}")
             # Else: assume formats were listed despite the exit code.

    def process_downloads(self, content_type):
        """Process downloads based on content type (audio/video)"""
        file_path = self.audio_file if content_type == "audio" else self.video_file
        download_func = self.download_audio if content_type == "audio" else self.download_video

        # Ensure the file exists before reading
        if not os.path.exists(file_path):
            print(f"{content_type.capitalize()} URL file not found: {file_path}. Creating it.")
            with open(file_path, "w", encoding='utf-8') as f:
                f.write("# Add URLs here, one per line\n")
            print("Please add URLs using the 'Manage URLs' menu and try again.")
            return # Exit if file was just created

        # Get cookies (do this once before processing all URLs)
        print("-" * 30)
        cookies_file = self.get_cookies()
        print("-" * 30)

        # Read URLs
        urls = self.read_urls(file_path)
        if not urls:
            print(f"No URLs found in {os.path.basename(file_path)}. Add URLs via the menu.")
            return # Exit if no URLs to process

        print(f"\nProcessing {len(urls)} URLs for {content_type} download...")
        print("-" * 30)

        successful_urls = [] # URLs that were processed (even if items skipped)
        failed_urls = []     # URLs that caused fatal errors during processing

        for i, url in enumerate(urls, 1):
            print(f"\n>>> Processing URL {i}/{len(urls)}: {url}")
            content_subtype = self.is_playlist_or_channel(url)
            print(f"URL type detected as: {content_subtype}")

            # Attempt the download
            success = download_func(url, cookies_file)

            if success:
                successful_urls.append(url)
                # --- Modified URL Removal ---
                # Only ask to remove if it was a SINGLE item and successful
                if content_subtype == "single":
                    remove_choice = input(f"Download process completed for single item. Remove URL from list? (y/n): ")
                    if remove_choice.lower() == 'y':
                        self.remove_url_from_file(file_path, url)
                else:
                    # For playlists/channels, don't ask automatically. User can manage via menu.
                    print(f"Finished processing {content_subtype} URL. Manage URLs via the main menu if needed.")
                # --- End Modified URL Removal ---
            else:
                failed_urls.append(url)
                print(f"Processing failed for URL: {url}")
                choice = input("Attempt to list available formats for this URL? (y/n): ")
                if choice.lower() == 'y':
                    self.show_available_formats(url)

            print("-" * 30) # Separator between URLs

        print("\n===== Download Summary =====")
        print(f"Processed {len(urls)} URLs from {os.path.basename(file_path)}.")
        print(f" - URLs processed successfully (may include skips/errors on individual items): {len(successful_urls)}")
        print(f" - URLs where processing encountered fatal errors: {len(failed_urls)}")
        if failed_urls:
             print("   Failed URLs:")
             for failed_url in failed_urls:
                  print(f"     - {failed_url}")
        print("==========================")

    def manage_urls(self, content_type):
        """Manage URLs in the specified file (View, Add, Remove)"""
        file_path = self.audio_file if content_type == "audio" else self.video_file

        # Ensure the file exists
        if not os.path.exists(file_path):
            print(f"Creating {content_type} file at: {file_path}")
            with open(file_path, "w", encoding='utf-8') as f:
                f.write("# Add URLs here, one per line\n")

        while True:
            print(f"\n===== Manage {content_type.capitalize()} URLs ({os.path.basename(file_path)}) =====")
            urls = self.read_urls(file_path) # Read fresh list each time
            if urls:
                print("Current URLs:")
                for i, url in enumerate(urls, 1):
                    url_type = self.is_playlist_or_channel(url)
                    print(f"{i: >3}. [{url_type.capitalize():<8}] {url}")
            else:
                print(f"No URLs currently in {os.path.basename(file_path)}")

            print("\nOptions:")
            print("1. Add new URL")
            print("2. Remove URL (by number)")
            print("3. Back to main menu")

            choice = input("Enter your choice (1-3): ").strip()

            if choice == "1":
                self.add_url(file_path) # Add_url now reads the file again to check duplicates
                # No need to reload urls here, loop does it

            elif choice == "2":
                if not urls:
                    print("No URLs to remove.")
                    continue

                try:
                    idx_input = input(f"Enter the number of the URL to remove (1-{len(urls)}, 0 to cancel): ")
                    idx = int(idx_input)
                    if 1 <= idx <= len(urls):
                        url_to_remove = urls[idx - 1]
                        if self.remove_url_from_file(file_path, url_to_remove):
                             print("URL removed successfully.")
                             # List will refresh on next loop iteration
                        else:
                             print("Failed to remove URL (maybe it was already removed?).")
                    elif idx == 0:
                         print("Removal cancelled.")
                    else:
                        print(f"Invalid number. Please enter between 1 and {len(urls)} or 0.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

            elif choice == "3":
                break # Exit manage URLs menu

            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

    def clear_archive(self):
        """Clear archive files to allow re-downloading content"""
        print("\n===== Clear Download Archives =====")
        print("WARNING: Clearing archives means yt-dlp will re-check")
        print("         *all* items in playlists/channels listed in your")
        print("         audio.txt/video.txt files on the next run,")
        print("         potentially re-downloading them if not already present.")
        print("-" * 20)
        print("1. Clear AUDIO archive only")
        print("2. Clear VIDEO archive only")
        print("3. Clear BOTH archives")
        print("4. Back to main menu")

        choice = input("Enter your choice (1-4): ").strip()

        files_to_clear = []
        if choice == "1":
            files_to_clear.append(self.audio_archive_file)
        elif choice == "2":
            files_to_clear.append(self.video_archive_file)
        elif choice == "3":
            files_to_clear.extend([self.audio_archive_file, self.video_archive_file])
        elif choice == "4":
            print("No archives cleared.")
            return
        else:
            print("Invalid choice.")
            return

        if not files_to_clear:
             return # Should not happen with current logic, but safe check

        confirm_msg = "Are you sure you want to clear the selected archive(s)? (y/n): "
        if len(files_to_clear) == 2:
            confirm_msg = "Are you sure you want to clear BOTH archives? (y/n): "
        elif "audio" in os.path.basename(files_to_clear[0]):
             confirm_msg = "Are you sure you want to clear the AUDIO archive? (y/n): "
        elif "video" in os.path.basename(files_to_clear[0]):
            confirm_msg = "Are you sure you want to clear the VIDEO archive? (y/n): "

        confirmation = input(confirm_msg)
        if confirmation.lower() == 'y':
            for file_path in files_to_clear:
                try:
                    with open(file_path, "w") as f:
                        pass # Truncate the file
                    print(f"Cleared archive: {os.path.basename(file_path)}")
                    logging.info(f"Cleared archive: {os.path.basename(file_path)}")
                except Exception as e:
                    print(f"Error clearing archive {os.path.basename(file_path)}: {e}")
                    logging.error(f"Error clearing archive {file_path}: {e}")
        else:
            print("Archive clearing cancelled.")

    def display_menu(self):
        """Display the main menu"""
        print("\n===== Media Downloader Main Menu =====")
        print("1. Download Audio (from audio.txt)")
        print("2. Download Video (from video.txt)")
        print("3. Manage Audio URLs")
        print("4. Manage Video URLs")
        print("5. Show Available Formats for a specific URL")
        print("6. Clear Download Archives")
        print("7. Exit")
        return input("Enter your choice (1-7): ").strip()

    def run(self):
        """Main program loop"""
        print("=== Media Downloader Initialized ===")
        # Initial state info already printed in __init__

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
                url = input("Enter URL to check formats: ").strip()
                if url:
                    self.show_available_formats(url)
                else:
                    print("No URL entered.")
            elif choice == "6":
                self.clear_archive()
            elif choice == "7":
                print("Exiting program. Goodbye!")
                logging.info("Media Downloader finished")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")

def main():
    # Optional: Add command-line argument parsing here if needed later
    # e.g., python download_script.py --download-audio
    downloader = MediaDownloader()
    downloader.run()

if __name__ == "__main__":
    # Ensure the script's directory is the working directory
    # This helps when running from different locations, ensuring relative paths work
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
    except NameError:
        # Handle interactive/packaged case
        try:
            script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
            os.chdir(script_dir)
        except Exception:
            print("Warning: Could not change directory to script location.")

    main()