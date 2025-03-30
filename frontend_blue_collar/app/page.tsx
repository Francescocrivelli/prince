"use client"

import React from 'react'
import Link from 'next/link'
import { motion } from 'framer-motion'
import Navbar from '@/components/navbar'
import Footer from '@/components/footer'
import { Button } from '@/components/ui/button'
import { ArrowRight, CheckCircle, Sparkles, Users, Award, MessageSquare, Zap, Phone, Briefcase, Calendar, Clock, Headphones, DollarSign } from 'lucide-react'

export default function Home() {
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

  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <main className="flex-1">
        {/* Hero Section */}
        <section className="relative overflow-hidden py-20 md:py-32 bg-gradient-to-br from-blue-50 to-white dark:from-gray-900 dark:to-gray-950">
          <div className="absolute inset-0 bg-grid-pattern opacity-[0.03] dark:opacity-[0.05]"></div>
          <div className="container px-4 md:px-6 relative">
            <div className="grid gap-10 lg:grid-cols-[1fr_400px] lg:gap-12 xl:grid-cols-[1fr_600px]">
              <motion.div
                className="flex flex-col justify-center space-y-6"
                initial="hidden"
                animate="visible"
                variants={fadeIn}
              >
                <div className="inline-flex items-center rounded-full border px-3 py-1 text-sm font-medium bg-white/30 dark:bg-gray-800/30 backdrop-blur-sm w-fit">
                  <span className="text-blue-600 dark:text-blue-400 mr-1">📞</span> 
                  Call or text to find work instantly
                </div>
                <div className="space-y-4">
                  <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl xl:text-6xl/none bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-cyan-600 dark:from-blue-400 dark:to-cyan-400">
                    JobConnect Voice Agent
                  </h1>
                  <p className="max-w-[600px] text-gray-600 dark:text-gray-300 text-lg">
                    Forget about JobBoards, let AI find you the best job tomorrow.
                  </p>
                </div>
                <div className="flex flex-col sm:flex-row gap-3">
                  <Link href="tel:+18005551234">
                    <Button size="lg" className="group bg-blue-600 hover:bg-blue-700 dark:bg-blue-600 dark:hover:bg-blue-700 text-white">
                      Call Now
                      <Phone className="ml-2 h-4 w-4" />
                    </Button>
                  </Link>
                  <Link href="#how-it-works">
                    <Button size="lg" variant="outline" className="dark:text-white dark:border-gray-700">
                      Learn More
                    </Button>
                  </Link>
                </div>
                <div className="flex items-center space-x-3 pt-3">
                  <div className="flex -space-x-3">
                    {[1, 2, 3, 4].map((i) => (
                      <div key={i} className="h-8 w-8 rounded-full border-2 border-white dark:border-gray-900 bg-blue-600 overflow-hidden relative">
                        <div className="absolute inset-0 flex items-center justify-center text-[10px] font-medium text-white">
                          {String.fromCharCode(64 + i)}
                        </div>
                      </div>
                    ))}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    Trusted by workers in <span className="font-medium">Construction</span>, <span className="font-medium">Restaurants</span>, <span className="font-medium">Warehouses</span>, and more
                  </div>
                </div>
              </motion.div>
              <motion.div
                className="flex items-center justify-center"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.8 }}
              >
                <div className="relative h-[400px] w-full max-w-[500px] overflow-hidden rounded-xl border bg-white dark:bg-gray-950 p-1 shadow-2xl">
                  <div className="absolute inset-0 bg-gradient-to-tr from-blue-100 via-white to-cyan-100 dark:from-gray-900 dark:via-gray-950 dark:to-blue-950 rounded-xl"></div>
                  <div className="absolute top-0 left-0 right-0 h-12 rounded-t-xl bg-white dark:bg-gray-900 flex items-center px-4 z-10 border-b">
                    <div className="flex space-x-2">
                      <div className="h-3 w-3 rounded-full bg-red-500" />
                      <div className="h-3 w-3 rounded-full bg-yellow-500" />
                      <div className="h-3 w-3 rounded-full bg-green-500" />
                    </div>
                    <div className="absolute inset-x-0 text-center text-xs font-medium text-gray-500 dark:text-gray-400">
                      Phone Conversation
                    </div>
                  </div>
                  <div className="absolute inset-0 mt-12 p-4 space-y-4 z-10">
                    <div className="space-y-3 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg backdrop-blur-sm">
                      <div className="flex items-start">
                        <div className="h-8 w-8 rounded-full bg-blue-100 dark:bg-blue-700 flex items-center justify-center mr-3 flex-shrink-0">
                          <Headphones className="h-4 w-4 text-blue-600 dark:text-blue-200" />
                        </div>
                        <div className="text-sm">
                          <p className="text-gray-700 dark:text-gray-200">
                            Hi! I'm the JobConnect voice agent. What kind of work are you looking for and where are you located?
                          </p>
                        </div>
                      </div>
                    </div>
                    <div className="space-y-3 p-3 bg-gray-50 dark:bg-gray-800/50 rounded-lg ml-12">
                      <div className="flex items-start">
                        <div className="text-sm">
                          <p className="text-gray-700 dark:text-gray-300">
                            I'm looking for construction work. I have experience with framing and drywall. I'm in the Chicago area.
                          </p>
                        </div>
                      </div>
                    </div>
                    <div className="space-y-3 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg backdrop-blur-sm">
                      <div className="flex items-start">
                        <div className="h-8 w-8 rounded-full bg-blue-100 dark:bg-blue-700 flex items-center justify-center mr-3 flex-shrink-0">
                          <Headphones className="h-4 w-4 text-blue-600 dark:text-blue-200" />
                        </div>
                        <div className="text-sm">
                          <p className="text-gray-700 dark:text-gray-200">
                            Great! I found 3 construction jobs in Chicago that need workers with your skills. Would you like me to connect you with these employers?
                          </p>
                        </div>
                      </div>
                    </div>
                    <div className="absolute bottom-4 left-0 right-0 flex justify-center">
                      <div className="h-10 w-[80%] rounded-full border bg-white dark:bg-gray-900 flex items-center px-4 text-sm text-gray-400">
                        Call (800) 555-1234 to get started...
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>
            </div>
          </div>
        </section>

        {/* How It Works Section */}
        <section id="how-it-works" className="py-20 bg-white dark:bg-gray-950">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center mb-12">
              <div className="inline-flex items-center rounded-full border px-3 py-1 text-sm font-medium bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-300 w-fit">
                How It Works
              </div>
              <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">Find Jobs With A Simple Phone Call</h2>
              <p className="max-w-[800px] text-gray-500 dark:text-gray-400 md:text-xl/relaxed">
                No resumes, no applications, no websites needed. Just call and we'll do the rest.
              </p>
            </div>

            <motion.div 
              className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mt-12"
              variants={staggerContainer}
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true, margin: "-100px" }}
            >
              {[
                {
                  icon: <Phone className="h-12 w-12 text-blue-600 dark:text-blue-400" />,
                  title: "1. Call Our Number",
                  description: "Call our easy-to-remember number or send us a text message to get started. No internet required."
                },
                {
                  icon: <MessageSquare className="h-12 w-12 text-blue-600 dark:text-blue-400" />,
                  title: "2. Tell Us About Your Skills",
                  description: "Our voice agent asks about your work experience, skills, and location preferences."
                },
                {
                  icon: <Briefcase className="h-12 w-12 text-blue-600 dark:text-blue-400" />,
                  title: "3. Get Matched to Jobs",
                  description: "We connect you with employers who need your skills right now, in your area."
                },
                {
                  icon: <Calendar className="h-12 w-12 text-blue-600 dark:text-blue-400" />,
                  title: "4. Start Working",
                  description: "Accept job offers via phone or text and start earning without delay."
                }
              ].map((feature, i) => (
                <motion.div 
                  key={i} 
                  className="flex flex-col items-center space-y-4 rounded-xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-gray-900 p-6 text-center"
                  variants={fadeIn}
                >
                  <div className="rounded-full bg-blue-50 dark:bg-blue-900/20 p-3">
                    {feature.icon}
                  </div>
                  <h3 className="text-xl font-bold">{feature.title}</h3>
                  <p className="text-gray-500 dark:text-gray-400">{feature.description}</p>
                </motion.div>
              ))}
            </motion.div>
          </div>
        </section>
        
        {/* Value Proposition */}
        <section id="success-stories" className="py-20 bg-gradient-to-br from-indigo-50 to-white dark:from-gray-900 dark:to-gray-950">
          <div className="container px-4 md:px-6">
            <div className="grid gap-10 lg:grid-cols-2">
              <motion.div 
                className="space-y-6"
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6 }}
                viewport={{ once: true }}
              >
                <div className="inline-flex items-center rounded-full border px-3 py-1 text-sm font-medium bg-indigo-50 dark:bg-indigo-900/20 text-indigo-600 dark:text-indigo-300 w-fit">
                  Why Workers Love Us
                </div>
                <h2 className="text-3xl font-bold">Built for Workers, by Workers</h2>
                <p className="text-gray-600 dark:text-gray-300">
                  We understand the challenges blue-collar workers face when finding reliable employment that values their skills.
                </p>
                <div className="space-y-4">
                  {[
                    "Save time: One call connects you directly to jobs that match your experience.",
                    "Skip the paperwork: No more filling out complicated applications or building resumes.",
                    "Local opportunities: Get matched with employers in your area who need your skills now.",
                    "Daily pay options: Many positions offer same-day or weekly payment options."
                  ].map((item, i) => (
                    <div key={i} className="flex items-start">
                      <CheckCircle className="h-5 w-5 text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                      <p className="text-gray-600 dark:text-gray-300">{item}</p>
                    </div>
                  ))}
                </div>
                <div className="pt-4">
                  <Link href="tel:+18005551234">
                    <Button size="lg" className="group bg-indigo-600 hover:bg-indigo-700 dark:bg-indigo-600 dark:hover:bg-indigo-700 text-white">
                      Call Now
                      <Phone className="ml-2 h-4 w-4" />
                    </Button>
                  </Link>
                </div>
              </motion.div>
              <motion.div
                className="relative h-[400px] lg:h-auto rounded-xl overflow-hidden"
                initial={{ opacity: 0, x: 20 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6 }}
                viewport={{ once: true }}
              >
                <div className="absolute inset-0 bg-gradient-to-tr from-indigo-500 to-purple-600 opacity-20 dark:opacity-30"></div>
                <div className="absolute inset-0 grid grid-cols-2 gap-4 p-6">
                  {Array.from({ length: 4 }).map((_, i) => (
                    <motion.div 
                      key={i}
                      className="rounded-lg bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm p-4 shadow-lg"
                      initial={{ opacity: 0, y: 20 }}
                      whileInView={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.4, delay: i * 0.1 }}
                      viewport={{ once: true }}
                    >
                      <div className="flex items-center space-x-3 mb-3">
                        <div className="h-8 w-8 rounded-full bg-indigo-100 dark:bg-indigo-800 flex items-center justify-center">
                          <span className="text-sm font-medium text-indigo-600 dark:text-indigo-300">
                            {String.fromCharCode(65 + i)}
                          </span>
                        </div>
                        <div className="text-sm font-medium">
                          {[
                            "Javier M. (Construction)",
                            "Miguel R. (Chipotle)",
                            "Isabela G. (Amazon)",
                            "Maria Q. (Medical Office)"
                          ][i]}
                        </div>
                      </div>
                      <p className="text-sm text-gray-600 dark:text-gray-300">
                        {[
                          "Found a construction job within 24 hours of calling. The pay is better than my last position and closer to home!",
                          "After my hours were cut at Chipotle, I called and got connected to three restaurants looking for line cooks right away.",
                          "I've been getting steady warehouse work at Amazon for 3 months now. They call me whenever they need extra hands.",
                          "As a medical office secretary, I can now pick up receptionist work at different clinics when I need extra income."
                        ][i]}
                      </p>
                    </motion.div>
                  ))}
                </div>
              </motion.div>
            </div>
          </div>
        </section>
        
        {/* Pricing Section */}
        <section id="pricing" className="py-20 bg-white dark:bg-gray-950">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <div className="inline-flex items-center rounded-full border px-3 py-1 text-sm font-medium bg-indigo-50 dark:bg-indigo-900/20 text-indigo-600 dark:text-indigo-300 w-fit">
                Simple Pricing
              </div>
              <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">
                Join Our Exclusive Community
              </h2>
              <p className="max-w-[600px] text-gray-500 dark:text-gray-400 md:text-xl/relaxed">
                Connect with top tech startups and like-minded students
              </p>
            </div>

            <motion.div 
              className="mx-auto max-w-md mt-12"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
            >
              <div className="rounded-xl border border-indigo-100 dark:border-indigo-800 bg-white dark:bg-gray-900 p-8 shadow-lg relative overflow-hidden">
                <div className="absolute top-0 right-0 bg-indigo-600 text-white text-xs font-bold px-3 py-1 rounded-bl-lg">
                  EXCLUSIVE
                </div>
                <div className="flex justify-center">
                  <div className="rounded-full bg-indigo-50 dark:bg-indigo-900/20 p-3">
                    <Sparkles className="h-8 w-8 text-indigo-600 dark:text-indigo-400" />
                  </div>
                </div>
                <h3 className="text-2xl font-bold text-center mt-4">Membership</h3>
                <div className="flex justify-center items-baseline mt-4 mb-6">
                  <span className="text-5xl font-extrabold">$129</span>
                  <span className="text-gray-500 dark:text-gray-400 ml-1">/month</span>
                </div>
                <ul className="space-y-3">
                  {[
                    "Access to AI career agent",
                    "Profile building and matching",
                    "Direct connections with tech startups",
                    "Interview opportunities",
                    "Exclusive community events",
                    "Network with other talented students"
                  ].map((feature, i) => (
                    <li key={i} className="flex">
                      <CheckCircle className="h-5 w-5 text-green-500 mr-2 flex-shrink-0" />
                      <span className="text-gray-600 dark:text-gray-300">{feature}</span>
                    </li>
                  ))}
                </ul>
                <div className="mt-8">
                  <Link href="https://docs.google.com/forms/d/1nK9EPoqgmn4q2mpD5Q53IZR29J3oAP1mOupAw292Oo4/edit" target="_blank" className="w-full">
                    <Button className="w-full bg-indigo-600 hover:bg-indigo-700 dark:bg-indigo-600 dark:hover:bg-indigo-700 text-white">
                      Apply Now
                    </Button>
                  </Link>
                </div>
                <p className="text-center text-xs text-gray-500 dark:text-gray-400 mt-4">
                  Only accepted applicants will be charged
                </p>
              </div>
            </motion.div>
          </div>
        </section>
        
        {/* Application Process */}
        <section className="py-20 bg-gradient-to-br from-indigo-50 to-white dark:from-gray-900 dark:to-gray-950">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center mb-12">
              <div className="inline-flex items-center rounded-full border px-3 py-1 text-sm font-medium bg-indigo-50 dark:bg-indigo-900/20 text-indigo-600 dark:text-indigo-300 w-fit">
                How to Join
              </div>
              <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl">The Application Process</h2>
              <p className="max-w-[600px] text-gray-500 dark:text-gray-400 md:text-lg">
                Our community is selective to ensure the highest quality opportunities for our members
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-8">
              {[
                {
                  step: "01",
                  title: "1-Minute Application",
                  description: "Fill out our short application form to tell us about your background and interests.",
                  highlight: "Takes just 60 seconds"
                },
                {
                  step: "02",
                  title: "Selection Process",
                  description: "Our team reviews applications to find talented students, researchers, and builders.",
                  highlight: "Selective acceptance"
                },
                {
                  step: "03",
                  title: "Talent Interview",
                  description: "If selected, you'll have a brief interview with one of our talent recruiters.",
                  highlight: "Get featured on our platform"
                }
              ].map((step, i) => (
                <motion.div 
                  key={i}
                  className="relative border border-gray-100 dark:border-gray-800 rounded-xl p-6 bg-white dark:bg-gray-900"
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: i * 0.1 }}
                  viewport={{ once: true }}
                >
                  <div className="absolute -top-3 -left-3 h-10 w-10 rounded-full bg-indigo-600 flex items-center justify-center text-white font-bold">
                    {step.step}
                  </div>
                  <h3 className="text-xl font-bold mt-4">{step.title}</h3>
                  <p className="text-gray-500 dark:text-gray-400 mt-2">{step.description}</p>
                  <div className="mt-4 inline-block bg-indigo-50 dark:bg-indigo-900/20 rounded-full px-3 py-1 text-xs font-medium text-indigo-600 dark:text-indigo-300">
                    {step.highlight}
                  </div>
                </motion.div>
              ))}
            </div>

            <div className="mt-12 text-center">
              <Link href="https://docs.google.com/forms/d/1nK9EPoqgmn4q2mpD5Q53IZR29J3oAP1mOupAw292Oo4/edit" target="_blank">
                <Button size="lg" className="group bg-indigo-600 hover:bg-indigo-700 dark:bg-indigo-600 dark:hover:bg-indigo-700 text-white">
                  Start Application
                  <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
                </Button>
              </Link>
            </div>
          </div>
        </section>
        
        {/* CTA Section */}
        <section id="cta" className="py-20 bg-blue-600 dark:bg-blue-700">
          <div className="container px-4 md:px-6">
            <motion.div 
              className="max-w-3xl mx-auto text-center space-y-6"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
            >
              <h2 className="text-3xl font-bold text-white">Ready to Find Your Next Job?</h2>
              <p className="text-blue-100">
                No resumes, no applications, no waiting. Just a simple phone call connects you with jobs that match your skills.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
                <Link href="tel:+18005551234">
                  <Button size="lg" className="bg-white text-blue-600 hover:bg-gray-100">
                    Call Now
                    <Phone className="ml-2 h-4 w-4" />
                  </Button>
                </Link>
                <Link href="#how-it-works">
                  <Button size="lg" className="bg-blue-700 hover:bg-blue-800 text-white">
                    See How It Works
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </Link>
              </div>
              <p className="text-blue-100 text-sm">
                Available 24/7 - Our voice agent is always ready to help
              </p>
            </motion.div>
          </div>
        </section>

        {/* Job Types Section */}
        <section id="job-types" className="py-20 bg-gradient-to-br from-blue-50 to-white dark:from-gray-900 dark:to-gray-950">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center mb-12">
              <div className="inline-flex items-center rounded-full border px-3 py-1 text-sm font-medium bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-300 w-fit">
                Job Types
              </div>
              <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">Jobs Available For Your Skills</h2>
              <p className="max-w-[800px] text-gray-500 dark:text-gray-400 md:text-xl/relaxed">
                We connect workers with a wide range of blue-collar job opportunities
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mt-12">
              {[
                {
                  title: "Construction",
                  description: "Framing, drywall, roofing, electrical, plumbing, and general construction labor jobs.",
                  icon: "🏗️"
                },
                {
                  title: "Restaurants",
                  description: "Kitchen staff, line cooks, dishwashers, servers, and food delivery positions.",
                  icon: "🍽️"
                },
                {
                  title: "Warehouse",
                  description: "Picking, packing, shipping, receiving, and forklift operation positions.",
                  icon: "📦"
                },
                {
                  title: "Cleaning",
                  description: "Residential, commercial, and industrial cleaning positions.",
                  icon: "🧹"
                },
                {
                  title: "Landscaping",
                  description: "Lawn care, gardening, tree trimming, and general landscaping work.",
                  icon: "🌱"
                },
                {
                  title: "Manufacturing",
                  description: "Assembly line, machine operation, quality control, and production positions.",
                  icon: "🏭"
                }
              ].map((jobType, i) => (
                <motion.div
                  key={i}
                  className="flex flex-col rounded-xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-gray-900 overflow-hidden"
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.1 }}
                  viewport={{ once: true }}
                >
                  <div className="p-6 flex-1">
                    <div className="text-4xl mb-4">{jobType.icon}</div>
                    <h3 className="text-xl font-bold mb-2">{jobType.title}</h3>
                    <p className="text-gray-500 dark:text-gray-400">{jobType.description}</p>
                  </div>
                  <div className="p-4 bg-gray-50 dark:bg-gray-800 border-t border-gray-100 dark:border-gray-700">
                    <Link href="tel:+18005551234">
                      <Button className="w-full bg-blue-600 hover:bg-blue-700 dark:bg-blue-600 dark:hover:bg-blue-700 text-white">
                        Find {jobType.title} Jobs
                      </Button>
                    </Link>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Benefits Section */}
        <section id="benefits" className="py-20 bg-white dark:bg-gray-950">
          <div className="container px-4 md:px-6">
            <div className="grid gap-10 lg:grid-cols-2">
              <motion.div 
                className="space-y-6"
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6 }}
                viewport={{ once: true }}
              >
                <div className="inline-flex items-center rounded-full border px-3 py-1 text-sm font-medium bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-300 w-fit">
                  Why Workers Trust Us
                </div>
                <h2 className="text-3xl font-bold">Built For Hard-Working People</h2>
                <p className="text-gray-600 dark:text-gray-300">
                  We understand the challenges blue-collar workers face when looking for reliable, steady work.
                </p>
                <div className="space-y-4">
                  {[
                    "No smartphone or internet needed - just a basic phone for calls or texts",
                    "Get job opportunities that match your actual skills and experience",
                    "Quick response - find work as soon as today or tomorrow",
                    "Steady work options - daily, weekly, or long-term positions",
                    "No paperwork, forms, or complicated applications",
                    "Work in your preferred location, close to home or public transit"
                  ].map((item, i) => (
                    <div key={i} className="flex items-start">
                      <CheckCircle className="h-5 w-5 text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                      <p className="text-gray-600 dark:text-gray-300">{item}</p>
                    </div>
                  ))}
                </div>
                <div className="pt-4">
                  <Link href="tel:+18005551234">
                    <Button size="lg" className="group bg-blue-600 hover:bg-blue-700 dark:bg-blue-600 dark:hover:bg-blue-700 text-white">
                      Call Now
                      <Phone className="ml-2 h-4 w-4" />
                    </Button>
                  </Link>
                </div>
              </motion.div>
              <motion.div
                className="relative h-[400px] lg:h-auto rounded-xl overflow-hidden"
                initial={{ opacity: 0, x: 20 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6 }}
                viewport={{ once: true }}
              >
                <div className="absolute inset-0 bg-gradient-to-r from-blue-400 to-cyan-500 rounded-xl"></div>
                <div className="absolute inset-0 bg-grid-pattern opacity-20"></div>
                <div className="absolute inset-0 flex flex-col justify-center items-center text-white p-8 text-center">
                  <Clock className="h-16 w-16 mb-6" />
                  <h3 className="text-2xl font-bold mb-2">Get To Work Faster</h3>
                  <p className="text-xl mb-6">Average time from call to job offer:</p>
                  <div className="text-5xl font-bold">24 Hours</div>
                  <p className="mt-6">Many workers start new jobs the very next day</p>
                </div>
              </motion.div>
            </div>
          </div>
        </section>

        {/* For Employers Section */}
        <section id="employers" className="py-20 bg-gray-50 dark:bg-gray-900">
          <div className="container px-4 md:px-6">
            <motion.div 
              className="max-w-3xl mx-auto text-center space-y-4 mb-10"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
            >
              <div className="inline-flex items-center rounded-full border px-3 py-1 text-sm font-medium bg-indigo-50 dark:bg-indigo-900/20 text-indigo-600 dark:text-indigo-300 w-fit mx-auto">
                For Business Owners & Managers
              </div>
              <h2 className="text-3xl font-bold">Hire Skilled Blue-Collar Workers On Demand</h2>
              <p className="text-gray-600 dark:text-gray-300">
                Connect with pre-screened workers who have the exact skills you need, when you need them.
              </p>
            </motion.div>
            
            <div className="grid gap-8 md:grid-cols-3">
              {[
                {
                  title: "Find Workers Fast",
                  description: "Post jobs once and our AI matches you with qualified workers in your area who are ready to start.",
                  icon: Users
                },
                {
                  title: "Reduce Hiring Costs",
                  description: "Eliminate expensive job boards, recruitment agencies, and wasted time on unqualified applicants.",
                  icon: DollarSign
                },
                {
                  title: "Flexible Staffing",
                  description: "Whether you need temporary help or permanent staff, our platform scales to your changing needs.",
                  icon: Calendar
                }
              ].map((item, i) => (
                <motion.div 
                  key={i}
                  className="flex flex-col items-center text-center p-6 bg-white dark:bg-gray-800 rounded-xl shadow-sm"
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: i * 0.1 }}
                  viewport={{ once: true }}
                >
                  <div className="p-3 rounded-full bg-indigo-100 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-300 mb-4">
                    {React.createElement(item.icon, { className: "h-6 w-6" })}
                  </div>
                  <h3 className="text-xl font-semibold mb-2">{item.title}</h3>
                  <p className="text-gray-600 dark:text-gray-300">{item.description}</p>
                </motion.div>
              ))}
            </div>
            
            <motion.div 
              className="mt-12 max-w-md mx-auto text-center"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              viewport={{ once: true }}
            >
              <Link href="#contact">
                <Button size="lg" className="bg-indigo-600 hover:bg-indigo-700 dark:bg-indigo-600 dark:hover:bg-indigo-700 text-white">
                  Request A Demo
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </Link>
              <p className="mt-4 text-sm text-gray-500 dark:text-gray-400">
                Join hundreds of businesses saving time and money on blue-collar hiring
              </p>
            </motion.div>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  )
}