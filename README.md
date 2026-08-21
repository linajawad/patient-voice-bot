
# Patient Voice Bot 📞

A Python voice-testing bot that acts like a patient and calls an AI healthcare phone agent.

I built this project to test how the agent handles real patient conversations, find bugs, and save the call results so I can review them later.

## What I Built

The bot:

* Creates patient test scenarios.
* Starts phone calls through the Bland AI API.
* Waits for the call to finish.
* Retrieves the call transcript.
* Saves transcripts and recordings.
* Helps me review the conversations and document bugs.

The main goal is to test the **quality and reliability** of the AI agent, not just whether the phone call works.

## How It Works

```text
Patient Scenario
      ↓
Python Bot
      ↓
Bland AI API
      ↓
AI Healthcare Agent
      ↓
Phone Conversation
      ↓
Transcript + Recording
      ↓
QA Review
      ↓
Bug Report
```


## Test Scenarios

I created 10 patient scenarios covering different types of conversations:

1. Appointment scheduling
2. General clinic questions
3. Appointment cancellation
4. Medication refill
5. Insurance questions
6. Appointment confirmation
7. Provider selection
8. Cancellation verification
9. Appointment rescheduling
10. New patient vs. regular office visit

Each scenario has a specific purpose. I used the conversations to look for incorrect information, unexpected behavior, and problems in the conversation flow.

## QA Findings

During testing, I found several issues in the AI agent.

### 1. Provider Identity Inconsistency

The agent gave one provider name when discussing available appointments and a different provider name when confirming the appointment.

**Risk:** A patient could receive incorrect provider information.

### 2. Appointment State Inconsistency

During a rescheduling call, the agent said that the patient did not have an upcoming appointment even though the patient was trying to change an existing appointment.

**Risk:** A patient could be given incorrect information about their appointment.

### 3. Speech Overlap / Barge-In

In some conversations, the agent continued speaking or repeating a response after the patient had already started talking.

**Risk:** This makes the conversation harder to follow and can cause important information to be missed.

### 4. Provider Name Recognition

Some provider names were not handled consistently during the same conversation.

**Risk:** This can create confusion when confirming an appointment.

More details and evidence are documented in [`bug_report.md`](bug_report.md).

## Project Structure

```text
patient-voice-bot/
│
├── main.py
├── README.md
├── ARCHITECTURE.md
├── bug_report.md
├── .env.example
├── .gitignore
│
└── calls/
    ├── recordings/
    │   ├── call-01.mp3
    │   ├── call-02.mp3
    │   ├── ...
    │   └── call-10.mp3
    │
    └── transcripts/
        ├── call-01.txt
        ├── call-02.txt
        ├── ...
        └── call-10.txt
```

## Technologies

* Python
* Bland AI REST API
* Requests
* python-dotenv
* Git / GitHub

## Setup

### Requirements

* Python 3.10+
* Bland AI account
* Bland AI API key
* Phone number configured for outbound calls

### Install

Clone the repository:


git clone https://github.com/linajawad/patient-voice-bot.git
cd patient-voice-bot


Install the dependencies:


pip install -r requirements.txt


If requirements.txt is not available:


pip install requests python-dotenv


## Environment Variables

Create a .env file in the project folder.


BLAND_API_KEY=your_api_key
BLAND_FROM_NUMBER=your_bland_phone_number
TEST_NUMBER=your_test_number


Do not commit your real API key or .env file to GitHub.

A .env.example file is included as a reference.

## Running the Bot

Run:


python main.py


Before running a new test, update the scenario information in `main.py`.

The bot then:

1. Starts the phone call.
2. Waits for the conversation to finish.
3. Retrieves the call information.
4. Saves the transcript.
5. Saves the recording when available.

## QA Evidence

The project includes transcripts and recordings from the completed test calls.

I reviewed the conversations and used them as evidence when documenting the bugs found during testing.

The bug details are available in [bug_report.md](bug_report.md).

## Security

API credentials are stored in .env and are excluded from Git.

The repository includes .env.example without real credentials.

The call recordings included in this repository were reviewed before being shared.

## Why I Built This

I wanted to build something that goes beyond making an API call.

This project gave me hands-on practice with:

* Python automation
* REST APIs
* Phone-based AI testing
* Scenario-based testing
* Reading real conversation transcripts
* Finding and documenting bugs
* Using Git and GitHub

The most important part for me was learning how to test an AI system from the **patient's point of view** and turn what I observed into clear, reproducible QA findings.
