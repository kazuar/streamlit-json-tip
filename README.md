# Streamlit JSON Tip

A Streamlit custom component for viewing JSON data with interactive tooltips and tags for individual fields.

![Streamlit JSON Tip Example](https://gist.github.com/kazuar/a33a82e702354f5da0f89bcd848632b9/raw/82a847a11de01d7e3340343035ce2fa20ac0da48/example.png)

## Features

- 🔍 **Interactive JSON Viewer**: Expand/collapse objects and arrays
- 📝 **Interactive Tooltips**: Add contextual help for any field with professional Tippy.js tooltips
- 🏷️ **Field Tags**: Categorize fields with colored tags (PII, CONFIG, etc.)
- 🎯 **Field Selection**: Click on fields to get detailed information
- 🎨 **Syntax Highlighting**: Color-coded JSON with proper formatting
- 📱 **Responsive Design**: Works well in different screen sizes

## Installation

### With uv (Recommended)

```bash
uv add streamlit-json-tip
```

Or for a one-off script:
```bash
uv run --with streamlit-json-tip streamlit run your_app.py
```

### With pip

```bash
pip install streamlit-json-tip
```

### From TestPyPI (Latest Development Version)

With uv:
```bash
uv add --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ streamlit-json-tip
```

With pip:
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ streamlit-json-tip
```

### Development Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/isaac/streamlit-json-tip.git
   cd streamlit-json-tip
   ```

2. Set up development environment with uv:
   ```bash
   # Install uv if you haven't already
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Create virtual environment and install all dependencies (including dev dependencies)
   uv sync
   ```

3. Run the example app:
   ```bash
   uv run streamlit run example_app.py
   ```

## Usage

```python
import streamlit as st
from streamlit_json_tip import json_viewer

# Your JSON data
data = {
    "user": {
        "id": 123,
        "name": "John Doe",
        "email": "john@example.com"
    }
}

# Help text for specific fields
help_text = {
    "user.id": "Unique user identifier",
    "user.name": "Full display name",
    "user.email": "Primary contact email"
}

# Tags for categorizing fields
tags = {
    "user.id": "ID",
    "user.name": "PII",
    "user.email": "PII"
}

# Display the JSON viewer
selected = json_viewer(
    data=data,
    help_text=help_text,
    tags=tags,
    height=400
)

# Handle field selection
if selected:
    st.write(f"Selected field: {selected['path']}")
    st.write(f"Value: {selected['value']}")
    if selected.get('help_text'):
        st.write(f"Help: {selected['help_text']}")
```

## Parameters

- **data** (dict): The JSON data to display
- **help_text** (dict, optional): Dictionary mapping field paths to help text
- **tags** (dict, optional): Dictionary mapping field paths to tags/labels  
- **height** (int, optional): Height of the component in pixels (default: 400)
- **key** (str, optional): Unique key for the component

## Field Path Format

Field paths use dot notation for objects and bracket notation for arrays:
- `"user.name"` - Object field
- `"items[0].title"` - Array item field
- `"settings.preferences.theme"` - Nested object field

## Development

### Frontend Development

1. Set up the development environment (see Development Setup above)

2. Navigate to the frontend directory:
   ```bash
   cd streamlit_json_tip/frontend
   ```

3. Install frontend dependencies:
   ```bash
   npm install
   ```

4. Start development server:
   ```bash
   npm start
   ```

5. In your Python code, set `_RELEASE = False` in `__init__.py`

6. Run the example app in another terminal:
   ```bash
   uv run streamlit run example_app.py
   ```

### Running Tests

#### Python Tests
```bash
# Run all Python unit tests with coverage
uv run pytest

# Run tests with verbose output
uv run pytest -v

# Generate HTML coverage report
uv run pytest --cov-report=html
```

#### Frontend Tests
```bash
cd streamlit_json_tip/frontend

# Run Jest tests once
npm test -- --ci --watchAll=false

# Run tests with coverage
npm test -- --coverage --ci --watchAll=false

# Run tests in watch mode (for development)
npm test
```

#### Run All Tests
Both Python and frontend tests run automatically in GitHub Actions on every push and pull request.

### Building for Production

1. Build the frontend:
   ```bash
   cd streamlit_json_tip/frontend
   npm run build
   ```

2. Set `_RELEASE = True` in `__init__.py`

3. Build the Python package:
   ```bash
   uv run python -m build
   ```

4. Upload to PyPI:
   ```bash
   uv run python -m twine upload dist/*
   ```

### Build Scripts

The project includes convenient uv scripts for common development tasks:

#### Frontend Development
```bash
uv run build-frontend        # Build React frontend for production
```

#### Package Building
```bash
uv run clean                 # Clean build artifacts
uv run build                 # Clean + build Python package
uv run build-check           # Build + validate package with twine
```

#### Publishing
```bash
uv run publish-test          # Build + upload to TestPyPI
uv run publish               # Build + upload to PyPI
```

#### Complete Workflow
```bash
uv run release-test          # Build frontend + publish to TestPyPI
uv run release               # Build frontend + publish to PyPI (production)
```

For a complete release, simply run:
```bash
uv run release
```

This will build the frontend, package the Python distribution, validate it, and upload to PyPI.

## Releasing a New Version

This project uses automated GitHub Actions for releases. Follow these steps to release a new version:

### 1. Update Version and Changelog

1. **Update the version** in `pyproject.toml`:
   ```toml
   version = "0.2.5"  # Increment according to semver
   ```

2. **Add changelog entry** in `CHANGELOG.md`:
   ```markdown
   ## [0.2.5] - 2025-01-26

   ### ✨ Added
   - New feature description

   ### 🔧 Fixed  
   - Bug fix description
   ```

3. **Commit your changes**:
   ```bash
   git add pyproject.toml CHANGELOG.md
   git commit -m "Bump version to 0.2.5"
   git push origin main
   ```

### 2. Create and Push Release Tag

```bash
git tag v0.2.5
git push origin v0.2.5
```

### 3. Automated Release Process

Once you push the tag, GitHub Actions will automatically:

- ✅ Build the frontend (React components)
- ✅ Build the Python package (wheel + source distribution)
- ✅ Extract changelog section for this version
- ✅ Create GitHub Release with changelog as release notes
- ✅ Upload distribution files as release assets
- ✅ Publish to PyPI

### 4. Monitor the Release

1. **Check GitHub Actions**: Go to the Actions tab to monitor the release workflow
2. **Verify GitHub Release**: Check that the release was created with proper changelog
3. **Verify PyPI**: Confirm the new version appears on PyPI

### Setup Requirements (One-time)

To use automated releases, you need:

1. **PyPI API Token**: Add `PYPI_API_TOKEN` to your repository secrets
   - Go to: Repository → Settings → Secrets and variables → Actions
   - Add your PyPI token as `PYPI_API_TOKEN`

### Manual Release (Alternative)

If you prefer manual releases or need to troubleshoot:

```bash
# Build everything
uv run build-frontend
uv run build

# Upload to PyPI manually
export TWINE_PASSWORD=your_pypi_token_here
python -m twine upload --username __token__ dist/*
```

## License

MIT License