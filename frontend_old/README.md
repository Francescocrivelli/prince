# Prince - Frontend

A modern, feature-rich frontend application built with Next.js and various powerful libraries.

## Features

- 🔐 Authentication with Supabase
- 💳 Stripe payment integration
- 🌓 Dark mode support
- 📱 Responsive design
- 🎨 Tailwind CSS styling
- 🔄 Framer Motion animations
- 🛡️ TypeScript support
- 📊 Error boundary implementation
- 🔍 SEO optimized

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn
- A Supabase account
- A Stripe account
- A Google Cloud Platform account (for Google Auth)

### Environment Variables

Create a `.env.local` file in the root directory with the following variables:

```
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8080
NEXT_PUBLIC_WS_URL=ws://localhost:8080

# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

# Stripe Configuration
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
NEXT_PUBLIC_STRIPE_BUTTON_ID=your_stripe_button_id
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret

# Google Auth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

### Installation

1. Clone the repository
2. Install dependencies:

```bash
npm install
# or
yarn install
```

3. Run the development server:

```bash
npm run dev
# or
yarn dev
```

4. Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Database Schema

The application expects the following tables to be set up in your Supabase database:

- `users`: Store user information
- `user_preferences`: Store user preferences
- `user_trials`: Manage trial periods
- `subscriptions`: Track user subscriptions

## Deployment

The application can be deployed to any platform that supports Next.js, such as Vercel, Netlify, or custom servers.

```bash
npm run build
npm run start
```

## Learn More

To learn more about the technologies used in this project:

- [Next.js Documentation](https://nextjs.org/docs)
- [Supabase Documentation](https://supabase.io/docs)
- [Stripe Documentation](https://stripe.com/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Framer Motion Documentation](https://www.framer.com/motion/)

## License

This project is licensed under the MIT License.