import React from 'react'

export const Header: React.FC = () => {
  return (
    <header className="nav">
      <div className="container nav-inner">
        <div className="logo">AI Logistics</div>
        <nav>
          <a href="#features">Features</a>
          <a href="#how">How it works</a>
          <a href="http://127.0.0.1:8000/docs" className="btn secondary">API Docs</a>
        </nav>
      </div>
    </header>
  )
}
