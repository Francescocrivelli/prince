"use client";

import { useEffect, useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';
import { useSubscription } from '@/hooks/useSubscription';
import { useTrialStatus } from '@/hooks/useTrialStatus';
import { CreditCard } from 'lucide-react';

const AUTH_TIMEOUT = 15000; // 15 seconds

export default function Dashboard() {
  const { user, isLoading: isAuthLoading } = useAuth();
  const router = useRouter();
  const { subscription, isLoading: isSubLoading } = useSubscription();
  const { isInTrial, isLoading: isTrialLoading } = useTrialStatus();
  const [authTimeout, setAuthTimeout] = useState(false);

  // Auth check
  useEffect(() => {
    if (!user && !isAuthLoading) {
      router.replace('/login');
    }
  }, [user, isAuthLoading, router]);

  // Auth timeout
  useEffect(() => {
    const timer = setTimeout(() => {
      if (!user && isAuthLoading) {
        setAuthTimeout(true);
      }
    }, AUTH_TIMEOUT);
    
    return () => clearTimeout(timer);
  }, [user, isAuthLoading]);

  // Loading state
  if (isAuthLoading || isSubLoading || isTrialLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-foreground">Loading...</div>
      </div>
    );
  }

  // Auth timeout state
  if (authTimeout) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-foreground">
          Authentication is taking longer than expected. Please refresh the page.
        </div>
      </div>
    );
  }

  // Not authenticated
  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-foreground">
          Please <button onClick={() => router.push('/login')} className="text-primary hover:underline">log in</button> to access your dashboard.
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen p-8 bg-background">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-foreground mb-2">Subscription Management</h1>
          <p className="text-muted-foreground">Manage your Prince subscription</p>
        </div>

        <div className="bg-card rounded-lg shadow-lg p-6 border border-border">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center">
              <CreditCard className="h-8 w-8 text-primary mr-3" />
              <div>
                <h2 className="text-xl font-semibold text-foreground">
                  {isInTrial ? 'Trial Period' : subscription ? 'Active Subscription' : 'No Active Subscription'}
                </h2>
                <p className="text-sm text-muted-foreground">
                  {isInTrial ? 'Your trial period is active' : 
                   subscription ? `Valid until ${new Date(subscription.current_period_end).toLocaleDateString()}` :
                   'Subscribe to access all features'}
                </p>
              </div>
            </div>
            <button
              onClick={() => {
                if (subscription) {
                  // For managing existing subscription, use the customer portal
                  window.location.href = `https://billing.stripe.com/p/login/test_${process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY}`;
                } else {
                  // For new subscriptions, use the checkout URL
                  window.location.href = `https://checkout.stripe.com/c/pay/${process.env.NEXT_PUBLIC_STRIPE_BUTTON_ID}`;
                }
              }}
              className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
            >
              {subscription ? 'Manage Subscription' : 'Subscribe Now'}
            </button>
          </div>

          {subscription && (
            <div className="border-t border-border pt-4 mt-4">
              <h3 className="text-lg font-medium text-foreground mb-2">Subscription Details</h3>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-muted-foreground">Status</p>
                  <p className="text-foreground capitalize">{subscription.status}</p>
                </div>
                <div>
                  <p className="text-muted-foreground">Renewal Date</p>
                  <p className="text-foreground">
                    {new Date(subscription.current_period_end).toLocaleDateString()}
                  </p>
                </div>
                <div>
                  <p className="text-muted-foreground">Subscription ID</p>
                  <p className="text-foreground font-mono text-xs">{subscription.stripe_subscription_id}</p>
                </div>
                <div>
                  <p className="text-muted-foreground">Auto-renew</p>
                  <p className="text-foreground">{subscription.cancel_at_period_end ? 'No' : 'Yes'}</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}