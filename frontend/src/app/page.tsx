"use client"

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Hero } from '@/components/hero'
import { Features } from '@/components/features'
import { HowItWorks } from '@/components/how-it-works'
import { MascotShowcase } from '@/components/mascot-showcase'
import { ScannerPreview } from '@/components/scanner-preview'
import { Navbar } from '@/components/navbar'
import { Footer } from '@/components/footer'
import { useLoading } from '@/hooks/use-loading'
import { ChatSection } from '@/components/chat-section'

export default function Home() {
  const { isLoading } = useLoading()

  return (
    <>
      <AnimatePresence>
        {isLoading && (
          <motion.div
            key="loader"
            className="fixed inset-0 z-[9999] bg-background flex items-center justify-center"
            initial={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.8 }}
          >
            <div className="flex flex-col items-center space-y-6">
              {/* Loading Spinner */}
              <motion.div
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ duration: 0.6, delay: 0.2 }}
                className="relative"
              >
                <div className="w-32 h-32 relative">
                  {/* Outer ring */}
                  <motion.div
                    className="absolute inset-0 border-4 border-primary/20 rounded-full"
                    animate={{ rotate: 360 }}
                    transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                  />
                  
                  {/* Inner ring */}
                  <motion.div
                    className="absolute inset-4 border-4 border-primary/40 rounded-full"
                    animate={{ rotate: -360 }}
                    transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
                  />
                  
                  {/* Center spinner */}
                  <motion.div
                    className="absolute inset-8 border-4 border-primary border-t-transparent rounded-full"
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                  />
                  
                  {/* Center icon */}
                  <motion.div
                    className="absolute inset-0 flex items-center justify-center"
                    animate={{ scale: [1, 1.1, 1] }}
                    transition={{ duration: 2, repeat: Infinity }}
                  >
                    <div className="w-8 h-8 bg-gradient-to-br from-primary to-secondary rounded-lg flex items-center justify-center">
                      <div className="w-4 h-4 bg-white rounded-sm" />
                    </div>
                  </motion.div>
                </div>
              </motion.div>

              {/* Loading Text */}
              <motion.div
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ duration: 0.6, delay: 0.4 }}
                className="text-center space-y-2"
              >
                <motion.h2
                  className="text-2xl font-bold text-foreground"
                  animate={{ opacity: [1, 0.5, 1] }}
                  transition={{ duration: 2, repeat: Infinity }}
                >
                  Loading PhishGuard
                </motion.h2>
                <motion.p
                  className="text-muted-foreground"
                  animate={{ opacity: [0.7, 1, 0.7] }}
                  transition={{ duration: 2, repeat: Infinity, delay: 0.5 }}
                >
                  Preparing your security tools...
                </motion.p>
              </motion.div>

              {/* Loading Dots */}
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.6, delay: 0.6 }}
                className="flex space-x-2"
              >
                {[0, 1, 2].map((index) => (
                  <motion.div
                    key={index}
                    className="w-2 h-2 bg-primary rounded-full"
                    animate={{
                      scale: [1, 1.2, 1],
                      opacity: [0.5, 1, 0.5]
                    }}
                    transition={{
                      duration: 1.5,
                      repeat: Infinity,
                      delay: index * 0.2
                    }}
                  />
                ))}
              </motion.div>

              {/* Progress Bar */}
              <motion.div
                initial={{ width: 0, opacity: 0 }}
                animate={{ width: "100%", opacity: 1 }}
                transition={{ duration: 0.8, delay: 0.8 }}
                className="w-64 h-1 bg-muted rounded-full overflow-hidden"
              >
                <motion.div
                  className="h-full bg-gradient-to-r from-primary to-secondary"
                  initial={{ width: "0%" }}
                  animate={{ width: "100%" }}
                  transition={{ duration: 3, ease: "easeInOut" }}
                />
              </motion.div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {!isLoading && (
          <motion.div
            key="content"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="min-h-screen relative overflow-hidden"
          >
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
              <ChatSection />
              <Footer />
            </main>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}
