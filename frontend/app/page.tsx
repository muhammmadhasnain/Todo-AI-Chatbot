'use client';

import { useEffect } from 'react';
import { useSession } from '../lib/auth-client';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function HomePage() {
  const { data: session, isPending: isLoading } = useSession();
  const router = useRouter();

  // Redirect to dashboard if user is logged in
  useEffect(() => {
    if (session?.user) {
      router.push('/dashboard');
    }
  }, [session, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-indigo-100">
      {/* Hero Section */}
      <section className="relative py-20 md:py-32 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-purple-600 to-indigo-700 opacity-10"></div>
        <div className="container mx-auto px-4 relative z-10">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
              AI-Powered <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-indigo-600">Task Management</span> with MCP
            </h1>
            <p className="text-xl text-gray-600 mb-10 max-w-2xl mx-auto">
              Experience the future of productivity with our AI-driven task management system powered by Model Context Protocol (MCP) architecture.
            </p>
            <div className="flex flex-wrap justify-center gap-4 mt-8">
              <span className="px-4 py-2 bg-purple-100 text-purple-800 rounded-full text-sm font-medium">AI-Powered</span>
              <span className="px-4 py-2 bg-indigo-100 text-indigo-800 rounded-full text-sm font-medium">MCP-First</span>
              <span className="px-4 py-2 bg-pink-100 text-pink-800 rounded-full text-sm font-medium">Stateless</span>
              <span className="px-4 py-2 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">Scalable</span>
            </div>
            <div className="flex flex-col sm:flex-row gap-4 justify-center mt-10">
              <Link
                href="/auth/register"
                className="px-8 py-4 bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-200"
              >
                Get Started Free
              </Link>
              <Link
                href="/auth/login"
                className="px-8 py-4 bg-white text-purple-600 font-semibold rounded-lg shadow-lg hover:shadow-xl border border-purple-200 transform hover:-translate-y-1 transition-all duration-200"
              >
                Sign In
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* MCP Architecture Section */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">MCP-First Architecture</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Built on standardized Model Context Protocol tools for seamless AI integration
            </p>
          </div>

          <div className="max-w-4xl mx-auto">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
              <div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">Standardized AI Integration</h3>
                <p className="text-gray-600 mb-6">
                  Our MCP-first architecture exposes every feature as a standardized tool that AI agents can understand and use. This creates a consistent interface between the AI and your application.
                </p>
                <ul className="space-y-3">
                  <li className="flex items-start">
                    <svg className="h-5 w-5 text-green-500 mr-2 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <span className="text-gray-600">5 standardized MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)</span>
                  </li>
                  <li className="flex items-start">
                    <svg className="h-5 w-5 text-green-500 mr-2 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <span className="text-gray-600">Stateless design with persistent database state</span>
                  </li>
                  <li className="flex items-start">
                    <svg className="h-5 w-5 text-green-500 mr-2 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <span className="text-gray-600">Natural language processing for all commands</span>
                  </li>
                  <li className="flex items-start">
                    <svg className="h-5 w-5 text-green-500 mr-2 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <span className="text-gray-600">Scalable and resilient architecture</span>
                  </li>
                </ul>
              </div>
              <div className="bg-gradient-to-br from-purple-50 to-indigo-50 p-8 rounded-xl border border-purple-100">
                <div className="bg-white p-6 rounded-lg shadow-inner">
                  <div className="flex items-center mb-4">
                    <div className="w-3 h-3 bg-red-400 rounded-full mr-2"></div>
                    <div className="w-3 h-3 bg-yellow-400 rounded-full mr-2"></div>
                    <div className="w-3 h-3 bg-green-400 rounded-full"></div>
                    <div className="ml-auto text-sm text-gray-500">AI Task Console</div>
                  </div>
                  <div className="space-y-3 font-mono text-sm">
                    <div className="p-3 bg-gray-100 rounded text-purple-700">AI: "Add a task to buy groceries"</div>
                    <div className="p-3 bg-blue-50 rounded text-blue-700">MCP: add_task(title="Buy groceries")</div>
                    <div className="p-3 bg-green-50 rounded text-green-700">Result: ✓ Task added (ID: 5)</div>
                    <div className="p-3 bg-gray-100 rounded text-purple-700">AI: "Show my pending tasks"</div>
                    <div className="p-3 bg-blue-50 rounded text-blue-700">MCP: list_tasks(status="pending")</div>
                    <div className="p-3 bg-green-50 rounded text-green-700">Result: Found 3 pending tasks</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* AI Capabilities Section */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">AI-Powered Capabilities</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Natural language interaction with intelligent task management
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Capability 1 */}
            <div className="bg-gradient-to-br from-white to-purple-50 p-8 rounded-xl shadow-lg border border-purple-100 hover:shadow-xl transition-shadow duration-300">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-6">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Natural Language Processing</h3>
              <p className="text-gray-600">
                Simply tell the AI what you want to do: "Add a task to prepare quarterly report" or "Show me what's pending for today".
              </p>
            </div>

            {/* Capability 2 */}
            <div className="bg-gradient-to-br from-white to-indigo-50 p-8 rounded-xl shadow-lg border border-indigo-100 hover:shadow-xl transition-shadow duration-300">
              <div className="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center mb-6">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Intelligent Task Management</h3>
              <p className="text-gray-600">
                The AI understands context and relationships between tasks, automatically organizing and prioritizing based on your preferences.
              </p>
            </div>

            {/* Capability 3 */}
            <div className="bg-gradient-to-br from-white to-pink-50 p-8 rounded-xl shadow-lg border border-pink-100 hover:shadow-xl transition-shadow duration-300">
              <div className="w-12 h-12 bg-pink-100 rounded-lg flex items-center justify-center mb-6">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-pink-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">MCP Tool Composition</h3>
              <p className="text-gray-600">
                The AI can chain multiple MCP tools in a single interaction, performing complex operations seamlessly.
              </p>
            </div>

            {/* Capability 4 */}
            <div className="bg-gradient-to-br from-white to-blue-50 p-8 rounded-xl shadow-lg border border-blue-100 hover:shadow-xl transition-shadow duration-300">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-6">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Stateless Architecture</h3>
              <p className="text-gray-600">
                Fully stateless design with persistent database storage ensures scalability and resilience across all interactions.
              </p>
            </div>

            {/* Capability 5 */}
            <div className="bg-gradient-to-br from-white to-green-50 p-8 rounded-xl shadow-lg border border-green-100 hover:shadow-xl transition-shadow duration-300">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-6">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Security-First</h3>
              <p className="text-gray-600">
                Enterprise-grade security with authentication required for all operations and strict user data isolation.
              </p>
            </div>

            {/* Capability 6 */}
            <div className="bg-gradient-to-br from-white to-yellow-50 p-8 rounded-xl shadow-lg border border-yellow-100 hover:shadow-xl transition-shadow duration-300">
              <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center mb-6">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Observability</h3>
              <p className="text-gray-600">
                Comprehensive logging and monitoring for all MCP tool calls and AI interactions with structured error handling.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Natural Language Examples */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Natural Language Commands</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Simply talk to the AI like a colleague to manage your tasks
            </p>
          </div>

          <div className="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="bg-gradient-to-br from-purple-50 to-indigo-50 p-6 rounded-xl border border-purple-100">
              <h3 className="text-lg font-semibold text-purple-700 mb-4">Task Creation</h3>
              <div className="space-y-4">
                <div className="p-4 bg-white rounded-lg shadow">
                  <p className="text-gray-700"><span className="font-semibold">You:</span> "Add a task to buy groceries"</p>
                  <p className="text-blue-600 mt-2"><span className="font-semibold">AI:</span> "Okay, I've added 'Buy groceries' to your task list (ID: 12)."</p>
                </div>
                <div className="p-4 bg-white rounded-lg shadow">
                  <p className="text-gray-700"><span className="font-semibold">You:</span> "I need to remember to call John about the project by Friday"</p>
                  <p className="text-blue-600 mt-2"><span className="font-semibold">AI:</span> "Got it! I've created 'Call John about the project' and noted the Friday deadline."</p>
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-br from-indigo-50 to-purple-50 p-6 rounded-xl border border-indigo-100">
              <h3 className="text-lg font-semibold text-indigo-700 mb-4">Task Management</h3>
              <div className="space-y-4">
                <div className="p-4 bg-white rounded-lg shadow">
                  <p className="text-gray-700"><span className="font-semibold">You:</span> "Show me all my tasks"</p>
                  <p className="text-blue-600 mt-2"><span className="font-semibold">AI:</span> "You have 5 tasks: 3 pending, 2 completed. Would you like me to list them?"</p>
                </div>
                <div className="p-4 bg-white rounded-lg shadow">
                  <p className="text-gray-700"><span className="font-semibold">You:</span> "Mark task 3 as complete"</p>
                  <p className="text-blue-600 mt-2"><span className="font-semibold">AI:</span> "Great! I've marked 'Prepare presentation' as completed."</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Technology Stack */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Built with Modern Tech Stack</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Cutting-edge technologies for exceptional performance and user experience
            </p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto">
            <div className="text-center">
              <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100">
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <svg className="w-6 h-6 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 0c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm-2 17l-5-5.299 1.399-1.43 3.574 3.736 6.572-7.007 1.455 1.403-8 8.597z"/>
                  </svg>
                </div>
                <h3 className="font-semibold text-gray-900">Next.js 16</h3>
                <p className="text-sm text-gray-600 mt-1">React Framework</p>
              </div>
            </div>

            <div className="text-center">
              <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100">
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <svg className="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 0c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm-2 17l-5-5.299 1.399-1.43 3.574 3.736 6.572-7.007 1.455 1.403-8 8.597z"/>
                  </svg>
                </div>
                <h3 className="font-semibold text-gray-900">FastAPI</h3>
                <p className="text-sm text-gray-600 mt-1">Python Backend</p>
              </div>
            </div>

            <div className="text-center">
              <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100">
                <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <svg className="w-6 h-6 text-purple-600" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 0c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm-2 17l-5-5.299 1.399-1.43 3.574 3.736 6.572-7.007 1.455 1.403-8 8.597z"/>
                  </svg>
                </div>
                <h3 className="font-semibold text-gray-900">MCP SDK</h3>
                <p className="text-sm text-gray-600 mt-1">Model Context Protocol</p>
              </div>
            </div>

            <div className="text-center">
              <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100">
                <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <svg className="w-6 h-6 text-yellow-600" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 0c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm-2 17l-5-5.299 1.399-1.43 3.574 3.736 6.572-7.007 1.455 1.403-8 8.597z"/>
                  </svg>
                </div>
                <h3 className="font-semibold text-gray-900">Better Auth</h3>
                <p className="text-sm text-gray-600 mt-1">Authentication</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-purple-600 to-indigo-700">
        <div className="container mx-auto px-4">
          <div className="max-w-3xl mx-auto text-center">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
              Transform Your Productivity with AI
            </h2>
            <p className="text-purple-100 mb-10 text-lg">
              Join thousands of users who have revolutionized their task management with our MCP-first AI platform.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/auth/register"
                className="px-8 py-4 bg-white text-purple-600 font-semibold rounded-lg shadow-lg hover:bg-gray-100 transform hover:-translate-y-1 transition-all duration-200"
              >
                Start Free Trial
              </Link>
              <Link
                href="/demo"
                className="px-8 py-4 bg-transparent border-2 border-white text-white font-semibold rounded-lg hover:bg-white hover:text-purple-600 transform hover:-translate-y-1 transition-all duration-200"
              >
                Watch Demo
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-xl font-bold mb-4">Todo AI</h3>
              <p className="text-gray-400">
                AI-powered task management with MCP-first architecture for the modern world.
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Product</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="#" className="hover:text-white transition-colors">Features</Link></li>
                <li><Link href="#" className="hover:text-white transition-colors">Pricing</Link></li>
                <li><Link href="#" className="hover:text-white transition-colors">Integrations</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="#" className="hover:text-white transition-colors">About</Link></li>
                <li><Link href="#" className="hover:text-white transition-colors">Blog</Link></li>
                <li><Link href="#" className="hover:text-white transition-colors">Careers</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Support</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="#" className="hover:text-white transition-colors">Help Center</Link></li>
                <li><Link href="#" className="hover:text-white transition-colors">Contact</Link></li>
                <li><Link href="#" className="hover:text-white transition-colors">Privacy Policy</Link></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2026 Todo AI. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}