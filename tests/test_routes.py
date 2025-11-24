"""
Tests for Flask routes
Student: [YOUR STUDENT NUMBER]
CA3 - DevOps
"""

import pytest
from app import create_app


@pytest.fixture
def app():
    """Create test application."""
    app = create_app('testing')
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


class TestPublicRoutes:
    """Test routes that don't require login."""

    def test_home_page(self, client):
        """Test home page loads."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Welcome to Dice Roller' in response.data

    def test_login_page(self, client):
        """Test login page loads."""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'Login' in response.data


class TestAuthentication:
    """Test login/logout functionality."""

    def test_login_valid_credentials(self, client):
        """Test login with correct credentials."""
        response = client.post('/login', data={
            'username': 'user',
            'password': 'password'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Hello user' in response.data

    def test_login_invalid_credentials(self, client):
        """Test login with wrong credentials."""
        response = client.post('/login', data={
            'username': 'user',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        assert b'Invalid username or password' in response.data

    def test_logout(self, client):
        """Test logout."""
        # Login first
        client.post('/login', data={
            'username': 'user',
            'password': 'password'
        })
        # Then logout
        response = client.get('/logout', follow_redirects=True)
        assert b'logged out' in response.data


class TestProtectedRoutes:
    """Test routes that require login."""

    def test_dashboard_requires_login(self, client):
        """Test dashboard redirects to login."""
        response = client.get('/dashboard')
        assert response.status_code == 302
        assert '/login' in response.location

    def test_dashboard_accessible_when_logged_in(self, client):
        """Test dashboard works after login."""
        client.post('/login', data={
            'username': 'user',
            'password': 'password'
        })
        response = client.get('/dashboard')
        assert response.status_code == 200
        assert b'Hello user' in response.data

    def test_stats_requires_login(self, client):
        """Test stats redirects to login."""
        response = client.get('/stats')
        assert response.status_code == 302


class TestDiceRolling:
    """Test dice rolling via web interface."""

    def test_roll_dice(self, client):
        """Test rolling dice."""
        # Login first
        client.post('/login', data={
            'username': 'user',
            'password': 'password'
        })
        # Roll dice
        response = client.post('/roll', data={
            'num_dice': '2',
            'sides': '6'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Rolled 2d6' in response.data