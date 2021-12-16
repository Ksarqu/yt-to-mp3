import json
import os
import pathlib
import re
import shutil
from os import system, rename, path

import yt_dlp as youtube_dl

lang_files_dir = "languages"
lang_files = os.listdir(lang_files_dir)
languages_data = {}
for file in lang_files:
    language = file.split(".")[0]  # separates the filename from the extension
    with open(f"{lang_files_dir}\\{file}", "r", encoding="utf-8") as current_file:
        languages_data[language] = json.load(current_file)

urls = []

if not path.isfile("config.json"):
    with open("config.json", 'w', encoding="utf-8") as config_file:
        config_data = {"path": "C:\\Users\\XXXUSERXXX\\Desktop",
                       "language": "EN"}
        json.dump(config_data,
                  config_file,
                  indent=4,
                  sort_keys=True)
        print("Please edit the config file as you want!")
        exit()
else:
    with open("config.json", "r") as config_file:
        config_data = json.load(config_file)
        lang = config_data["language"]


def collect_urls():
    while True:
        print(languages_data[lang]["period_warner"])
        url = input(languages_data[lang]["enter_url"])
        system("cls")
        if url == ".":
            break
        else:
            pass
        if "youtube.com" in url:
            urls.append(url)
        else:
            print(languages_data[lang]["wrong_url"])


def download():
    for url in urls:
        video_info = youtube_dl.YoutubeDL().extract_info(url=url, download=False)
        filename = re.sub('[#<$+%>!"`&*|{}@:/?=]', '', video_info['title'])[:200] + ".mp3"
        options = {
            'format': 'bestaudio/best',
            'keepvideo': False,
            'outtmpl': "music.mp3",
        }
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])
        with open("config.json", "r") as f:
            destination_file = json.load(f)
        source = str(pathlib.Path(__file__).parent)
        destination = destination_file["path"] + f"\\{filename}"
        rename("music.mp3", filename)
        shutil.move(source + f"\\{filename}", destination)


collect_urls()
download()
