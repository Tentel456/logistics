import React from 'react'

export const Footer: React.FC = () => {
  const year = new Date().getFullYear()
  return (
    <footer className="footer">
      <div className="container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>© {year} AI Logistics Ecosystem</div>
        <div className="links">
          <a href="http://127.0.0.1:8000/docs" style={{ marginLeft: 12, color: 'inherit', textDecoration: 'none' }}>API</a>
          <a href="#features" style={{ marginLeft: 12, color: 'inherit', textDecoration: 'none' }}>Features</a>
        </div>
      </div>
    </footer>
  )
}
