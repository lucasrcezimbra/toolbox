# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Installation and Setup
```bash
make install          # Install dependencies, setup pre-commit hooks, copy env file, run migrations
```

### Development Server
```bash
make dev              # Start Django development server
```

### Testing and Quality
```bash
make test             # Run pytest test suite
make lint             # Run pre-commit hooks (includes ruff linting, djlint, and other checks)
poetry run pytest    # Run specific tests
```

### Data Management
```bash
# Data collection and import workflow:
make datacollect github=<username>  # Collect GitHub starred repos data
make dbload                        # Import collected data into database
make dataupdate github=<username>  # Full data refresh (collect + rebuild DB + load)

# Database operations:
make dbnew            # Reset database (drops and recreates)
make dbdump           # Export current data to JSON files
make datafix          # Fix data inconsistencies
```

### Static Site Generation
```bash
make build            # Generate static site using django-distill
```

## Architecture Overview

This is a Django-based web application that manages a catalog of development tools, primarily sourced from GitHub starred repositories.

### Core Models
- **Tool**: Represents a development tool with GitHub URL, documentation, tags, star count, and notes
- **List**: Curated collections of tools with many-to-many relationship to tools
- **User**: Custom user model (extends Django's base user)

### Data Flow
1. **Collection**: `github-to-sqlite` extracts starred repos to `github.sqlite3`
2. **Import**: `import_from_github.py` script processes GitHub data into Django models
3. **Enhancement**: `loadnotes.py` adds curated notes from `data/partial_tools_notes.json`
4. **Presentation**: Django views serve tools, lists, and tags with HTMX interactivity

### Key Components
- **Views**: Simple function-based views in `toolbox/core/views.py`
- **Templates**: Bootstrap-based templates with HTMX for dynamic content
- **URL Patterns**: Uses `django-distill` for static site generation capabilities
- **Tags**: Leverages `django-taggit` for flexible tagging system
- **Scripts**: Django management scripts in `toolbox/core/scripts/` for data operations

### Technology Stack
- Django 5.2 with HTMX for interactivity
- SQLite database (with django-distill for static generation)
- Poetry for dependency management
- Bootstrap for UI styling
- Pre-commit hooks with ruff for code quality

### Development Notes
- Uses Poetry for dependency management - always use `poetry run` for commands
- Pre-commit hooks enforce code quality (ruff linting, djlint for templates)
- Static files served via whitenoise with compression
- Database URL configured via environment variables
- Tools are automatically tagged with "opensource" and programming language tags

### Best Practices
- Always prefer make commands; avoid using poetry and python directly
- Always run dbnew before dbload

### Data Import and URL Management
The data import process handles GitHub repository URL changes automatically:

1. **URL Normalization**: `import_from_github.py` converts all GitHub URLs to lowercase to ensure consistency
2. **Automatic URL Fixing**: When `loadnotes.py` fails due to changed GitHub URLs, the CI workflow automatically runs `make datafix`
3. **Datafix Process**: The `bin/datafix` script detects failed URLs, follows redirects, and updates JSON files with correct URLs
4. **CI Integration**: GitHub Actions workflow automatically handles URL changes by running datafix on failures and creating PRs with fixes

**Important**: The `loadnotes.py` script is designed to fail fast when encountering missing tools, allowing the automated datafix process to resolve URL changes. This ensures the CI process can automatically maintain data consistency when GitHub repositories are moved or renamed.
