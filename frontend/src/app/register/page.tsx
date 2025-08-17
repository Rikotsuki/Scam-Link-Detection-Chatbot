"use client"

import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useForm } from 'react-hook-form'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Progress } from '@/components/ui/progress'
import { 
  Form, 
  FormControl, 
  FormField, 
  FormItem, 
  FormLabel, 
  FormMessage,
  FormDescription
} from '@/components/ui/form'
import { Badge } from '@/components/ui/badge'
import { 
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle
} from '@/components/ui/dialog'
import { 
  Shield, 
  Mail, 
  Lock, 
  Eye, 
  EyeOff, 
  ArrowLeft,
  Chrome,
  CheckCircle,
  User,
  Phone,
  Check,
  AlertCircle
} from 'lucide-react'
import { GradientAnimatedDottedLine } from '@/components/animated-dotted-line'
import { authApi } from '@/lib/api'

interface RegisterFormData {
  firstName: string
  lastName: string
  userName: string
  email: string
  password: string
  confirmPassword: string
  phone?: string
  acceptPolicy: boolean
}

// Password strength calculator
const calculatePasswordStrength = (password: string) => {
  let score = 0
  let feedback = []

  if (password.length >= 8) {
    score += 25
  } else {
    feedback.push('Use at least 8 characters')
  }

  if (/[A-Z]/.test(password)) {
    score += 25
  } else {
    feedback.push('Add uppercase letters')
  }

  if (/[a-z]/.test(password)) {
    score += 25
  } else {
    feedback.push('Add lowercase letters')
  }

  if (/\d/.test(password)) {
    score += 25
  } else {
    feedback.push('Add numbers')
  }

  if (/[^A-Za-z0-9]/.test(password)) {
    score += 10
  } else {
    feedback.push('Add special characters')
  }

  return { score: Math.min(score, 100), feedback }
}

export default function RegisterPage() {
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [showOnboarding, setShowOnboarding] = useState(false)
  const [passwordStrength, setPasswordStrength] = useState({ score: 0, feedback: [] as string[] })
  const [currentStep, setCurrentStep] = useState(1)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()
  
  const form = useForm<RegisterFormData>({
    defaultValues: {
      firstName: '',
      lastName: '',
      userName: '',
      email: '',
      password: '',
      confirmPassword: '',
      phone: '',
      acceptPolicy: false
    }
  })

  const password = form.watch('password')

  React.useEffect(() => {
    if (password) {
      setPasswordStrength(calculatePasswordStrength(password))
    }
  }, [password])

  const onSubmit = async (data: RegisterFormData) => {
    setIsLoading(true)
    setError(null)
    console.log('Analytics: auth_signup_attempt')
    
    try {
      const result = await authApi.register({
        firstName: data.firstName,
        lastName: data.lastName,
        userName: data.userName,
        email: data.email,
        password: data.password
      })
      
      if (result.error) {
        setError(result.error)
      } else {
        // Store token
        localStorage.setItem('token', result.data?.token || '')
        localStorage.setItem('user', JSON.stringify({
          firstName: data.firstName,
          lastName: data.lastName,
          userName: data.userName,
          email: data.email
        }))
        
        console.log('Registration successful:', result.data)
        setIsLoading(false)
        setShowOnboarding(true)
      }
    } catch (err) {
      setError('Network error. Please try again.')
      console.error('Registration error:', err)
      setIsLoading(false)
    }
  }

  const nextStep = () => {
    if (currentStep === 1) {
      // Validate step 1 fields
      const step1Fields = ['firstName', 'lastName', 'username']
      const step1Valid = step1Fields.every(field => {
        const value = form.getValues(field as keyof RegisterFormData)
        return value && value.toString().length > 0
      })
      
      if (step1Valid) {
        setCurrentStep(2)
      } else {
        step1Fields.forEach(field => {
          form.trigger(field as keyof RegisterFormData)
        })
      }
    }
  }

  const prevStep = () => {
    setCurrentStep(1)
  }

  const getPasswordStrengthColor = (score: number) => {
    if (score < 30) return 'bg-red-500'
    if (score < 70) return 'bg-yellow-500'
    if (score < 90) return 'bg-blue-500'
    return 'bg-green-500'
  }

  const getPasswordStrengthText = (score: number) => {
    if (score < 30) return 'Weak'
    if (score < 70) return 'Fair'
    if (score < 90) return 'Good'
    return 'Strong'
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary/5 via-background to-secondary/5 flex items-center justify-center p-4">
      {/* Back to Home */}
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        className="absolute top-6 left-6"
      >
        <Button variant="ghost" asChild>
          <Link href="/" className="flex items-center gap-2">
            <ArrowLeft className="w-4 h-4" />
            Back to Home
          </Link>
        </Button>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="w-full max-w-md"
      >
        <Card className="shadow-2xl border-0">
          <CardHeader className="text-center pb-3">
            <div className="text-center mb-3">
              <motion.div 
                className="mx-auto w-16 h-16 bg-gradient-to-br from-primary to-secondary rounded-2xl flex items-center justify-center mb-6 shadow-lg"
                initial={{ scale: 0, rotate: -180 }}
                animate={{ scale: 1, rotate: 0 }}
                transition={{ type: "spring", stiffness: 260, damping: 20 }}
              >
                <Shield className="w-8 h-8 text-white" />
              </motion.div>
              
              <motion.h1 
                className="text-2xl font-bold mb-2 text-foreground relative"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
              >
                <span className="relative">
                  Join PhishGuard today
                  <div className="absolute -bottom-1 left-0 w-full h-0.5 bg-gradient-to-r from-primary via-secondary to-primary rounded-full"></div>
                </span>
              </motion.h1>
              
              <motion.p 
                className="text-muted-foreground"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
              >
                Create your account to start protecting yourself from online threats
              </motion.p>
            </div>
          </CardHeader>

          <CardContent className="space-y-2">
            {error && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="p-3 bg-destructive/10 border border-destructive/20 rounded-lg flex items-center gap-2 text-destructive"
              >
                <AlertCircle className="w-4 h-4" />
                <span className="text-sm">{error}</span>
              </motion.div>
            )}
            
            {/* Progress Indicator */}
            <div className="flex items-center justify-between mb-1">
              <div className="flex items-center gap-2">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                  currentStep >= 1 ? 'bg-primary text-white' : 'bg-muted text-muted-foreground'
                }`}>
                  1
                </div>
                <span className={`text-sm ${currentStep >= 1 ? 'text-foreground' : 'text-muted-foreground'}`}>
                  Account Details
                </span>
              </div>
              <div className="flex-1 mx-4 relative">
                <div className="h-px bg-border"></div>
                <div className="absolute inset-0 flex items-center justify-center">
                  <GradientAnimatedDottedLine 
                    dots={8} 
                    duration={3}
                    className="opacity-60"
                  />
                </div>
              </div>
              <div className="flex items-center gap-2">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                  currentStep >= 2 ? 'bg-primary text-white' : 'bg-muted text-muted-foreground'
                }`}>
                  2
                </div>
                <span className={`text-sm ${currentStep >= 2 ? 'text-foreground' : 'text-muted-foreground'}`}>
                  Additional Info
                </span>
              </div>
            </div>

            <Form {...form}>
              <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                <AnimatePresence mode="wait">
                  {currentStep === 1 ? (
                    <motion.div
                      key="step1"
                      initial={{ opacity: 0, x: 20 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: -20 }}
                      transition={{ duration: 0.3 }}
                      className="space-y-3"
                    >
                      {/* First Name */}
                      <FormField
                        control={form.control}
                        name="firstName"
                        rules={{
                          required: 'First name is required',
                          minLength: {
                            value: 2,
                            message: 'First name must be at least 2 characters'
                          }
                        }}
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel className="flex items-center gap-2">
                              <User className="w-4 h-4" />
                              First Name
                            </FormLabel>
                            <FormControl>
                              <Input
                                {...field}
                                placeholder="John"
                                disabled={isLoading}
                              />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />

                      {/* Last Name */}
                      <FormField
                        control={form.control}
                        name="lastName"
                        rules={{
                          required: 'Last name is required',
                          minLength: {
                            value: 2,
                            message: 'Last name must be at least 2 characters'
                          }
                        }}
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel className="flex items-center gap-2">
                              <User className="w-4 h-4" />
                              Last Name
                            </FormLabel>
                            <FormControl>
                              <Input
                                {...field}
                                placeholder="Doe"
                                disabled={isLoading}
                              />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />

                      {/* Username */}
                      <FormField
                        control={form.control}
                        name="userName"
                        rules={{
                          required: 'Username is required',
                          minLength: {
                            value: 3,
                            message: 'Username must be at least 3 characters'
                          },
                          maxLength: {
                            value: 20,
                            message: 'Username must be less than 20 characters'
                          },
                          pattern: {
                            value: /^[a-zA-Z0-9_]+$/,
                            message: 'Username can only contain letters, numbers, and underscores'
                          },
                          validate: (value) => {
                            if (typeof value === 'string') {
                              if (value.startsWith('_')) {
                                return 'Username cannot start with an underscore'
                              }
                              if (value.endsWith('_')) {
                                return 'Username cannot end with an underscore'
                              }
                              if (/_{2,}/.test(value)) {
                                return 'Username cannot contain consecutive underscores'
                              }
                            }
                            return true
                          }
                        }}
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel className="flex items-center gap-2">
                              <User className="w-4 h-4" />
                              Username
                            </FormLabel>
                            <FormControl>
                              <Input
                                {...field}
                                placeholder="johndoe123"
                                disabled={isLoading}
                              />
                            </FormControl>
                            <FormDescription className="text-xs">
                              Letters, numbers, and underscores only (3-20 characters)
                            </FormDescription>
                            <FormMessage />
                          </FormItem>
                        )}
                      />

                      {/* Next Button */}
                      <Button
                        type="button"
                        onClick={nextStep}
                        className="w-full gradient-bg text-white"
                        disabled={isLoading}
                      >
                        Next Step
                      </Button>
                    </motion.div>
                  ) : (
                    <motion.div
                      key="step2"
                      initial={{ opacity: 0, x: 20 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: -20 }}
                      transition={{ duration: 0.3 }}
                      className="space-y-3"
                    >
                      {/* Email */}
                      <FormField
                        control={form.control}
                        name="email"
                        rules={{
                          required: 'Email is required',
                          pattern: {
                            value: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
                            message: 'Please enter a valid email address'
                          },
                          validate: (value) => {
                            if (value) {
                              const email = value.toLowerCase()
                              if (email.includes('..')) {
                                return 'Email cannot contain consecutive dots'
                              }
                              if (email.startsWith('.') || email.endsWith('.')) {
                                return 'Email cannot start or end with a dot'
                              }
                              if (email.includes('@.') || email.includes('.@')) {
                                return 'Invalid email format'
                              }
                              const [localPart, domain] = email.split('@')
                              if (localPart.length > 64 || domain.length > 253) {
                                return 'Email address is too long'
                              }
                            }
                            return true
                          }
                        }}
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel className="flex items-center gap-2">
                              <Mail className="w-4 h-4" />
                              Email Address
                            </FormLabel>
                            <FormControl>
                              <Input
                                {...field}
                                type="email"
                                placeholder="your.email@example.com"
                                disabled={isLoading}
                              />
                            </FormControl>
                            <FormDescription className="text-xs">
                              Enter a valid email address for account verification
                            </FormDescription>
                            <FormMessage />
                          </FormItem>
                        )}
                      />

                      {/* Password */}
                      <FormField
                        control={form.control}
                        name="password"
                        rules={{
                          required: 'Password is required',
                          minLength: {
                            value: 8,
                            message: 'Password must be at least 8 characters'
                          },
                          maxLength: {
                            value: 128,
                            message: 'Password must be less than 128 characters'
                          },
                          validate: (value) => {
                            if (value) {
                              if (!/[A-Z]/.test(value)) {
                                return 'Password must contain at least one uppercase letter'
                              }
                              if (!/[a-z]/.test(value)) {
                                return 'Password must contain at least one lowercase letter'
                              }
                              if (!/\d/.test(value)) {
                                return 'Password must contain at least one number'
                              }
                              if (!/[!@#$%^&*(),.?":{}|<>]/.test(value)) {
                                return 'Password must contain at least one special character'
                              }
                              if (/\s/.test(value)) {
                                return 'Password cannot contain spaces'
                              }
                            }
                            return true
                          }
                        }}
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel className="flex items-center gap-2">
                              <Lock className="w-4 h-4" />
                              Password
                            </FormLabel>
                            <FormControl>
                              <div className="relative">
                                <Input
                                  {...field}
                                  type={showPassword ? 'text' : 'password'}
                                  placeholder="Create a strong password"
                                  disabled={isLoading}
                                />
                                <Button
                                  type="button"
                                  variant="ghost"
                                  size="icon"
                                  className="absolute right-2 top-0 h-full px-3 hover:bg-transparent"
                                  onClick={() => setShowPassword(!showPassword)}
                                >
                                  {showPassword ? (
                                    <EyeOff className="w-4 h-4 text-muted-foreground" />
                                  ) : (
                                    <Eye className="w-4 h-4 text-muted-foreground" />
                                  )}
                                </Button>
                              </div>
                            </FormControl>
                            
                            {/* Password Strength Meter */}
                            {password && (
                              <div className="space-y-2">
                                <div className="flex items-center justify-between">
                                  <span className="text-xs text-muted-foreground">
                                    Password strength:
                                  </span>
                                  <span className={`text-xs font-medium ${
                                    passwordStrength.score < 30 ? 'text-red-600' :
                                    passwordStrength.score < 70 ? 'text-yellow-600' :
                                    passwordStrength.score < 90 ? 'text-blue-600' :
                                    'text-green-600'
                                  }`}>
                                    {getPasswordStrengthText(passwordStrength.score)}
                                  </span>
                                </div>
                                <Progress
                                  value={passwordStrength.score}
                                  className="h-2"
                                />
                                {passwordStrength.feedback.length > 0 && (
                                  <ul className="text-xs text-muted-foreground space-y-1">
                                    {passwordStrength.feedback.map((item, index) => (
                                      <li key={index} className="flex items-center gap-2">
                                        <AlertCircle className="w-3 h-3" />
                                        {item}
                                      </li>
                                    ))}
                                  </ul>
                                )}
                              </div>
                            )}
                            <FormMessage />
                          </FormItem>
                        )}
                      />

                      {/* Confirm Password */}
                      <FormField
                        control={form.control}
                        name="confirmPassword"
                        rules={{
                          required: 'Please confirm your password',
                          validate: (value) =>
                            value === password || 'Passwords do not match'
                        }}
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel className="flex items-center gap-2">
                              <Lock className="w-4 h-4" />
                              Confirm Password
                            </FormLabel>
                            <FormControl>
                              <div className="relative">
                                <Input
                                  {...field}
                                  type={showConfirmPassword ? 'text' : 'password'}
                                  placeholder="Confirm your password"
                                  disabled={isLoading}
                                />
                                <Button
                                  type="button"
                                  variant="ghost"
                                  size="icon"
                                  className="absolute right-2 top-0 h-full px-3 hover:bg-transparent"
                                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                                >
                                  {showConfirmPassword ? (
                                    <EyeOff className="w-4 h-4 text-muted-foreground" />
                                  ) : (
                                    <Eye className="w-4 h-4 text-muted-foreground" />
                                  )}
                                </Button>
                              </div>
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />

                      {/* Phone (Optional) */}
                      <FormField
                        control={form.control}
                        name="phone"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel className="flex items-center gap-2">
                              <Phone className="w-4 h-4" />
                              Phone Number
                              <Badge variant="secondary" className="text-xs">Optional</Badge>
                            </FormLabel>
                            <FormControl>
                              <Input
                                {...field}
                                type="tel"
                                placeholder="+95 123 456 789"
                                disabled={isLoading}
                              />
                            </FormControl>
                            <FormDescription className="text-xs">
                              For account recovery and security alerts
                            </FormDescription>
                            <FormMessage />
                          </FormItem>
                        )}
                      />

                      {/* Terms and Privacy */}
                      <FormField
                        control={form.control}
                        name="acceptPolicy"
                        rules={{
                          required: 'You must accept the terms and privacy policy'
                        }}
                        render={({ field }) => (
                          <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                            <FormControl>
                              <input
                                type="checkbox"
                                checked={field.value}
                                onChange={field.onChange}
                                className="rounded border-gray-300 mt-1"
                                disabled={isLoading}
                              />
                            </FormControl>
                            <div className="space-y-1 leading-none">
                              <FormLabel className="text-sm leading-relaxed">
                                I accept the{' '}
                                <Link href="/terms" className="text-primary hover:underline">
                                  Terms of Service
                                </Link>{' '}
                                and{' '}
                                <Link href="/privacy" className="text-primary hover:underline">
                                  Privacy Policy
                                </Link>
                              </FormLabel>
                              <FormMessage />
                            </div>
                          </FormItem>
                        )}
                      />

                      {/* Navigation Buttons */}
                      <div className="flex gap-3">
                        <Button
                          type="button"
                          variant="outline"
                          onClick={prevStep}
                          className="flex-1"
                          disabled={isLoading}
                        >
                          Back
                        </Button>
                        <Button
                          type="submit"
                          className="flex-1 gradient-bg text-white"
                          disabled={isLoading || !form.watch('acceptPolicy')}
                        >
                          {isLoading ? 'Creating Account...' : 'Create Account'}
                        </Button>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </form>
            </Form>

            {/* Divider */}
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t" />
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-background px-2 text-muted-foreground">
                  Or continue with
                </span>
              </div>
            </div>

            {/* Google Sign Up */}
            <Button variant="outline" className="w-full" disabled>
              <Chrome className="w-4 h-4 mr-2" />
              Continue with Google
              <Badge variant="secondary" className="ml-2 text-xs">
                Coming Soon
              </Badge>
            </Button>
          </CardContent>
        </Card>

        {/* Sign In Link */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          className="text-center mt-6"
        >
          <p className="text-muted-foreground">
            Already have an account?{' '}
            <Link href="/login" className="text-primary hover:underline font-medium">
              Sign in
            </Link>
          </p>
        </motion.div>
      </motion.div>

      {/* Onboarding Modal */}
      <Dialog open={showOnboarding} onOpenChange={setShowOnboarding}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader className="text-center">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: "spring", duration: 0.6 }}
              className="flex justify-center mb-4"
            >
              <div className="w-16 h-16 rounded-full gradient-bg flex items-center justify-center">
                <CheckCircle className="w-8 h-8 text-white" />
              </div>
            </motion.div>
            <DialogTitle className="text-xl">Welcome to PhishGuard!</DialogTitle>
            <DialogDescription className="text-center">
              Your account has been created successfully. Ready to scan your first link?
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-4 mt-6">
            <Button className="w-full gradient-bg text-white" asChild>
              <Link href="/#scanner">
                Scan Your First Link
              </Link>
            </Button>
            <Button variant="outline" className="w-full" asChild>
              <Link href="/">
                Explore Features
              </Link>
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  )
} 