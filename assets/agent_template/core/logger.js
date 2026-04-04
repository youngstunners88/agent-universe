// Logger: appends JSON events to the shared universe log
const fs = require('fs');
const path = require('path');

const SHARED_LOG_DIR = process.env.SHARED_LOG_DIR || '/root/.openclaw/workspace/agent-universe/agents/shared';
const SHARED_LOG_PATH = path.join(SHARED_LOG_DIR, 'universe.log');

// Ensure the directory exists
if (!fs.existsSync(SHARED_LOG_DIR)) {
  fs.mkdirSync(SHARED_LOG_DIR, { recursive: true });
}

/**
 * Log an event to the shared universe log.
 * @param {Object} event - { ts, agent, type, payload }
 */
function logEvent(event) {
  const logLine = JSON.stringify(event) + '\n';
  // fs.appendFileSync is atomic for writes <= 4KB on Linux/ext4
  fs.appendFileSync(SHARED_LOG_PATH, logLine, { encoding: 'utf8' });
}

module.exports = { logEvent };