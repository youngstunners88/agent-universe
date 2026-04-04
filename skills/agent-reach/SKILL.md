---
name: agent-reach
description: Integrate Agent-Reach to give AI agents the ability to fetch and extract clean content from any public URL. Use when agents need to access live web information, scrape articles, fetch documentation, or gather real-time data for decision-making without expensive APIs.
---

# Agent-Reach Skill

This skill integrates the Agent-Reach tool (https://github.com/Panniantong/Agent-Reach) to enable AI agents to fetch and process web content directly.

## What is Agent-Reach?

Agent-Reach is a Python-based tool that acts as a vision module for AI agents, allowing them to:
- Fetch content from any public URL
- Extract clean, readable text stripped of ads, navigation, and clutter
- Provide the extracted content as context for LLMs to answer questions, summarize, or make decisions

## When to Use This Skill

Use this skill when your agent needs to:
- Access the latest information from news articles, blogs, or documentation
- Verify facts by checking live web pages
- Gather data from websites for research or analysis
- Fetch content from URLs without relying on paid APIs
- Build research agents that compare information across multiple sources
- Create customer support bots that reference live FAQ pages
- Develop coding assistants that pull current documentation

## How It Works

The skill provides access to the `fetch_url_content(url)` function from Agent-Reach, which:
1. Takes a URL as input
2. Retrieves the HTML content
3. Uses readability-lxml to extract the main content
4. Returns clean text ready for LLM consumption

## Setup Instructions

The tool requires:
- Python 3.x
- Required dependencies: requests, readability-lxml, lxml, html2text

These are typically installed via:
```bash
pip install -r requirements.txt
```

## Usage in Agent Code

To use Agent-Reach in your agent's Python code:

```python
from agent_reach import fetch_url_content

# Fetch content from a URL
url = "https://example.com/article"
content = fetch_url_content(url)

# Use the content in your agent's reasoning process
print(f"Fetched {len(content)} characters from {url}")
# Pass content to LLM for summarization, Q&A, etc.
```

## Example Applications

1. **Research Agent**: Fetch and compare articles on a topic from multiple sources
2. **Fact Checker**: Verify claims by checking authoritative sources
3. **Documentation Assistant**: Fetch latest framework documentation for coding help
4. **News Monitor**: Track developing stories by periodically fetching news URLs
5. **Content Curator**: Extract key information from blogs for newsletters

## Integration with OpenClaw Universe

In the OpenClaw agent universe, this skill can be used by:
- Perception agents to gather environmental data from web sources
- Research agents to build knowledge bases from online content
- Communication agents to reference live information in messages
- Decision-making agents to ground choices in current data

## Safety Notes

- Agent-Reach fetches only public web content
- The tool does not execute JavaScript, so some dynamic content may not be extracted
- Always verify the source and credibility of fetched information
- Respect website terms of service and robots.txt when scraping
- The skill does not handle authentication or bypass paywalls

## Troubleshooting

Common issues and solutions:
- **URL blocked**: Some sites block automated fetches; try different user agents or delays
- **Content extraction fails**: Complex sites may need custom parsing rules
- **Encoding issues**: The tool handles UTF-8 but may struggle with exotic encodings

For detailed configuration, see the Agent-Reach repository README.

## Related Skills

- `web-scraping-leads`: For more advanced, targeted lead extraction from specific sites
- `dev-browser`: For JavaScript-heavy sites requiring full browser rendering
- `browsing-internet`: For general web search and browsing capabilities

---