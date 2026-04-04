---
name: autonomous-agent-orchestrator
description: Builds an autonomous agent orchestrator with WhatsApp, Gmail, TikTok integration, quantum MCP architecture, and TTS/STT capabilities. Use when you need to create a self-sufficient AI agent that can communicate across platforms, manage its own file/routing/state systems, and perform automated tasks with reporting. This skill guides the creation, testing, and optimization of the agent through 11 rounds of stress tests and audits.
---

# Autonomous Agent Orchestrator

## Overview

This skill enables the creation of a fully autonomous AI agent that operates across WhatsApp, Gmail, and TikTok platforms. The agent features a quantum-inspired MCP (Multi-Channel Platform) architecture with optimized file system, next-generation routing, and impeccable state management. It includes integrated TTS/STT capabilities from multiple engines (Coqui TTS, Bark, Piper, MeloTTS, SpeechT5) for cost efficiency and can leverage MiroShark for network analysis. The agent autonomously generates summaries of its activities, learns, and plans future actions.

## Capabilities-Based Structure

This skill is organized around the core capabilities of the autonomous agent orchestrator:

### Core Capabilities
1. **Quantum MCP Architecture** - High-level file/folder system, routing, and state management
2. **Multi-Platform Communication** - WhatsApp, Gmail, TikTok integration
3. **TTS/STT Engine Integration** - Cost-optimized speech synthesis and transcription
4. **Network Analysis & Security** - MiroShark integration for 20-minute process embedding
5. **Autonomous Reporting & Learning** - Self-generated summaries of activities and plans
6. **Testing & Optimization Framework** - 11 rounds of stress tests, audits, and bug fixes

## 1. Quantum MCP Architecture

The agent's foundation is a quantum-inspired MCP architecture that provides:

### File & Folder System
- Hierarchical structure with lazy loading and code splitting
- Clear separation of concerns: /core, /platforms, /engines, /utils, /logs
- Example structure:
  ```
  agent/
  ├── core/
  │   ├── file_system.js
  │   ├── routing_system.js
  │   └── state_management.js
  ├── platforms/
  │   ├── whatsapp.js
  │   ├── gmail.js
  │   └── tiktok.js
  ├── engines/
  │   ├── tts/
  │   │   ├── coqui.js
  │   │   ├── bark.js
  │   │   ├── piper.js
  │   │   ├── melotts.js
  │   │   └── speecht5.js
  │   └── stt/
  │       └── whisper.js
  ├── utils/
  │   ├── miroShark.js
  │   └── reporting.js
  └── logs/
      ├── activity.log
      └── audit.log
  ```

### Routing System
- RESTful architecture with API/web/internal routes
- Performance targets: <1ms resolution, <50ms API response
- Route prioritization based on channel urgency and type

### State Management
- Redux Toolkit approach with structured state (UI/App/Domain/Server)
- <16ms update targets
- Immutability and time-travel debugging capabilities

## 2. Multi-Platform Communication

### WhatsApp Integration
- Uses official WhatsApp Business API or websocket-based libraries
- Handles message sending, receiving, and media processing
- Includes rate limiting and error recovery

### Gmail Integration
- OAuth2 authentication for secure access
- Sends, reads, and manages emails
- Processes attachments and formats outgoing messages

### TikTok Integration
- Uses TikTok API for content posting and analytics
- Handles video uploads, comments, and direct messages
- Implements trend detection for content optimization

## 3. TTS/STT Engine Integration

To save costs, the agent integrates multiple free/open-source TTS and STT engines:

### TTS Engines
- **Coqui TTS** - High-quality, multilingual synthesis
- **Bark** - Transformer-based text-to-audio
- **Piper** - Fast, lightweight neural TTS
- **MeloTTS** - High-performance multilingual TTS
- **SpeechT5** - Microsoft's unified speech-to-text/text-to-speech

### STT Engine
- **Whisper** - Robust speech recognition (OpenAI)

The agent intelligently selects the optimal engine based on:
- Language requirements
- Quality vs. speed trade-offs
- Current system load
- Cost considerations (all selected engines are free/open-source)

## 4. Network Analysis & Security (MiroShark Integration)

The agent embeds MiroShark for network analysis during its 20-minute process:

### Installation
```bash
git clone https://github.com/aaronjmars/MiroShark.git
cd MiroShark
# Follow installation instructions in README
```

### Usage
- Runs a 20-minute network analysis cycle
- Embeds results into agent's security audit logs
- Uses findings to harden agent's external communications
- Provides vulnerability scanning for outbound connections

## 5. Autonomous Reporting & Learning

The agent automatically generates summaries of:

### Activity Reports
- What it learned during interactions
- What it performed (actions taken)
- Plans for future actions
- Sent to designated channels (email, WhatsApp, etc.) on schedule

### Learning Mechanism
- Analyzes past interactions for patterns
- Updates internal knowledge base
- Adjusts communication strategies based on response rates
- Optimizes TTS/STT engine selection over time

## 6. Testing & Optimization Framework

The skill includes a rigorous testing protocol:

### 11 Rounds of Testing
1. **Basic Functionality Test** - Core systems operational
2. **Integration Test** - All platforms communicate
3. **Load Test** - Simultaneous multi-platform operations
4. **Stress Test** - Beyond normal operational capacity
5. **Security Audit** - Vulnerability scanning (with MiroShark)
6. **Error Handling Test** - Fault injection and recovery
7. **Performance Benchmark** - Latency and throughput measurements
8. **Resource Usage Test** - Memory, CPU, disk optimization
9. **Network Resilience Test** - Connection loss and recovery
10. **End-to-End Workflow Test** - Complete task cycles
11. **Optimization Round** - Apply fixes and re-test critical paths

### Audit Process
- Each round includes automated vulnerability scanning
- Manual code review for logic flaws
- Penetration testing simulation
- Dependency security checks
- Bug tracking and resolution

## Resources

### scripts/
Contains executable scripts for agent setup, testing, and optimization:

- `setup_agent.sh` - Initializes the agent structure and installs dependencies
- `install_engines.sh` - Sets up TTS/STT engines (Coqui, Bark, Piper, MeloTTS, SpeechT5)
- `install_miroshark.sh` - Clones and installs MiroShark
- `run_tests.sh` - Executes the 11-round testing suite
- `audit_agent.sh` - Performs security audits and vulnerability scans
- `optimize_agent.sh` - Applies optimizations based on test results
- `generate_report.py` - Creates activity and learning summaries

### references/
Detailed documentation for deep dives:

- `quantum_mcp_architecture.md` - In-depth guide to the MCP design
- `platform_integrations.md` - WhatsApp, Gmail, TikTok API specifics
- `tts_stt_engines.md` - Engine selection criteria and usage patterns
- `miroshark_integration.md` - Embedding network analysis in agent workflows
- `testing_protocol.md` - Detailed 11-round testing procedure
- `reporting_learning_system.md` - Autonomous reporting mechanisms

### assets/
Template files and boilerplate code:

- `agent_structure/` - Boilerplate directory structure for the agent
- `config_templates/` - Example configuration files for each platform
- `test_scenarios/` - Pre-defined test cases for the 11 rounds
- `report_templates/` - Markdown templates for activity summaries

---
**Not every skill requires all three types of resources.**
