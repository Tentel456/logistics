import React from 'react'

export const Hero: React.FC = () => {
  return (
    <section className="hero">
      <div className="container hero-inner">
        <div className="hero-copy">
          <h1>Intelligent, autonomous logistics platform</h1>
          <p>Unify marketplaces, carriers, warehouses, and city infrastructure into one AI-driven ecosystem. Real-time routing, auto-assignment, smart pricing, and resilience to incidents.</p>
          <div className="cta">
            <a href="#features" className="btn primary">Explore capabilities</a>
            <a href="http://127.0.0.1:8000/docs" className="btn">Open Swagger</a>
          </div>
          <div className="badges">
            <span>JWT Security</span>
            <span>Truck-aware Routing</span>
            <span>SQLite-backed</span>
          </div>
        </div>
        <div className="hero-art">
          <img src="/hero-map.svg" alt="map visualization" />
        </div>
      </div>
    </section>
  )
}
