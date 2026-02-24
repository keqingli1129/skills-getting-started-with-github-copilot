"""
FastAPI tests for Mergington High School Activities Management System

Tests are structured using the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test data and initial conditions
- Act: Execute the code being tested
- Assert: Verify the results
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_activities_returns_list(self):
        """Test that GET /activities returns all available activities"""
        # Arrange
        # No special setup needed - activities are pre-loaded

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert isinstance(activities, dict)
        assert len(activities) > 0


class TestGetRoot:
    """Tests for GET / endpoint"""

    def test_root_redirects_to_static(self):
        """Test that GET / redirects to /static/index.html"""
        # Arrange
        # No special setup needed

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert "/static/index.html" in response.headers["location"]


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_successful(self):
        """Test successful student signup for an activity"""
        # Arrange
        activity_name = "Chess Club"
        email = "newemail@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_activity_not_found(self):
        """Test signup fails when activity does not exist"""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "test@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_signup_duplicate_fails(self):
        """Test that duplicate signup attempts are rejected"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered in initial data

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/participants/{email} endpoint"""

    def test_unregister_successful(self):
        """Test successful student unregistration from activity"""
        # Arrange
        activity_name = "Basketball Team"
        email = "james@mergington.edu"  # Already registered in initial data

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_unregister_activity_not_found(self):
        """Test unregister fails when activity does not exist"""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "test@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_unregister_student_not_found(self):
        """Test unregister fails when student is not registered"""
        # Arrange
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "not signed up" in data["detail"]
