
# Patient Voice Bot - AI Phone Agent Assessor

An automated Python voice bot built to evaluate, stress-test, and identify quality issues and bugs in an AI-powered healthcare phone agent.

The bot acts as a realistic patient, makes automated phone calls through the Bland AI API, retrieves completed call data, and saves transcripts and available recordings locally for QA analysis.

## Features

* **Scenario Automation:** Programmatically triggers realistic patient phone calls through the Bland AI API.
* **Automated Call Tracking:** Waits for calls to complete and retrieves final call metadata.
* **Transcript Archiving:** Automatically saves completed call transcripts to `calls/transcripts/`.
* **Recording Archiving:** Automatically downloads available call recordings to `calls/recordings/`.
* **Scenario-Based Testing:** Tests realistic patient workflows including scheduling, cancellation, rescheduling, medication refills, insurance questions, and appointment-type questions.
* **QA Analysis:** Uses real call transcripts to identify functional, conversational, and state-consistency issues.
* **Bug Documentation:** Records confirmed issues and expected behavior in `bug_report.md`.

## Architecture

```text
Patient Voice Bot
       |
       v
Python Test Scenario
       |
       v
Bland AI REST API
       |
       v
Automated Phone Call
       |
       v
Target AI Voice Agent
       |
       v
Call Completion
       |
       +-------------------+
       |                   |
       v                   v
   Transcript          Recording
       |                   |
       v                   v
calls/transcripts/   calls/recordings/
       |                   |
       +---------+---------+
                 |
                 v
             QA Review
                 |
                 v
           Bug Report
```

See [`ARCHITECTURE.md`](ARCHITECTURE.md) for the detailed system architecture and technical decisions.

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
    │   └── call recordings
    │
    └── transcripts/
        ├── call-01.txt
        ├── call-02.txt
        ├── call-03.txt
        ├── ...
        └── call-10.txt
```

## Prerequisites

* Python 3.10+
* A Bland AI account
* A Bland AI API key
* A phone number configured for outbound calling

## Installation

Clone the repository:

```bash
git clone https://github.com/linajawad/patient-voice-bot.git
cd patient-voice-bot
```

Install dependencies:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not present, install the required packages:

```bash
pip install requests python-dotenv
```

## Environment Variables

Create a `.env` file in the project root:

```text
BLAND_API_KEY=your_bland_api_key
BLAND_FROM_NUMBER=your_bland_phone_number
TEST_NUMBER=target_test_phone_number
```

Never commit your real `.env` file or API key to GitHub.

A `.env.example` file is included as a configuration reference.

## Running the Bot

The main test runner is:

```bash
python main.py
```

Before starting a new scenario, update:

```python
CALL_NUMBER = 11
SCENARIO_NAME = "Your Scenario Name"
```

and replace the `SCENARIO` text with the desired patient behavior.

The script then:

1. Sends the outbound call.
2. Receives the Bland AI call ID.
3. Waits for the conversation to finish.
4. Retrieves the completed call.
5. Saves the transcript automatically.
6. Attempts to download the recording.
7. Reports the final result.

## Call Evidence

The project contains archived transcripts from multiple test scenarios.

These calls were used to evaluate:

* Appointment scheduling
* Appointment cancellation
* Appointment rescheduling
* Medication refill requests
* Insurance questions
* Clinic information requests
* Appointment-type questions
* Provider preferences
* Appointment confirmation
* Patient support escalation

The transcripts provide evidence for the QA findings documented in `bug_report.md`.

## Key Findings

Testing produced several real-world issues in the target AI phone agent.

### 1. Provider Identity Inconsistency

The agent provided one provider name during appointment availability and a different provider name during final confirmation.

**Impact:** Patients could receive incorrect provider information after booking.

**Severity:** Medium

### 2. Speech Overlap and Barge-In Handling

During appointment scheduling, the agent continued repeating a response after the patient interrupted, creating overlapping and repetitive conversation.

**Impact:** Reduces conversation quality and can make the agent difficult to interact with.

**Severity:** Medium

### 3. Appointment State Inconsistency

During a rescheduling scenario, the patient stated that an appointment already existed, but the agent reported that no upcoming appointment was found and redirected the conversation toward creating a new appointment.

**Impact:** Could cause patients to incorrectly believe their appointment does not exist.

**Severity:** Medium

## QA Approach

The project treats each phone conversation as a QA test case.

The goal is not simply to determine whether a call succeeds. Each conversation is reviewed for:

* Functional correctness
* State consistency
* Provider identity consistency
* Appointment date and time accuracy
* Conversation flow
* Interruption handling
* Repeated responses
* Incorrect confirmations
* Escalation behavior
* Patient experience

Findings are documented only when there is evidence in the actual conversation transcript.

## Bug Reporting

Confirmed issues are documented in:

```text
bug_report.md
```

Each report includes:

* Bug description
* Severity
* Test call
* Evidence
* Expected behavior
* Potential impact

## Technology Stack

| Component       | Technology                      |
| --------------- | ------------------------------- |
| Language        | Python                          |
| Telephony API   | Bland AI REST API               |
| HTTP Client     | Requests                        |
| Configuration   | python-dotenv                   |
| Testing         | Scenario-based voice QA         |
| Evidence        | Call transcripts and recordings |
| Version Control | Git / GitHub                    |
| Documentation   | Markdown                        |

## Security

Sensitive credentials are stored in `.env` and excluded from version control.

The repository uses `.env.example` to show the required configuration without exposing the actual API key.

Call recordings and other potentially sensitive artifacts should not be committed to a public repository unless they have been reviewed and are safe to share.

# Patient Voice Bot 🤖📞

An automated Python voice-testing bot built to evaluate, stress-test, and identify quality issues in an AI healthcare phone agent.

The bot acts as a realistic patient, places automated phone calls through the Bland AI API, retrieves the resulting conversations, and stores transcripts and recordings locally for QA analysis.

## What I Built

This project combines:

* Python automation
* REST API integration
* AI voice-agent testing
* Scenario-based QA
* Conversation analysis
* Bug documentation
* Local test artifact storage

The goal is not simply to make a phone call. The goal is to **test how reliably an AI agent handles realistic patient interactions and edge cases.**

## How It Works

```text
Patient Scenario
      ↓
Python Test Bot
      ↓
Bland AI Telephony API
      ↓
AI Healthcare Agent
      ↓
Phone Conversation
      ↓
Call Completion
      ↓
Python Retrieves Call Data
      ↓
Transcript + Recording
      ↓
Local QA Evidence
      ↓
Bug Report
```

## Test Scenarios

The project includes 10 completed patient scenarios covering workflows such as:

1. Appointment scheduling
2. General clinic questions
3. Appointment cancellation
4. Medication refill request
5. Insurance questions
6. Appointment confirmation
7. Provider selection
8. Appointment cancellation verification
9. Appointment rescheduling
10. New-patient vs. regular office visit

Each scenario is designed to test a specific patient workflow rather than simply generate a successful call.

## QA Findings

During testing, I identified issues including:

### Provider Identity Inconsistency

The agent presented one provider during appointment availability and a different provider during final confirmation.

**Risk:** A patient could receive incorrect appointment information.

### Appointment State Inconsistency

During a rescheduling scenario, the agent reported that the patient had no upcoming appointment even though the patient was calling specifically to modify an existing appointment.

**Risk:** The patient may be unable to correctly manage an existing appointment.

### Speech Overlap / Barge-In Handling

The agent sometimes continued repeating portions of a response after the patient had already started speaking.

**Risk:** Important information can be missed and the conversation feels unnatural.

### Provider Name Recognition

Provider names were sometimes pronounced or represented inconsistently during the same conversation.

**Risk:** This can contribute to confusion during appointment confirmation.

More details are documented in [`bug_report.md`](bug_report.md).

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
    │   └── call recordings
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

## Technical Architecture

The system uses Python as the orchestration layer and communicates with the Bland AI REST API.

The bot is responsible for:

1. Loading configuration from environment variables.
2. Sending structured patient scenarios to the telephony API.
3. Initiating outbound test calls.
4. Waiting for call completion.
5. Retrieving call metadata and transcripts.
6. Saving transcripts locally.
7. Attempting to download call recordings.
8. Organizing test evidence for QA review.

See [`ARCHITECTURE.md`](ARCHITECTURE.md) for the technical design and trade-offs.

## Setup

### Requirements

* Python 3.10+
* Bland AI API key
* A phone number configured for outbound calling

### Install Dependencies

```bash
pip install requests python-dotenv
```

### Environment Variables

Create a `.env` file based on `.env.example`.

```env
BLAND_API_KEY=your_api_key
BLAND_FROM_NUMBER=your_bland_phone_number
TEST_NUMBER=your_test_number
```

**Never commit your real `.env` file or API keys to GitHub.**

## Run the Test Bot

```bash
python main.py
```

The bot will:

* Start the configured patient scenario.
* Place the test call.
* Wait for completion.
* Retrieve the transcript.
* Save the transcript under `calls/transcripts/`.
* Attempt to save the recording under `calls/recordings/`.

## QA Evidence

The repository contains locally archived transcripts from the completed test scenarios.

These transcripts were used as evidence when documenting the observed bugs and conversational issues.

## Why This Project Matters

This project demonstrates practical experience with more than API usage.

It shows how I approached an AI system as a **QA engineer and tester**:

* I designed realistic user scenarios.
* I tested multi-step workflows.
* I looked for state inconsistencies.
* I evaluated conversational behavior.
* I documented reproducible bugs.
* I preserved test evidence.
* I automated the collection of call results.

The project focuses on finding issues that may not be visible when evaluating an AI agent based only on whether a call technically succeeds.

## Future Improvements

Potential next steps include:

* Automated regression testing
* Structured JSON test results
* Automatic bug classification
* Response-quality scoring
* Provider/date/time consistency checks
* Automatic detection of speech overlap
* CI-based test reporting
* Dashboard for test results and trends
