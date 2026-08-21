# AI Voice Agent QA Bug Report

This document records functional and conversational issues identified during scenario-based testing of the AI phone agent.

Each finding is based on an observed behavior in an actual test conversation.

---

## Bug 1: Provider Identity Inconsistency During Appointment Booking

**Severity:** Medium

**Category:** Data Consistency / Appointment Booking

**Test Call:** Call #01

### Description

During the appointment scheduling flow, the agent initially presented one provider name when discussing available appointment times. During final confirmation, the provider name changed to a different provider.

### Expected Behavior

The provider identity should remain consistent from availability search through final appointment confirmation.

### Impact

A patient could believe they booked an appointment with one physician while the system confirms the appointment with another physician.

This creates a risk of incorrect appointment information and reduces trust in the scheduling system.

---

## Bug 2: Speech Overlap and Poor Barge-In Handling

**Severity:** Medium

**Category:** Conversational Quality / Voice Interaction

**Test Call:** Call #07

### Description

During the appointment scheduling flow, the patient attempted to respond while the agent was speaking. The agent continued repeating portions of its previous response instead of immediately yielding to the patient.

The conversation contained repeated fragments such as:

> "the earliest"

### Expected Behavior

When the patient begins speaking, the agent should detect the interruption, stop its current response, and continue from the patient's latest input.

### Impact

The behavior creates awkward overlapping speech and makes the agent feel less natural and less responsive.

It can also cause the patient to miss important appointment information.

---

## Bug 3: Appointment State Inconsistency During Rescheduling

**Severity:** Medium

**Category:** State Management / Appointment Scheduling

**Test Call:** Call #09

### Description

The patient called specifically to move an existing appointment to another date.

After patient verification, the agent reported that no upcoming appointment was scheduled.

The patient then explained that they wanted to keep the appointment but move it to another date. The agent continued reporting that no appointment was available and eventually treated the interaction as if the patient may have contacted the wrong office.

### Expected Behavior

If an appointment exists, the agent should retrieve the existing appointment and provide the available rescheduling options.

If the appointment cannot be found, the agent should clearly explain the discrepancy and provide an appropriate recovery path rather than repeatedly redirecting the patient toward a new appointment.

### Impact

A patient could incorrectly believe their appointment does not exist or abandon the rescheduling process.

This is particularly important because appointment state is a core part of a healthcare scheduling workflow.

---

## Bug 4: Inconsistent Provider Name Recognition and Pronunciation

**Severity:** Low

**Category:** Speech Recognition / Conversational Quality

**Test Calls:** Calls #07 and #10

### Description

Provider names were pronounced and transcribed inconsistently throughout conversations.

The same provider was represented using noticeably different pronunciations or names during different parts of the scheduling flow.

### Expected Behavior

Provider names should be consistently recognized, pronounced, and repeated throughout a single conversation.

### Impact

Inconsistent provider names can confuse patients and may contribute to provider identity errors during appointment confirmation.

---

# Additional Quality Observations

The following behaviors were observed during testing but are currently treated as quality observations rather than confirmed functional bugs.

### 1. Repeated Responses

The agent occasionally repeated parts of a response after the patient had already acknowledged the information.

### 2. Delayed Turn-Taking

Several conversations contained noticeable pauses where the patient asked:

> "Hello? Are you there?"

This suggests the agent may sometimes have delayed response timing or turn-taking issues.

### 3. Verification During Informational Requests

The agent may request patient verification even when the caller is initially asking for general clinic information such as location, hours, or insurance acceptance.

For general informational questions, unnecessary verification can add friction to the conversation.

---

# QA Methodology

The Patient Voice Bot uses realistic patient scenarios to evaluate the target AI phone agent.

Each test focuses on a specific workflow or edge case.

The testing process is:

1. Define a realistic patient scenario.
2. Generate an outbound phone call through the Bland AI API.
3. Allow the AI agent to handle the conversation.
4. Retrieve the completed call transcript.
5. Save the transcript locally.
6. Review the conversation for functional and conversational issues.
7. Document reproducible findings.
8. Compare observed behavior against expected behavior.

The goal is to evaluate more than whether a call completes successfully.

Testing focuses on:

* Functional correctness
* Appointment state consistency
* Provider identity consistency
* Date and time accuracy
* Conversation flow
* Barge-in handling
* Speech recognition
* Repeated responses
* Patient verification
* Escalation behavior
* Patient experience

---

# Severity Definitions

### High

The issue can cause incorrect medical, appointment, or patient information, prevent a critical workflow, or create significant patient risk.

### Medium

The issue can cause incorrect workflow behavior, confusion, or loss of trust but does not directly create an immediate safety risk.

### Low

The issue primarily affects usability, conversational quality, wording, or minor workflow friction.

---

# Summary

The testing identified multiple issues involving provider identity consistency, appointment state management, and conversational turn-taking.

The most important findings demonstrate that an AI phone agent can appear functional while still producing incorrect or inconsistent behavior during multi-step workflows.

This project therefore evaluates the agent using **scenario-based testing and real conversation evidence**, rather than relying only on successful call completion.
