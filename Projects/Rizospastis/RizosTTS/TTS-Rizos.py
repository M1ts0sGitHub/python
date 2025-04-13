from gtts import gTTS
import sys
import time
import datetime
import subprocess
import threading
import textwrap
import os

def speed_up_mp3(input_file, output_file, speed):
    command = ["ffmpeg", "-i", input_file, "-af", f"atempo={speed}", output_file]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.communicate()  # This will wait for the command to finish without displaying output

def synthesize_text_to_speech(text, output_file):
    tts = gTTS(text=text, lang="el")
    tts.save("temp.mp3")
    currentdate = datetime.datetime.now().strftime("%Y%m%d")
    speed_up_mp3("temp.mp3", f"{currentdate}_Rizospastis.mp3", 1.6)
    os.remove("temp.mp3")

def get_text(input_file):
    subprocess.run(["notepad", input_file])
    with open(input_file, "r", encoding="utf-8") as file:
        text = file.read()
    return text

def print_text(text, typing_speed, line_length):
    paragraphs = text.split('\n')
    for para in paragraphs:
        lines = textwrap.wrap(para, width=line_length)
        for line in lines:
            for char in line:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(typing_speed)
            print()  # Move to the next line after completing a line of text
        print()  # Add a new line for paragraph breaks

def text_and_speech_in_parallel():

    # Create threads for printing text and synthesizing speech
    speech_thread = threading.Thread(target=synthesize_text_to_speech, args=(text, "rizospastis.mp3"))
    print_thread = threading.Thread(target=print_text, args=(text,0.06,40))

    print_thread.start()
    speech_thread.start()


if __name__ == "__main__":
    os.system("title TTS - Rizospastis Edition")
    os.system("start https://www.rizospastis.gr/textOnly.do?nav=true")

    text = get_text("input.txt")

    text_and_speech_in_parallel()
