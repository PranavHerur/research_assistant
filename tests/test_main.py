"""
Test cases for the main module.
"""

from research_assistant.main import hello


def test_hello():
    """Test the hello function."""
    assert hello() == "Hello from Research Assistant!"
