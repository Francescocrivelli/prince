import { loadStripe } from '@stripe/stripe-js'

export const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!)

export async function redirectToCheckout(priceId: string) {
  const stripe = await stripePromise
  
  // Call your backend to create the Checkout session
  const response = await fetch('/api/create-checkout-session', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ priceId }),
  })
  
  const { sessionId } = await response.json()
  
  // Redirect to Checkout
  const result = await stripe?.redirectToCheckout({
    sessionId,
  })
  
  if (result?.error) {
    console.error(result.error.message)
  }
}