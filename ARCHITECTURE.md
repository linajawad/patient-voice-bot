# System Architecture & Technical Decisions

### Architecture Overview
The Patient Voice Bot is built as a lightweight Python orchestration layer that interfaces with Bland AI's REST Telephony API. Instead of implementing low-level WebSockets, WebRTC, or Realtime Audio Pipelines from scratch, the system uses Python to define structured test scenarios, issue automated outbound calls to the target clinic (+1-805-439-8008), and fetch post-call execution metadata including multi-turn transcripts and summaries.

### Design Choices & Trade-offs
* **Telephony Orchestration over Custom WebSockets:** Utilizing an API-first voice platform drastically reduced system complexity, handling SIP trunking, turn-taking latency, and speech-to-text-to-speech pipelines natively.
* **Programmatic Retrieval & Local Archiving:** By querying Bland's `/v1/calls` endpoints via Python, the system automatically pulls call transcripts and builds structured artifacts for evaluation without manual UI overhead or redundant API charges.
