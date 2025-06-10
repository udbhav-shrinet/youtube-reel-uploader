import os
import pickle
import yt_dlp
import time
from flask import Flask
from google.auth.transport.requests import Request
import google_auth_oauthlib.flow
import googleapiclient.discovery
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google.oauth2 import service_account

app = Flask(__name__)

SERVICE_ACCOUNT_FILE = 'service_secret.json'
SCOPES_SHEETS = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1sKTouJQ9oVMiUtswozA0CR7TaxgKgP3vRTXJ1TFj2fo'
RANGE_NAME = 'Sheet1!A2:F'
LAST_PROCESSED_FILE = 'last_row.txt'


def read_sheet():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES_SHEETS)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    return result.get('values', [])


def write_back_status(row_index, status, video_url):
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES_SHEETS)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    values = [[status, video_url]]
    update_range = f'Sheet1!E{row_index}:F{row_index}'

    body = {'values': values}
    sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=update_range,
        valueInputOption='RAW',
        body=body
    ).execute()


def download_instagram_reel(instagram_url, output_path='reel.mp4'):
    ydl_opts = {
        'outtmpl': output_path,
        'quiet': False,
        'format': 'best',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print("⬇️ Downloading Instagram Reel...")
        ydl.download([instagram_url])
    print("✅ Download complete!")


def get_youtube_credentials():
    TOKEN_DIR = os.path.expanduser('.credentials')
    os.makedirs(TOKEN_DIR, exist_ok=True)
    TOKEN_PATH = os.path.join(TOKEN_DIR, 'youtube_token.pickle')

    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
    CLIENT_SECRETS_FILE = 'client_secret.json'

    creds = None
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token_file:
            creds = pickle.load(token_file)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, 'wb') as token_file:
            pickle.dump(creds, token_file)

    return creds


def upload_video(file_path, title, description, tags=None, privacy='public'):
    creds = get_youtube_credentials()
    youtube = googleapiclient.discovery.build('youtube', 'v3', credentials=creds)

    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags if tags else ['instagram', 'shorts', 'api upload']
        },
        'status': {
            'privacyStatus': privacy
        }
    }

    mediaFile = MediaFileUpload(file_path, resumable=True)
    print("⬆️ Uploading to YouTube...")
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=mediaFile
    )
    response = request.execute()

    print("✅ Video uploaded!")
    video_url = f"https://www.youtube.com/watch?v={response['id']}"
    print("📺 Link:", video_url)
    return video_url


def get_last_processed_row():
    if not os.path.exists(LAST_PROCESSED_FILE):
        return 1
    with open(LAST_PROCESSED_FILE, 'r') as f:
        return int(f.read().strip())


def set_last_processed_row(index):
    with open(LAST_PROCESSED_FILE, 'w') as f:
        f.write(str(index))


def process_new_row():
    rows = read_sheet()
    last_index = get_last_processed_row()

    if len(rows) < last_index:
        print("No new rows.")
        return

    row = rows[last_index - 1]
    row_index = last_index + 1

    if len(row) < 3:
        print("❌ Not enough data.")
        return

    try:
        instagram_url = row[0]
        title = row[1]
        description = row[2]
        tags = [tag.strip() for tag in row[3].split(',')] if len(row) > 3 else ['instagram', 'shorts', 'api upload']
        reel_path = f'reel_{row_index}.mp4'

        print(f"\n▶️ Processing row {row_index}: {title}")
        download_instagram_reel(instagram_url, output_path=reel_path)
        video_url = upload_video(reel_path, title, description, tags=tags, privacy="public")
        write_back_status(row_index, "✅ Success", video_url)
        os.remove(reel_path)
        set_last_processed_row(last_index + 1)

    except Exception as e:
        print(f"❌ Error: {e}")
        write_back_status(row_index, f"❌ Failed: {e}", "")
        set_last_processed_row(last_index + 1)


@app.route('/')
def home():
    process_new_row()
    return "Checked for new row and processed if available."


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
