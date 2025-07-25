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

### From PyPI (Recommended)

```bash
pip install streamlit-json-tip
```

### From TestPyPI (Latest Development Version)

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

## License

MIT License