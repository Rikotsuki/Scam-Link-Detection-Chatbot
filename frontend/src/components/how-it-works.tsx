"use client"

import React from 'react'
import { motion } from 'framer-motion'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  Search, 
  Brain, 
  ShieldCheck, 
  ArrowRight, 
  Cpu, 
  Database,
  AlertTriangle
} from 'lucide-react'

const steps = [
  {
    id: 1,
    icon: Search,
    title: "Paste & Scan",
    description: "AI + RAG + threat APIs analyze the link",
    details: [
      "URL structure analysis",
      "Domain reputation check", 
      "Machine learning classification",
      "Real-time threat intelligence"
    ],
    tech: "AI-Powered Analysis",
    color: "from-primary/80 to-primary",
    bgColor: "primary/5"
  },
  {
    id: 2,
    icon: Brain,
    title: "Get a Clear Score",
    description: "Easy verdict + reasons + confidence",
    details: [
      "Risk score (0-100)",
      "Plain English explanation",
      "Confidence percentage",
      "Detailed reasoning"
    ],
    tech: "Smart Interpretation",
    color: "from-secondary/80 to-secondary",
    bgColor: "secondary/5"
  },
  {
    id: 3,
    icon: ShieldCheck,
    title: "Recover or Report",
    description: "Recovery checklist + report option",
    details: [
      "Step-by-step recovery guide",
      "Emergency contact information",
      "Report to community database",
      "Prevention tips for future"
    ],
    tech: "Action-Oriented Support",
    color: "from-accent/80 to-accent",
    bgColor: "accent/5"
  }
]

const StepCard = ({ step, index, isLast }: { 
  step: typeof steps[0], 
  index: number, 
  isLast: boolean 
}) => {
  const Icon = step.icon

  return (
    <div className="relative">
      {/* Timeline connector - desktop */}
      {!isLast && (
        <div className="hidden lg:block absolute top-1/2 left-full transform -translate-y-1/2 w-16 h-0.5 bg-gradient-to-r from-primary to-transparent z-10">
          <ArrowRight className="absolute right-0 top-1/2 transform -translate-y-1/2 translate-x-2 w-4 h-4 text-primary" />
        </div>
      )}

      {/* Timeline connector - mobile */}
      {!isLast && (
        <div className="lg:hidden absolute top-full left-1/2 transform -translate-x-1/2 w-0.5 h-16 bg-gradient-to-b from-primary to-transparent z-10">
          <ArrowRight className="absolute bottom-0 left-1/2 transform -translate-x-1/2 translate-y-2 rotate-90 w-4 h-4 text-primary" />
        </div>
      )}

      <motion.div
        initial={{ opacity: 0, y: 50 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: index * 0.2 }}
        viewport={{ once: false, margin: "-50px" }}
        className="relative z-20"
      >
        <Card className="h-full border-2 border-border/40 shadow-xl hover:shadow-2xl hover:border-primary/30 transition-all duration-300 relative overflow-hidden group">
          {/* Theme-based background */}
          <div className={`absolute inset-0 bg-${step.bgColor} group-hover:bg-${step.bgColor.replace('/5', '/10')} transition-all duration-300`} />
          
          <CardContent className="p-8 relative z-10">
            {/* Step number */}
            <div className="flex items-center justify-between mb-6">
              <div className={`w-12 h-12 rounded-full bg-gradient-to-br ${step.color} text-white flex items-center justify-center font-bold text-lg shadow-lg`}>
                {step.id}
              </div>
              <Badge variant="outline" className="text-xs border-primary/20">
                {step.tech}
              </Badge>
            </div>

            {/* Icon */}
            <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${step.color} text-white flex items-center justify-center mb-6 shadow-lg group-hover:scale-105 transition-transform duration-300`}>
              <Icon className="w-8 h-8" />
            </div>

            {/* Content */}
            <div className="space-y-4">
              <h3 className="text-2xl font-bold text-foreground group-hover:text-primary transition-colors duration-300">
                {step.title}
              </h3>
              
              <p className="text-muted-foreground text-lg leading-relaxed">
                {step.description}
              </p>

              {/* Details list */}
              <div className="space-y-2">
                <h4 className="font-semibold text-sm text-foreground/80 uppercase tracking-wider">
                  Key Features
                </h4>
                <ul className="space-y-2">
                  {step.details.map((detail, detailIndex) => (
                    <li key={detailIndex} className="flex items-start gap-3 text-sm text-muted-foreground">
                      <div className={`w-1.5 h-1.5 rounded-full bg-gradient-to-r ${step.color} mt-2 flex-shrink-0`} />
                      {detail}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  )
}

export const HowItWorks = () => {
  return (
    <section id="how-it-works" className="py-24 px-4 bg-gradient-to-b from-muted/20 to-background">
      <div className="max-w-7xl mx-auto">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: false, margin: "-100px" }}
          className="text-center mb-20"
        >
          <div className="flex items-center justify-center gap-2 mb-6">
            <Cpu className="w-6 h-6 text-primary" />
            <Badge variant="outline">How It Works</Badge>
          </div>
          
          <h2 className="text-4xl lg:text-5xl font-bold mb-6 relative">
            <span className="text-primary relative inline-block">
              Three Simple Steps
              <div className="absolute -bottom-1 left-0 w-full h-0.5 bg-gradient-to-r from-primary to-secondary rounded-full"></div>
            </span>{' '}
            to Protection
          </h2>
          
          <p className="text-lg text-muted-foreground max-w-3xl mx-auto leading-relaxed">
            Our advanced AI system combines multiple detection methods to give you 
            instant, accurate results you can trust.
          </p>
        </motion.div>

        {/* Timeline Steps */}
        <div className="grid lg:grid-cols-3 gap-8 lg:gap-4 mb-20">
          {steps.map((step, index) => (
            <StepCard 
              key={step.id} 
              step={step} 
              index={index} 
              isLast={index === steps.length - 1}
            />
          ))}
        </div>

        {/* Technology Stack Preview */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          viewport={{ once: false, margin: "-100px" }}
          className="bg-gradient-to-r from-primary/5 to-secondary/5 rounded-2xl p-8 border border-primary/10"
        >
          <div className="text-center mb-8">
            <h3 className="text-2xl font-bold mb-4">Powered by Advanced AI</h3>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Our system combines multiple AI technologies and threat intelligence sources 
              for the most accurate protection available.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mx-auto mb-4">
                <Brain className="w-6 h-6 text-primary" />
              </div>
              <h4 className="font-semibold mb-2">Machine Learning</h4>
              <p className="text-sm text-muted-foreground">
                Advanced pattern recognition trained on millions of URLs
              </p>
            </div>

            <div className="text-center">
              <div className="w-12 h-12 rounded-xl bg-secondary/10 flex items-center justify-center mx-auto mb-4">
                <Database className="w-6 h-6 text-secondary" />
              </div>
              <h4 className="font-semibold mb-2">RAG System</h4>
              <p className="text-sm text-muted-foreground">
                Real-time knowledge retrieval from threat databases
              </p>
            </div>

            <div className="text-center">
              <div className="w-12 h-12 rounded-xl bg-green-500/10 flex items-center justify-center mx-auto mb-4">
                <AlertTriangle className="w-6 h-6 text-green-600" />
              </div>
              <h4 className="font-semibold mb-2">Threat Intelligence</h4>
              <p className="text-sm text-muted-foreground">
                Integration with global security APIs and feeds
              </p>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
} 