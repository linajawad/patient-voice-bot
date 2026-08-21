# System Architecture & Technical Decisions

## 1. Overview

The Patient Voice Bot is a lightweight Python-based QA automation system designed to test and evaluate AI-powered healthcare phone agents.

The system acts as a simulated patient. It sends predefined patient scenarios to a telephony API, initiates outbound calls to the target AI agent, retrieves the completed call data, and stores the resulting transcripts and recordings for analysis.

The architecture intentionally uses an API-first approach rather than implementing telephony infrastructure, SIP, WebRTC, or real-time audio processing from scratch.

---

## 2. High-Level Architecture

```text
                    Patient Voice Bot
                           |
                           v
                     Python / main.py
                           |
                           v
                  Scenario Definition
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
             +-------------+-------------+
             |                           |
             v                           v
      Call Transcript               Call Recording
             |                           |
             v                           v
   calls/transcripts/          calls/recordings/
             |                           |
             +-------------+-------------+
                           |
                           v
                    QA / Bug Analysis
                           |
                           v
                  bug_report.md
```

---

## 3. Core Components

### `main.py`

The main orchestration layer.

Its responsibilities include:

1. Loading environment variables
2. Loading the Bland AI API key
3. Defining the patient testing scenario
4. Initiating an outbound call
5. Tracking the call ID
6. Waiting for the call to complete
7. Retrieving call details
8. Extracting the conversation transcript
9. Saving the transcript locally
10. Attempting to download the call recording
11. Saving available recordings locally
12. Reporting the result to the tester

The script is designed to make repeated test calls without requiring manual transcript copying.

---

## 4. Test Scenario Layer

Each automated call represents a realistic patient scenario.

Examples include:

* Appointment scheduling
* Appointment cancellation
* Appointment rescheduling
* Medication refill requests
* Insurance questions
* General clinic information
* New-patient vs. established-patient questions
* Provider preference testing
* Appointment confirmation testing

The scenarios are intentionally designed to test both normal workflows and edge cases.

---

## 5. Telephony Layer

Bland AI provides the telephony infrastructure used by the project.

The Patient Voice Bot communicates with the service through its REST API rather than directly managing:

* SIP
* Phone carrier infrastructure
* WebRTC
* Audio codecs
* Speech-to-text
* Text-to-speech
* Call routing

This significantly reduces implementation complexity and allows the project to focus on **AI agent quality assurance rather than telephony infrastructure**.

---

## 6. Call Lifecycle

A typical test follows this lifecycle:

```text
1. Define patient scenario
          |
          v
2. Submit outbound call
          |
          v
3. Receive call ID
          |
          v
4. Wait for completion
          |
          v
5. Retrieve call details
          |
          v
6. Extract transcript
          |
          v
7. Save transcript locally
          |
          v
8. Retrieve recording URL
          |
          v
9. Download recording when available
          |
          v
10. Review conversation
          |
          v
11. Document bugs
```

If a recording is temporarily unavailable through the API, the transcript can still be preserved. The recording may then be downloaded manually from the provider dashboard when available.

---

## 7. Local Artifact Storage

Test artifacts are organized by type:

```text
calls/
├── recordings/
│   ├── call-01.*
│   ├── call-02.*
│   └── ...
│
└── transcripts/
    ├── call-01.txt
    ├── call-02.txt
    ├── call-03.txt
    └── ...
```

This separation makes it easier to review individual conversations and associate audio evidence with transcript evidence.

---

## 8. QA and Bug Analysis

The project does not stop after making a successful phone call.

Each completed conversation is treated as a QA test case.

The transcript is reviewed for:

* Incorrect information
* Provider identity changes
* Appointment state inconsistencies
* Incorrect dates or times
* Unexpected workflow changes
* Unnecessary patient verification
* Conversation loops
* Repeated responses
* Speech overlap
* Poor interruption handling
* Incorrect confirmations
* Failure to escalate appropriately

Confirmed issues are documented in:

```text
bug_report.md
```

Each bug includes:

* Severity
* Test call
* Evidence
* Description
* Expected behavior
* Impact
* Recommendation

---

## 9. Design Decisions

### API-First Telephony

Instead of implementing a custom phone system, the project uses Bland AI's API.

**Reason:**

This allows the project to focus engineering effort on AI agent testing and QA rather than low-level telephony infrastructure.

---

### Local Evidence Storage

Transcripts and available recordings are stored locally.

**Reason:**

Local artifacts make test results reproducible and provide evidence when documenting bugs.

---

### Scenario-Based Testing

Calls are based on explicit patient scenarios rather than random conversations.

**Reason:**

Structured scenarios make results easier to compare and reproduce across multiple test runs.

---

### Separation of Testing and Analysis

The system separates call execution from bug documentation.

```text
Call Execution
      |
      v
Evidence Collection
      |
      v
Human QA Review
      |
      v
Bug Report
```

This prevents assumptions about whether a behavior is actually a bug until the conversation has been reviewed.

---

## 10. Security Considerations

Sensitive credentials are stored in `.env` and are not committed to GitHub.

The repository uses `.env.example` to document required configuration without exposing the real API key.

Generated call recordings are also excluded from version control because they may contain sensitive conversational data and large binary files.

---

## 11. Trade-Offs

### Advantages

* Simple architecture
* Fast to develop
* Easy to reproduce test scenarios
* Minimal infrastructure
* Real phone-call testing
* Automatic transcript collection
* Easy evidence organization

### Limitations

* Depends on the external telephony provider
* Recording availability may depend on the provider API
* Some call behavior must still be evaluated manually
* The current system is primarily sequential rather than a distributed test runner

---

## 12. Future Improvements

Potential future improvements include:

* Automated scenario configuration using JSON or YAML
* Batch test execution
* Automatic call status polling
* Structured transcript parsing
* Automatic detection of provider-name mismatches
* Appointment date/time consistency checks
* Automated bug severity classification
* Regression testing across agent versions
* HTML or dashboard-based QA reports
* CI/CD integration
* Automated comparison of expected vs. observed agent behavior

---

## 13. Technology Stack

| Component       | Technology                   |
| --------------- | ---------------------------- |
| Language        | Python                       |
| Telephony API   | Bland AI REST API            |
| HTTP Client     | Requests                     |
| Configuration   | python-dotenv                |
| Testing Method  | Scenario-based voice testing |
| Evidence        | Transcripts + recordings     |
| Version Control | Git / GitHub                 |
| Documentation   | Markdown                     |

---

## 14. Architecture Summary

The Patient Voice Bot follows a simple orchestration architecture:

```text
Scenario
   ↓
Python
   ↓
Bland AI
   ↓
Phone Call
   ↓
AI Agent
   ↓
Transcript / Recording
   ↓
QA Analysis
   ↓
Bug Report
```

The key architectural goal is to turn real AI phone conversations into **repeatable QA evidence** that can be reviewed, reproduced, and converted into actionable bug reports.
