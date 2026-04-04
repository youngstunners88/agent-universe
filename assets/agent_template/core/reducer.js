// Reducer for the agent's state
// Handles actions dispatched from the event bus and shared log tailer

/**
 * Reducer function
 * @param {Object} state - current state
 * @param {Object} action - { type, payload }
 * @returns {Object} new state
 */
function reducer(state, action) {
  switch (action.type) {
    // Shared log events (from tailer)
    case 'PERCEPTION_LEADS_RAW':
      return {
        ...state,
        UNIVERSE: {
          ...state.UNIVERSE,
          leads: [...state.UNIVERSE.leads, ...action.payload],
          lastUpdated: Date.now()
        }
      };
    case 'COGNITION_LEADS_SCORED':
      return {
        ...state,
        UNIVERSE: {
          ...state.UNIVERSE,
          leads: state.UNIVERSE.leads.map(lead => {
            const scored = action.payload.find(p => p.id === lead.id);
            return scored ? { ...lead, score: scored.score } : lead;
          }),
          lastUpdated: Date.now()
        }
      };
    case 'VALUE_SETTLEMENT':
      return {
        ...state,
        UNIVERSE: {
          ...state.UNIVERSE,
          settledValue: state.UNIVERSE.settledValue + action.payload.amount,
          lastUpdated: Date.now()
        }
      };
    case 'AGENT_HEARTBEAT':
      return {
        ...state,
        UNIVERSE: {
          ...state.UNIVERSE,
          agents: {
            ...state.UNIVERSE.agents,
            [action.payload.agentId]: {
              lastSeen: action.payload.timestamp,
              queueLength: action.payload.queueLength
            }
          },
          lastHeartbeat: action.payload.timestamp
        }
      };
    // Agent-specific actions (from sensorium, actuators, value)
    case 'AGENT_SET_CONFIG':
      return {
        ...state,
        config: action.payload
      };
    default:
      return state;
  }
}

module.exports = { reducer };