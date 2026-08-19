# Patient Voice Bot - AI Phone Agent Assessor

An automated Python voice bot built to evaluate, stress-test, and identify quality issues/bugs in the clinic's AI voice agent at `+1-805-439-8008`.

## Features
* **Scenario Automation:** Programmatically triggers realistic patient phone calls via Bland AI API.
* **Transcript & Metadata Retrieval:** Automatically pulls full multi-turn call transcripts and structures them locally.
* **Bug Detection:** Identified functional and state-consistency issues during test calls.

## Prerequisites
* Python 3.10+
* A Bland AI API key

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <YOUR_GITHUB_REPO_URL>
   cd patient-voice-bot
   import os
import requests
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

BLAND_API_KEY = os.getenv("BLAND_API_KEY")

def fetch_all_calls():
    url = "https://api.bland.ai/v1/calls"
    headers = {"authorization": BLAND_API_KEY}
    return requests.get(url, headers=headers)

def get_single_call_details(call_id):
    url = f"https://api.bland.ai/v1/calls/{call_id}"
    headers = {"authorization": BLAND_API_KEY}
    res = requests.get(url, headers=headers)
    return res.json() if res.status_code == 200 else None

def download_recordings():
    recordings_dir = Path(__file__).parent / "calls" / "recordings"
    recordings_dir.mkdir(parents=True, exist_ok=True)
    
    res = fetch_all_calls()
    if res.status_code != 200:
        print("Failed to fetch call list")
        return
        
    calls = res.json()
    calls = calls.get("calls", calls) if isinstance(calls, dict) else calls
    
    downloaded = 0
    print("Checking audio recordings availability for existing calls...")
    
    for idx, item in enumerate(calls, start=1):
        call_id = item.get("call_id") or item.get("c_id") or item.get("id")
        if not call_id:
            continue
            
        details = get_single_call_details(call_id)
        if not details:
            continue
            
        rec_url = details.get("recording_url")
        if rec_url:
            file_name = f"recording-{idx:02d}.mp3"
            file_path = recordings_dir / file_name
            
            audio_res = requests.get(rec_url)
            if audio_res.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(audio_res.content)
                downloaded += 1
                print(f"Downloaded: {file_name} (Call ID: {call_id})")
            else:
                print(f"Failed audio download for call {call_id}")
        else:
            print(f"No recording URL found for call {call_id}")

    print(f"\nSummary: Successfully downloaded {downloaded} audio recordings.")

if __name__ == "__main__":
    download_recordings()
    