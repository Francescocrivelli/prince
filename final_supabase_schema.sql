
-- Required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ========== USERS ==========
DROP TABLE IF EXISTS public.users CASCADE;
CREATE TABLE public.users (
  id uuid NOT NULL,
  phone text UNIQUE,
  email text UNIQUE,
  created_at timestamp with time zone NOT NULL DEFAULT timezone('utc'::text, now()),
  updated_at timestamp with time zone NOT NULL DEFAULT timezone('utc'::text, now()),
  is_deleted boolean DEFAULT false,
  deleted_at timestamp with time zone,
  reactivated_at timestamp with time zone,
  CONSTRAINT users_pkey PRIMARY KEY (id),
  CONSTRAINT users_id_fkey FOREIGN KEY (id) REFERENCES auth.users (id)
);

-- ========== USER PROFILES ==========
DROP TABLE IF EXISTS public.user_profiles CASCADE;
CREATE TABLE public.user_profiles (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  user_id uuid NOT NULL UNIQUE,
  full_name text,
  university text,
  major text,
  location text,
  stage text,
  bio text,
  most_impressive_fact text,
  linkedin text,
  github text,
  website text,
  twitter text,
  devpost text,
  skills text[],
  interests text[],
  is_verified boolean DEFAULT false,
  created_at timestamp with time zone DEFAULT timezone('utc'::text, now()),
  updated_at timestamp with time zone DEFAULT timezone('utc'::text, now()),
  CONSTRAINT user_profiles_pkey PRIMARY KEY (id),
  CONSTRAINT user_profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- ========== STRIPE SUBSCRIPTIONS ==========
DROP TABLE IF EXISTS public.subscriptions CASCADE;
CREATE TABLE public.subscriptions (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  user_id uuid,
  stripe_customer_id text,
  stripe_subscription_id text,
  status text,
  price_id text,
  cancel_at_period_end boolean DEFAULT false,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  current_period_end timestamp with time zone,
  CONSTRAINT subscriptions_pkey PRIMARY KEY (id),
  CONSTRAINT subscriptions_user_id_fkey FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- ========== RLS ENFORCEMENT ==========
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;
-- Commented out: call_sessions not defined
-- ALTER TABLE public.call_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.subscriptions ENABLE ROW LEVEL SECURITY;

-- ========== RLS POLICIES ==========

-- USERS
CREATE POLICY "Users can read their own data" ON public.users
  FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update their own data" ON public.users
  FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "Service role full access to users" ON public.users
  FOR ALL TO service_role USING (true);

-- USER PROFILES
CREATE POLICY "Users can read their own profiles" ON public.user_profiles
  FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can update their own profiles" ON public.user_profiles
  FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can insert their own profiles" ON public.user_profiles
  FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Service role full access to profiles" ON public.user_profiles
  FOR ALL TO service_role USING (true);

-- SUBSCRIPTIONS
CREATE POLICY "Users can read their own subscriptions" ON public.subscriptions
  FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can update their own subscriptions" ON public.subscriptions
  FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can insert their own subscriptions" ON public.subscriptions
  FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Service role full access to subscriptions" ON public.subscriptions
  FOR ALL TO service_role USING (true);
