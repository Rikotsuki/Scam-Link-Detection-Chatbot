"use client"

import { useState, useEffect } from 'react'

export const useLoading = () => {
  const [isLoading, setIsLoading] = useState(true)
  const [isOnline, setIsOnline] = useState(true)

  useEffect(() => {
    // Check if page is fully loaded
    const handleLoad = () => {
      // Simulate minimum loading time for better UX
      setTimeout(() => {
        setIsLoading(false)
      }, 2000) // Minimum 2 seconds loading time
    }

    // Check online status
    const handleOnline = () => {
      setIsOnline(true)
    }

    const handleOffline = () => {
      setIsOnline(false)
      setIsLoading(true) // Show loading when going offline
    }

    // Check if page is already loaded
    if (document.readyState === 'complete') {
      handleLoad()
    } else {
      window.addEventListener('load', handleLoad)
    }

    // Network status listeners
    window.addEventListener('online', handleOnline)
    window.addEventListener('offline', handleOffline)

    // Check initial online status
    setIsOnline(navigator.onLine)

    return () => {
      window.removeEventListener('load', handleLoad)
      window.removeEventListener('online', handleOnline)
      window.removeEventListener('offline', handleOffline)
    }
  }, [])

  // Function to manually trigger loading (for route changes, etc.)
  const startLoading = () => {
    setIsLoading(true)
  }

  const stopLoading = () => {
    setIsLoading(false)
  }

  return {
    isLoading,
    isOnline,
    startLoading,
    stopLoading
  }
} 