import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv


# ============================================================
# PATIENT VOICE BOT
# ============================================================
# This script creates outbound test calls through the Bland AI
# API, waits for the call to finish, and saves the transcript
# and recording for QA review.
# ============================================================


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

BLAND_API_KEY = os.getenv("BLAND_API_KEY")
BLAND_FROM_NUMBER = os.getenv("BLAND_FROM_NUMBER")
TEST_NUMBER = os.getenv("TEST_NUMBER")

BASE_URL = "https://api.bland.ai/v1"

# Update these values when running a new test scenario.
# The existing project contains completed calls 01-10.
CALL_NUMBER = 10
SCENARIO_NAME = "New Patient Scenario"

MAX_DURATION = 4
MAX_WAIT_SECONDS = 420
POLL_INTERVAL_SECONDS = 10

RECORDINGS_DIR = BASE_DIR / "calls" / "recordings"
TRANSCRIPTS_DIR = BASE_DIR / "calls" / "transcripts"


# ============================================================
# TEST SCENARIO
# ============================================================

SCENARIO = """
You are a realistic human patient calling a medical clinic.

Stay completely in character as a normal patient.

Never say that you are an AI, bot, automated tester, or that
this is a test.

Speak naturally and conversationally.

[REPLACE THIS SECTION WITH THE PATIENT SCENARIO.]

If the agent asks for your name, provide the patient name
specified by the scenario.

If the agent asks for your date of birth, provide the date
specified by the scenario.

Follow the scenario naturally.

Do not intentionally make the conversation longer than
necessary.

Do not rush the conversation.

If the agent provides the requested information or completes
the requested action, respond naturally and end the call
politely.
"""


# ============================================================
# HTTP HELPERS
# ============================================================

def get_headers():
    """Return headers required by the Bland AI API."""
    return {
        "authorization": BLAND_API_KEY,
        "Content-Type": "application/json",
    }


def get_call_details(call_id):
    """Retrieve details for a specific call."""

    try:
        response = requests.get(
            f"{BASE_URL}/calls/{call_id}",
            headers=get_headers(),
            timeout=30,
        )
    except requests.RequestException as exc:
        print(f"ERROR: Could not retrieve call details: {exc}")
        return None

    if not response.ok:
        print(
            f"ERROR: Call details request failed "
            f"({response.status_code})"
        )
        print(response.text)
        return None

    try:
        return response.json()
    except ValueError:
        print("ERROR: Bland returned an invalid JSON response.")
        return None


# ============================================================
# SAVE TRANSCRIPT
# ============================================================

def save_transcript(call_data):
    """Save the completed call transcript locally."""

    transcript = call_data.get("concatenated_transcript")

    if not transcript:
        print("WARNING: No transcript was returned for this call.")
        return None

    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

    transcript_path = (
        TRANSCRIPTS_DIR / f"call-{CALL_NUMBER:02d}.txt"
    )

    transcript_path.write_text(
        transcript,
        encoding="utf-8",
    )

    print("")
    print("Transcript saved:")
    print(transcript_path)

    return transcript_path


# ============================================================
# SAVE RECORDING
# ============================================================

def save_recording(call_id):
    """Download the call recording when available."""

    RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)

    print("")
    print("Downloading recording...")

    try:
        response = requests.get(
            f"{BASE_URL}/calls/{call_id}/recording",
            headers=get_headers(),
            timeout=60,
        )
    except requests.RequestException as exc:
        print(f"WARNING: Recording download failed: {exc}")
        return None

    print(f"Recording status: {response.status_code}")

    if not response.ok:
        print(
            "WARNING: Recording could not be downloaded automatically."
        )

        if response.text:
            print(response.text)

        print("")
        print(
            "If the recording is available in the Bland dashboard,"
        )
        print("download it manually and save it as:")
        print(
            RECORDINGS_DIR
            / f"call-{CALL_NUMBER:02d}.mp3"
        )

        return None

    recording_path = (
        RECORDINGS_DIR / f"call-{CALL_NUMBER:02d}.mp3"
    )

    recording_path.write_bytes(response.content)

    size_mb = recording_path.stat().st_size / (1024 * 1024)

    print("Recording saved:")
    print(recording_path)
    print(f"Recording size: {size_mb:.2f} MB")

    return recording_path


# ============================================================
# WAIT FOR CALL
# ============================================================

def wait_for_call(call_id):
    """Poll the call until it reaches a terminal state."""

    print("")
    print("Waiting for the conversation to finish...")
    print("")

    waited = 0

    terminal_statuses = {
        "completed",
        "failed",
        "error",
        "no-answer",
        "busy",
        "canceled",
    }

    while waited < MAX_WAIT_SECONDS:

        time.sleep(POLL_INTERVAL_SECONDS)
        waited += POLL_INTERVAL_SECONDS

        call_data = get_call_details(call_id)

        if not call_data:
            continue

        status = call_data.get("status")

        print(
            f"Call status: {status} "
            f"({waited}/{MAX_WAIT_SECONDS}s)"
        )

        if status in terminal_statuses:
            return call_data

    print("")
    print("WARNING: Maximum wait time reached.")
    print("Attempting one final call-details request...")

    return get_call_details(call_id)


# ============================================================
# SAVE CALL ARTIFACTS
# ============================================================

def save_call(call_id, call_data=None):
    """Save transcript and recording for a completed call."""

    print("")
    print("========================================")
    print(" SAVING CALL ARTIFACTS")
    print("========================================")

    if call_data is None:
        call_data = get_call_details(call_id)

    if not call_data:
        print("ERROR: Unable to retrieve final call data.")
        return

    print(f"Call status: {call_data.get('status')}")
    print(f"Call length: {call_data.get('call_length')} minutes")

    save_transcript(call_data)
    save_recording(call_id)


# ============================================================
# VALIDATE CONFIGURATION
# ============================================================

def validate_configuration():
    """Check that all required environment variables exist."""

    required_variables = {
        "BLAND_API_KEY": BLAND_API_KEY,
        "BLAND_FROM_NUMBER": BLAND_FROM_NUMBER,
        "TEST_NUMBER": TEST_NUMBER,
    }

    missing = [
        name
        for name, value in required_variables.items()
        if not value
    ]

    if missing:
        print("ERROR: Missing environment variables:")

        for variable in missing:
            print(f"  - {variable}")

        print("")
        print("Check your .env file.")
        return False

    return True


# ============================================================
# MAKE OUTBOUND TEST CALL
# ============================================================

def make_call():
    """Create and monitor one outbound patient test call."""

    if not validate_configuration():
        return

    request_data = {
        "phone_number": TEST_NUMBER,
        "from": BLAND_FROM_NUMBER,
        "task": SCENARIO,
        "model": "enhanced",
        "max_duration": MAX_DURATION,
        "record": True,
    }

    print("========================================")
    print(" PATIENT VOICE BOT")
    print("========================================")
    print(f"Call number:       #{CALL_NUMBER:02d}")
    print(f"Scenario:          {SCENARIO_NAME}")
    print(f"From:              {BLAND_FROM_NUMBER}")
    print(f"To:                {TEST_NUMBER}")
    print(f"Maximum duration:  {MAX_DURATION} minutes")
    print("Recording:         ON")
    print("")
    print("Sending call...")

    try:
        response = requests.post(
            f"{BASE_URL}/calls",
            headers=get_headers(),
            json=request_data,
            timeout=30,
        )
    except requests.RequestException as exc:
        print(f"ERROR: Request failed: {exc}")
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

    if not response.ok:
        print("")
        print("ERROR: Call was not accepted.")
        return

    call_id = result.get("call_id")

    if not call_id:
        print("")
        print("ERROR: No call ID was returned.")
        return

    print("")
    print("========================================")
    print(f" CALL #{CALL_NUMBER:02d} SUCCESSFULLY QUEUED")
    print("========================================")
    print(f"Call ID: {call_id}")
    print("")
    print("The bot will wait for the call to finish.")
    print("Transcript and recording will be saved automatically.")
    print("")

    final_call_data = wait_for_call(call_id)

    if final_call_data:
        save_call(
            call_id,
            final_call_data,
        )

    print("")
    print("========================================")
    print(f" CALL #{CALL_NUMBER:02d} PROCESS COMPLETE")
    print("========================================")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    make_call()