import React from 'react'

export const HowItWorks: React.FC = () => (
  <section id="how" className="how">
    <div className="container">
      <h2>How it works</h2>
      <ol className="steps">
        <li><b>Connect</b> your fleets and warehouses via API Gateway.</li>
        <li><b>Create orders</b> via backend `/orders` and get instant pricing.</li>
        <li><b>Auto-assign</b> selects the best vehicle and warehouse.</li>
        <li><b>Route</b> with constraints and monitor status transitions.</li>
        <li><b>Recover</b> from incidents with auto-redirect.</li>
      </ol>
      <a className="btn primary" href="http://127.0.0.1:8000/docs">Start in Swagger</a>
    </div>
  </section>
)
