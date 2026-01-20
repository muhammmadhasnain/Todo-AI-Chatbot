'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useSession, signOut } from '../lib/auth-client';
import { Button } from './ui/Button';

export default function Navigation() {
  const pathname = usePathname();
  const { data: session, isPending: isLoading } = useSession();

  const handleSignOut = async () => {
    await signOut();
  };

  const navLinks = [
    { name: 'Home', href: '/' },
    { name: 'Dashboard', href: '/dashboard' },
    { name: 'Tasks', href: '/tasks' },
  ];

  return (
    <nav className="bg-white dark:bg-gray-800 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href={session?.user ? '/dashboard' : '/'} className="flex-shrink-0 flex items-center">
              <span className="text-xl font-bold text-indigo-600 dark:text-indigo-400">
                Todo AI
              </span>
            </Link>
            <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
              {navLinks.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`${
                    pathname === link.href
                      ? 'border-indigo-500 text-gray-900 dark:text-white'
                      : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 dark:text-gray-300 dark:hover:text-white'
                  } inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium`}
                >
                  {link.name}
                </Link>
              ))}
            </div>
          </div>
          <div className="flex items-center">
            {isLoading ? (
              <div className="text-gray-500 dark:text-gray-400">Loading...</div>
            ) : session?.user ? (
              <div className="flex items-center space-x-4">
                <span className="text-gray-700 dark:text-gray-300 hidden md:block">
                  {session.user.email}
                </span>
                <Button
                  onClick={handleSignOut}
                  variant="outline"
                  className="text-sm"
                >
                  Sign Out
                </Button>
              </div>
            ) : (
              <div className="flex space-x-4">
                <Link href="/auth/login">
                  <Button variant="outline" className="text-sm">
                    Log in
                  </Button>
                </Link>
                <Link href="/auth/register">
                  <Button className="text-sm">Sign up</Button>
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}