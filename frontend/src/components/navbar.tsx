"use client"

import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  Home, 
  Shield, 
  FileText, 
  MessageCircle, 
  User,
  Menu,
  X,
  ChevronUp
} from 'lucide-react'
import Link from 'next/link'
import { DarkModeToggle } from './dark-mode-toggle'

// Navigation items
const navItems = [
  { id: 'home', label: 'Home', icon: Home, href: '/' },
  { id: 'scanner', label: 'Scanner', icon: Shield, href: '#scanner' },
  { id: 'reports', label: 'Reports', icon: FileText, href: '#reports' },
  { id: 'chat', label: 'Chat (Ai)', icon: MessageCircle, href: '#chat' },
  { id: 'profile', label: 'Profile', icon: User, href: '/login' }
]

const desktopNavItems = [
  { label: 'Features', href: '#features' },
  { label: 'How it Works', href: '#how-it-works' },
  { label: 'Scanner', href: '#scanner' },
  { label: 'Reports', href: '#reports' },
  { label: 'Pricing', href: '#pricing' }
]

export const Navbar = () => {
  const [isScrolled, setIsScrolled] = useState(false)
  const [isFloating, setIsFloating] = useState(false)
  const [showScrollTop, setShowScrollTop] = useState(false)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [isMobile, setIsMobile] = useState(false)

  useEffect(() => {
    // Check if mobile
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 1024)
    }
    
    checkMobile()
    window.addEventListener('resize', checkMobile)

    // Scroll handler
    const handleScroll = () => {
      const scrollY = window.scrollY
      setIsScrolled(scrollY > 120)
      setIsFloating(scrollY > 120)
      setShowScrollTop(scrollY > 300)
      
      // Analytics events
      if (scrollY > 120 && !isFloating) {
        console.log('Analytics: navbar_floated')
      }
      if (scrollY <= 120 && isFloating) {
        console.log('Analytics: navbar_returned')
      }
    }

    // Throttle scroll events
    let ticking = false
    const throttledHandleScroll = () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          handleScroll()
          ticking = false
        })
        ticking = true
      }
    }

    window.addEventListener('scroll', throttledHandleScroll)
    
    return () => {
      window.removeEventListener('scroll', throttledHandleScroll)
      window.removeEventListener('resize', checkMobile)
    }
  }, [isFloating])

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  // Desktop Navbar
  const DesktopNavbar = () => (
    <motion.nav
      initial={{ y: 0 }}
      animate={{ 
        y: isFloating ? -6 : 0,
        scale: isFloating ? 1.01 : 1,
        opacity: isFloating ? 0.98 : 1
      }}
      transition={{ 
        type: "spring", 
        stiffness: 80, 
        damping: 15,
        duration: 1.2,
        ease: [0.25, 0.46, 0.45, 0.94]
      }}
      className={`
        fixed top-0 left-0 right-0 z-50 transition-all duration-500 ease-out
        ${isFloating 
          ? 'navbar-floating' 
          : ''
        }
      `}
    >
      <div         className={`
          mx-auto transition-all duration-1200 ease-out
          ${isFloating 
            ? 'max-w-5xl mt-4 rounded-2xl shadow-2xl' 
            : 'max-w-full'
          }
        `}>
          <div className={`
            bg-background/85 backdrop-blur-xl border-border/40
            ${isFloating ? 'rounded-2xl border-2 border-primary/20 shadow-xl' : 'border-b border-border/20'}
            transition-all duration-1200 ease-out
          `}>
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              {/* Logo */}
              <Link href="/" className="flex items-center gap-2 group">
                <motion.div
                  whileHover={{ rotate: 5, scale: 1.05 }}
                  transition={{ type: "spring", stiffness: 400, damping: 10 }}
                >
                  <Shield className="w-8 h-8 text-primary group-hover:text-secondary transition-colors duration-300" />
                </motion.div>
                <span className="text-xl font-bold text-foreground relative">
                  PhishGuard
                  <div className="absolute -bottom-1 left-0 w-full h-0.5 bg-gradient-to-r from-primary via-secondary to-primary rounded-full"></div>
                </span>
              </Link>

              {/* Desktop Navigation */}
              <div className="hidden lg:flex items-center gap-8">
                {desktopNavItems.map((item, index) => (
                  <motion.a
                    key={item.label}
                    href={item.href}
                    className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors duration-300 relative group"
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    whileHover={{ y: -2 }}
                  >
                    {item.label}
                    <motion.div
                      className="absolute -bottom-1 left-0 right-0 h-0.5 bg-gradient-to-r from-primary to-secondary rounded-full"
                      initial={{ scaleX: 0 }}
                      whileHover={{ scaleX: 1 }}
                      transition={{ duration: 0.3 }}
                    />
                  </motion.a>
                ))}
              </div>

              {/* Action Buttons */}
              <div className="flex items-center gap-3">
                <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                  <Button variant="ghost" size="sm" asChild className="text-muted-foreground hover:text-primary">
                    <Link href="/login">Sign In</Link>
                  </Button>
                </motion.div>
                <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                  <Button size="sm" className="gradient-bg text-white shadow-lg hover:shadow-xl transition-all duration-300" asChild>
                    <Link href="/register">Get Started</Link>
                  </Button>
                </motion.div>
                
                {/* Dark Mode Toggle */}
                <DarkModeToggle />
                
                {/* Mobile menu button */}
                <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="lg:hidden text-muted-foreground hover:text-primary"
                    onClick={() => setMobileMenuOpen(true)}
                  >
                    <Menu className="w-5 h-5" />
                  </Button>
                </motion.div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </motion.nav>
  )

  // Mobile Bottom Navigation
  const MobileBottomNav = () => (
    <motion.nav
      initial={{ y: 100 }}
      animate={{ y: 0 }}
      transition={{ type: "spring", stiffness: 300, damping: 30 }}
      className="lg:hidden fixed bottom-0 left-0 right-0 z-50 bottom-nav-safe"
    >
      <div className="bg-background/90 backdrop-blur-xl border-t border-border/30 shadow-2xl">
        <div className="flex items-center justify-around py-2">
          {navItems.map((item, index) => {
            const Icon = item.icon
            return (
              <motion.a
                key={item.id}
                href={item.href}
                className="flex flex-col items-center gap-1 p-2 min-w-0 flex-1 group"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1, type: "spring" }}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <div className="w-6 h-6 flex items-center justify-center">
                  <Icon className="w-5 h-5 text-muted-foreground group-hover:text-primary transition-colors duration-300" />
                </div>
                <span className="text-xs text-muted-foreground group-hover:text-primary transition-colors duration-300 truncate">
                  {item.label}
                </span>
              </motion.a>
            )
          })}
        </div>
      </div>
    </motion.nav>
  )

  // Mobile Menu Overlay
  const MobileMenu = () => (
    <AnimatePresence>
      {mobileMenuOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="lg:hidden fixed inset-0 z-50 bg-black/50 backdrop-blur-sm"
          onClick={() => setMobileMenuOpen(false)}
        >
          <motion.div
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
            className="fixed top-0 right-0 bottom-0 w-80 bg-background/95 backdrop-blur-xl border-l border-border/30 shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="p-6">
              <div className="flex items-center justify-between mb-8">
                <div className="flex items-center gap-2">
                  <Shield className="w-6 h-6 text-primary" />
                  <span className="text-lg font-bold">PhishGuard</span>
                </div>
                <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    <X className="w-5 h-5" />
                  </Button>
                </motion.div>
              </div>

              <div className="space-y-4">
                {desktopNavItems.map((item, index) => (
                  <motion.a
                    key={item.label}
                    href={item.href}
                    className="block py-3 px-4 text-lg font-medium hover:bg-accent/50 rounded-lg transition-all duration-300 border border-transparent hover:border-primary/20"
                    onClick={() => setMobileMenuOpen(false)}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    whileHover={{ x: 4 }}
                  >
                    {item.label}
                  </motion.a>
                ))}
                
                <div className="pt-4 border-t border-border/30">
                  <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                    <Button variant="ghost" className="w-full justify-start mb-2" asChild>
                      <Link href="/login">Sign In</Link>
                    </Button>
                  </motion.div>
                  <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                    <Button className="w-full gradient-bg text-white shadow-lg" asChild>
                      <Link href="/register">Get Started</Link>
                    </Button>
                  </motion.div>
                </div>
              </div>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )

  // Scroll to Top Button
  const ScrollToTopButton = () => (
    <AnimatePresence>
      {showScrollTop && (
        <motion.button
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.8 }}
          whileHover={{ scale: 1.1, rotate: 5 }}
          whileTap={{ scale: 0.9 }}
          onClick={scrollToTop}
          className={`
            fixed z-40 w-12 h-12 rounded-full gradient-bg text-white shadow-xl
            hover:shadow-2xl transition-all duration-300 backdrop-blur-sm
            ${isMobile ? 'bottom-20 right-4' : 'bottom-8 right-8'}
          `}
        >
          <ChevronUp className="w-6 h-6 mx-auto" />
        </motion.button>
      )}
    </AnimatePresence>
  )

  return (
    <>
      {/* Desktop Navigation - hidden on mobile */}
      <div className="hidden lg:block">
        <DesktopNavbar />
      </div>

      {/* Mobile Bottom Navigation - hidden on desktop */}
      <MobileBottomNav />

      {/* Mobile Menu Overlay */}
      <MobileMenu />

      {/* Scroll to Top Button */}
      <ScrollToTopButton />

      {/* Spacer for fixed navbar on desktop */}
      <div className="hidden lg:block h-16" />
      
      {/* Spacer for bottom nav on mobile */}
      <div className="lg:hidden h-16 bottom-nav-safe" />
    </>
  )
} 