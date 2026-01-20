'use client';

import { useState, useEffect } from 'react';
import { useSession, authClient } from '../../lib/auth-client';
import { useRouter } from 'next/navigation';
import { apiClient } from '../../lib/api-client';
import { User } from '../../types/task';

export default function ProfilePage() {
  const { data: session, isPending: isLoading } = useSession();
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [name, setName] = useState('');
  const [isUpdating, setIsUpdating] = useState(false);

  useEffect(() => {
    if (session?.user) {
      fetchUserProfile();
    }
  }, [session]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-gray-600 dark:text-gray-400">Loading...</div>
      </div>
    );
  }

  if (!session?.user) {
    router.push('/auth/login');
    return null;
  }

  const fetchUserProfile = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiClient.get<User>(`/users/${session.user.id}`);
      setUser(response);
      setName(response.name || '');
    } catch (err) {
      setError('Failed to load profile');
      if (process.env.NODE_ENV === 'development') {
        console.error('Error fetching profile:', err);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateProfile = async () => {
    if (!user) return;

    try {
      setIsUpdating(true);
      setError(null);

      const updatedUser = await apiClient.put<User>(`/users/${user.user_id}`, {
        name: name.trim() || null,
      });

      setUser(updatedUser);
      setIsEditing(false);

      // Update session with new name
      if (session?.user && updatedUser.name) {
        await authClient.updateUser({
          name: updatedUser.name
        });
      }
    } catch (err) {
      setError('Failed to update profile');
      if (process.env.NODE_ENV === 'development') {
        console.error('Error updating profile:', err);
      }
    } finally {
      setIsUpdating(false);
    }
  };

  const handleDeleteAccount = async () => {
    if (!user || !window.confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
      return;
    }

    try {
      await apiClient.delete(`/users/${user.user_id}`);
      // Log out after account deletion
      await authClient.signOut();
      router.push('/auth/login');
    } catch (err) {
      setError('Failed to delete account');
      if (process.env.NODE_ENV === 'development') {
        console.error('Error deleting account:', err);
      }
    }
  };

  if (error && !loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 text-center">
            <p className="text-red-700 dark:text-red-300">{error}</p>
            <button
              onClick={fetchUserProfile}
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
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Profile</h1>
          <p className="text-gray-600 dark:text-gray-400">
            Manage your account settings
          </p>
        </div>

        {loading ? (
          <div className="flex justify-center py-8">
            <div className="text-gray-600 dark:text-gray-400">Loading profile...</div>
          </div>
        ) : user ? (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div className="space-y-6">
              <div>
                <h2 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Account Information</h2>

                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Email
                    </label>
                    <div className="text-gray-900 dark:text-white">{user.email}</div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Name
                    </label>
                    {isEditing ? (
                      <div className="flex space-x-2">
                        <input
                          type="text"
                          value={name}
                          onChange={(e) => setName(e.target.value)}
                          className="flex-1 border border-gray-300 dark:border-gray-600 rounded-md px-3 py-2 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                          placeholder="Enter your name"
                        />
                        <button
                          onClick={handleUpdateProfile}
                          disabled={isUpdating}
                          className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 disabled:opacity-50"
                        >
                          {isUpdating ? 'Saving...' : 'Save'}
                        </button>
                        <button
                          onClick={() => {
                            setIsEditing(false);
                            setName(user.name || '');
                          }}
                          className="border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 px-4 py-2 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700"
                        >
                          Cancel
                        </button>
                      </div>
                    ) : (
                      <div className="flex items-center justify-between">
                        <div className="text-gray-900 dark:text-white">
                          {user.name || 'Not set'}
                        </div>
                        <button
                          onClick={() => setIsEditing(true)}
                          className="text-indigo-600 dark:text-indigo-400 hover:underline text-sm"
                        >
                          Edit
                        </button>
                      </div>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Account Status
                    </label>
                    <div className="text-gray-900 dark:text-white">
                      {user.email_verified ? 'Verified' : 'Unverified'} •
                      Created: {new Date(user.created_at).toLocaleDateString()}
                    </div>
                  </div>
                </div>
              </div>

              <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
                <h2 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Danger Zone</h2>
                <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
                  <h3 className="text-red-800 dark:text-red-200 font-medium mb-2">Delete Account</h3>
                  <p className="text-red-700 dark:text-red-300 text-sm mb-4">
                    Permanently delete your account and all associated data. This action cannot be undone.
                  </p>
                  <button
                    onClick={handleDeleteAccount}
                    disabled={isUpdating}
                    className="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 disabled:opacity-50"
                  >
                    Delete Account
                  </button>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-500 dark:text-gray-400">No profile data available</p>
          </div>
        )}
      </div>
    </div>
  );
}