"use client"

import { useState } from 'react'
import Link from 'next/link'
import { motion } from 'framer-motion'
import Navbar from '@/components/navbar'
import Footer from '@/components/footer'
import { Button } from '@/components/ui/button'
import { CheckCircle2, ArrowRight, Zap, Shield, Globe } from 'lucide-react'

export default function Home() {
  const [isHovered, setIsHovered] = useState(false)

  const fadeIn = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.6,
      },
    },
  }

  const staggerContainer = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  }

  const features = [
    {
      title: "Authentication",
      description: "Secure user authentication with Supabase.",
      icon: <Shield className="h-10 w-10 text-primary" />,
    },
    {
      title: "Payments",
      description: "Integrated payment processing with Stripe.",
      icon: <Zap className="h-10 w-10 text-primary" />,
    },
    {
      title: "Responsive Design",
      description: "Works seamlessly on all devices and screen sizes.",
      icon: <Globe className="h-10 w-10 text-primary" />,
    },
  ]

  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <main className="flex-1">
        {/* Hero Section */}
        <section className="relative overflow-hidden py-20 md:py-32">
          <div className="container px-4 md:px-6">
            <div className="grid gap-6 lg:grid-cols-[1fr_400px] lg:gap-12 xl:grid-cols-[1fr_600px]">
              <motion.div
                className="flex flex-col justify-center space-y-4"
                initial="hidden"
                animate="visible"
                variants={fadeIn}
              >
                <div className="space-y-2">
                  <h1 className="text-3xl font-bold tracking-tighter sm:text-5xl xl:text-6xl/none">
                    Your AI-Powered Productivity Assistant
                  </h1>
                  <p className="max-w-[600px] text-gray-500 dark:text-gray-400 md:text-xl">
                    Boost your productivity with Prince. Our AI-powered platform helps you focus on what matters most.
                  </p>
                </div>
                <div className="flex flex-col gap-2 min-[400px]:flex-row">
                  <Link href="/signup">
                    <Button size="lg" className="group">
                      Get Started
                      <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
                    </Button>
                  </Link>
                  <Link href="/features">
                    <Button size="lg" variant="outline">
                      Learn More
                    </Button>
                  </Link>
                </div>
              </motion.div>
              <motion.div
                className="flex items-center justify-center"
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.8 }}
                onMouseEnter={() => setIsHovered(true)}
                onMouseLeave={() => setIsHovered(false)}
              >
                <div className="relative h-[350px] w-full max-w-[500px] overflow-hidden rounded-lg border bg-white dark:bg-gray-950 p-2 shadow-xl">
                  <div className="absolute top-0 left-0 right-0 h-12 rounded-t-lg bg-gray-100 dark:bg-gray-900 flex items-center px-4">
                    <div className="flex space-x-2">
                      <div className="h-3 w-3 rounded-full bg-red-500" />
                      <div className="h-3 w-3 rounded-full bg-yellow-500" />
                      <div className="h-3 w-3 rounded-full bg-green-500" />
                    </div>
                  </div>
                  <div className="mt-12 p-4 space-y-4">
                    <motion.div
                      className="h-8 w-4/5 rounded-md bg-gray-100 dark:bg-gray-800"
                      animate={{ 
                        backgroundColor: isHovered ? "rgb(243 244 246 / 0.2)" : "rgb(243 244 246)"
                      }}
                      transition={{ duration: 0.3 }}
                    />
                    <motion.div
                      className="h-8 w-3/5 rounded-md bg-gray-100 dark:bg-gray-800"
                      animate={{ 
                        backgroundColor: isHovered ? "rgb(243 244 246 / 0.2)" : "rgb(243 244 246)"
                      }}
                      transition={{ duration: 0.3, delay: 0.1 }}
                    />
                    <motion.div
                      className="h-24 w-full rounded-md bg-gray-100 dark:bg-gray-800"
                      animate={{ 
                        backgroundColor: isHovered ? "rgb(243 244 246 / 0.2)" : "rgb(243 244 246)"
                      }}
                      transition={{ duration: 0.3, delay: 0.2 }}
                    />
                    <motion.div
                      className="h-8 w-2/5 rounded-md bg-gray-100 dark:bg-gray-800"
                      animate={{ 
                        backgroundColor: isHovered ? "rgb(243 244 246 / 0.2)" : "rgb(243 244 246)"
                      }}
                      transition={{ duration: 0.3, delay: 0.3 }}
                    />
                  </div>
                </div>
              </motion.div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="bg-gray-50 dark:bg-gray-900 py-20">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <div className="space-y-2">
                <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">Features</h2>
                <p className="max-w-[900px] text-gray-500 dark:text-gray-400 md:text-xl/relaxed">
                  Everything you need to build your next project.
                </p>
              </div>
            </div>
            <motion.div 
              className="mx-auto grid max-w-5xl grid-cols-1 gap-6 py-12 md:grid-cols-3"
              variants={staggerContainer}
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true, margin: "-100px" }}
            >
              {features.map((feature, i) => (
                <motion.div 
                  key={i} 
                  className="flex flex-col items-center space-y-4 rounded-lg border bg-white dark:bg-gray-950 p-6 shadow-sm"
                  variants={fadeIn}
                >
                  {feature.icon}
                  <h3 className="text-xl font-bold">{feature.title}</h3>
                  <p className="text-gray-500 dark:text-gray-400">{feature.description}</p>
                </motion.div>
              ))}
            </motion.div>
          </div>
        </section>
        
        {/* CTA Section */}
        <section className="py-20">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <motion.div 
                className="space-y-2"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
                viewport={{ once: true }}
              >
                <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">Ready to get started?</h2>
                <p className="max-w-[600px] text-gray-500 dark:text-gray-400 md:text-xl/relaxed">
                  Sign up today and experience the future of productivity.
                </p>
              </motion.div>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.2 }}
                viewport={{ once: true }}
              >
                <Link href="/signup">
                  <Button size="lg" className="group">
                    Get Started
                    <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
                  </Button>
                </Link>
              </motion.div>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  )
}