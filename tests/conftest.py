"""
Pytest configuration and fixtures for Playwright tests.
"""
import pytest
from pathlib import Path


def pytest_configure(config):
    """Create screenshots directory if it doesn't exist."""
    screenshots_dir = Path(__file__).parent / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context for tests."""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
    }
