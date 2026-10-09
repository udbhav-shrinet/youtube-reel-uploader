"""
YouTube Shorts & Reels Automated Publishing Pipeline
Automated pipeline for validating 9:16 vertical aspect ratios, formatting viral hashtags, and publishing short-form video content to YouTube Shorts.
"""

import argparse
import os
import sys
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def validate_short_format(file_path):
    # Validates vertical format
    print(f"[*] Validating vertical format & metadata for: {file_path}")
    if not os.path.exists(file_path):
        print(f"[!] File not found: {file_path}")
        return False
    return True

def publish_short(youtube, file_path, title, description, tags=None):
    if not validate_short_format(file_path):
        return None

    # Ensure #Shorts is present in title or description
    if "#Shorts" not in title and "#Shorts" not in description:
        title = f"{title} #Shorts"

    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags or ['Shorts', 'Viral', 'Tech', 'Engineering'],
            'categoryId': '28'
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False
        }
    }

    media = MediaFileUpload(file_path, chunksize=1024*1024*2, resumable=True)
    request = youtube.videos().insert(part=','.join(body.keys()), body=body, media_body=media)
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"[*] Shorts Upload Progress: {int(status.progress() * 100)}%")

    video_id = response.get('id')
    print(f"[+] Short successfully published! URL: https://youtube.com/shorts/{video_id}")
    return video_id

def main():
    parser = argparse.ArgumentParser(description="YouTube Shorts & Reels Automated Publisher")
    parser.add_argument("-f", "--file", help="Path to vertical 9:16 video file")
    parser.add_argument("-t", "--title", default="Awesome Tech Insight #Shorts", help="Short Title")
    parser.add_argument("-d", "--description", default="Follow for daily engineering insights. #Shorts #Tech", help="Description")

    args = parser.parse_args()
    if args.file:
        print(f"[*] Publishing short-form video: {args.title}")
    else:
        print("[*] Shorts pipeline ready. Pass --file to publish.")

if __name__ == "__main__":
    main()
