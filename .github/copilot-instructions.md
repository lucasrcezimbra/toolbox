# Copilot Instructions for Toolbox

This repository contains a Django-based web application that manages a curated catalog of development tools, primarily sourced from GitHub starred repositories.

## Project Overview

**Toolbox** is a Django 5.2 web application that:
- Collects development tools from GitHub starred repositories using `github-to-sqlite`
- Organizes tools with tagging, notes, and curated lists
- Provides a web interface with Bootstrap styling and HTMX interactivity
- Generates static sites for deployment to GitHub Pages using `django-distill`

## Architecture

### Core Technologies
- **Backend**: Django 5.2 with SQLite database
- **Frontend**: Bootstrap 5 with HTMX for dynamic interactions
- **Data Collection**: `github-to-sqlite` for extracting starred repos
- **Static Generation**: `django-distill` for GitHub Pages deployment
- **Package Management**: Poetry for dependency management
- **Code Quality**: Pre-commit hooks with ruff linting and djlint

### Key Models
- **Tool**: Represents a development tool with GitHub URL, documentation, tags, star count, and notes
- **List**: Curated collections of tools with many-to-many relationship to tools
- **User**: Custom user model extending Django's base user

### Data Flow
1. **Collection**: `github-to-sqlite` extracts starred repos to `github.sqlite3`
2. **Import**: `import_from_github.py` processes GitHub data into Django models
3. **Enhancement**: `loadnotes.py` adds curated notes from `data/partial_tools_notes.json`
4. **Presentation**: Django views serve tools, lists, and tags with HTMX interactivity

## Development Workflow

### Setup Commands
```bash
make install          # Install dependencies, setup pre-commit hooks, copy env file, run migrations
make datacollect github=<username>  # Collect GitHub starred repos data
make dbnew                         # Reset database (drops and recreates)
make dbload                        # Import collected data into database
```

### Development Commands
```bash
make dev              # Start Django development server
make test             # Run pytest test suite
make lint             # Run pre-commit hooks (ruff linting, djlint, etc.)
make build            # Generate static site for deployment
```

### Data Management
```bash
make dataupdate github=<username>  # Full data refresh (collect + rebuild DB + load)
make dbdump           # Export current data to JSON files
make datafix          # Fix data inconsistencies (URL redirects, etc.)
```

## Code Style and Conventions

### Python Code
- Use **ruff** for linting with the configuration in `pyproject.toml`
- Follow Django best practices for models, views, and templates
- Use function-based views (current pattern in `toolbox/core/views.py`)
- Prefer simple, readable code over complex abstractions

### Django Patterns
- Models use natural keys for data import/export
- Management scripts are in `toolbox/core/scripts/` for data operations
- Templates use Bootstrap classes and HTMX attributes for interactivity
- URL patterns support both regular views and django-distill static generation

### Testing
- Use **pytest** with `pytest-django` plugin
- Tests are in `*/tests/` directories
- Use `@pytest.mark.django_db` for database-dependent tests
- Use `model-bakery` for creating test data
- Follow the pattern in `toolbox/core/tests/test_view_index.py`

### Templates
- Use **djlint** for template linting
- Follow Bootstrap conventions for styling
- Use HTMX attributes for dynamic content loading
- Templates are in `toolbox/core/templates/`

## Key Files and Directories

### Core Application
- `toolbox/core/models.py` - Tool, List, and core data models
- `toolbox/core/views.py` - Main view functions
- `toolbox/core/templates/` - HTML templates
- `toolbox/core/scripts/` - Data management scripts
- `toolbox/settings.py` - Django configuration

### Development Configuration
- `pyproject.toml` - Poetry dependencies and tool configuration
- `Makefile` - Development commands and workflows
- `.pre-commit-config.yaml` - Code quality hooks
- `CLAUDE.md` - Detailed development documentation

### Data Management
- `data/` - JSON files for lists and tool notes
- `bin/datafix` - Script for fixing URL redirects and data issues
- `manage.py` - Django management interface

### CI/CD
- `.github/workflows/python-app.yml` - Test workflow
- `.github/workflows/publish.yaml` - Deployment workflow with automatic data fixing

## Development Guidelines

### Making Changes
1. **Always use Poetry**: Run commands with `poetry run` or use `make` commands
2. **Always run `make lint` before each commit**: This runs pre-commit hooks (ruff, black, djlint, etc.) to ensure code quality and style consistency
3. **Database workflow**: Always run `make dbnew` before `make dbload` for fresh data
4. **Testing**: Write tests for new functionality following existing patterns
5. **Data migrations**: Not needed - database is recreated by `dbnew` script
6. **URL handling**: The system automatically fixes GitHub URL redirects via `datafix`

### Common Tasks
- **Adding new tools**: Import via GitHub data collection, enhance with manual notes
- **Creating lists**: Use Django admin or management scripts
- **Updating dependencies**: Use `poetry add/update` commands
- **Fixing data issues**: Use `make datafix` for automatic URL correction

### Best Practices
- Prefer `make` commands over direct poetry/python calls
- **Always run `make lint` before committing changes** to ensure code quality and prevent CI failures
- Always test locally before pushing changes
- Use existing Bootstrap and HTMX patterns for UI changes
- Keep the codebase simple and maintainable
- Document any new data collection or processing logic

## Static Site Generation

The application generates static sites for GitHub Pages deployment:
- Uses `django-distill` to render all pages as static HTML
- Static files are compressed using whitenoise with brotli
- CNAME file is automatically generated for custom domain
- All database queries are executed during build time

## Troubleshooting

### Common Issues
- **Missing SECRET_KEY**: Copy `contrib/env-sample` to `.env`
- **Test failures**: Ensure database is migrated with `poetry run python manage.py migrate`
- **URL errors in data**: Run `make datafix` to resolve GitHub redirects
- **Build failures**: Check that all dependencies are installed with `make install`

### Data Consistency
- The system is designed to fail fast on missing tools to trigger automatic fixes
- CI automatically runs `datafix` on failures and creates PRs with corrections
- URL normalization converts all GitHub URLs to lowercase for consistency
