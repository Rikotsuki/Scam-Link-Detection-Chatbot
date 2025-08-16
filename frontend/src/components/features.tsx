"use client"

import React from 'react'
import { motion } from 'framer-motion'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  Shield, 
  LifeBuoy, 
  Users, 
  BookOpen,
  ArrowRight,
  Zap,
  Eye,
  Heart
} from 'lucide-react'

const features = [
  {
    id: 1,
    icon: Shield,
    title: "Phishing Link Scanner",
    description: "Paste a link; get an instant risk score and explanation.",
    cta: "Try Scanner",
    badge: "AI-Powered",
    color: "from-primary/80 to-primary",
    bgColor: "primary/5",
    href: "#scanner"
  },
  {
    id: 2,
    icon: LifeBuoy,
    title: "Emergency Recovery Guide",
    description: "Step-by-step help for hacked accounts.",
    cta: "Open Guide",
    badge: "24/7 Available",
    color: "from-secondary/80 to-secondary",
    bgColor: "secondary/5",
    href: "#recovery"
  },
  {
    id: 3,
    icon: Users,
    title: "Community Reports",
    description: "View & submit anonymized scam reports.",
    cta: "View Reports",
    badge: "Community-Driven",
    color: "from-accent/80 to-accent",
    bgColor: "accent/5",
    href: "#reports"
  },
  {
    id: 4,
    icon: BookOpen,
    title: "Digital Safety Tips",
    description: "Short practical steps to avoid common scams.",
    cta: "Read Tips",
    badge: "Educational",
    color: "from-muted-foreground/80 to-muted-foreground",
    bgColor: "muted/5",
    href: "#tips"
  }
]

const FeatureCard = ({ feature, index }: { feature: typeof features[0], index: number }) => {
  const Icon = feature.icon

  return (
    <motion.article
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: index * 0.1 }}
      viewport={{ once: false, margin: "-50px" }}
      whileHover={{ y: -8 }}
      className="group h-full"
    >
      <Card className="h-full border-2 border-border/40 shadow-lg hover:shadow-xl transition-all duration-300 hover:border-primary/30 cursor-pointer relative overflow-hidden">
        {/* Theme-based background */}
        <div className={`absolute inset-0 bg-${feature.bgColor} group-hover:bg-${feature.bgColor.replace('/5', '/10')} transition-all duration-300`} />
        
        <CardHeader className="relative z-10">
          <div className="flex items-start justify-between mb-4">
            <div className={`p-3 rounded-xl bg-gradient-to-br ${feature.color} text-white shadow-md`}>
              <Icon className="w-6 h-6" />
            </div>
            <Badge variant="outline" className="text-xs border-primary/20">
              {feature.badge}
            </Badge>
          </div>
          
          <CardTitle className="text-xl font-bold group-hover:text-primary transition-colors duration-300">
            {feature.title}
          </CardTitle>
        </CardHeader>

        <CardContent className="relative z-10 flex flex-col justify-between flex-1">
          <p className="text-muted-foreground mb-6 leading-relaxed">
            {feature.description}
          </p>
          
          <Button 
            variant="ghost" 
            className="w-full justify-between group-hover:bg-primary/5 transition-colors duration-300"
            asChild
          >
            <a href={feature.href}>
              {feature.cta}
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform duration-300" />
            </a>
          </Button>
        </CardContent>

        {/* Hover effect */}
        <div className="absolute inset-0 ring-2 ring-transparent group-hover:ring-primary/20 rounded-xl transition-all duration-300" />
      </Card>
    </motion.article>
  )
}

export const Features = () => {
  return (
    <section className="py-24 px-4 bg-gradient-to-b from-background to-muted/20">
      <div className="max-w-7xl mx-auto">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: false, margin: "-100px" }}
          className="text-center mb-16"
        >
          <div className="flex items-center justify-center gap-2 mb-4">
            <Zap className="w-6 h-6 text-primary" />
            <Badge variant="outline">Core Features</Badge>
          </div>
          
          <h2 className="text-4xl lg:text-5xl font-bold mb-6 relative">
            Everything you need to{' '}
            <span className="text-primary relative inline-block">
              stay protected
              <div className="absolute -bottom-1 left-0 w-full h-0.5 bg-gradient-to-r from-primary to-secondary rounded-full"></div>
            </span>
          </h2>
          
          <p className="text-lg text-muted-foreground max-w-3xl mx-auto leading-relaxed">
            Our comprehensive suite of AI-powered tools helps you identify threats, 
            recover from attacks, and learn to stay safe online.
          </p>
        </motion.div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
          {features.map((feature, index) => (
            <FeatureCard key={feature.id} feature={feature} index={index} />
          ))}
        </div>

        {/* Stats Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          viewport={{ once: false, margin: "-100px" }}
          className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16"
        >
          <div className="text-center">
            <div className="text-3xl font-bold text-primary mb-2">10,000+</div>
            <div className="text-muted-foreground">Links Scanned</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-secondary mb-2">95%</div>
            <div className="text-muted-foreground">Accuracy Rate</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600 mb-2">24/7</div>
            <div className="text-muted-foreground">Protection</div>
          </div>
        </motion.div>

        {/* Trust Indicators */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.5 }}
          viewport={{ once: false, margin: "-100px" }}
          className="flex items-center justify-center gap-8 mt-12 text-sm text-muted-foreground"
        >
          <div className="flex items-center gap-2">
            <Eye className="w-4 h-4" />
            <span>Privacy First</span>
          </div>
          <div className="flex items-center gap-2">
            <Heart className="w-4 h-4" />
            <span>Community Driven</span>
          </div>
          <div className="flex items-center gap-2">
            <Shield className="w-4 h-4" />
            <span>Open Source</span>
          </div>
        </motion.div>
      </div>
    </section>
  )
} 