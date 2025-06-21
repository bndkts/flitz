# Contributing

Thank you for your interest in contributing to Flitz!

## Development Setup

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/flitz.git
   cd flitz
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

5. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Development Workflow

### Code Style

We use several tools to maintain code quality:

- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

Run all checks:
```bash
pre-commit run --all-files
```

### Testing

Run the test suite:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=flitz --cov-report=html
```

### Documentation

Build documentation locally:
```bash
cd docs
make html
```

The documentation will be available in `docs/_build/html/index.html`.

## Submitting Changes

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature-name
   ```

2. Make your changes and add tests

3. Ensure all tests pass:
   ```bash
   pytest
   pre-commit run --all-files
   ```

4. Commit your changes:
   ```bash
   git add .
   git commit -m "Add feature description"
   ```

5. Push to your fork:
   ```bash
   git push origin feature-name
   ```

6. Create a Pull Request on GitHub

## Guidelines

### Code Guidelines

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write docstrings for all public functions and classes
- Keep functions small and focused
- Use pathlib instead of os.path

### Testing Guidelines

- Write tests for all new features
- Use pytest fixtures instead of TestCase classes
- Aim for high test coverage
- Test both happy path and error cases

### Documentation Guidelines

- Update documentation for any user-facing changes
- Use clear, concise language
- Include code examples where helpful
- Keep the README up to date

## Issue Reporting

When reporting issues:

1. Check if the issue already exists
2. Provide a clear description
3. Include steps to reproduce
4. Mention your operating system and Python version
5. Include relevant error messages

## Feature Requests

When requesting features:

1. Check if the feature already exists or is planned
2. Provide a clear use case
3. Explain why the feature would be valuable
4. Consider if it fits the project's scope

## Getting Help

- Check the documentation first
- Search existing issues
- Ask questions in discussions
- Join our community chat (if available)

Thank you for contributing to Flitz!
