'use client';

import { useEffect, useState } from 'react';
import { useSession } from '../../lib/auth-client';
import { useRouter } from 'next/navigation';
import { apiClient } from '../../lib/api-client';
import { Task } from '../../types/task';

export default function DashboardPage() {
  const { data: session, isPending: isLoading } = useSession();
  const router = useRouter();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [totalTasks, setTotalTasks] = useState(0);

  // Handle redirect outside of render conditionals
  useEffect(() => {
    if (!isLoading && !session?.user) {
      router.push('/auth/login');
    }
  }, [session, isLoading, router]);

  useEffect(() => {
    if (session?.user) {
      fetchTasks();
    }
  }, [session]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      if (!session?.user) return;
      const response = await apiClient.get<Task[]>(`/${session.user.id}/tasks`);
      const fetchedTasks = response || [];
      setTasks(fetchedTasks);

      // Calculate total tasks
      setTotalTasks(fetchedTasks.length);
    } catch (err) {
      if (process.env.NODE_ENV === 'development') {
        console.error('Error fetching tasks:', err);
      }
    } finally {
      setLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-gray-600 dark:text-gray-400">Loading...</div>
      </div>
    );
  }

  if (!session?.user) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-gray-600 dark:text-gray-400">Redirecting to login...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-8">
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              Welcome, {session.user.name || session.user.email}!
            </h1>
            <p className="text-gray-600 dark:text-gray-300">
              Manage your tasks and chat with our AI assistant to help you stay organized.
            </p>
          </div>

          {/* Total Tasks Display */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 border-l-4 border-blue-500">
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-1">Total Tasks</h3>
              <p className="text-3xl font-bold text-blue-600 dark:text-blue-400">{totalTasks}</p>
            </div>

            <div className="bg-indigo-50 dark:bg-indigo-900/20 rounded-lg p-6 border border-indigo-100 dark:border-indigo-800">
              <h2 className="text-lg font-semibold text-indigo-800 dark:text-indigo-200 mb-2">
                Tasks Overview
              </h2>
              <p className="text-gray-600 dark:text-gray-300 mb-4">
                View and manage your tasks efficiently.
              </p>
              <a
                href="/tasks"
                className="inline-block bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
              >
                Manage Tasks
              </a>
            </div>

            <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-6 border border-blue-100 dark:border-blue-800">
              <h2 className="text-lg font-semibold text-blue-800 dark:text-blue-200 mb-2">
                Profile
              </h2>
              <p className="text-gray-600 dark:text-gray-300 mb-4">
                Manage your account settings.
              </p>
              <a
                href="/profile"
                className="inline-block bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
              >
                View Profile
              </a>
            </div>
          </div>

          {/* Recent Tasks */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Recent Tasks</h2>
            {loading ? (
              <div className="text-center py-4 text-gray-600 dark:text-gray-400">Loading tasks...</div>
            ) : tasks.length === 0 ? (
              <div className="text-center py-4 text-gray-500 dark:text-gray-400">
                No tasks yet. Start by adding your first task!
              </div>
            ) : (
              <div className="space-y-3">
                {tasks.slice(0, 5).map((task) => (
                  <div
                    key={task.id}
                    className={`flex items-center p-3 rounded-md border ${
                      task.completed
                        ? 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800'
                        : 'bg-gray-50 dark:bg-gray-700/50 border-gray-200 dark:border-gray-700'
                    }`}
                  >
                    <input
                      type="checkbox"
                      checked={task.completed}
                      readOnly
                      className="h-4 w-4 text-indigo-600 rounded disabled:opacity-50"
                    />
                    <span className={`ml-3 flex-1 ${task.completed ? 'line-through text-gray-500 dark:text-gray-400' : 'text-gray-900 dark:text-white'}`}>
                      {task.title}
                    </span>
                    <span className="text-xs text-gray-500 dark:text-gray-400">
                      {new Date(task.created_at).toLocaleDateString()}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}