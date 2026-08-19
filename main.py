import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

BLAND_API_KEY = os.getenv("BLAND_API_KEY")

def fetch_all_calls():
    url = "https://api.bland.ai/v1/calls"
    headers = {"authorization": BLAND_API_KEY}
    response = requests.get(url, headers=headers)
    return response

def get_single_call_details(call_id):
    url = f"https://api.bland.ai/v1/calls/{call_id}"
    headers = {"authorization": BLAND_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def save_all_transcripts(calls_list):
    output_dir = Path(__file__).parent / "calls" / "transcripts"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    saved_count = 0
    print("\nFetching full details for each call...")
    
    for idx, item in enumerate(calls_list, start=1):
        call_id = item.get("call_id") or item.get("c_id") or item.get("id")
        if not call_id:
            continue
            
        details = get_single_call_details(call_id)
        if not details:
            continue
            
        transcript = details.get("concatenated_transcript", "")
        if transcript:
            file_name = f"transcript-{idx:02d}.txt"
            file_path = output_dir / file_name
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"Call ID: {call_id}\n")
                f.write(f"Duration: {details.get('call_length')} mins\n")
                f.write(f"Summary: {details.get('summary')}\n")
                f.write("="*40 + "\n\n")
                f.write(transcript)
                
            saved_count += 1
            print(f"Saved: {file_name} (Call ID: {call_id})")

    print(f"\nDone! Saved {saved_count} transcripts to: {output_dir}")

def main():
    print("=== Fetching All Existing Calls ===")
    response = fetch_all_calls()
    
    if response.status_code == 200:
        data = response.json()
        calls = data.get("calls", data) if isinstance(data, dict) else data
        
        if isinstance(calls, list):
            print(f"Found {len(calls)} calls in account.")
            save_all_transcripts(calls)
        else:
            print("Unexpected API response structure.")
    else:
        print("Failed to fetch calls list:", response.text)

if __name__ == "__main__":
    main()
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
    import os
import json
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

def harvest_transcripts(calls_list):
    output_dir = Path(__file__).parent / "calls" / "transcripts"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    saved_count = 0
    for idx, item in enumerate(calls_list, start=1):
        call_id = item.get("call_id") or item.get("c_id") or item.get("id")
        if not call_id:
            continue
            
        details = get_single_call_details(call_id)
        if not details:
            continue
            
        transcript = details.get("concatenated_transcript", "")
        if transcript:
            file_name = f"transcript-{idx:02d}.txt"
            file_path = output_dir / file_name
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"Call ID: {call_id}\n")
                f.write(f"Duration: {details.get('call_length')} mins\n")
                f.write(f"Summary: {details.get('summary')}\n")
                f.write("="*40 + "\n\n")
                f.write(transcript)
                
            saved_count += 1

    print(f"Transcript Harvesting Complete: {saved_count} files stored.")

def main():
    print("=== Patient Voice Bot Orchestrator ===")
    res = fetch_all_calls()
    
    if res.status_code == 200:
        data = res.json()
        calls = data.get("calls", data) if isinstance(data, dict) else data
        if isinstance(calls, list):
            harvest_transcripts(calls)
    else:
        print("Failed to access Bland API:", res.text)

if __name__ == "__main__":
    main()
    
    
