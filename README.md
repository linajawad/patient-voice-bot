# Patient Voice Bot — AI Voice Agent QA Tester

A Python-based voice testing bot designed to evaluate, stress-test, and identify bugs in AI-powered healthcare phone agents.

The bot acts as a realistic patient, places automated outbound calls through the Bland AI telephony API, follows predefined patient scenarios, and saves call transcripts locally for quality analysis.

## Project Goal

The goal of this project is to test an AI phone agent from the perspective of a real patient.

Instead of manually making every test call, the Patient Voice Bot automates repeatable scenarios such as:

* Scheduling an appointment
* Asking about insurance
* Canceling an appointment
* Rescheduling an appointment
* Requesting a medication refill
* Asking general clinic questions
* Verifying provider and appointment information
* Testing conversational interruptions and edge cases

The resulting conversations are reviewed to identify functional, conversational, and state-consistency bugs.

## Architecture

```text
Patient Voice Bot
       |
       v
   Python / main.py
       |
       v
 Bland AI REST API
       |
       v
 Automated Phone Call
       |
       v
 Healthcare AI Agent
       |
       v
 Call Transcript + Recording
       |
       v
 Local QA Artifacts
   |            |
   v            v
Transcripts   Recordings
   |
   v
Bug Analysis / QA Reports
```

### Main Components

**`main.py`**

The primary orchestration script. It:

1. Loads configuration from `.env`
2. Defines the patient scenario
3. Sends an outbound call through Bland AI
4. Enables call recording
5. Retrieves completed call details
6. Saves the transcript locally
7. Attempts to download the recording automatically
8. Stores test artifacts under the `calls/` directory

**`ARCHITECTURE.md`**

Documents the system architecture, technical decisions, and API-based design trade-offs.

**`bug_report.md`**

Contains bugs discovered during testing, including provider identity inconsistencies, unnecessary profile creation, and speech-overlap behavior.

## Test Evidence

The project contains transcripts from multiple completed test calls:

```text
calls/
├── recordings/
│   └── Local call recordings
│
└── transcripts/
    ├── call-01.txt
    ├── call-02.txt
    ├── call-03.txt
    ├── call-04.txt
    ├── call-05.txt
    ├── call-06.txt
    ├── call-07.txt
    ├── call-08.txt
    ├── call-09.txt
    └── call-10.txt
```

Audio recordings are intentionally excluded from Git version control because they are large binary files. They are stored locally for testing and review.

## Bugs Identified

Testing uncovered several issues in the target AI phone agent.

### 1. Provider Identity Inconsistency

**Severity:** Medium

The agent offered an appointment with one provider but used a different provider name during final confirmation.

**Expected behavior:** The provider identity should remain consistent from appointment search through final confirmation.

### 2. Profile Creation During Basic Questions

**Severity:** Low

During informational calls, the agent attempted to initiate patient-profile behavior even though the caller was only asking basic questions such as clinic location and office hours.

**Expected behavior:** General informational questions should be answered directly without unnecessary patient registration.

### 3. Speech Overlap / Barge-In Handling

**Severity:** Medium

During some conversations, the AI agent continued speaking after the caller attempted to interrupt or clarify a response. This resulted in repeated phrases, awkward overlaps, and incomplete responses.

**Expected behavior:** When caller speech is detected, the agent should stop or clear the current response and process the caller's new input.

## Example Test Scenarios

### Appointment Scheduling

The patient asks to schedule a non-urgent appointment and evaluates whether the agent:

* Identifies the correct appointment type
* Provides available providers
* Provides accurate appointment times
* Maintains provider identity
* Confirms the correct date and time

### Appointment Cancellation

The patient requests cancellation and checks whether the agent:

* Locates the correct appointment
* Confirms the appointment being canceled
* Requests an appropriate reason
* Correctly confirms cancellation

### Appointment Rescheduling

The patient requests a different appointment date and checks whether the agent:

* Finds the existing appointment
* Understands the request
* Searches alternative dates
* Preserves the original provider when appropriate

### Medication Refill

The patient requests a medication refill and checks whether the agent:

* Identifies the refill request
* Handles missing medication records
* Provides an appropriate next step
* Transfers the patient when necessary

### General Information

The patient asks about:

* Clinic location
* Office hours
* Insurance acceptance
* Required documents

This tests whether the agent can answer simple questions without unnecessary workflows.

## Technology Stack

* **Python**
* **Bland AI REST API**
* **Requests**
* **python-dotenv**
* **REST API**
* **Git / GitHub**

## Setup

### Requirements

* Python 3.10+
* Bland AI account
* Bland AI API key
* A phone number configured for outbound testing

### Install Dependencies

```bash
pip install requests python-dotenv
```

### Configure Environment Variables

Create a local `.env` file:

```env
BLAND_API_KEY=your_api_key
BLAND_FROM_NUMBER=your_bland_phone_number
TEST_NUMBER=target_test_number
```

Never commit `.env` to GitHub.

The repository includes `.env.example` as a safe configuration template.

## Run the Bot

From the project directory:

```bash
python main.py
```

The bot will:

1. Send the configured patient scenario to Bland AI
2. Place the test call
3. Wait for the call to complete
4. Retrieve the call details
5. Save the transcript
6. Attempt to download the recording

Transcripts are stored in:

```text
calls/transcripts/
```

Recordings are stored locally in:

```text
calls/recordings/
```

If a recording is not available through the API endpoint, the transcript is still saved and the recording can be downloaded manually from the Bland dashboard when available.

## Security

Sensitive configuration and local test artifacts are intentionally excluded from version control.

The `.gitignore` excludes:

```text
.env
__pycache__/
*.pyc
*.wav
*.mp3
calls/recordings/
```

API credentials should never be committed to GitHub.

## What This Project Demonstrates

This project demonstrates practical experience with:

* Python API integration
* REST API workflows
* Automated voice-agent testing
* Conversational QA
* Edge-case testing
* Bug identification
* Transcript analysis
* State consistency validation
* Telephony API orchestration
* Git and GitHub
* Local test artifact management

The project focuses not only on making an AI phone call, but on systematically testing the behavior of an AI agent and turning conversation results into actionable QA findings.

## Author

**Lina Jawad**

Cybersecurity student and aspiring AI / QA engineer focused on practical automation, AI agent testing, and technical problem solving.
