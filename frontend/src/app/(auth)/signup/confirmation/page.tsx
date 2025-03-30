"use client"

import Link from 'next/link'
import { motion } from 'framer-motion'
import { Button } from '@/components/ui/button'
import Navbar from '@/components/navbar'
import Footer from '@/components/footer'
import { CheckCircle2, Mail } from 'lucide-react'

export default function SignupConfirmation() {
  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <main className="flex-1 flex items-center justify-center py-12">
        <motion.div
          className="mx-auto w-full max-w-md space-y-6 px-4 text-center"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", stiffness: 200, damping: 10, delay: 0.2 }}
          >
            <CheckCircle2 className="mx-auto h-16 w-16 text-primary" />
          </motion.div>
          <div className="space-y-2">
            <h1 className="text-3xl font-bold">Check your email</h1>
            <p className="text-muted-foreground">
              We've sent you a confirmation link. Please check your email to activate your account.
            </p>
          </div>
          <div className="pt-4">
            <div className="rounded-lg border border-border bg-muted/30 p-6">
              <Mail className="mx-auto h-8 w-8 text-muted-foreground mb-4" />
              <p className="text-sm text-muted-foreground">
                If you don't see the email in your inbox, please check your spam folder or request a new confirmation link.
              </p>
            </div>
          </div>
          <div className="pt-4">
            <Link href="/login">
              <Button variant="outline" className="w-full">
                Back to Login
              </Button>
            </Link>
          </div>
        </motion.div>
      </main>
      <Footer />
    </div>
  )
}