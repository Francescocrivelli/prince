"use client"

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { motion } from 'framer-motion'
import { supabase } from '@/lib/supabase'
import { Button } from '@/components/ui/button'
import Navbar from '@/components/navbar'
import Footer from '@/components/footer'
import { User, CreditCard, AlertCircle, Loader2 } from 'lucide-react'
import { redirectToCheckout } from '@/lib/stripe'

type UserData = {
  id: string
  email: string
  subscription?: {
    status: string
    current_period_end: string
  } | null
}

export default function Dashboard() {
  const [user, setUser] = useState<UserData | null>(null)
  const [loading, setLoading] = useState(true)
  const [subscriptionLoading, setSubscriptionLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  useEffect(() => {
    const checkUser = async () => {
      try {
        const { data: { session } } = await supabase.auth.getSession()
        
        if (!session) {
          router.push('/login')
          return
        }
        
        // Fetch user data
        const { data: userData, error: userError } = await supabase
          .from('users')
          .select('*, subscriptions(*)')
          .eq('id', session.user.id)
          .single()
          
        if (userError) throw userError
        
        setUser({
          id: session.user.id,
          email: session.user.email || '',
          subscription: userData?.subscriptions?.[0] || null
        })
      } catch (error: any) {
        console.error('Error fetching user data:', error)
        setError(error.message)
      } finally {
        setLoading(false)
      }
    }
    
    checkUser()
  }, [router])

  const handleSubscribe = async (priceId: string) => {
    setSubscriptionLoading(true)
    try {
      await redirectToCheckout(priceId)
    } catch (error: any) {
      console.error('Error during checkout:', error)
      setError('Failed to redirect to checkout')
    } finally {
      setSubscriptionLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex min-h-screen flex-col">
        <Navbar />
        <main className="flex-1 flex items-center justify-center">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
        </main>
        <Footer />
      </div>
    )
  }

  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <main className="flex-1 container py-12">
        <motion.div
          className="space-y-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="flex flex-col md:flex-row md:items-center md:justify-between">
            <h1 className="text-3xl font-bold">Dashboard</h1>
            <div className="mt-4 md:mt-0">
              <Button variant="outline" onClick={() => router.push('/settings')}>
                Settings
              </Button>
            </div>
          </div>

          {error && (
            <div className="rounded-md bg-destructive/15 p-4 text-sm text-destructive flex items-center">
              <AlertCircle className="h-4 w-4 mr-2" />
              {error}
            </div>
          )}

          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            <div className="rounded-lg border bg-card p-6">
              <div className="flex items-center gap-4">
                <User className="h-10 w-10 text-primary" />
                <div>
                  <h3 className="font-semibold">Account</h3>
                  <p className="text-sm text-muted-foreground">{user?.email}</p>
                </div>
              </div>
            </div>

            <div className="rounded-lg border bg-card p-6">
              <div className="flex items-center gap-4">
                <CreditCard className="h-10 w-10 text-primary" />
                <div>
                  <h3 className="font-semibold">Subscription</h3>
                  <p className="text-sm text-muted-foreground">
                    {user?.subscription?.status === 'active'
                      ? 'Active'
                      : 'No active subscription'}
                  </p>
                </div>
              </div>
              {user?.subscription?.status !== 'active' && (
                <Button
                  className="mt-4 w-full"
                  onClick={() => handleSubscribe(process.env.NEXT_PUBLIC_STRIPE_BUTTON_ID || '')}
                  disabled={subscriptionLoading}
                >
                  {subscriptionLoading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : null}
                  Subscribe Now
                </Button>
              )}
            </div>
          </div>

          <div className="rounded-lg border bg-card p-6">
            <h2 className="text-xl font-semibold mb-4">Welcome to Your Dashboard</h2>
            <p className="text-muted-foreground">
              This is a sample dashboard for your application. Here you can display user-specific information
              and provide access to various features.
            </p>
          </div>
        </motion.div>
      </main>
      <Footer />
    </div>
  )
}