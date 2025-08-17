"use client"

import React from 'react'
import { motion } from 'framer-motion'
import Link from 'next/link'
import { Shield, Github, Twitter, Mail, ExternalLink, Heart } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip'
import { GradientAnimatedDottedLine } from '@/components/animated-dotted-line'

const footerLinks = {
  product: {
    title: 'Product',
    links: [
      { label: 'Features', href: '#features' },
      { label: 'How it Works', href: '#how-it-works' },
      { label: 'Scanner', href: '#scanner' },
      { label: 'Pricing', href: '#pricing' }
    ]
  },
  resources: {
    title: 'Resources',
    links: [
      { label: 'Documentation', href: '/docs' },
      { label: 'API Reference', href: '/api' },
      { label: 'Help Center', href: '/help' },
      { label: 'Blog', href: '/blog' }
    ]
  },
  company: {
    title: 'Company',
    links: [
      { label: 'About Us', href: '/about' },
      { label: 'Team', href: '/team' },
      { label: 'Careers', href: '/careers' },
      { label: 'Contact', href: '/contact' }
    ]
  },
  legal: {
    title: 'Legal',
    links: [
      { label: 'Privacy Policy', href: '/privacy' },
      { label: 'Terms of Service', href: '/terms' },
      { label: 'Security', href: '/security' },
      { label: 'Cookie Policy', href: '/cookies' }
    ]
  }
}

const socialLinks = [
  { icon: Github, href: 'https://github.com/phishguard', label: 'GitHub' },
  { icon: Twitter, href: 'https://twitter.com/phishguard', label: 'Twitter' },
  { icon: Mail, href: 'mailto:hello@phishguard.com', label: 'Email' }
]

export const Footer = () => {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.3
      }
    }
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0
    }
  }

  return (
    <TooltipProvider>
      <footer className="relative bg-gradient-to-br from-background via-background/95 to-primary/5 border-t border-border/40 overflow-hidden">
        {/* Background Animation */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <motion.div
            className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-primary/10 to-secondary/10 rounded-full blur-3xl"
            animate={{
              scale: [1, 1.1, 1],
              rotate: [0, 90, 0]
            }}
            transition={{
              duration: 20,
              repeat: Infinity,
              ease: "linear"
            }}
          />
          <motion.div
            className="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-tr from-secondary/10 to-primary/10 rounded-full blur-3xl"
            animate={{
              scale: [1.1, 1, 1.1],
              rotate: [0, -90, 0]
            }}
            transition={{
              duration: 25,
              repeat: Infinity,
              ease: "linear"
            }}
          />
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 lg:py-12">
          <motion.div
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: false, margin: "-100px" }}
          >
            {/* Main Footer Content */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-8 lg:gap-8 mb-8">
              {/* Brand Section */}
              <motion.div variants={itemVariants} className="sm:col-span-2 lg:col-span-2 mb-6 sm:mb-0">
                <Link href="/" className="flex items-center gap-2 lg:gap-3 group mb-6 justify-center sm:justify-start">
                  <motion.div whileHover={{ rotate: 5 }} transition={{ duration: 0.2 }}>
                    <Shield className="w-6 h-6 lg:w-8 lg:h-8 text-primary group-hover:text-secondary transition-colors duration-300" />
                  </motion.div>
                  <span className="text-xl lg:text-2xl font-bold text-foreground relative">
                    PhishGuard
                    <div className="absolute -bottom-1 left-0 w-full h-0.5 bg-gradient-to-r from-primary via-secondary to-primary rounded-full"></div>
                  </span>
                </Link>
                <p className="text-muted-foreground text-sm lg:text-base mb-6 max-w-sm leading-relaxed text-center sm:text-left">
                  AI-powered scam detection and step-by-step recovery guidance for Myanmar. 
                  Keep yourself and your loved ones safe online.
                </p>
                
                {/* Social Links */}
                <div className="flex items-center gap-3 justify-center sm:justify-start">
                  {socialLinks.map((social, index) => {
                    const Icon = social.icon
                    return (
                      <Tooltip key={social.label}>
                        <TooltipTrigger asChild>
                          <motion.div
                            initial={{ opacity: 0, scale: 0.8 }}
                            whileInView={{ opacity: 1, scale: 1 }}
                            viewport={{ once: false, margin: "-50px" }}
                            transition={{ delay: index * 0.1 }}
                            whileHover={{ scale: 1.1 }}
                            whileTap={{ scale: 0.95 }}
                          >
                            <Button
                              variant="ghost"
                              size="icon"
                              asChild
                              className="h-10 w-10 text-muted-foreground hover:text-primary hover:bg-primary/10 transition-all duration-300"
                            >
                              <a
                                href={social.href}
                                target="_blank"
                                rel="noopener noreferrer"
                                aria-label={social.label}
                              >
                                <Icon className="w-5 h-5" />
                              </a>
                            </Button>
                          </motion.div>
                        </TooltipTrigger>
                        <TooltipContent>
                          <p>{social.label}</p>
                        </TooltipContent>
                      </Tooltip>
                    )
                  })}
                </div>
              </motion.div>

              {/* Footer Links - Mobile Stacked */}
              <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-6 lg:gap-8 sm:col-span-2 lg:col-span-4">
                {Object.entries(footerLinks).map(([key, section], sectionIndex) => (
                  <motion.div
                    key={key}
                    variants={itemVariants}
                    className="space-y-4"
                  >
                    <h3 className="font-semibold text-foreground text-sm uppercase tracking-wider text-center sm:text-left">
                      {section.title}
                    </h3>
                    <ul className="space-y-3">
                      {section.links.map((link, linkIndex) => (
                        <motion.li
                          key={link.label}
                          initial={{ opacity: 0, x: -10 }}
                          whileInView={{ opacity: 1, x: 0 }}
                          viewport={{ once: false, margin: "-50px" }}
                          transition={{ 
                            delay: (sectionIndex * 0.1) + (linkIndex * 0.05),
                            duration: 0.3
                          }}
                        >
                          <Link
                            href={link.href}
                            className="text-sm text-muted-foreground hover:text-primary transition-colors duration-300 flex items-center gap-1 group justify-center sm:justify-start"
                          >
                            {link.label}
                            {link.href.startsWith('http') && (
                              <ExternalLink className="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                            )}
                          </Link>
                        </motion.li>
                      ))}
                    </ul>
                  </motion.div>
                ))}
              </div>
            </div>

            {/* Newsletter Section */}
            <motion.div variants={itemVariants} className="mb-8">
              <Separator className="mb-8" />
              
              {/* Animated dotted line decoration */}
              <div className="flex justify-center mb-8">
                <GradientAnimatedDottedLine 
                  dots={12} 
                  duration={5}
                  className="opacity-30"
                />
              </div>
              
              <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-8">
                <div className="text-center lg:text-left">
                  <h3 className="font-semibold text-foreground mb-3 text-lg lg:text-xl">Stay Updated</h3>
                  <p className="text-sm lg:text-base text-muted-foreground max-w-md mx-auto lg:mx-0">
                    Get the latest security tips and product updates delivered to your inbox.
                  </p>
                </div>
                <div className="flex flex-col sm:flex-row gap-4 lg:gap-4 w-full lg:w-auto">
                  <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                    <Button variant="outline" size="sm" className="border-primary/20 hover:border-primary/40 w-full sm:w-auto">
                      Subscribe to Newsletter
                    </Button>
                  </motion.div>
                  <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                    <Button size="sm" className="gradient-bg text-white shadow-lg hover:shadow-xl w-full sm:w-auto">
                      Get Started Free
                    </Button>
                  </motion.div>
                </div>
              </div>
            </motion.div>

            {/* Bottom Section */}
            <motion.div variants={itemVariants}>
              <Separator className="mb-6" />
              <div className="flex flex-col gap-6 lg:flex-row lg:justify-between lg:items-center">
                <div className="flex flex-col items-center gap-4 lg:flex-row lg:gap-6 text-xs lg:text-sm text-muted-foreground text-center lg:text-left">
                  <span>© 2025 PhishGuard. All rights reserved.</span>
                  <div className="flex items-center gap-2">
                    <Heart className="w-3 h-3 lg:w-4 lg:h-4 text-red-500" />
                    <span>3D Model is Free Resource</span>
                  </div>
                </div>
                
                <div className="flex flex-col items-center gap-4 lg:flex-row lg:gap-6 text-xs lg:text-sm text-muted-foreground text-center lg:text-left">
                  <span>UI Design and AI Bot Images by Arkar Moe</span>
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                    <span>All systems operational</span>
                  </div>
                </div>
              </div>
            </motion.div>
          </motion.div>
        </div>
      </footer>
    </TooltipProvider>
  )
} 