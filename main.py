import os
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

# ========================================
# LOAD ENVIRONMENT VARIABLES
# ========================================

env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

BLAND_API_KEY = os.getenv("BLAND_API_KEY")
BLAND_FROM_NUMBER = os.getenv("BLAND_FROM_NUMBER")
TEST_NUMBER = os.getenv("TEST_NUMBER")

BASE_URL = "https://api.bland.ai/v1"

# ========================================
# CALL SETTINGS
# ========================================

CALL_NUMBER = 10
MAX_DURATION = 3

RECORDINGS_DIR = Path(__file__).parent / "calls" / "recordings"
TRANSCRIPTS_DIR = Path(__file__).parent / "calls" / "transcripts"


def get_headers():
    return {
        "authorization": BLAND_API_KEY,
        "Content-Type": "application/json",
    }


# ========================================
# CALL #10 SCENARIO
# ========================================

SCENARIO = """
You are a realistic human patient calling a medical clinic.

Stay completely in character as a normal patient.
Never say that you are an AI, bot, automated tester, or that this is a test.

Your goal is to make a non-urgent appointment.

Start naturally by saying:

"Hi, I'd like to make an appointment, but I'm not sure whether
I need a new patient visit or a regular office visit."

If the agent asks for your name, say:

"John Smith."

If the agent asks for your date of birth, say:

"January fifteenth, nineteen eighty."

Explain:

"I've been having some mild shoulder pain for the last couple
of weeks. It's not an emergency, but I'd like a doctor to take
a look at it."

If the agent asks whether this is a follow-up, say:

"No, this is the first time I'm coming in for this problem."

Ask:

"Would that be considered a new patient visit?"

If the agent explains the appointment type, ask one reasonable
follow-up question about what the visit includes.

If the agent asks whether you have a preferred provider, say:

"I don't have a specific doctor in mind. I'd like the earliest
reasonable appointment."

If the agent offers an appointment, ask:

"Is that appointment with an orthopedic doctor?"

Before accepting, ask:

"Can you confirm the date, time, and doctor's name?"

If the appointment details are clear, accept the appointment.

Do not intentionally make the conversation longer than necessary.
Do not rush the conversation.

Thank the agent and end the call naturally.
"""


# ========================================
# SAVE CALL DATA
# ========================================

def save_call(call_id):

    headers = get_headers()

    RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)
    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

    print("")
    print("Getting final call details...")

    try:
        response = requests.get(
            f"{BASE_URL}/calls/{call_id}",
            headers=headers,
            timeout=30,
        )
    except requests.RequestException as e:
        print(f"ERROR: Could not get call details: {e}")
        return

    print(f"Details status: {response.status_code}")

    if not response.ok:
        print("ERROR: Could not retrieve call details.")
        print(response.text)
        return

    call_data = response.json()

    print(f"Call status: {call_data.get('status')}")
    print(f"Call length: {call_data.get('call_length')} minutes")

    # ========================================
    # SAVE TRANSCRIPT
    # ========================================

    transcript = call_data.get("concatenated_transcript")

    if transcript:

        transcript_path = (
            TRANSCRIPTS_DIR /
            f"call-{CALL_NUMBER:02d}.txt"
        )

        transcript_path.write_text(
            transcript,
            encoding="utf-8"
        )

        print("")
        print("Transcript saved:")
        print(transcript_path)

    else:
        print("")
        print("WARNING: No transcript found.")

    # ========================================
    # DOWNLOAD RECORDING
    # ========================================

    print("")
    print("Downloading recording...")

    try:
        recording_response = requests.get(
            f"{BASE_URL}/calls/{call_id}/recording",
            headers=headers,
            timeout=60,
        )
    except requests.RequestException as e:
        print(f"WARNING: Could not download recording: {e}")
        return

    print(f"Recording status: {recording_response.status_code}")

    if recording_response.ok:

        recording_path = (
            RECORDINGS_DIR /
            f"call-{CALL_NUMBER:02d}.mp3"
        )

        recording_path.write_bytes(
            recording_response.content
        )

        print("Recording saved:")
        print(recording_path)

        print(
            f"Recording size: "
            f"{recording_path.stat().st_size / 1024 / 1024:.2f} MB"
        )

    else:

        print("WARNING: Recording could not be downloaded automatically.")
        print(recording_response.text)

        print("")
        print("Download the recording manually from Bland as MP3 or OGG.")
        print("Save it as:")

        print(
            RECORDINGS_DIR /
            f"call-{CALL_NUMBER:02d}.mp3"
        )


# ========================================
# MAKE CALL #10
# ========================================

def make_call():

    if not BLAND_API_KEY:
        print("ERROR: BLAND_API_KEY is missing from .env")
        return

    if not BLAND_FROM_NUMBER:
        print("ERROR: BLAND_FROM_NUMBER is missing from .env")
        return

    if not TEST_NUMBER:
        print("ERROR: TEST_NUMBER is missing from .env")
        return

    request_data = {
        "phone_number": TEST_NUMBER,
        "from": BLAND_FROM_NUMBER,
        "task": SCENARIO,
        "model": "enhanced",
        "max_duration": MAX_DURATION,
        "record": True,
    }

    headers = get_headers()

    print("========================================")
    print(" PATIENT VOICE BOT - CALL #10")
    print("========================================")
    print(f"From: {BLAND_FROM_NUMBER}")
    print(f"To:   {TEST_NUMBER}")
    print(f"Maximum duration: {MAX_DURATION} minutes")
    print("Recording: ON")
    print("")
    print("Scenario: Ambiguous Appointment Type")
    print("")
    print("Sending call...")

    try:
        response = requests.post(
            f"{BASE_URL}/calls",
            headers=headers,
            json=request_data,
            timeout=30,
        )
    except requests.RequestException as e:
        print(f"ERROR: Request failed: {e}")
        return

    print(f"Status code: {response.status_code}")
    print("")

    try:
        result = response.json()
    except ValueError:
        print("ERROR: Invalid response from Bland.")
        print(response.text)
        return

    print("Bland response:")
    print(result)

    if not response.ok or not result.get("call_id"):
        print("")
        print("ERROR: Call was not accepted.")
        return

    call_id = result["call_id"]

    print("")
    print("========================================")
    print(" CALL #10 SUCCESSFULLY QUEUED")
    print("========================================")
    print(f"Call ID: {call_id}")
    print("")
    print("Wait for the conversation to finish.")
    print("The transcript and recording will be saved automatically.")
    print("")

    # ========================================
    # WAIT FOR CALL TO FINISH
    # ========================================

    max_wait_seconds = 420
    waited = 0

    while waited < max_wait_seconds:

        time.sleep(10)
        waited += 10

        try:
            status_response = requests.get(
                f"{BASE_URL}/calls/{call_id}",
                headers=headers,
                timeout=30,
            )
        except requests.RequestException as e:
            print(f"Status check error: {e}")
            continue

        if not status_response.ok:
            print(
                f"Status check failed: "
                f"{status_response.status_code}"
            )
            continue

        call_data = status_response.json()
        status = call_data.get("status")

        print(f"Call status: {status}")

        if status in [
            "completed",
            "failed",
            "error",
            "no-answer"
        ]:
            break

    # ========================================
    # SAVE EVERYTHING AUTOMATICALLY
    # ========================================

    save_call(call_id)

    print("")
    print("========================================")
    print(" CALL #10 PROCESS COMPLETE")
    print("========================================")


# ========================================
# RUN
# ========================================

if __name__ == "__main__":
    make_call()
    