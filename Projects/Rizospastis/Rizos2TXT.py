from typing import List
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import ctypes
import os
import time
import textwrap
import sys

def set_console_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

def get_article_content(url):
    # Fetch HTML content
    response = requests.get(url)
    html_content = response.content

    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract title
    title_tag = soup.find('div', class_='title4')
    title = title_tag.text.strip() if title_tag else None

    # Extract article content
    article_tag = soup.find('div', class_='story_body')
    article = article_tag.text.strip() if article_tag else None

    return title, article

def SaveArticle(link, filename):
    # Initialize file_name with None
    file_name = None

    # Parse the URL to extract the date
    parsed_url = urlparse(link)
    query_params = parse_qs(parsed_url.query)
    date_param = query_params.get('publDate', [''])[0]

    # If a date is found in the URL, use it; otherwise, use the current date
    if date_param:
        current_date = datetime.now().strftime('%d/%m/%Y')
        new_url = link.replace(date_param, current_date)
    else:
        new_url = link

    # Get title and article content
    title, article = get_article_content(new_url)

    # Check if both title and article content are present
    if title is not None and article is not None:
        # Create a file name based on the provided or current date
        article_date = datetime.strptime(current_date, '%d/%m/%Y').strftime('%Y-%m-%d')
        file_name = f'{article_date} {filename}.txt'

        # Write title and article content to file
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(f'{title}\n\n')
            file.write(f'{article}')

        print(f'Το άρθρο "{filename}" κατέβηκε με επιτυχία')
    
    # Return file_name whether it's None or a valid value
    return file_name


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

def print_article(file_name,width):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.read()
            print_text(content, typing_speed=0.06, line_length=width)
    except FileNotFoundError:
        print(f'The file "{file_name}" does not exist.')

if __name__ == "__main__":
    # Set the desired title for the CLI window
    new_title = "Ριζοσπάστης Downloader"

    # Call the function to set the console title
    set_console_title(new_title)

    # Add the articles you want to download
    articles_to_download = [
        ("https://www.rizospastis.gr/columnStory.do?publDate=06/10/2023&columnId=7401", "Η άποψη μας"),
        ("https://www.rizospastis.gr/columnStory.do?publDate=14/11/2023&columnId=7124", "Αποκαλυπτικά"),
        ("https://www.rizospastis.gr/columnPage.do?publDate=04/11/2023&columnId=662", "Επιστήμη"),
        ("https://www.rizospastis.gr/columnStory.do?publDate=04/11/2023&columnId=521", "Πατριδογνωμόνιο"),
        ("https://www.rizospastis.gr/columnPage.do?publDate=4/11/2023&columnId=81", "ΑπόΜέρα")
    ]

    # Download all articles and store their file names
    downloaded_files = []
    for link, title in articles_to_download:
        downloaded_file = SaveArticle(link, title)
        if downloaded_file:
            downloaded_files.append(downloaded_file)

    # Print the content of all downloaded articles
    def print_text(text: str, typing_speed: float, line_length: int) -> None:
        lines = text.split('\n')
        for line in lines:
            for char in line:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(typing_speed)
            print()  # Move to the next line after completing a line of text
        print()  # Add a new line for paragraph breaks

    for file_name in downloaded_files:
        print(f'\nΑπό το αρχείο {file_name}:\n')
        print_text(file_name, 0.1, 40)
