import os
import zipfile
import shutil
import requests
from colorama import init, Fore, Back
import datetime
import re

init(autoreset=True)

link = "https://github.com/lCloudyyl/Mod-pack/releases/latest/download/mods.zip" 

responses = requests.get(link)

print(responses.headers)

print("Checking link")

def file_info(headers):

    cd = headers.get('content-disposition')

    if not cd:
        return None, 0

    fname_match = re.findall(r'filename="?([^";]+)"?', cd)
    filename = fname_match[0].strip() if fname_match else None

    if not filename:
        return None, 0

    size = int(headers.get('Content-Length', 0))

    return filename, size

def main():
    filename, size = file_info(responses.headers)

    print(f"Name: {filename} Size: {size}")


if __name__ == "__main__":
    main()

