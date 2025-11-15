import React from 'react'

export const Features: React.FC = () => (
  <section id="features" className="features">
    <div className="container grid-3">
      <div className="card">
        <h3>API Gateway</h3>
        <p>Unified REST API for marketplaces, delivery services, logistics systems, and municipal data.</p>
      </div>
      <div className="card">
        <h3>OMS</h3>
        <p>Order intake, tracking codes, auto-assign transport & warehouse, status transitions.</p>
      </div>
      <div className="card">
        <h3>Transport Hub</h3>
        <p>Vehicle registry with dimensions and load capacity, emergency stop.</p>
      </div>
      <div className="card">
        <h3>Warehouse Hub</h3>
        <p>Capacity monitoring, incidents (fire/overflow) auto-redirect to alternative storage.</p>
      </div>
      <div className="card">
        <h3>Routing</h3>
        <p>Truck-aware heuristics. Replaceable with real providers.</p>
      </div>
      <div className="card">
        <h3>Analytics</h3>
        <p>KPIs by status, fleet/storage overview.</p>
      </div>
    </div>
  </section>
)
