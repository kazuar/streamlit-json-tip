import streamlit as st
from streamlit_json_viewer import json_viewer

st.set_page_config(page_title="JSON Viewer Demo", layout="wide")

st.title("🔍 JSON Viewer with Help Text and Tags")
st.write("This demo shows how to use the JSON Viewer component with help text and tags for individual fields.")

# Sample JSON data
sample_data = {
    "user": {
        "id": 12345,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "profile": {
            "avatar_url": "https://example.com/avatar.jpg",
            "bio": "Software developer",
            "location": "San Francisco, CA"
        },
        "preferences": {
            "theme": "dark",
            "notifications": True,
            "language": "en"
        }
    },
    "posts": [
        {
            "id": 1,
            "title": "Hello World",
            "content": "This is my first post!",
            "published": True,
            "tags": ["intro", "welcome"]
        },
        {
            "id": 2,
            "title": "Learning Streamlit",
            "content": "Streamlit is amazing for building data apps!",
            "published": False,
            "tags": ["streamlit", "python", "data"]
        }
    ],
    "metadata": {
        "created_at": "2024-01-15T10:30:00Z",
        "last_updated": "2024-01-20T15:45:00Z",
        "version": "1.2.0"
    }
}

# Help text for specific fields
help_text = {
    "user.id": "Unique identifier for the user account",
    "user.name": "Full display name of the user",
    "user.email": "Primary email address for account notifications",
    "user.profile.avatar_url": "URL to the user's profile picture",
    "user.profile.bio": "Short biography or description",
    "user.preferences.theme": "UI theme preference (light/dark)",
    "user.preferences.notifications": "Whether to receive email notifications",
    "posts[0].published": "Whether this post is visible to the public",
    "posts[1].published": "Whether this post is visible to the public",
    "metadata.created_at": "ISO timestamp of account creation",
    "metadata.version": "Current API version"
}

# Tags for categorizing fields
tags = {
    "user.id": "PII",
    "user.name": "PII",
    "user.email": "PII",
    "user.profile.avatar_url": "URL",
    "user.preferences.theme": "CONFIG",
    "user.preferences.notifications": "CONFIG",
    "user.preferences.language": "CONFIG",
    "posts[0].published": "STATUS",
    "posts[1].published": "STATUS",
    "posts[0].tags": "METADATA",
    "posts[1].tags": "METADATA",
    "metadata.created_at": "TIMESTAMP",
    "metadata.last_updated": "TIMESTAMP",
    "metadata.version": "VERSION"
}

st.subheader("Interactive JSON Viewer")
st.write("Click on any field to see its details. Hover over ℹ️ icons to see help text.")

# Display the JSON viewer
selected = json_viewer(
    data=sample_data,
    help_text=help_text,
    tags=tags,
    height=500,
    key="json_viewer_demo"
)

# Show selected field information
if selected:
    st.subheader("Selected Field Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Path:**", selected.get("path"))
        st.write("**Value:**", selected.get("value"))
    
    with col2:
        if selected.get("help_text"):
            st.write("**Help Text:**", selected.get("help_text"))
        if selected.get("tag"):
            st.write("**Tag:**", selected.get("tag"))

# Instructions
st.subheader("How to Use")
st.write("""
1. **Expand/Collapse**: Click on the `{` or `[` brackets to expand or collapse objects and arrays
2. **Select Fields**: Click on any field value to select it and see details below
3. **Help Text**: Hover over the ℹ️ icon to see help text for specific fields
4. **Tags**: Fields with tags will show colored labels for easy categorization
5. **Field Types**: Different value types are color-coded (strings in green, numbers in blue, etc.)
""")

# Code example
st.subheader("Code Example")
st.code('''
from streamlit_json_viewer import json_viewer

# Your JSON data
data = {"name": "John", "age": 30}

# Help text for fields
help_text = {
    "name": "The person's full name",
    "age": "Age in years"
}

# Tags for categorization
tags = {
    "name": "PII",
    "age": "DEMOGRAPHIC"
}

# Display the viewer
selected = json_viewer(
    data=data,
    help_text=help_text,
    tags=tags,
    height=400
)

if selected:
    st.write(f"Selected: {selected}")
''', language='python')