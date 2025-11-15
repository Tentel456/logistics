import React from 'react'

const items = [
  { title: 'Last-mile Delivery', text: 'Couriers and bikes with dynamic routing and proof of delivery.' },
  { title: 'Freight & Trucking', text: 'Heavy vehicles with gabarit-aware navigation and incidents handling.' },
  { title: 'Warehousing', text: 'Smart capacity and overflow redirection between hubs.' },
]

export const Segments: React.FC = () => (
  <section className="segments">
    <div className="container">
      <h2>Segments We Serve</h2>
      <div className="cards">
        {items.map((it) => (
          <div className="card seg" key={it.title}>
            <div className="thumb" aria-hidden>
              <div className="img-ph" />
            </div>
            <h3>{it.title}</h3>
            <p>{it.text}</p>
          </div>
        ))}
      </div>
    </div>
  </section>
)
