"use client"

import { motion } from 'framer-motion'

interface AnimatedDottedLineProps {
  className?: string
  direction?: 'horizontal' | 'vertical'
  dots?: number
  duration?: number
  color?: string
}

export const AnimatedDottedLine = ({
  className = "",
  direction = 'horizontal',
  dots = 20,
  duration = 2,
  color = "currentColor"
}: AnimatedDottedLineProps) => {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: duration / dots,
        delayChildren: 0.1
      }
    }
  }

  const dotVariants = {
    hidden: { 
      opacity: 0,
      scale: 0,
      ...(direction === 'horizontal' ? { x: -10 } : { y: -10 })
    },
    visible: { 
      opacity: 1,
      scale: 1,
      ...(direction === 'horizontal' ? { x: 0 } : { y: 0 }),
      transition: {
        type: "spring",
        stiffness: 300,
        damping: 20
      }
    }
  }

  const pulseVariants = {
    initial: { opacity: 0.3, scale: 0.8 },
    animate: {
      opacity: [0.3, 1, 0.3],
      scale: [0.8, 1.2, 0.8],
      transition: {
        duration: 2,
        repeat: Infinity,
        ease: "easeInOut"
      }
    }
  }

  return (
    <motion.div
      className={`flex ${direction === 'horizontal' ? 'flex-row' : 'flex-col'} items-center justify-center ${className}`}
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {Array.from({ length: dots }).map((_, index) => (
        <motion.div
          key={index}
          className={`w-2 h-2 rounded-full mx-1 ${direction === 'vertical' ? 'my-1' : ''}`}
          style={{ backgroundColor: color }}
          variants={dotVariants}
          whileHover={{ scale: 1.5 }}
        >
          <motion.div
            className="w-full h-full rounded-full"
            style={{ backgroundColor: color }}
            variants={pulseVariants}
            initial="initial"
            animate="animate"
            transition={{ delay: index * 0.1 }}
          />
        </motion.div>
      ))}
    </motion.div>
  )
}

// Gradient animated dotted line variant
export const GradientAnimatedDottedLine = ({
  className = "",
  direction = 'horizontal',
  dots = 20,
  duration = 2
}: Omit<AnimatedDottedLineProps, 'color'>) => {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: duration / dots,
        delayChildren: 0.1
      }
    }
  }

  const dotVariants = {
    hidden: { 
      opacity: 0,
      scale: 0,
      ...(direction === 'horizontal' ? { x: -10 } : { y: -10 })
    },
    visible: { 
      opacity: 1,
      scale: 1,
      ...(direction === 'horizontal' ? { x: 0 } : { y: 0 }),
      transition: {
        type: "spring",
        stiffness: 300,
        damping: 20
      }
    }
  }

  const gradientVariants = {
    initial: { 
      background: "linear-gradient(90deg, #3b82f6, #ec4899)",
      opacity: 0.5,
      scale: 0.8 
    },
    animate: {
      background: [
        "linear-gradient(90deg, #3b82f6, #ec4899)",
        "linear-gradient(90deg, #ec4899, #3b82f6)",
        "linear-gradient(90deg, #3b82f6, #ec4899)"
      ],
      opacity: [0.5, 1, 0.5],
      scale: [0.8, 1.2, 0.8],
      transition: {
        duration: 3,
        repeat: Infinity,
        ease: "easeInOut"
      }
    }
  }

  return (
    <motion.div
      className={`flex ${direction === 'horizontal' ? 'flex-row' : 'flex-col'} items-center justify-center ${className}`}
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {Array.from({ length: dots }).map((_, index) => (
        <motion.div
          key={index}
          className={`w-2 h-2 rounded-full mx-1 ${direction === 'vertical' ? 'my-1' : ''}`}
          variants={dotVariants}
          whileHover={{ scale: 1.5 }}
        >
          <motion.div
            className="w-full h-full rounded-full"
            variants={gradientVariants}
            initial="initial"
            animate="animate"
            transition={{ delay: index * 0.1 }}
          />
        </motion.div>
      ))}
    </motion.div>
  )
} 