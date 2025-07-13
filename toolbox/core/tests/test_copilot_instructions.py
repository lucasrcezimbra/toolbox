import os
from pathlib import Path


def test_copilot_instructions_file_exists():
    """Test that the copilot instructions file exists in the correct location."""
    project_root = Path(__file__).parents[3]  # Go up from toolbox/core/tests to project root
    copilot_file = project_root / ".github" / "copilot-instructions.md"
    assert copilot_file.exists(), "copilot-instructions.md should exist in .github directory"


def test_copilot_instructions_file_content():
    """Test that the copilot instructions file contains expected sections."""
    project_root = Path(__file__).parents[3]
    copilot_file = project_root / ".github" / "copilot-instructions.md"
    
    content = copilot_file.read_text()
    
    # Check for key sections that should be in a comprehensive copilot instructions file
    expected_sections = [
        "# Copilot Instructions for Toolbox",
        "## Project Overview",
        "## Architecture",
        "## Development Workflow", 
        "## Code Style and Conventions",
        "## Key Files and Directories",
        "Django",
        "Poetry",
        "make test",
        "pytest"
    ]
    
    for section in expected_sections:
        assert section in content, f"Expected section '{section}' not found in copilot instructions"


def test_copilot_instructions_file_size():
    """Test that the file has reasonable content (not empty, not too small)."""
    project_root = Path(__file__).parents[3]
    copilot_file = project_root / ".github" / "copilot-instructions.md"
    
    file_size = copilot_file.stat().st_size
    assert file_size > 1000, "Copilot instructions file should contain substantial content"
    assert file_size < 50000, "Copilot instructions file should not be excessively large"