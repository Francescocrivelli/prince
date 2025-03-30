"use client"

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { ThemeToggle } from './ui/theme-toggle'
import { Button } from './ui/button'
import { cn } from '@/utils/cn'
import { Menu, X, Sparkles } from 'lucide-react'

export default function Navbar() {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false)
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState<boolean>(false)
  const router = useRouter()

  // In a real app, you'd check authentication with Supabase here
  // For now, we'll just mock it
  useEffect(() => {
    const checkUser = async () => {
      setIsAuthenticated(false) // Mock: not authenticated by default
    }

    checkUser()
  }, [])

  const handleSignOut = async () => {
    // Mock sign out
    setIsAuthenticated(false)
    router.push('/')
  }

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen)
  }

  const scrollToSection = (id: string) => {
    setIsMobileMenuOpen(false)
    const element = document.getElementById(id)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' })
    }
  }

  return (
    <nav className="sticky top-0 z-50 w-full border-b border-solid border-gray-200 dark:border-gray-800 bg-white/90 dark:bg-gray-950/90 backdrop-blur-sm">
      <div className="container flex h-16 items-center justify-between">
        <div className="flex items-center gap-6">
          <Link href="/" className="flex items-center gap-2">
            <div className="h-8 w-8 rounded-md bg-indigo-600 dark:bg-indigo-500 flex items-center justify-center">
              <span className="text-lg text-white">🐰</span>
            </div>
            <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-violet-600 dark:from-indigo-400 dark:to-violet-400">
              Find My Bun
            </span>
          </Link>
          <div className="hidden md:flex items-center gap-6">
            <button
              onClick={() => scrollToSection('features')}
              className="text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors"
            >
              Features
            </button>
            <button
              onClick={() => scrollToSection('pricing')}
              className="text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors"
            >
              Pricing
            </button>
            <button
              onClick={() => scrollToSection('success-stories')}
              className="text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors"
            >
              Success Stories
            </button>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="hidden md:flex items-center gap-4">
            {isAuthenticated ? (
              <>
                <Link href="/profile">
                  <Button variant="ghost" className="hover:text-indigo-600 dark:hover:text-indigo-400">Dashboard</Button>
                </Link>
                <Button 
                  variant="outline" 
                  onClick={handleSignOut}
                  className="border-gray-200 dark:border-gray-800 hover:border-indigo-600 hover:text-indigo-600 dark:hover:border-indigo-400 dark:hover:text-indigo-400"
                >
                  Sign Out
                </Button>
              </>
            ) : (
              <>
                <Link href="/login">
                  <Button 
                    variant="ghost" 
                    className="hover:text-indigo-600 dark:hover:text-indigo-400"
                  >
                    Sign In
                  </Button>
                </Link>
                <Link href="https://docs.google.com/forms/d/1nK9EPoqgmn4q2mpD5Q53IZR29J3oAP1mOupAw292Oo4/edit" target="_blank">
                  <Button className="bg-indigo-600 hover:bg-indigo-700 dark:bg-indigo-600 dark:hover:bg-indigo-700 text-white">
                    Apply Now
                  </Button>
                </Link>
              </>
            )}
          </div>
          <ThemeToggle />
          <Button
            variant="ghost"
            size="icon"
            className="md:hidden"
            onClick={toggleMobileMenu}
          >
            {isMobileMenuOpen ? (
              <X className="h-5 w-5" />
            ) : (
              <Menu className="h-5 w-5" />
            )}
          </Button>
        </div>
      </div>

      {/* Mobile menu */}
      <div
        className={cn(
          "md:hidden fixed inset-x-0 top-16 z-50 mt-px bg-white dark:bg-gray-950 border-b border-solid border-gray-200 dark:border-gray-800 transition-all duration-200 ease-in-out",
          isMobileMenuOpen ? "block" : "hidden"
        )}
      >
        <div className="container space-y-4 py-4">
          <button
            onClick={() => scrollToSection('features')}
            className="block w-full text-left py-2 text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-indigo-600 dark:hover:text-indigo-400"
          >
            Features
          </button>
          <button
            onClick={() => scrollToSection('pricing')}
            className="block w-full text-left py-2 text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-indigo-600 dark:hover:text-indigo-400"
          >
            Pricing
          </button>
          <button
            onClick={() => scrollToSection('success-stories')}
            className="block w-full text-left py-2 text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-indigo-600 dark:hover:text-indigo-400"
          >
            Success Stories
          </button>
          <div className="flex flex-col gap-2 pt-2">
            {isAuthenticated ? (
              <>
                <Link href="/profile" onClick={() => setIsMobileMenuOpen(false)}>
                  <Button variant="ghost" className="w-full justify-start hover:text-indigo-600 dark:hover:text-indigo-400">
                    Dashboard
                  </Button>
                </Link>
                <Button 
                  variant="outline" 
                  onClick={handleSignOut} 
                  className="w-full justify-start border-gray-200 dark:border-gray-800 hover:border-indigo-600 hover:text-indigo-600 dark:hover:border-indigo-400 dark:hover:text-indigo-400"
                >
                  Sign Out
                </Button>
              </>
            ) : (
              <>
                <Link href="/login" onClick={() => setIsMobileMenuOpen(false)}>
                  <Button variant="ghost" className="w-full justify-start hover:text-indigo-600 dark:hover:text-indigo-400">
                    Sign In
                  </Button>
                </Link>
                <Link 
                  href="https://docs.google.com/forms/d/1nK9EPoqgmn4q2mpD5Q53IZR29J3oAP1mOupAw292Oo4/edit" 
                  target="_blank" 
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  <Button className="w-full justify-start bg-indigo-600 hover:bg-indigo-700 dark:bg-indigo-600 dark:hover:bg-indigo-700 text-white">
                    Apply Now
                  </Button>
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}