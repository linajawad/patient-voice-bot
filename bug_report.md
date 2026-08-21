# AI Voice Agent QA Bug Report

This document contains issues I found while testing the AI healthcare phone agent.

I tested the agent using 10 patient scenarios and reviewed the call transcripts and recordings to confirm the issues.

---

## Bug 1: Provider Name Changes During Appointment Confirmation

**Severity:** Medium  
**Category:** Data Consistency  
**Test Call:** call-01

### Description

The agent gave one provider name when discussing available appointments, but a different provider name during the final appointment confirmation.

### Expected Behavior

The provider name should remain the same throughout the conversation and during final confirmation.

### Actual Behavior

The provider name changed during the appointment confirmation.

### Impact

A patient could receive incorrect information about which provider they are scheduled to see.

### Evidence

The call transcript shows that the provider name changed between the appointment availability discussion and the final confirmation.

**Evidence:** `calls/transcripts/call-01.txt`

---

## Bug 2: Existing Appointment Not Found During Rescheduling

**Severity:** Medium  
**Category:** Appointment State  
**Test Call:** call-09

### Description

During a rescheduling conversation, the patient was trying to change an existing appointment, but the agent said there was no upcoming appointment.

### Expected Behavior

The agent should correctly identify the patient's existing appointment and allow the patient to reschedule it.

### Actual Behavior

The agent reported that no upcoming appointment was found and moved the conversation toward creating a new appointment.

### Impact

A patient could incorrectly believe that their appointment does not exist or could accidentally create a duplicate appointment.

### Evidence

The call transcript shows that the agent reported no upcoming appointment during a rescheduling request.

**Evidence:** `calls/transcripts/call-09.txt`

---

## Bug 3: Agent Continues Speaking After Patient Interrupts

**Severity:** Medium  
**Category:** Conversational Quality  
**Test Call:** call-02

### Description

The agent sometimes continued speaking or repeated part of its response after the patient had already started talking.

### Expected Behavior

The agent should recognize the interruption and stop speaking so the patient can continue.

### Actual Behavior

The agent continued speaking after the patient started talking.

### Impact

This makes the conversation harder to follow and can cause important information to be missed.

### Evidence

The call recording and transcript show the agent continuing its response after the patient began speaking.

**Evidence:** `calls/transcripts/call-02.txt`

---

## Bug 4: Provider Name Is Not Handled Consistently

**Severity:** Low  
**Category:** Speech Recognition  
**Test Call:** call-01

### Description

A provider's name was handled inconsistently during the same conversation.

### Expected Behavior

The provider name should be recognized and presented consistently throughout the call.

### Actual Behavior

The provider name was represented or pronounced differently during the conversation.

### Impact

This can create confusion when the patient is confirming an appointment.

### Evidence

The call transcript shows inconsistent handling of the provider's name during the same conversation.

**Evidence:** `calls/transcripts/call-01.txt`

---

## Testing Summary

| Item | Result |
|------|--------|
| Patient scenarios tested | 10 |
| Calls completed | 10 |
| Bugs identified | 4 |
| Evidence reviewed | Transcripts and recordings |

---

## Severity

- **High:** Could cause significant patient or appointment-related risk.
- **Medium:** Could cause incorrect workflow behavior or patient confusion.
- **Low:** Mainly affects usability or conversation quality.

---

## QA Approach

Each phone conversation was treated as a separate test case.

For each scenario, I reviewed the conversation for:

- Accuracy
- Appointment state consistency
- Provider information
- Conversation flow
- Interruption handling
- Patient experience

I only documented issues that I could confirm from the actual test conversations.

---

## Notes

These bugs were documented based on actual test conversations and supporting transcripts or recordings.

The goal of this testing was not only to check whether the call completed successfully, but also to evaluate how reliably the AI agent handled realistic patient interactions.