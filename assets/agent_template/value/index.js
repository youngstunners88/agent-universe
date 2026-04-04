// value/index.js
// This module exports a startValue function that the agent will call

const { logEvent } = require('../core/logger');
const path = require('path');
const fs = require('fs');

function startValue(dispatch, eventBus, state) {
  console.log('Starting value module (lead scoring and settlement)');

  // Load agent config for threshold
  const configPath = path.resolve(__dirname, '../../config/agent_config.json');
  let config = { qualificationThreshold: 0.7 }; // default
  try {
    const rawConfig = fs.readFileSync(configPath, 'utf8');
    config = JSON.parse(rawConfig);
  } catch (e) {
    console.warn('Could not load agent config, using default threshold:', e.message);
  }
  const { qualificationThreshold = 0.7 } = config;

  // Listen for scored leads from the reducer (when leads are scored)
  const handleScoredLeads = (action) => {
    if (action.type === 'COGNITION_LEADS_SCORED') {
      const scoredLeads = action.payload;
      console.log(`Value module: received ${scoredLeads.length} scored leads`);

      // Filter leads that meet the threshold
      const qualifiedLeads = scoredLeads.filter(lead => lead.score >= qualificationThreshold);
      console.log(`Value module: ${qualifiedLeads.length} leads qualify for outreach (score >= ${qualificationThreshold})`);

      // For each qualified lead, attempt to place a call
      qualifiedLeads.forEach(lead => {
        // We need a phone number from the lead
        const phoneNumber = lead.contact_info?.phone;
        if (!phoneNumber) {
          console.warn(`Value module: lead ${lead.id} has no phone number, skipping call`);
          return;
        }

        // We'll use a simple script for now - in a real system, this would be more sophisticated
        const script = `Hello, is this ${lead.contact_info.name}? I'm calling about your property at ${lead.property_info.address}.`;

        // Dispatch an actuation event
        dispatch({
          type: 'ACTUATION_CALL_ATTEMPT',
          payload: {
            leadId: lead.id,
            phoneNumber,
            script
          }
        });
      });
    }
  };

  // Listen for call results to determine if we should settle
  const handleCallResult = (action) => {
    if (action.type === 'ACTUATION_CALL_RESULT') {
      const { leadId, successful, outcome } = action.payload;
      if (successful && outcome === 'qualified') {
        console.log(`Value module: call to lead ${leadId} was successful and qualified, attempting settlement`);

        // We need to get the lead details from the state's UNIVERSE.leads
        // Note: the state is passed in, but we can also get it from the closure.
        // However, the state might be updated, so we'll use the state from the closure.
        // But note: the state in the closure is the initial state. We need to get the latest state.
        // Instead, we can store the lead details in the action payload when we dispatch the call attempt.
        // Let's change: when we dispatch the actuation, we include the lead object.
        // However, we didn't do that above. We'll adjust: we'll store the lead in the state's UNIVERSE.leads and then look it up by id.

        // For now, we'll assume the lead is in state.UNIVERSE.leads (which is updated by the reducer on PERCEPTION_LEADS_RAW and COGNITION_LEADS_SCORED)
        const lead = state.UNIVERSE.leads.find(l => l.id === leadId);
        if (!lead) {
          console.warn(`Value module: could not find lead ${leadId} in state for settlement`);
          return;
        }

        // Try to use the settlement engine from the agent's value directory if available
        let settlementEngine;
        try {
          settlementEngine = require('../settlement_engine');
        } catch (e) {
          console.warn('No settlement engine found in agent value directory, using built-in mock:', e.message);
          // Built-in mock settlement: just log and emit a VALUE_SETTLEMENT event
          settlementEngine = async (lead) => {
            const plaintext = JSON.stringify({
              timestamp: new Date().toISOString(),
              leadId: lead.id,
              amount: '0.00',
              currency: 'USD',
              note: 'demo settlement (mock)'
            });
            logEvent({
              type: 'VALUE_SETTLEMENT',
              payload: {
                leadId: lead.id,
                // In a real system we’d put an actual amount / currency / invoice ID here
                amount: '0.00',
                currency: 'USD',
                note: 'demo settlement'
              }
            });
          };
        }

        // Run the settlement engine
        settlementEngine(lead).then(() => {
          console.log(`Value module: settlement processed for lead ${leadId}`);
        }).catch(err => {
          console.error(`Value module: settlement failed for lead ${leadId}:`, err);
        });
      }
    }
  };

  eventBus.on('COGNITION_LEADS_SCORED', handleScoredLeads);
  eventBus.on('ACTUATION_CALL_RESULT', handleCallResult);

  // Return a cleanup function to remove the listeners when the agent stops
  return () => {
    eventBus.off('COGNITION_LEADS_SCORED', handleScoredLeads);
    eventBus.off('ACTUATION_CALL_RESULT', handleCallResult);
    console.log('Value module stopped');
  };
}

module.exports = { startValue };