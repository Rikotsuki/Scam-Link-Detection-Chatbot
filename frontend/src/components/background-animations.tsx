"use client"

import { motion } from 'framer-motion'

export const BackgroundAnimations = () => {
  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
      {/* Floating geometric shapes */}
      <motion.div
        className="absolute top-20 left-10 w-8 h-8 bg-blue-500/20 rounded-full"
        animate={{
          y: [0, -30, 0],
          x: [0, 20, 0],
          rotate: [0, 180, 360],
        }}
        transition={{
          duration: 8,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />
      
      <motion.div
        className="absolute top-40 right-20 w-6 h-6 bg-pink-500/20 rounded-lg"
        animate={{
          y: [0, 40, 0],
          x: [0, -30, 0],
          rotate: [0, -180, -360],
        }}
        transition={{
          duration: 10,
          repeat: Infinity,
          ease: "easeInOut",
          delay: 1
        }}
      />
      
      <motion.div
        className="absolute bottom-40 left-1/4 w-10 h-10 bg-purple-500/20 rounded-full"
        animate={{
          y: [0, -50, 0],
          x: [0, 40, 0],
          scale: [1, 1.2, 1],
        }}
        transition={{
          duration: 12,
          repeat: Infinity,
          ease: "easeInOut",
          delay: 2
        }}
      />

      {/* Passing objects from left to right */}
      <motion.div
        className="absolute top-1/4 w-4 h-4 bg-blue-500/30 rounded-full"
        animate={{
          x: [-100, "100vw"],
        }}
        transition={{
          duration: 15,
          repeat: Infinity,
          ease: "linear"
        }}
      />
      
      <motion.div
        className="absolute top-1/3 w-6 h-6 bg-pink-500/30 rounded-lg"
        animate={{
          x: [-100, "100vw"],
        }}
        transition={{
          duration: 20,
          repeat: Infinity,
          ease: "linear",
          delay: 3
        }}
      />
      
      <motion.div
        className="absolute top-1/2 w-3 h-3 bg-purple-500/30 rounded-full"
        animate={{
          x: [-100, "100vw"],
        }}
        transition={{
          duration: 18,
          repeat: Infinity,
          ease: "linear",
          delay: 6
        }}
      />

      {/* Passing objects from right to left */}
      <motion.div
        className="absolute bottom-1/4 w-5 h-5 bg-green-500/30 rounded-lg"
        animate={{
          x: ["100vw", -100],
        }}
        transition={{
          duration: 16,
          repeat: Infinity,
          ease: "linear",
          delay: 2
        }}
      />
      
      <motion.div
        className="absolute bottom-1/3 w-4 h-4 bg-yellow-500/30 rounded-full"
        animate={{
          x: ["100vw", -100],
        }}
        transition={{
          duration: 22,
          repeat: Infinity,
          ease: "linear",
          delay: 8
        }}
      />

      {/* Floating particles */}
      <motion.div
        className="absolute top-1/6 left-1/3 w-2 h-2 bg-blue-500/40 rounded-full"
        animate={{
          y: [0, -20, 0],
          opacity: [0.4, 1, 0.4],
        }}
        transition={{
          duration: 4,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />
      
      <motion.div
        className="absolute top-2/3 right-1/4 w-2 h-2 bg-pink-500/40 rounded-full"
        animate={{
          y: [0, -15, 0],
          opacity: [0.4, 1, 0.4],
        }}
        transition={{
          duration: 5,
          repeat: Infinity,
          ease: "easeInOut",
          delay: 1
        }}
      />
      
      <motion.div
        className="absolute bottom-1/6 left-2/3 w-2 h-2 bg-purple-500/40 rounded-full"
        animate={{
          y: [0, -25, 0],
          opacity: [0.4, 1, 0.4],
        }}
        transition={{
          duration: 6,
          repeat: Infinity,
          ease: "easeInOut",
          delay: 2
        }}
      />

      {/* Large floating orbs */}
      <motion.div
        className="absolute top-10 right-1/4 w-16 h-16 bg-blue-500/10 rounded-full"
        animate={{
          y: [0, -40, 0],
          x: [0, 30, 0],
          scale: [1, 1.1, 1],
        }}
        transition={{
          duration: 15,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />
      
      <motion.div
        className="absolute bottom-20 left-1/3 w-20 h-20 bg-pink-500/10 rounded-full"
        animate={{
          y: [0, 50, 0],
          x: [0, -40, 0],
          scale: [1, 0.9, 1],
        }}
        transition={{
          duration: 18,
          repeat: Infinity,
          ease: "easeInOut",
          delay: 5
        }}
      />

      {/* Diagonal passing objects */}
      <motion.div
        className="absolute top-0 left-0 w-3 h-3 bg-green-500/30 rounded-full"
        animate={{
          x: [0, "100vw"],
          y: [0, "100vh"],
        }}
        transition={{
          duration: 25,
          repeat: Infinity,
          ease: "linear"
        }}
      />
      
      <motion.div
        className="absolute top-0 right-0 w-4 h-4 bg-yellow-500/30 rounded-lg"
        animate={{
          x: [0, "-100vw"],
          y: [0, "100vh"],
        }}
        transition={{
          duration: 30,
          repeat: Infinity,
          ease: "linear",
          delay: 10
        }}
      />
    </div>
  )
} 