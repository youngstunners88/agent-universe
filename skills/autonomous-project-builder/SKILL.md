---
name: autonomous-project-builder
description: Build autonomous projects (AI agents, systems, applications) with optimized file system, routing, state management, and modular architecture. Includes foundations for communication integrations, AI ensemble, network tools, quantum-enhanced concepts, testing, auditing, and iterative improvement loops. Use when you need to create self-sufficient, cooperating systems that operate continuously without human permission.
---

# Autonomous Project Builder

This skill provides a structured workflow to create a functional autonomous project that can operate across multiple communication channels, process information with advanced AI models, and continuously improve through testing and auditing.

## Phase 1: Foundations

### 1.1 File System
- Create optimized hierarchical structure with lazy loading and code splitting.
- Separate concerns: `src/`, `config/`, `logs/`, `data/`, `modules/`.
- Example structure:
  ```
  project/
  ├── src/
  │   ├── core/
  │   ├── communication/
  │   ├── ai/
  │   └── utils/
  ├── config/
  │   ├── routing.json
  │   ├── state.json
  │   └── credentials/
  ├── logs/
  ├── data/
  └── modules/
      ├── whatsapp/
      ├── gmail/
      ├── tiktok/
      ├── tts/
      └── stt/
  ```

### 1.2 Routing System
- Implement RESTful architecture with API/web/internal routes.
- Performance targets: <1ms route resolution, <50ms API response.
- Use a lightweight router (e.g., Express.js, FastAPI) or custom implementation.

### 1.3 State Management
- Adopt Redux Toolkit approach with structured state (UI/App/Domain/Server).
- Update targets: <16ms.
- Persist state to local storage or database for recovery.

## Phase 2: Communication Integrations

### 2.1 WhatsApp
- Install `whatsapp-web.js` or use official Cloud API.
- Configure session persistence.
- Implement message sending/receiving, media handling.

### 2.2 Gmail
- Use Gmail API via OAuth2.
- Enable reading, sending, drafting emails.
- Set up push notifications for new emails.

### 2.3 TikTok
- Use TikTok API (requires developer access).
- Implement video upload, comment fetching, analytics.

### 2.4 Summary Reporting
- Create a summarization module that compiles:
  - Learned information (from interactions, data processing).
  - Performed actions (API calls, messages sent).
  - Planned actions (upcoming tasks, goals).
- Deliver summaries via preferred channel (e.g., WhatsApp digest email).

## Phase 3: AI Ensemble (TTS/STT)

### 3.1 Speech-to-Text (STT)
- Integrate multiple STT engines for cost savings and accuracy:
  - Whisper (OpenAI) - high accuracy.
  - Coqui STT - open-source, offline capable.
  - Vosk - lightweight, offline.
  - Google Speech-to-Text (if API available).
- Implement fallback mechanism: try cheaper/free first, then paid for accuracy.

### 3.2 Text-to-Speech (TTS)
- Integrate multiple TTS engines:
  - Coqui TTS - high quality, open-source.
  - Bark - transformer-based, multilingual.
  - Piper - fast, lightweight.
  - MeloTTS - multilingual, efficient.
  - SpeechT5 - Microsoft's unified model.
  - ElevenLabs (if API available) - premium quality.
  - Retell AI (for conversational AI).
- Implement caching and selection based on language, latency, cost.

### 3.3 Voice Cloning (Optional)
- If user provides voice sample, integrate with ElevenLabs or Coqui for cloning.
- Store securely and use for personalized output.

## Phase 4: Network & Analysis Tools

### 4.1 MiroShark Installation
- Clone and install MiroShark:
  ```bash
  git clone https://github.com/aaronjmars/MiroShark.git
  cd MiroShark
  # Follow installation instructions (likely Node.js based)
  npm install
  ```
- Integrate packet capture and analysis into project's network monitoring module.
- Use for detecting anomalies, securing communications, and diagnosing issues.

### 4.2 Meta MMS (Multilingual Speech)
- Clone and set up MMS:
  ```bash
  git clone https://github.com/facebookresearch/fairseq.git
  cd fairseq/examples/mms
  # Install dependencies and download models
  pip install -r requirements.txt
  # Download pretrained models as per README
  ```
- Use for speech recognition and translation in low-resource languages.
- Integrate with STT ensemble for expanded language coverage.

## Phase 5: Quantum-Enhanced MCP (Conceptual)

*Note: Quantum MCP is speculative. Implement as a placeholder for future quantum-enhanced model context protocol.*
- Research quantum annealing or variational quantum classifiers for routing decisions.
- Simulate quantum effects using classical algorithms for now.
- Design MCP interface that could later be replaced with quantum backend.

## Phase 6: Testing, Auditing & Improvement Loop

### 6.1 Stress Testing (5 rounds)
- Define test scenarios:
  - High message volume (WhatsApp/Gmail).
  - Concurrent API requests.
  - Network failure simulation.
  - STT/TTS under load.
  - Memory leak detection.
- Use tools like Artillery, Locust, or custom scripts.
- Record performance metrics and failures.

### 6.2 Auditing
- Security audit: check for hardcoded credentials, injection vulnerabilities.
- Dependency audit: `npm audit`, `pip check`.
- Code audit: linting, formatting (ESLint, Prettier, Flake8).
- Update dependencies and patch vulnerabilities.

### 6.3 Bug Fixing & Error Handling
- Implement centralized error logging.
- Add retry mechanisms with exponential backoff.
- Create circuit breakers for external APIs.
- Improve logging and debugging capabilities.

### 6.4 Iteration
- After each test-audit-fix cycle, rebuild and retest.
- Aim for 11 rounds of tests/audits/fixes as requested.
- Continuously optimize file system, routing, and state management.

## Phase 7: Deployment & Continuous Operation

- Containerize with Docker for portability.
- Set up health checks and auto-restart.
- Monitor logs and performance metrics.
- Implement self-update mechanism (pull from repo, restart).

## Usage Notes

- This skill provides a blueprint; actual implementation requires filling in API keys, configuring credentials, and writing glue code.
- Start with Phase 1, then incrementally add integrations.
- Test each module in isolation before integrating.
- Keep the project's core loop simple: perceive -> think -> act -> learn.

## References

- See `references/` for detailed API documentation, example configurations, and scripts.
- See `scripts/` for setup and testing utilities.