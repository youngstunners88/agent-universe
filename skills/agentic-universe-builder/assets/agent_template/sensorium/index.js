// sensorium/index.js
// This module exports a startSensorium function that the agent will call

// We'll generate fake leads every 30 seconds for demonstration
// In a real agent, this would be replaced with actual web scraping

const { logEvent } = require('../core/logger');

function startSensorium(dispatch, eventBus, state) {
  console.log('Starting sensorium (mock web scraping leads)');

  // Generate a fake lead every 30 seconds
  const interval = setInterval(() => {
    const fakeLead = {
      id: `lead-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
      source: 'facebook_marketplace',
      timestamp: new Date().toISOString(),
      contact_info: {
        name: `Seller ${Math.floor(Math.random() * 100)}`,
        phone: `(555) ${Math.floor(Math.random()*900)+100}-${Math.floor(Math.random()*9000)+1000}`,
        email: `seller${Math.floor(Math.random()*1000)}@example.com`,
        address: `${Math.floor(Math.random()*10000)} Fake St, City, ST ${Math.floor(Math.random()*90000)+10000}`
      },
      property_info: {
        address: `${Math.floor(Math.random()*10000)} Fake St, City, ST ${Math.floor(Math.random()*90000)+10000}`,
        price: Math.floor(Math.random()*200000)+50000,
        beds: Math.floor(Math.random()*5)+1,
        baths: Math.floor(Math.random()*3)+1,
        sqft: Math.floor(Math.random()*2000)+800,
        lot_size: `${Math.floor(Math.random()*10)+0.25} acres`,
        year_built: Math.floor(Math.random()*60)+1940,
        condition: Math.random() > 0.5 ? 'Good' : 'Needs Repair'
      },
      seller_info: {
        motivation: Math.random() > 0.5 ? 'Relocating for job' : 'Financial distress',
        timeline: Math.random() > 0.5 ? 'ASAP' : 'Flexible',
        price_expectation: Math.floor(Math.random()*200000)+50000
      },
      metadata: {
        raw_data_url: 'https://example.com/fake-lead',
        scraper_version: '0.1.0',
        confidence_score: Math.random()
      }
    };

    // Emit the perception event
    dispatch({
      type: 'PERCEPTION_LEADS_RAW',
      payload: [fakeLead]
    });

    console.log(`Sensorium: emitted lead ${fakeLead.id}`);
  }, 30000); // 30 seconds

  // Return a cleanup function to clear the interval when the agent stops
  return () => {
    clearInterval(interval);
    console.log('Sensorium stopped');
  };
}

module.exports = { startSensorium };