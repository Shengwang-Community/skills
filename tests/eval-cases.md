# Skill Evaluation Cases

Evaluation-driven iteration. Run these cases to regression-test after every skill change.

## Evaluation Method

For each case:
1. Send "User Input" to the model (with skills loaded)
2. Check if model behavior matches "Expected Behavior"
3. Mark PASS / FAIL
4. Failed cases drive skill modifications

---

## 1. Routing Accuracy (Root Router → Intake / Product Module)

### R-01: Vague request must go through intake

- User Input: "I want to build an AI customer service bot"
- Expected Behavior: Enter intake flow, analyze needs, recommend ConvoAI + RTC SDK
- Pass Criteria: Model does not generate code directly; asks for details or outputs needs analysis first
- Result: ___

### R-02: Product name alone does not skip intake

- User Input: "Help me integrate ConvoAI"
- Expected Behavior: Enter ConvoAI intake and ask for all missing blocking fields in one consolidated message
- Pass Criteria: Model does not generate /join code directly; it shows the missing questions plus available options/defaults in one reply
- Result: ___

### R-03: Specific operation skips intake

- User Input: "Stop agent agent_abc12345"
- Expected Behavior: Route directly to ConvoAI module, generate /leave call
- Pass Criteria: Model does not go through intake flow; executes operation directly
- Result: ___

### R-04: Error query skips intake

- User Input: "ConvoAI returned 403, what does it mean"
- Expected Behavior: Route directly to convoai/common-errors.md
- Pass Criteria: Model provides the three causes of 403 and their fixes
- Result: ___

### R-05: Multi-product request goes through intake

- User Input: "I want video calling plus an AI assistant"
- Expected Behavior: Enter intake, identify RTC + ConvoAI combination
- Pass Criteria: Model outputs a multi-product needs analysis and, if ConvoAI is primary, reminds the user that the client still needs RTC SDK
- Result: ___

### R-06: Token request routes directly

- User Input: "Generate an RTC token in Go"
- Expected Behavior: Route directly to token-server
- Pass Criteria: Model generates Go token code without going through intake
- Result: ___

### R-07: RTC request routes to RTC module

- User Input: "How do I implement a video call on Web"
- Expected Behavior: Route to rtc, fetch Web quick start doc
- Pass Criteria: Model provides integration guidance based on RTC Web SDK
- Result: ___

### R-08: Download request routes directly

- User Input: "Download ConvoAI Go SDK"
- Expected Behavior: Route to relevant product module, provide correct URL
- Pass Criteria: Model provides correct URL or runs git clone
- Result: ___

---

## 2. ConvoAI Code Generation Quality

### C-01: agent_rtc_uid type is correct

- User Input: (after intake) "Create a ConvoAI agent in Python"
- Expected Behavior: Generated code has `agent_rtc_uid` as string `"0"`
- Pass Criteria: Not int `0`
- Result: ___

### C-02: remote_rtc_uids type is correct

- User Input: Same as above
- Expected Behavior: Generated code has `remote_rtc_uids` as `["*"]`
- Pass Criteria: Not string `"*"`
- Result: ___

### C-03: Agent name uniqueness

- User Input: Same as above
- Expected Behavior: Agent `name` includes a random suffix (e.g. `agent_{uuid[:8]}`)
- Pass Criteria: Not a fixed string like `"my_agent"`
- Result: ___

### C-04: Credentials not hardcoded

- User Input: Same as above
- Expected Behavior: AppID, Customer Key/Secret read from environment variables
- Pass Criteria: No hardcoded credential values in code
- Result: ___

### C-05: 409 error handling

- User Input: "Got 409 when creating an agent, what should I do"
- Expected Behavior: Suggest extracting existing agent_id or generating a new name and retrying
- Pass Criteria: Provides both solutions
- Result: ___

### C-06: Doc fetching

- User Input: "Integrate ConvoAI in Go"
- Expected Behavior: Model fetches Go quick start doc URL
- Pass Criteria: Fetches content by running `bash skills/voice-ai-integration/scripts/fetch-doc-content.sh "docs://default/convoai/restful/get-started/quick-start-go"`
- Result: ___

---

## 3. Intake Needs Analysis Quality

### I-01: Correct product combination identification

- User Input: "I want to build an online education platform where teachers and students have video classes, with session replay afterwards"
- Expected Behavior: Identify RTC SDK (video) + Cloud Recording (replay)
- Pass Criteria: Needs analysis output includes both products
- Result: ___

### I-02: ConvoAI depends on RTC reminder

- User Input: "I want to build an AI voice assistant"
- Expected Behavior: Identify ConvoAI (primary) + RTC SDK (client-side companion)
- Pass Criteria: Explicitly tells user that client side needs RTC SDK
- Result: ___

### I-03: Fast-path triggers correctly

- User Input: "Integrate ConvoAI, I have credentials, use deepseek, Python backend"
- Expected Behavior: Ask only for the remaining missing fields in one consolidated message
- Pass Criteria: Does not ask Q1/Q2/Q3 one by one; includes explicit options/defaults for the unresolved fields only
- Result: ___

### I-04: Full checklist when little is known

- User Input: "Integrate ConvoAI in Python"
- Expected Behavior: Produce one consolidated ConvoAI checklist covering the missing kickoff and provider fields
- Pass Criteria: Shows credentials, App Certificate, ASR, ASR language, LLM, and TTS options in one reply rather than separate turns
- Result: ___

### I-05: Structured spec after one reply

- User Input: "ConvoAI for a Web voice assistant, Python backend, credentials ready, App Certificate off, use defaults"
- Expected Behavior: Normalize the answer into a single ConvoAI spec and continue
- Pass Criteria: Outputs the structured spec without asking another confirmation question
- Result: ___

---

## 4. Failure Path Coverage

### F-01: Download failure

- User Input: "Download https://github.com/AgoraIO/nonexistent-repo"
- Expected Behavior: Report download failure, suggest checking URL
- Pass Criteria: Does not fail silently or fabricate content
- Result: ___

### F-02: Doc fetch unavailable fallback

- Scenario: HTTP doc fetch fails
- User Input: "Integrate ConvoAI in Python"
- Expected Behavior: Use Generation Rules + fallback URL to generate code, prompt user to verify
- Pass Criteria: Informs user doc fetch failed, provides fallback URL
- Result: ___

### F-03: Missing credentials guidance

- User Input: "Create a ConvoAI agent" (no .env file)
- Expected Behavior: Detect missing credentials, guide to credentials-and-auth.md
- Pass Criteria: Does not generate code with placeholder credentials
- Result: ___

---

## Evaluation Log

| Date | Version | Pass | Fail | Failed Cases | Fix Actions |
|------|---------|------|------|-------------|-------------|
| | | | | | |
