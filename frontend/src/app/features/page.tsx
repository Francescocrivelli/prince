"use client"

import Link from 'next/link'
import { motion } from 'framer-motion'
import Navbar from '@/components/navbar'
import Footer from '@/components/footer'
import { Button } from '@/components/ui/button'
import { Shield, Zap, Globe, Moon, Sparkles, Gauge, LineChart, ArrowRight } from 'lucide-react'

export default function Features() {
  const features = [
    {
      icon: <Shield className="h-10 w-10 text-primary" />,
      title: "Authentication",
      description: "Secure user authentication with Supabase, including email/password and social logins.",
    },
    {
      icon: <Zap className="h-10 w-10 text-primary" />,
      title: "Stripe Integration",
      description: "Handle payments and subscriptions with ease using Stripe's powerful payment infrastructure.",
    },
    {
      icon: <Moon className="h-10 w-10 text-primary" />,
      title: "Dark Mode",
      description: "Built-in dark mode support for a comfortable viewing experience in any lighting condition.",
    },
    {
      icon: <Globe className="h-10 w-10 text-primary" />,
      title: "Responsive Design",
      description: "Beautiful layouts that work perfectly on desktops, tablets, and mobile devices.",
    },
    {
      icon: <Sparkles className="h-10 w-10 text-primary" />,
      title: "Framer Motion",
      description: "Smooth animations and transitions that bring your user interface to life.",
    },
    {
      icon: <Gauge className="h-10 w-10 text-primary" />,
      title: "TypeScript",
      description: "Type-safe code with TypeScript to catch errors early and improve developer experience.",
    },
    {
      icon: <Shield className="h-10 w-10 text-primary" />,
      title: "Error Boundaries",
      description: "Graceful error handling to prevent the entire application from crashing.",
    },
    {
      icon: <LineChart className="h-10 w-10 text-primary" />,
      title: "SEO Optimized",
      description: "Built-in SEO best practices to help your application rank better in search engines.",
    },
  ]

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.5,
      },
    },
  }

  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <main className="flex-1">
        <section className="py-12 md:py-24">
          <div className="container px-4 md:px-6">
            <motion.div
              className="mx-auto max-w-3xl text-center space-y-4"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <h1 className="text-3xl font-bold tracking-tighter sm:text-5xl">
                Powerful Features for Modern Development
              </h1>
              <p className="mx-auto max-w-[700px] text-muted-foreground md:text-xl">
                Everything you need to build a modern, feature-rich web application.
              </p>
            </motion.div>

            <motion.div
              className="mx-auto grid max-w-5xl grid-cols-1 gap-6 py-12 md:grid-cols-2 lg:grid-cols-3"
              variants={containerVariants}
              initial="hidden"
              animate="visible"
            >
              {features.map((feature, i) => (
                <motion.div
                  key={i}
                  className="flex flex-col space-y-3 rounded-lg border bg-card p-6"
                  variants={itemVariants}
                >
                  <div className="mb-2">{feature.icon}</div>
                  <h3 className="text-xl font-bold">{feature.title}</h3>
                  <p className="text-muted-foreground">{feature.description}</p>
                </motion.div>
              ))}
            </motion.div>

            <motion.div
              className="mx-auto max-w-3xl text-center"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.5 }}
            >
              <Link href="/signup">
                <Button size="lg" className="group">
                  Get Started
                  <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
                </Button>
              </Link>
            </motion.div>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  )
}