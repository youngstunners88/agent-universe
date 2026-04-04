// actuators/index.js
// This module exports a startActuators function that the agent will call

const { logEvent } = require('../core/logger');

function startActuators(dispatch, eventBus, state) {
  console.log('Starting actuators (mock)');

  // Listen for actuation events from the event bus (internal) or from the shared log via dispatch?
  // In this architecture, actuation events are dispatched by the agent's own logic (e.g., value module) and then we act on them.
  // We'll listen for a specific event type, e.g., 'ACTUATION_CALL_ATTEMPT'
  const handleActuation = (action) => {
    if (action.type === 'ACTUATION_CALL_ATTEMPT') {
      const { leadId, phoneNumber, script } = action.payload;
      console.log(`Actuator: Attempting call to lead ${leadId} at ${phoneNumber}`);
      // In a real system, we would place the call here (e.g., using Retell AI)
      // For now, we just log and then emit a settlement event if the call is successful (mock)
      // Simulate a random outcome
      const callSuccessful = Math.random() > 0.5; // 50% success rate for demo
      if (callSuccessful) {
        // After a successful call, we might want to log a settlement event (if the call led to a qualified lead)
        // But note: the settlement engine is in the value module. We'll let the value module handle settlement based on call results.
        // For now, we just log that the call was successful.
        console.log(`Actuator: Call to lead ${leadId} was successful`);
        // We could dispatch a call result event here for the value module to process
        dispatch({
          type: 'ACTUATION_CALL_RESULT',
          payload: {
            leadId,
            successful: true,
            duration: Math.floor(Math.random()*10)+10, // 10-20 seconds
            outcome: 'qualified' // or 'not interested', etc.
          }
        });
      } else {
        console.log(`Actuator: Call to lead ${leadId} failed or no answer`);
        dispatch({
          type: 'ACTUATION_CALL_RESULT',
          payload: {
            leadId,
            successful: false,
            duration: 0,
            outcome: 'no_answer'
          }
        });
      }
    }
  };

  eventBus.on('ACTUATION_CALL_ATTEMPT', handleActuation);

  // Return a cleanup function to remove the listener when the agent stops
  return () => {
    eventBus.off('ACTUATION_CALL_ATTEMPT', handleActuation);
    console.log('Actuators stopped');
  };
}

module.exports = { startActuators };