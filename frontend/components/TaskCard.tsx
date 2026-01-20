'use client';

import React, { useState } from 'react';
import { Button } from './ui/Button';
import { Task } from '../../types/task';
import toast from 'react-hot-toast';

interface TaskCardProps {
  task: Task;
  onToggleComplete: (id: number, completed: boolean) => void;
  onUpdate: (id: number, updates: Partial<Task>) => void;
  onDelete: (id: number) => void;
  isUpdating?: boolean;
}

export const TaskCard: React.FC<TaskCardProps> = ({
  task,
  onToggleComplete,
  onUpdate,
  onDelete,
  isUpdating = false,
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || '');

  const handleSave = () => {
    onUpdate(task.id, { title, description });
    setIsEditing(false);
    toast.success('Task updated successfully!');
  };

  const handleCancel = () => {
    setTitle(task.title);
    setDescription(task.description || '');
    setIsEditing(false);
  };

  const handleDelete = () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      onDelete(task.id);
      toast.success('Task deleted successfully!');
    }
  };

  const handleToggleComplete = (e: React.ChangeEvent<HTMLInputElement>) => {
    const completed = e.target.checked;
    onToggleComplete(task.id, completed);
    toast.success(completed ? 'Task marked as complete!' : 'Task marked as incomplete!');
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4 border border-gray-200 dark:border-gray-700">
      {isEditing ? (
        <div className="space-y-3">
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            placeholder="Task title"
          />
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            placeholder="Task description"
            rows={3}
          />
          <div className="flex space-x-2">
            <Button onClick={handleSave} disabled={isUpdating}>
              {isUpdating ? 'Saving...' : 'Save'}
            </Button>
            <Button onClick={handleCancel} variant="outline">
              Cancel
            </Button>
          </div>
        </div>
      ) : (
        <div>
          <div className="flex items-start space-x-3">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={handleToggleComplete}
              className="mt-1 h-5 w-5 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
            />
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between">
                <h3
                  className={`text-lg font-medium ${
                    task.completed
                      ? 'text-gray-500 dark:text-gray-400 line-through'
                      : 'text-gray-900 dark:text-white'
                  }`}
                >
                  {task.title}
                </h3>
                <span className="text-xs font-mono bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-gray-600 dark:text-gray-300">
                  ID: {task.id}
                </span>
              </div>
              {task.description && (
                <p className="mt-1 text-gray-600 dark:text-gray-300">
                  {task.description}
                </p>
              )}
              <div className="mt-2 text-sm text-gray-500 dark:text-gray-400">
                <span>Created: {new Date(task.created_at).toLocaleDateString()}</span>
                {task.updated_at !== task.created_at && (
                  <span className="ml-2">
                    Updated: {new Date(task.updated_at).toLocaleDateString()}
                  </span>
                )}
              </div>
            </div>
          </div>
          <div className="mt-4 flex justify-end space-x-2">
            <Button onClick={() => setIsEditing(true)} variant="outline" size="sm">
              Edit
            </Button>
            <Button onClick={handleDelete} variant="outline" size="sm" className="text-red-600 dark:text-red-400">
              Delete
            </Button>
          </div>
        </div>
      )}
    </div>
  );
};