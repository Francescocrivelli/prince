"use client"

import { useState } from 'react'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { Button } from '@/components/ui/button'
import Navbar from '@/components/navbar'
import Footer from '@/components/footer'
import { Check } from 'lucide-react'

export default function Pricing() {
  const [annualBilling, setAnnualBilling] = useState(true)

  const toggleBilling = () => {
    setAnnualBilling(!annualBilling)
  }

  const plans = [
    {
      name: "Free",
      description: "Basic features for getting started",
      price: {
        monthly: "$0",
        annually: "$0",
      },
      features: [
        "Limited access to basic features",
        "1 project only",
        "Community support",
        "Basic analytics",
      ],
      buttonText: "Get Started",
      buttonVariant: "outline" as const,
      popular: false,
    },
    {
      name: "Pro",
      description: "Perfect for professionals and teams",
      price: {
        monthly: "$19",
        annually: "$190",
      },
      features: [
        "All Free features",
        "Unlimited projects",
        "Priority support",
        "Advanced analytics",
        "Team collaboration",
      ],
      buttonText: "Subscribe",
      buttonVariant: "default" as const,
      popular: true,
    },
    {
      name: "Enterprise",
      description: "Advanced features for large organizations",
      price: {
        monthly: "$49",
        annually: "$490",
      },
      features: [
        "All Pro features",
        "Dedicated support",
        "Custom integrations",
        "Advanced security",
        "SLA guarantees",
      ],
      buttonText: "Contact Sales",
      buttonVariant: "outline" as const,
      popular: false,
    },
  ]

  const fadeIn = {
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
              className="mx-auto text-center space-y-4 md:space-y-8"
              initial="hidden"
              animate="visible"
              variants={fadeIn}
            >
              <div className="space-y-2">
                <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">
                  Simple, Transparent Pricing
                </h1>
                <p className="mx-auto max-w-[700px] text-muted-foreground md:text-xl">
                  Choose the plan that's right for you and start building today.
                </p>
              </div>

              <div className="flex items-center justify-center space-x-4">
                <span className={`text-sm ${!annualBilling ? "text-foreground" : "text-muted-foreground"}`}>
                  Monthly
                </span>
                <button
                  onClick={toggleBilling}
                  type="button"
                  className="relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent bg-primary transition-colors duration-200 ease-in-out focus:outline-none"
                  role="switch"
                  aria-checked={annualBilling}
                >
                  <span
                    aria-hidden="true"
                    className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
                      annualBilling ? "translate-x-5" : "translate-x-0"
                    }`}
                  />
                </button>
                <span className={`text-sm ${annualBilling ? "text-foreground" : "text-muted-foreground"}`}>
                  Annual <span className="rounded-full bg-primary/10 px-2 py-0.5 text-xs text-primary">Save 20%</span>
                </span>
              </div>
            </motion.div>

            <div className="mx-auto grid max-w-screen-lg gap-8 py-12 md:grid-cols-3">
              {plans.map((plan, i) => (
                <motion.div
                  key={plan.name}
                  className={`relative flex flex-col rounded-lg border bg-card p-6 shadow-sm ${
                    plan.popular ? "border-primary" : "border-border"
                  }`}
                  initial="hidden"
                  animate="visible"
                  variants={{
                    hidden: { opacity: 0, y: 20 },
                    visible: {
                      opacity: 1,
                      y: 0,
                      transition: {
                        duration: 0.5,
                        delay: i * 0.1,
                      },
                    },
                  }}
                >
                  {plan.popular && (
                    <div className="absolute -top-3 left-0 right-0 mx-auto w-fit rounded-full bg-primary px-3 py-1 text-xs font-medium text-primary-foreground">
                      Most Popular
                    </div>
                  )}
                  <div className="space-y-2">
                    <h3 className="text-xl font-bold">{plan.name}</h3>
                    <p className="text-sm text-muted-foreground">{plan.description}</p>
                  </div>
                  <div className="mt-6 space-y-1">
                    <div className="flex items-baseline">
                      <span className="text-3xl font-bold">
                        {annualBilling ? plan.price.annually : plan.price.monthly}
                      </span>
                      <span className="ml-1 text-sm text-muted-foreground">
                        {plan.name !== "Free" && (annualBilling ? "/year" : "/month")}
                      </span>
                    </div>
                    {annualBilling && plan.name !== "Free" && (
                      <p className="text-xs text-muted-foreground">
                        Billed annually ({parseInt(plan.price.annually.replace("$", "")) / 12}/month)
                      </p>
                    )}
                  </div>
                  <ul className="mt-6 space-y-3">
                    {plan.features.map((feature) => (
                      <li key={feature} className="flex items-center text-sm">
                        <Check className="mr-2 h-4 w-4 text-primary" />
                        {feature}
                      </li>
                    ))}
                  </ul>
                  <div className="mt-auto pt-8">
                    <Link href={plan.name === "Free" ? "/signup" : "/login"}>
                      <Button variant={plan.buttonVariant} className="w-full" size="lg">
                        {plan.buttonText}
                      </Button>
                    </Link>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  )
}