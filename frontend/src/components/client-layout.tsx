"use client"

import { CustomCursor } from '@/components/custom-cursor'
import { BackgroundAnimations } from '@/components/background-animations'

interface ClientLayoutProps {
  children: React.ReactNode
}

export const ClientLayout = ({ children }: ClientLayoutProps) => {
  return (
    <>
      <BackgroundAnimations />
      <CustomCursor />
      {children}
    </>
  )
} 