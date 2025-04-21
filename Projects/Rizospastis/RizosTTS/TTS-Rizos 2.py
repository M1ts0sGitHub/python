from gtts import gTTS
import datetime
import os
import subprocess
import sys
import time
import threading
from pathlib import Path
import shutil

# Check if ffmpeg is installed and in PATH
def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def progress_bar_thread(stop_event):
    symbols = ['|', '/', '-', '\\']
    i = 0
    while not stop_event.is_set():
        sys.stdout.write('\r' + f"Processing... {symbols[i]} ")
        sys.stdout.flush()
        time.sleep(0.2)
        i = (i + 1) % len(symbols)
    sys.stdout.write('\r' + ' ' * 20 + '\r')
    sys.stdout.flush()

def show_progress_bar(operation):
    stop_event = threading.Event()
    print(f"{operation}...")
    progress_thread = threading.Thread(target=progress_bar_thread, args=(stop_event,))
    progress_thread.daemon = True
    progress_thread.start()
    return stop_event, progress_thread

def speed_up_mp3(input_file, output_file, speed):
    stop_event, progress_thread = show_progress_bar(f"Speeding up audio to {speed}x")
    
    try:
        # Make sure input exists and has content
        if not os.path.exists(input_file) or os.path.getsize(input_file) == 0:
            stop_event.set()
            time.sleep(0.3)
            print(f"Error: Input file {input_file} doesn't exist or is empty.")
            return False
        
        # Direct ffmpeg output to a log file for debugging
        log_file = os.path.splitext(output_file)[0] + "_ffmpeg.log"
        
        # Run ffmpeg with timeout
        command = ["ffmpeg", "-y", "-i", input_file, "-af", f"atempo={speed}", output_file]
        
        with open(log_file, 'w') as log:
            process = subprocess.Popen(command, stdout=log, stderr=log)
            
            # Check process status with timeout
            try:
                process.wait(timeout=60)  # 60 seconds timeout
                success = process.returncode == 0
                
                if not success:
                    print(f"\nffmpeg error (code {process.returncode}). Check {log_file} for details.")
                    return False
                    
            except subprocess.TimeoutExpired:
                process.kill()
                print("\nffmpeg process timed out after 60 seconds. Killing process.")
                stop_event.set()
                time.sleep(0.3)
                return False
                
    except Exception as e:
        print(f"\nError during audio processing: {e}")
        return False
    finally:
        stop_event.set()
        time.sleep(0.3)  # Give thread time to clean up display
    
    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
        return True
    
    print("\nError: Output file was not created properly.")
    return False

def synthesize_text_to_speech(text, script_dir):
    # Path operations to ensure files are in script directory
    temp_file = script_dir / "temp.mp3"
    currentdate = datetime.datetime.now().strftime("%Y%m%d")
    output_file = script_dir / f"{currentdate}_Rizospastis.mp3"
    
    # Generate TTS
    stop_event, progress_thread = show_progress_bar("Generating speech with Google TTS")
    try:
        tts = gTTS(text=text, lang="el")
        tts.save(str(temp_file))
        stop_event.set()
        time.sleep(0.3)
        
        if not os.path.exists(temp_file) or os.path.getsize(temp_file) == 0:
            print("Error: TTS did not generate a valid audio file.")
            return None
            
        print(f"TTS file created successfully: {os.path.getsize(temp_file)} bytes")
        
        # Speed up
        result = speed_up_mp3(str(temp_file), str(output_file), 1.6)
        
        # Clean up
        if os.path.exists(str(temp_file)):
            os.remove(str(temp_file))
        
        if result:
            print(f"\nCreated: {output_file}")
            print(f"File location: {os.path.abspath(output_file)}")
            return str(output_file)
        else:
            # Try direct copy as fallback
            print("\nFallback: Using original speed audio")
            shutil.copy(str(temp_file), str(output_file))
            
            if os.path.exists(str(output_file)):
                print(f"\nCreated (original speed): {output_file}")
                print(f"File location: {os.path.abspath(output_file)}")
                return str(output_file)
            
            print("\nError creating speech file.")
            return None
    except Exception as e:
        stop_event.set()
        time.sleep(0.3)
        print(f"\nError in TTS generation: {e}")
        return None

def get_text(input_file):
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            text = file.read()
        return text
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def display_text_stats(text):
    if text:
        char_count = len(text)
        word_count = len(text.split())
        line_count = text.count('\n') + 1
        
        print(f"Text statistics:")
        print(f"  - Characters: {char_count}")
        print(f"  - Words: {word_count}")
        print(f"  - Lines: {line_count}")
        print(f"  - Estimated audio duration: {word_count / 150:.1f} minutes at 1.6x speed")
        print("-" * 50)

if __name__ == "__main__":
    # Get the directory the script is running from
    script_dir = Path(__file__).parent.absolute()
    
    os.system("title TTS - Rizospastis Edition")
    
    # Check if ffmpeg is installed
    if not check_ffmpeg():
        print("ERROR: ffmpeg is not installed or not in your PATH.")
        print("Please install ffmpeg to use this script: https://ffmpeg.org/download.html")
        sys.exit(1)
    
    input_file = script_dir / "input.txt"
    print(f"Reading from: {input_file}")
    
    text = get_text(str(input_file))
    
    if text:
        display_text_stats(text)
        print(f"Converting text to speech...")
        output_path = synthesize_text_to_speech(text, script_dir)
        
        if output_path:
            print("\nConversion completed successfully!")
            user_response = input("Would you like to play the audio now? (y/n): ")
            if user_response.lower() == 'y':
                os.system(f'start "" "{output_path}"')
    else:
        os.system("start https://www.rizospastis.gr/textOnly.do?nav=true")
        os.system(f"notepad  {input_file}")
