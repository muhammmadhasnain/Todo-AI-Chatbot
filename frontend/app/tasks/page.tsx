'use client';

import { useState, useEffect } from 'react';
import { useSession } from '../../lib/auth-client';
import { useRouter } from 'next/navigation';
import { TaskForm } from '../../components/TaskForm';
import { TaskCard } from '../../components/TaskCard';
import { Task } from '../../types/task';
import { apiClient } from '../../lib/api-client';

export default function TasksPage() {
  const { data: session, isPending: isLoading } = useSession();
  const router = useRouter();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch tasks when component mounts and session is available
  useEffect(() => {
    if (session?.user) {
      fetchTasks();
    }
  }, [session]);

  // Handle redirect outside of render conditionals
  useEffect(() => {
    if (!isLoading && !session?.user) {
      router.push('/auth/login');
    }
  }, [session, isLoading, router]);

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

  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);

      // Validate session data exists before attempting API call
      if (!session?.user?.id) {
        throw new Error('User session is not properly initialized');
      }

      const response = await apiClient.get<Task[]>(`/${session.user.id}/tasks`);
      setTasks(response || []);
    } catch (err) {
      if (process.env.NODE_ENV === 'development') {
        console.error('Error fetching tasks:', err);
      }
      setError(err instanceof Error ? err.message : 'Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleAddTask = async (title: string, description?: string) => {
    try {
      // Validate session data exists before attempting API call
      if (!session?.user?.id) {
        throw new Error('User session is not properly initialized');
      }

      const newTask = await apiClient.post<Task>(`/${session.user.id}/tasks`, {
        title,
        description,
      });
      setTasks([newTask, ...tasks]);
    } catch (err) {
      if (process.env.NODE_ENV === 'development') {
        console.error('Error adding task:', err);
      }
      setError(err instanceof Error ? err.message : 'Failed to add task');
    }
  };

  const handleToggleComplete = async (id: number, completed: boolean) => {
    try {
      // Validate session data exists before attempting API call
      if (!session?.user?.id) {
        throw new Error('User session is not properly initialized');
      }

      const updatedTask = await apiClient.put<Task>(`/${session.user.id}/tasks/${id}`, {
        completed: completed,
      });

      setTasks(tasks.map(task =>
        task.id === id ? updatedTask : task
      ));
    } catch (err) {
      if (process.env.NODE_ENV === 'development') {
        console.error('Error updating task:', err);
      }
      setError(err instanceof Error ? err.message : 'Failed to update task');
    }
  };

  const handleUpdateTask = async (id: number, updates: Partial<Task>) => {
    try {
      // Validate session data exists before attempting API call
      if (!session?.user?.id) {
        throw new Error('User session is not properly initialized');
      }

      const updatedTask = await apiClient.put<Task>(`/${session.user.id}/tasks/${id}`, updates);

      setTasks(tasks.map(task =>
        task.id === id ? updatedTask : task
      ));
    } catch (err) {
      if (process.env.NODE_ENV === 'development') {
        console.error('Error updating task:', err);
      }
      setError(err instanceof Error ? err.message : 'Failed to update task');
    }
  };

  const handleDeleteTask = async (id: number) => {
    try {
      // Validate session data exists before attempting API call
      if (!session?.user?.id) {
        throw new Error('User session is not properly initialized');
      }

      await apiClient.delete(`/${session.user.id}/tasks/${id}`);
      setTasks(tasks.filter(task => task.id !== id));
    } catch (err) {
      if (process.env.NODE_ENV === 'development') {
        console.error('Error deleting task:', err);
      }
      setError(err instanceof Error ? err.message : 'Failed to delete task');
    }
  };

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 text-center">
            <p className="text-red-700 dark:text-red-300">{error}</p>
            <button
              onClick={fetchTasks}
              className="mt-2 text-red-600 dark:text-red-400 hover:underline"
            >
              Retry
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Your Tasks</h1>
          <p className="text-gray-600 dark:text-gray-400">
            Manage your tasks and stay organized
          </p>
        </div>

        <TaskForm onSubmit={handleAddTask} />

        {loading ? (
          <div className="flex justify-center py-8">
            <div className="text-gray-600 dark:text-gray-400">Loading tasks...</div>
          </div>
        ) : tasks.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500 dark:text-gray-400">No tasks yet. Add your first task above!</p>
          </div>
        ) : (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
              {tasks.filter(t => !t.completed).length} pending, {tasks.filter(t => t.completed).length} completed
            </h2>
            <div className="space-y-4">
              {tasks.map(task => (
                <TaskCard
                  key={task.id}
                  task={task}
                  onToggleComplete={handleToggleComplete}
                  onUpdate={handleUpdateTask}
                  onDelete={handleDeleteTask}
                />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}