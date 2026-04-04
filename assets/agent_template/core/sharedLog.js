// Shared log tailer - reads new lines from shared universe.log and feeds them into agent's universe view
const fs = require('fs');
const path = require('path');

class SharedLog {
  constructor(handler) {
    // Get shared log path from environment or use default
    this.sharedLogPath = process.env.SHARED_LOG_PATH || 
                       '/root/.openclaw/workspace/agent-universe/agents/shared/universe.log';
    this.handler = handler;
    this.lastPosition = 0;
    
    // Initialize last position to end of file (so we only get new events)
    try {
      const stats = fs.statSync(this.sharedLogPath);
      this.lastPosition = stats.size;
    } catch (error) {
      // File doesn't exist yet, that's okay - we'll start from 0
      this.lastPosition = 0;
    }
  }
  
  async start() {
    // Start tailing the log
    return this.tailLog();
  }
  
  async tailLog() {
    while (true) {
      try {
        // Check if file exists
        if (!fs.existsSync(this.sharedLogPath)) {
          // Wait a bit and try again
          await new Promise(resolve => setTimeout(resolve, 1000));
          continue;
        }
        
        // Get current file size
        const currentSize = fs.statSync(this.sharedLogPath).size;
        
        // If file has grown, read new content
        if (currentSize > this.lastPosition) {
          const data = fs.readFileSync(this.sharedLogPath, { 
            encoding: 'utf8', 
            start: this.lastPosition,
            end: currentSize - 1
          });
          
          // Split into lines and process each
          const lines = data.trim().split('\n');
          for (const line of lines) {
            if (line.trim()) {
              try {
                const event = JSON.parse(line);
                // Only process events from other agents (to avoid feedback loop)
                if (event.agent !== process.env.AGENT_ID) {
                  this.handler(event);
                }
              } catch (parseError) {
                // Invalid JSON line, skip
                console.warn(`Invalid JSON in shared log: ${line.substring(0, 100)}`);
              }
            }
          }
          
          this.lastPosition = currentSize;
        }
        
        // Wait before checking again
        await new Promise(resolve => setTimeout(resolve, 1000));
      } catch (error) {
        console.error(`Error in shared log tailer: ${error.message}`);
        await new Promise(resolve => setTimeout(resolve, 5000)); // Wait longer on error
      }
    }
  }
}

module.exports = { SharedLog };