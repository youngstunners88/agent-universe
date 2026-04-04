// Memory: persists agent state to daily YYYY-MM-DD.md (for memory‑management distillation)
const fs = require('fs');
const path = require('path');

const MEMORY_DIR = process.env.MEMORY_DIR || '/root/.openclaw/workspace/agent-universe/agents/shared';
const MEMORY_FILE = (date) => path.join(MEMORY_DIR, `${date}.md`);

/**
 * Save state to memory file (today's date)
 * @param {Object} state - the agent state to save
 */
function memorySave(state) {
  const today = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
  const file = MEMORY_FILE(today);
  // We'll save a simplified version of the state (just the UNIVERSE part for now)
  const memoryContent = `# Agent State - ${today}\n\n\`\`\`json\n${JSON.stringify(state.UNIVERSE, null, 2)}\n\`\`\`\n`;
  fs.writeFileSync(file, memoryContent, { encoding: 'utf8' });
}

/**
 * Load state from memory file (today's date). If not found, return null.
 * @returns {Object|null} state or null if not found
 */
function memoryLoad() {
  const today = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
  const file = MEMORY_FILE(today);
  if (!fs.existsSync(file)) {
    return null;
  }
  const content = fs.readFileSync(file, { encoding: 'utf8' });
  // Extract the JSON from the markdown code block
  const jsonMatch = content.match(/```json\n([\s\S]*?)\n```/);
  if (jsonMatch) {
    try {
      const universe = JSON.parse(jsonMatch[1]);
      return { UNIVERSE: universe };
    } catch (e) {
      console.error('Failed to parse memory file:', e);
      return null;
    }
  }
  return null;
}

module.exports = { memorySave, memoryLoad };