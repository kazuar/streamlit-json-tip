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

# Demo for dynamic tooltips
st.subheader("Dynamic Tooltips Example")
st.write("This example shows dynamic tooltips based on field values and context.")

# Example data with dynamic scoring
dynamic_data = [
    {"name": "john", "spirit_animal": "dog", "age": 25},
    {"name": "jake", "spirit_animal": "cow", "age": 30},
    {"name": "alice", "spirit_animal": "cat", "age": 28}
]

# Dynamic tooltip function
def create_dynamic_tooltip(path, value, full_data):
    """Create custom tooltips based on field path, value, and context"""
    
    # Score tooltips for names based on length
    if path.endswith(".name") and isinstance(value, str):
        score = len(value) * 2  # Simple scoring: 2 points per character
        return f"Name score: {score} points"
    
    # Age category tooltips
    if path.endswith(".age") and isinstance(value, int):
        if value < 25:
            return "Category: Young Adult"
        elif value < 30:
            return "Category: Adult"
        else:
            return "Category: Mature Adult"
    
    # Spirit animal rarity tooltips
    if path.endswith(".spirit_animal") and isinstance(value, str):
        rarity_map = {
            "dog": "Common (found in 60% of profiles)",
            "cat": "Uncommon (found in 25% of profiles)", 
            "cow": "Rare (found in 5% of profiles)",
            "dragon": "Legendary (found in 0.1% of profiles)"
        }
        return rarity_map.get(value, "Unknown rarity")
    
    # Array element tooltips
    if path.startswith("[") and "].name" in path:
        # Extract index from path like "[0].name" 
        try:
            index = int(path.split("]")[0][1:])
            return f"Person #{index + 1} in the list"
        except:
            pass
    
    return None

st.write("**Dynamic Data:**")
st.json(dynamic_data)

selected_dynamic = json_viewer(
    data=dynamic_data,
    dynamic_tooltips=create_dynamic_tooltip,
    height=300,
    key="dynamic_tooltip_demo"
)

if selected_dynamic:
    st.write(f"**Selected:** {selected_dynamic.get('path')} = {selected_dynamic.get('value')}")
    if selected_dynamic.get('help_text'):
        st.write(f"**Dynamic Tooltip:** {selected_dynamic.get('help_text')}")

st.subheader("Static Tooltips Example")
st.write("Click on any field to see its details. Hover over ℹ️ icons to see help text.")

# Display the JSON viewer with static tooltips
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

# Static tooltips
data = {"name": "John", "age": 30}
help_text = {"name": "The person's full name", "age": "Age in years"}
tags = {"name": "PII", "age": "DEMOGRAPHIC"}

selected = json_viewer(data=data, help_text=help_text, tags=tags)

# Dynamic tooltips
users = [{"name": "john", "score": 85}, {"name": "jake", "score": 92}]

def dynamic_tooltip(path, value, full_data):
    if path.endswith(".name"):
        # Find the score for this user
        try:
            index = int(path.split("]")[0][1:])  # Extract index from "[0].name"
            score = full_data[index]["score"]
            return f"Performance score: {score}/100"
        except:
            pass
    return None

selected = json_viewer(data=users, dynamic_tooltips=dynamic_tooltip)
''', language='python')