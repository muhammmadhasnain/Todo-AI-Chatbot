// End-to-end tests for authentication flows
// These tests verify the complete authentication flow from registration to API access

import { test, expect, describe } from '@playwright/test';

describe('Authentication Flow Tests', () => {
  test('Complete registration and login flow', async ({ page }) => {
    // Navigate to registration page
    await page.goto('/register');

    // Fill in registration form
    await page.locator('input[name="email"]').fill('test@example.com');
    await page.locator('input[name="password"]').fill('securePassword123');
    await page.locator('input[name="confirmPassword"]').fill('securePassword123');

    // Submit registration
    await page.locator('button[type="submit"]').click();

    // Verify redirect to email verification page
    await expect(page).toHaveURL(/\/verify-email/);

    // Simulate email verification (in real tests, you'd need to handle the email verification)
    // For now, we'll assume verification happened and go to login

    await page.goto('/login');

    // Fill in login form
    await page.locator('input[name="email"]').fill('test@example.com');
    await page.locator('input[name="password"]').fill('securePassword123');

    // Submit login
    await page.locator('button[type="submit"]').click();

    // Verify successful login redirects to dashboard
    await expect(page).toHaveURL(/\/dashboard/);
  });

  test('API access with valid session', async ({ page, request }) => {
    // First, authenticate the user
    await page.goto('/login');
    await page.locator('input[name="email"]').fill('test@example.com');
    await page.locator('input[name="password"]').fill('securePassword123');
    await page.locator('button[type="submit"]').click();

    // Wait for session to be established
    await page.waitForURL('/dashboard');

    // Get the session token from local storage or cookies
    const storageState = await page.context().storageState();

    // Make an API request with the session
    const response = await request.get('/api/test-user-id/tasks', {
      headers: {
        'Authorization': `Bearer ${storageState.cookies.find(c => c.name.includes('auth'))?.value || 'mock-token'}`
      }
    });

    expect(response.status()).toBe(200);
  });

  test('Session invalidation handling', async ({ page }) => {
    // Test that expired/invalid sessions redirect to login
    await page.goto('/dashboard');

    // Simulate session expiration (this would depend on your implementation)
    // Clear auth cookies/tokens to simulate invalid session
    await page.context().clearCookies();

    // Try to access protected route
    await page.goto('/dashboard');

    // Should redirect to login
    await expect(page).toHaveURL(/\/login/);
  });
});