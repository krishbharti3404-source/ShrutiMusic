# ig.py
"""
Heroku Safe Instagram + Pinterest Downloader
"""

import os
import requests
from bs4 import BeautifulSoup


# ---------------- INSTAGRAM -------------------
def download_instagram(url):
    try:
        print("➡ Fetching Instagram data…")

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        r = requests.get(url, headers=headers)
        html = r.text

        soup = BeautifulSoup(html, "html.parser")
        meta = soup.find("meta", property="og:video") or soup.find("meta", property="og:image")

        if not meta:
            print("⚠ Error: Media not found")
            return False

        media_url = meta.get("content")

        if not os.path.exists("downloads"):
            os.makedirs("downloads")

        ext = "mp4" if ".mp4" in media_url else "jpg"
        filename = f"downloads/ig_media.{ext}"

        print("➡ Downloading…")
        data = requests.get(media_url).content
        with open(filename, "wb") as f:
            f.write(data)

        print(f"✔ Done! saved to {filename}")
        return True

    except Exception as e:
        print("Instagram Error:", e)
        return False


# ---------------- PINTEREST -------------------
def download_pinterest(url):
    try:
        print("➡ Fetching Pinterest data…")

        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")

        video = soup.find("video")
        img = soup.find("img")

        if not os.path.exists("downloads"):
            os.makedirs("downloads")

        if video and video.get("src"):
            media = video.get("src")
            ext = "mp4"
        else:
            media = img.get("src")
            ext = "jpg"

        filename = f"downloads/pin_media.{ext}"

        print("➡ Downloading…")
        data = requests.get(media).content
        with open(filename, "wb") as f:
            f.write(data)

        print(f"✔ Done! Saved to {filename}")
        return True

    except Exception as e:
        print("Pinterest Error:", e)
        return False


# ------------ ROUTER ------------------------
def start_download(link):
    if "instagram.com" in link:
        return download_instagram(link)
    elif "pinterest." in link:
        return download_pinterest(link)
    else:
        print("⚠ Unsupported URL")
        return False
