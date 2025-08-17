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
  ChevronUp,
  Search
} from 'lucide-react'
import Link from 'next/link'
import { DarkModeToggle } from './dark-mode-toggle'
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger, SheetClose, SheetDescription } from '@/components/ui/sheet'

// Navigation items for mobile menu
const mobileNavItems = [
  { id: 'home', label: 'Home', icon: Home, href: '/' },
  { id: 'features', label: 'Features', icon: Shield, href: '#features' },
  { id: 'scanner', label: 'Scanner', icon: Search, href: '#scanner' },
  { id: 'how-it-works', label: 'How it Works', icon: FileText, href: '#how-it-works' },
  { id: 'guardians', label: 'Guardians', icon: MessageCircle, href: '#mascot' },
  { id: 'chat', label: 'Chat', icon: MessageCircle, href: '#chat' }
]

const desktopNavItems = [
  { label: 'Home', href: '/' },
  { label: 'Features', href: '#features' },
  { label: 'How it Works', href: '#how-it-works' },
  { label: 'Scanner', href: '#scanner' },
  { label: 'Chat', href: '#chat' }
]

export const Navbar = () => {
  const [isScrolled, setIsScrolled] = useState(false)
  const [isFloating, setIsFloating] = useState(false)
  const [showScrollTop, setShowScrollTop] = useState(false)
  const [isMobile, setIsMobile] = useState(false)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

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

  const handleMobileNavClick = () => {
    setMobileMenuOpen(false)
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
      <div className={`
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
                <Sheet open={mobileMenuOpen} onOpenChange={setMobileMenuOpen}>
                  <SheetTrigger asChild>
                    <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="lg:hidden text-muted-foreground hover:text-primary"
                      >
                        <Menu className="w-5 h-5" />
                      </Button>
                    </motion.div>
                  </SheetTrigger>
                  <SheetContent side="right" className="w-80 bg-gradient-to-br from-background via-background/95 to-primary/5 border-l border-primary/20">
                    <SheetHeader className="border-b border-border/30 pb-4">
                      <SheetTitle className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-secondary flex items-center justify-center">
                          <Shield className="w-5 h-5 text-white" />
                        </div>
                        <span className="text-lg font-bold">PhishGuard</span>
                      </SheetTitle>
                      <SheetDescription className="sr-only">
                        Mobile navigation menu for PhishGuard application
                      </SheetDescription>
                    </SheetHeader>
                    <div className="flex flex-col gap-1 mt-6">
                      {mobileNavItems.map((item, index) => {
                        const Icon = item.icon
                        return (
                          <SheetClose asChild key={item.id}>
                            <motion.a
                              href={item.href}
                              className="flex items-center gap-3 py-3 px-4 text-base font-medium hover:bg-gradient-to-r hover:from-primary/10 hover:to-secondary/10 rounded-xl transition-all duration-300 border border-transparent hover:border-primary/20 group"
                              initial={{ opacity: 0, x: 20 }}
                              animate={{ opacity: 1, x: 0 }}
                              transition={{ delay: index * 0.1 }}
                              whileHover={{ x: 4 }}
                              onClick={handleMobileNavClick}
                            >
                              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary/10 to-secondary/10 flex items-center justify-center group-hover:from-primary/20 group-hover:to-secondary/20 transition-all duration-300">
                                <Icon className="w-4 h-4 text-foreground group-hover:!text-blue-500 dark:group-hover:!text-pink-400 transition-colors duration-300" />
                              </div>
                              <span className="text-foreground group-hover:!text-blue-500 dark:group-hover:!text-pink-400 transition-colors duration-300">{item.label}</span>
                            </motion.a>
                          </SheetClose>
                        )
                      })}
                      
                      <div className="pt-3 border-t border-border/30 mt-3">
                        {/* Dark Mode Toggle */}
                        <div className="flex items-center justify-center py-3 px-4 mb-3">
                          <DarkModeToggle />
                        </div>
                        
                        <div className="flex gap-2">
                          <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} className="flex-1">
                            <SheetClose asChild>
                              <Button variant="ghost" className="w-full h-10 rounded-xl bg-gradient-to-r from-muted/50 to-muted/30 hover:from-muted/70 hover:to-muted/50" asChild>
                                <Link href="/login" onClick={handleMobileNavClick}>Sign In</Link>
                              </Button>
                            </SheetClose>
                          </motion.div>
                          <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} className="flex-1">
                            <SheetClose asChild>
                              <Button className="w-full h-10 rounded-xl gradient-bg text-white shadow-lg hover:shadow-xl transition-all duration-300" asChild>
                                <Link href="/register" onClick={handleMobileNavClick}>Get Started</Link>
                              </Button>
                            </SheetClose>
                          </motion.div>
                        </div>
                      </div>
                    </div>
                  </SheetContent>
                </Sheet>
              </div>
            </div>
          </div>
        </div>
      </div>
    </motion.nav>
  )

  // Mobile-only navbar (simplified top bar)
  const MobileNavbar = () => (
    <motion.nav
      initial={{ y: -50 }}
      animate={{ y: 0 }}
      transition={{ type: "spring", stiffness: 300, damping: 30 }}
      className="lg:hidden fixed top-0 left-0 right-0 z-50 bg-background/95 backdrop-blur-xl border-b border-border/30 shadow-lg"
    >
      <div className="bg-gradient-to-r from-background/95 via-background/98 to-background/95 backdrop-blur-xl border-b border-primary/10">
        <div className="flex justify-between items-center h-16 px-4 max-w-7xl mx-auto">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 group">
            <motion.div
              whileHover={{ rotate: 5, scale: 1.05 }}
              transition={{ type: "spring", stiffness: 400, damping: 10 }}
              className="relative"
            >
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-secondary flex items-center justify-center shadow-lg">
                <Shield className="w-5 h-5 text-white" />
              </div>
              <div className="absolute inset-0 rounded-lg bg-gradient-to-br from-primary/20 to-secondary/20 blur-sm -z-10"></div>
            </motion.div>
            <span className="text-lg font-bold text-foreground relative">
              PhishGuard
              <div className="absolute -bottom-1 left-0 w-full h-0.5 bg-gradient-to-r from-primary via-secondary to-primary rounded-full"></div>
            </span>
          </Link>

          {/* Mobile menu trigger */}
          <Sheet open={mobileMenuOpen} onOpenChange={setMobileMenuOpen}>
            <SheetTrigger asChild>
              <motion.div
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="relative"
              >
                <Button
                  variant="ghost"
                  size="icon"
                  className="w-10 h-10 rounded-lg bg-gradient-to-br from-primary/10 to-secondary/10 hover:from-primary/20 hover:to-secondary/20 border border-primary/20 hover:border-primary/40 text-primary hover:text-primary transition-all duration-300"
                >
                  <Menu className="w-5 h-5" />
                </Button>
                <div className="absolute inset-0 rounded-lg bg-gradient-to-br from-primary/5 to-secondary/5 blur-sm -z-10"></div>
              </motion.div>
            </SheetTrigger>
            <SheetContent side="right" className="w-80 bg-gradient-to-br from-background via-background/95 to-primary/5 border-l border-primary/20">
              <SheetHeader className="border-b border-border/30 pb-4">
                <SheetTitle className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-secondary flex items-center justify-center">
                    <Shield className="w-5 h-5 text-white" />
                  </div>
                  <span className="text-lg font-bold">PhishGuard</span>
                </SheetTitle>
                <SheetDescription className="sr-only">
                  Mobile navigation menu for PhishGuard application
                </SheetDescription>
              </SheetHeader>
              <div className="flex flex-col gap-1 mt-6">
                {mobileNavItems.map((item, index) => {
                  const Icon = item.icon
                  return (
                    <SheetClose asChild key={item.id}>
                      <motion.a
                        href={item.href}
                        className="flex items-center gap-3 py-3 px-4 text-base font-medium hover:bg-gradient-to-r hover:from-primary/10 hover:to-secondary/10 rounded-xl transition-all duration-300 border border-transparent hover:border-primary/20 group"
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                        whileHover={{ x: 4 }}
                        onClick={handleMobileNavClick}
                      >
                        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary/10 to-secondary/10 flex items-center justify-center group-hover:from-primary/20 group-hover:to-secondary/20 transition-all duration-300">
                          <Icon className="w-4 h-4 text-foreground group-hover:!text-blue-500 dark:group-hover:!text-pink-400 transition-colors duration-300" />
                        </div>
                        <span className="text-foreground group-hover:!text-blue-500 dark:group-hover:!text-pink-400 transition-colors duration-300">{item.label}</span>
                      </motion.a>
                    </SheetClose>
                  )
                })}
                
                <div className="pt-3 border-t border-border/30 mt-3">
                  {/* Dark Mode Toggle */}
                  <div className="flex items-center justify-center py-3 px-4 mb-3">
                    <DarkModeToggle />
                  </div>
                  
                  <div className="flex gap-2">
                    <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} className="flex-1">
                      <SheetClose asChild>
                        <Button variant="ghost" className="w-full h-10 rounded-xl bg-gradient-to-r from-muted/50 to-muted/30 hover:from-muted/70 hover:to-muted/50" asChild>
                          <Link href="/login" onClick={handleMobileNavClick}>Sign In</Link>
                        </Button>
                      </SheetClose>
                    </motion.div>
                    <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} className="flex-1">
                      <SheetClose asChild>
                        <Button className="w-full h-10 rounded-xl gradient-bg text-white shadow-lg hover:shadow-xl transition-all duration-300" asChild>
                          <Link href="/register" onClick={handleMobileNavClick}>Get Started</Link>
                        </Button>
                      </SheetClose>
                    </motion.div>
                  </div>
                </div>
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </motion.nav>
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
            ${isMobile ? 'bottom-8 right-4' : 'bottom-8 right-8'}
          `}
        >
          <ChevronUp className="w-6 h-6 mx-auto" />
        </motion.button>
      )}
    </AnimatePresence>
  )

  return (
    <>
      {/* Desktop Navigation */}
      <div className="hidden lg:block">
        <DesktopNavbar />
      </div>

      {/* Mobile Navigation */}
      <div className="lg:hidden">
        <MobileNavbar />
      </div>

      {/* Scroll to Top Button */}
      <ScrollToTopButton />

      {/* Spacer for fixed navbar */}
      <div className="h-16" />
    </>
  )
} 