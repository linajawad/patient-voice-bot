
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

## Limitations

* Recording availability depends on the telephony provider.
* Some recordings may return an unavailable response even after the call completes.
* Some QA findings still require human review.
* The current test runner executes scenarios sequentially.

## Future Improvements

Potential improvements include:

* JSON/YAML-based scenario configuration
* Batch scenario execution
* Automated regression testing
* Structured transcript parsing
* Automatic provider-name consistency checks
* Appointment date/time validation
* Automated bug classification
* HTML QA reports
* Dashboard-based test results
* CI/CD integration
* Expected-vs-observed behavior comparison

## Project Goal

The goal of this project is to demonstrate how an AI-powered voice agent can be tested systematically using realistic patient scenarios, automated phone calls, locally archived evidence, and structured QA analysis.

Rather than building only a voice bot, this project focuses on **testing the reliability, consistency, and real-world behavior of AI voice agents**.
