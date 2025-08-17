"use client"

import { useEffect, useState, useCallback, useMemo } from 'react'
import { motion, useMotionValue, useTransform } from 'framer-motion'

export const CustomCursor = () => {
  const mouseX = useMotionValue(0)
  const mouseY = useMotionValue(0)
  const [isVisible, setIsVisible] = useState(false)
  const [isDarkMode, setIsDarkMode] = useState(false)
  const [isMobile, setIsMobile] = useState(false)

  // Mobile detection function
  const checkIsMobile = useCallback(() => {
    // Check for touch support
    const hasTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0
    
    // Check user agent
    const userAgent = navigator.userAgent || navigator.vendor || (window as any).opera
    const mobileRegex = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i
    const isMobileUserAgent = mobileRegex.test(userAgent)
    
    // Check screen size - more lenient for desktop
    const isSmallScreen = window.innerWidth <= 768
    
    // Check for specific mobile indicators - more precise detection
    // Only consider mobile if it's actually a mobile device, not just touch-capable
    const isMobileIndicator = isMobileUserAgent || (hasTouch && isSmallScreen)
    
    return isMobileIndicator
  }, [])

  // Optimized mouse position update with throttling
  const updateMousePosition = useCallback((e: MouseEvent) => {
    if (!isMobile) {
      mouseX.set(e.clientX)
      mouseY.set(e.clientY)
      setIsVisible(true)
    }
  }, [mouseX, mouseY, isMobile])

  // Optimized theme check
  const checkTheme = useCallback(() => {
    setIsDarkMode(document.documentElement.classList.contains('dark'))
  }, [])

  // Memoized cursor colors
  const cursorColors = useMemo(() => ({
    light: 'rgb(142, 197, 255)',
    dark: '#f472b6'
  }), [])

  // Memoized filter styles
  const filterStyles = useMemo(() => ({
    light: `drop-shadow(0 0 8px ${cursorColors.light}) drop-shadow(0 0 16px ${cursorColors.light})`,
    dark: `drop-shadow(0 0 8px ${cursorColors.dark}) drop-shadow(0 0 16px ${cursorColors.dark})`
  }), [cursorColors])

  // Separate effect to handle cursor visibility when switching between mobile/desktop
  useEffect(() => {
    if (!isMobile && !isVisible) {
      setIsVisible(true)
    }
  }, [isMobile, isVisible])

  useEffect(() => {
    // Check if mobile on mount and resize
    const handleResize = () => {
      const newIsMobile = checkIsMobile()
      setIsMobile(newIsMobile)
    }

    // Initial checks
    handleResize()
    checkTheme()

    // Early return if mobile - don't add any event listeners
    if (isMobile) {
      return
    }

    const handleMouseLeave = () => setIsVisible(false)
    const handleMouseEnter = () => setIsVisible(true)

    // Optimized theme observer
    const observer = new MutationObserver(checkTheme)
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['class']
    })

    // Throttled mouse move listener
    let ticking = false
    const throttledMouseMove = (e: MouseEvent) => {
      if (!ticking && !isMobile) {
        requestAnimationFrame(() => {
          updateMousePosition(e)
          ticking = false
        })
        ticking = true
      }
    }

    // Add event listeners only for non-mobile devices
    window.addEventListener('mousemove', throttledMouseMove, { passive: true })
    document.addEventListener('mouseleave', handleMouseLeave)
    document.addEventListener('mouseenter', handleMouseEnter)
    window.addEventListener('resize', handleResize)

    return () => {
      window.removeEventListener('mousemove', throttledMouseMove)
      document.removeEventListener('mouseleave', handleMouseLeave)
      document.removeEventListener('mouseenter', handleMouseEnter)
      window.removeEventListener('resize', handleResize)
      observer.disconnect()
    }
  }, [updateMousePosition, checkTheme, checkIsMobile, isMobile])

  // Don't render cursor on mobile devices
  if (isMobile) {
    return null
  }

  return (
    <>
      {/* Main cursor arrow */}
      <motion.div
        className="fixed top-0 left-0 w-6 h-6 pointer-events-none z-[9999]"
        style={{
          x: mouseX,
          y: mouseY,
          scale: isVisible ? 1 : 0,
          opacity: isVisible ? 1 : 0,
        }}
        transition={{
          type: "spring",
          stiffness: 500,
          damping: 28,
          mass: 0.5,
        }}
      >
        <svg
          viewBox="0 0 24 24"
          fill="none"
          className="w-full h-full"
          style={{
            filter: isDarkMode ? filterStyles.dark : filterStyles.light,
            transform: 'translate(-3px, -3px)'
          }}
        >
          <path
            d="M3 3L21 12L3 21V3Z"
            style={{
              fill: isDarkMode ? cursorColors.dark : cursorColors.light,
              stroke: isDarkMode ? cursorColors.dark : cursorColors.light,
              strokeWidth: '0.5'
            }}
          />
        </svg>
      </motion.div>
    </>
  )
} 