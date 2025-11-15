import React from 'react'
import { Header } from '@components/Header'
import { Hero } from '@components/Hero'
import { Features } from '@components/Features'
import { HowItWorks } from '@components/HowItWorks'
import { Footer } from '@components/Footer'
import { Stats } from '@components/Stats'
import { Segments } from '@components/Segments'

export const App: React.FC = () => {
  return (
    <div className="app-root">
      <Header />
      <main>
        <Hero />
        <Stats />
        <Features />
        <Segments />
        <HowItWorks />
      </main>
      <Footer />
    </div>
  )
}
