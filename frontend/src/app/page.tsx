import { Hero } from '@/components/hero'
import { Features } from '@/components/features'
import { HowItWorks } from '@/components/how-it-works'
import { MascotShowcase } from '@/components/mascot-showcase'
import { ScannerPreview } from '@/components/scanner-preview'
import { Navbar } from '@/components/navbar'
import { Footer } from '@/components/footer'

export default function Home() {
  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Background animations */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute -top-1/2 -left-1/2 w-full h-full bg-gradient-to-br from-primary/5 via-transparent to-secondary/5 animate-spin" style={{ animationDuration: '60s' }} />
        <div className="absolute -top-1/4 -right-1/4 w-1/2 h-1/2 bg-gradient-to-bl from-secondary/3 via-transparent to-primary/3 animate-pulse" />
        <div className="absolute -bottom-1/4 -left-1/4 w-1/2 h-1/2 bg-gradient-to-tr from-primary/3 via-transparent to-secondary/3 animate-pulse" style={{ animationDelay: '2s' }} />
      </div>
      
      <main className="relative z-10">
        <Navbar />
        <Hero />
        <Features />
        <HowItWorks />
        <MascotShowcase />
        <ScannerPreview />
        <Footer />
      </main>
    </div>
  )
}
