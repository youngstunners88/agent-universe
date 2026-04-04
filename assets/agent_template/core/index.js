// Agent main loop
// Sets up event bus, state reducer, log tailer, and starts the agent

const EventEmitter = require('eventemitter3');
const { reducer } = require('./reducer');
const { tailLog } = require('./sharedLog');
const { logEvent } = require('./logger');
const { memorySave, memoryLoad } = require('./memory');
const { startSensorium } = require('../sensorium');
const { startActuators } = require('../actuators');
const { startValue } = require('../value');
const config = require('../config/agent_config.json');

// Initialize state from memory or defaults
let state = memoryLoad() || {
  UNIVERSE: {
    leads: [],
    settledValue: 0,
    agents: {},
    lastHeartbeat: Date.now()
  },
  // agent-specific state can be added here
};

// Event emitter for internal communication
const eventBus = new EventEmitter();

// Redux-style store
function dispatch(action) {
  state = reducer(state, action);
  // Save state to memory periodically (or on every action for simplicity)
  memorySave(state);
  // Emit the action for any listeners
  eventBus.emit(action.type, action.payload);
}

// Initialize
async function init() {
  // Load any existing state from shared log (optional, for replay)
  // For now, we start fresh and let the shared log bring us up to date via tailer

  // Start tailing the shared log
  tailLog(dispatch);

  // Start sensorium (perception)
  startSensorium(dispatch, eventBus, state);

  // Start actuators (output)
  startActuators(dispatch, eventBus, state);

  // Start value (scoring, settlement)
  startValue(dispatch, eventBus, state);

  // Set up heartbeat
  setInterval(() => {
    dispatch({
      type: 'AGENT_HEARTBEAT',
      payload: {
        agentId: config.agentId,
        timestamp: Date.now(),
        queueLength: eventBus.listenerCount('any'), // rough metric
        // Add any agent-specific metrics here
      }
    });
  }, 30000); // every 30 seconds

  console.log(`Agent ${config.agentId} started`);
}

// Start the agent
init().catch(console.error);

module.exports = { dispatch, eventBus, state };