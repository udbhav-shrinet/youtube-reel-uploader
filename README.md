# youtube-reel-uploader

A Python script to upload vertical videos (Shorts/Reels) to YouTube via the YouTube Data API v3.

## How it works

1. Checks if the video file exists.
2. Ensures the title or description contains `#Shorts` so YouTube indexes it as a Short.
3. Uploads the video in 2MB resumable chunks using `google-api-python-client`.
4. Outputs the published Short URL (`https://youtube.com/shorts/<id>`).

## Usage

```bash
pip install -r requirements.txt
python app.py --file "video.mp4" --title "My Short Title" --description "Optional description"
```
