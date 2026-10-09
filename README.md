# YouTube Shorts & Reels Automated Publishing Pipeline

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Interactive Demo](https://img.shields.io/badge/demo-GitHub%20Pages-pink.svg)](https://udbhav-shrinet.github.io/youtube-reel-uploader/)
[![Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11-blue.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> Automated short-form video ingestion engine designed for validating 9:16 vertical ratios, optimizing hook titles, and publishing YouTube Shorts via YouTube Data API v3.

---

## 🚀 Live Interactive Showcase

Preview vertical videos in a simulated mobile device viewer:  
👉 **[Launch Shorts & Reels Studio](https://udbhav-shrinet.github.io/youtube-reel-uploader/)**

---

## ✨ Key Features

- **9:16 Aspect Ratio Validation**: Ensures video formats adhere strictly to vertical mobile requirements before upload.
- **Hashtag & Metadata Formatting**: Automatically injects requisite `#Shorts` tags into video payloads.
- **Interactive Mobile Studio**: Client-side preview studio for simulating live mobile playback overlays.
- **OAuth API Integration**: Reliable token handling with resumable chunked upload support.

---

## 🛠️ System Architecture

```text
┌─────────────────────────┐       ┌────────────────────────┐       ┌──────────────────────┐
│  Vertical 9:16 Video    │ ───>  │ Aspect Ratio Validator │ ───>  │  YouTube Shorts API  │
│  (1080x1920 MP4/MOV)    │       │ Hashtag & Metadata     │       │ Resumable Uploader   │
└─────────────────────────┘       └────────────────────────┘       └──────────┬───────────┘
                                                                              │
                                                   ┌──────────────────────────┴──────────────────────────┐
                                                   ▼                                                     ▼
                                       ┌─────────────────────────┐                           ┌───────────────────────┐
                                       │   Live YouTube Short    │                           │  GitHub Pages Studio  │
                                       │  Feed Recommendation    │                           │  Mobile Simulator     │
                                       └─────────────────────────┘                           └───────────────────────┘
```

---

## 📦 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/udbhav-shrinet/youtube-reel-uploader.git
   cd youtube-reel-uploader
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Publish a Short**:
   ```bash
   python app.py --file "short_render.mp4" --title "Distributed Systems Explained #Shorts"
   ```

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
