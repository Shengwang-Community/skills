# Skill Evaluation Cases

Evaluation-driven iteration. Run these cases to regression-test after every skill change.

## Evaluation Method

For each case:
1. Send "User Input" to the model (with skills loaded)
2. Check if model behavior matches "Expected Behavior"
3. Mark PASS / FAIL
4. Failed cases drive skill modifications

---

## 1. Routing Accuracy (SKILL.md → Product Module)

### R-01: Vague request triggers clarification before routing

- User Input: "I want to build an AI customer service bot"
- Expected Behavior: Use SKILL.md routing aids to infer ConvoAI + RTC SDK, or ask one clarifying question
- Pass Criteria: Model does not generate code directly; asks for details or outputs routing recap first
- Result: ___

### R-02: Product name alone does not skip ConvoAI internal intake

- User Input: "Help me integrate ConvoAI"
- Expected Behavior: Route to ConvoAI module, enter ConvoAI quickstart and ask for all missing blocking fields in one consolidated message
- Pass Criteria: Model does not generate /join code directly; it shows the missing questions plus available options/defaults in one reply
- Result: ___

### R-03: Specific operation routes directly

- User Input: "Stop agent agent_abc12345"
- Expected Behavior: Route directly to ConvoAI module, generate /leave call
- Pass Criteria: Model routes directly without asking clarifying questions
- Result: ___

### R-04: Error query routes directly

- User Input: "ConvoAI returned 403, what does it mean"
- Expected Behavior: Route directly to convoai/common-errors.md
- Pass Criteria: Model provides the three causes of 403 and their fixes
- Result: ___

### R-05: Multi-product request triggers routing clarification

- User Input: "I want video calling plus an AI assistant"
- Expected Behavior: Identify RTC + ConvoAI combination using SKILL.md common combinations table
- Pass Criteria: Model outputs a multi-product needs analysis and, if ConvoAI is primary, reminds the user that the client still needs RTC SDK
- Result: ___

### R-06: Token request routes directly

- User Input: "Generate an RTC token in Go"
- Expected Behavior: Route directly to token-server
- Pass Criteria: Model generates Go token code without asking clarifying questions
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

- User Input: (after ConvoAI quickstart) "Create a ConvoAI agent in Python"
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

### C-07: Existing pipeline ID keeps the sample config style and removes provider-only config

- User Input: (after the pipeline-ID path resolves) "Implement the selected sample with my existing pipeline ID"
- Expected Behavior: Reuse the matching sample structure, keep the sample's config style for `SHENGWANG_PIPELINE_ID`, and remove stale `ASR` / `LLM` / `TTS` config when pipeline mode replaces the old request path
- Pass Criteria: Generated code/config reads `SHENGWANG_PIPELINE_ID` using the sample's config style and does not keep unused provider-only config in the replaced flow
- Result: ___

### C-08: Pipeline request code matches the fixed request shape

- User Input: (after the pipeline-ID path resolves) "Generate the request code for my selected platform"
- Expected Behavior: Generate platform-specific request code that preserves the fixed pipeline request shape: `POST /projects/{appId}/join/`, `Authorization: agora token=...`, and JSON body fields `name`, `pipeline_id`, `properties.agent_rtc_uid`, `properties.channel`, `properties.remote_rtc_uids`, and `properties.token`
- Pass Criteria: The generated request code uses the fixed request shape, reads `pipeline_id` from the sample's config style, sets `name = channel`, generates separate RTC tokens for the header and `properties.token` via the sample's existing token rules, and does not hardcode literal token values from the request example
- Result: ___

### C-09: Pipeline response parsing and Web proxy behavior are preserved

- User Input: (after the pipeline-ID path resolves) "Implement the Web pipeline path"
- Expected Behavior: Keep a thin server proxy for Web, execute the pipeline join request there, and parse the success response fields `agent_id`, `create_ts`, and `status`
- Pass Criteria: The Web path does not expose the pipeline join request tokens in frontend code, discovers the current server request path from the sample before editing it, and keeps the three response fields available after the request succeeds
- Result: ___

### C-10: Native pipeline adaptation stays close to the sample

- User Input: (after the pipeline-ID path resolves and the user selects Android) "Implement the Android pipeline path"
- Expected Behavior: Reuse the native sample subdirectory, replace only the provider-based request/config path, keep the existing token-generation path, and preserve the rest of the sample structure
- Pass Criteria: The generated Android flow keeps the sample app structure intact, inspects config/request/token files before UI files, adds `SHENGWANG_PIPELINE_ID` through the sample's existing config path, uses separate RTC tokens for header and agent, removes stale provider config, and parses `agent_id`, `create_ts`, and `status`
- Result: ___

### C-11: Normal implementation does not ask the user to paste pipeline ID or curl

- User Input: (after the pipeline-ID path resolves) "Implement the iOS pipeline path"
- Expected Behavior: Use the fixed pipeline request shape from the skill, add `SHENGWANG_PIPELINE_ID` as config placeholder, and continue implementation without asking the user to paste the live pipeline ID value or the curl again
- Pass Criteria: The model does not ask for the actual pipeline ID value or the pipeline curl during normal code generation
- Result: ___

### C-12: Platform config stays close to the sample style

- User Input: (after the pipeline-ID path resolves) "Implement the selected pipeline path"
- Expected Behavior: Keep the selected sample's config style, remove stale provider config, and add `SHENGWANG_PIPELINE_ID` as a placeholder without inventing a new config system
- Pass Criteria: The generated platform config stays close to the sample's style, does not add unnecessary config-loading layers, does not treat config key names as literal runtime values, and does not introduce extra computed properties or helper wrappers just to read `SHENGWANG_PIPELINE_ID` unless the sample already used them
- Result: ___

### C-13: Code generation stops before dependency installation

- User Input: (after the pipeline-ID path resolves) "Implement the iOS pipeline path"
- Expected Behavior: Finish code generation and file edits, then tell the user to run `pod install` themselves if needed, instead of executing it automatically
- Pass Criteria: The model does not run dependency installation commands such as `pod install`, `bun install`, or `pip install` unless the user explicitly asked for them
- Result: ___

---

## 3. ConvoAI Quickstart Intake Quality

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

### I-03: Partially specified request stays focused

- User Input: "Integrate ConvoAI, use deepseek, Python backend"
- Expected Behavior: Ask only for the remaining missing fields in one consolidated message
- Pass Criteria: Does not ask Q1/Q2/Q3 one by one; still shows unresolved defaultable questions in the same prompt, marks platform/backend/provider defaults as optional, and expects a sparse one-line numeric reply
- Result: ___

### I-04: Full checklist when little is known

- User Input: "Integrate ConvoAI in Python"
- Expected Behavior: Produce one consolidated ConvoAI checklist covering the missing kickoff and provider fields
- Pass Criteria: Stays focused on platform/backend/provider choices, lists unresolved platform/backend/LLM/TTS/ASR/language questions as optional, and includes a sparse example such as `5A 6A`
- Result: ___

### I-05: Structured spec after one reply

- User Input: "ConvoAI for a Web voice assistant, Python backend, use defaults"
- Expected Behavior: Normalize the answer into a single ConvoAI spec and continue
- Pass Criteria: Outputs the structured spec with only quickstart-scoped fields, and omitted optional fields become `default applied`
- Result: ___

### I-06: Numeric reply parses correctly

- User Input: "5A 6A"
- Expected Behavior: Parse the numeric reply against the current prompt and normalize it into the ConvoAI spec
- Pass Criteria: Accepts sparse numeric codes and applies defaults to omitted optional questions, including platform and backend when omitted
- Result: ___

### I-07: Other-option follow-up is narrow

- User Input: "4C 5A 6A"
- Expected Behavior: Ask only for the custom language value after parsing the rest of the codes
- Pass Criteria: Does not reopen already-resolved fields
- Result: ___

### I-08: Out-of-scope setup statement does not derail quickstart intake

- User Input: "1A 2E 3G 4C 5A 6A 7A, and I'll handle setup later"
- Expected Behavior: Keep the quickstart intake focused on product choices and ignore extra out-of-scope statements
- Pass Criteria: Does not introduce any new non-quickstart question as part of the intake
- Result: ___

### I-09: Default-provider prompt includes the Pipeline ID option

- User Input: After the prerequisite prompt, the user replies "A"
- Expected Behavior: Show the default-provider prompt with three options: defaults / custom providers / Pipeline ID
- Pass Criteria: The next turn is the default-provider prompt, it includes the `C` option for Shengwang Pipeline ID, and the Studio URL is shown with that option
- Result: ___

### I-10: Choosing the Pipeline option exits the provider path

- User Input: After the default-provider prompt, the user replies "C"
- Expected Behavior: Stop the provider path and, only if platform is still unknown, ask a platform-only checklist using the same style as the Detailed Provider Checklist
- Pass Criteria: After the user picks `C`, the model does not show the full provider checklist; it continues into the pipeline path and only asks for platform if still unresolved
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
