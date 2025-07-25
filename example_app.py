import streamlit as st
from streamlit_json_tip import json_viewer

st.set_page_config(page_title="JSON Tip Demo", layout="wide")

st.title("🔍 JSON Tip - Interactive JSON Viewer with Smart Tooltips")
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

# Dynamic tooltip function with custom icons
def create_dynamic_tooltip(path, value, full_data):
    """Create custom tooltips based on field path, value, and context"""
    
    # Score tooltips for names based on length
    if path.endswith(".name") and isinstance(value, str):
        score = len(value) * 2  # Simple scoring: 2 points per character
        return {
            "text": f"Name score: {score} points",
            "icon": "👤"
        }
    
    # Age category tooltips
    if path.endswith(".age") and isinstance(value, int):
        if value < 25:
            return {
                "text": "Category: Young Adult",
                "icon": "🟢"
            }
        elif value < 30:
            return {
                "text": "Category: Adult", 
                "icon": "🟡"
            }
        else:
            return {
                "text": "Category: Mature Adult",
                "icon": "🟠"
            }
    
    # Spirit animal rarity tooltips
    if path.endswith(".spirit_animal") and isinstance(value, str):
        rarity_map = {
            "dog": {"text": "Common (found in 60% of profiles)", "icon": "🐕"},
            "cat": {"text": "Uncommon (found in 25% of profiles)", "icon": "🐱"}, 
            "cow": {"text": "Rare (found in 5% of profiles)", "icon": "🐄"},
            "dragon": {"text": "Legendary (found in 0.1% of profiles)", "icon": "🐉"}
        }
        return rarity_map.get(value, {"text": "Unknown rarity", "icon": "❓"})
    
    # Array element tooltips
    if path.startswith("[") and "].name" in path:
        # Extract index from path like "[0].name" 
        try:
            index = int(path.split("]")[0][1:])
            return {
                "text": f"Person #{index + 1} in the list",
                "icon": "🔢"
            }
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

st.subheader("Tooltip Configuration Examples")
st.write("Different tooltip configurations using Tippy.js options:")

# Initialize selection variables
selected1 = selected2 = selected3 = selected4 = selected_advanced = None

# Create tabs for different configurations
tab1, tab2, tab3, tab4 = st.tabs(["Default", "Interactive", "Animated", "Positioned"])

with tab1:
    st.write("**Default Configuration**: Standard tooltips with fade animation")
    selected1 = json_viewer(
        data=sample_data,
        help_text=help_text,
        tags=tags,
        tooltip_icon="💡",  # Custom global icon
        height=400,
        key="default_config"
    ) or None

with tab2:
    st.write("**Interactive Tooltips**: Hoverable tooltips with custom styling")
    selected2 = json_viewer(
        data=sample_data,
        help_text=help_text,
        tags=tags,
        tooltip_config={
            "interactive": True,
            "delay": [200, 100],
            "maxWidth": 300,
            "hideOnClick": False,
            "trigger": "mouseenter"
        },
        height=400,
        key="interactive_config"
    ) or None

with tab3:
    st.write("**Animated Tooltips**: Scale animation with custom timing")
    selected3 = json_viewer(
        data=sample_data,
        help_text=help_text,
        tags=tags,
        tooltip_config={
            "animation": "scale",
            "duration": [400, 200],
            "delay": 300,
            "arrow": True
        },
        height=400,
        key="animated_config"
    ) or None

with tab4:
    st.write("**Positioned Tooltips**: Right-side placement with custom width")
    selected4 = json_viewer(
        data=sample_data,
        help_text=help_text,
        tags=tags,
        tooltip_config={
            "placement": "right",
            "maxWidth": 200,
            "animation": "shift-away",
            "sticky": True
        },
        height=400,
        key="positioned_config"
    ) or None

st.subheader("Advanced Example: Context-Aware Tooltips")
st.write("Combining dynamic tooltips with custom configuration:")

# Advanced example with both dynamic tooltips and custom config
advanced_data = {
    "performance": {
        "cpu_usage": 85.2,
        "memory_usage": 67.8,
        "disk_usage": 45.3
    },
    "alerts": [
        {"level": "warning", "message": "High CPU usage detected"},
        {"level": "info", "message": "System running normally"}
    ]
}

def advanced_tooltip(path, value, data):
    if path.endswith("_usage"):
        if value > 80:
            return {
                "text": f"Critical: {value}% - Immediate attention required",
                "icon": "🚨"
            }
        elif value > 60:
            return {
                "text": f"Warning: {value}% - Monitor closely", 
                "icon": "⚠️"
            }
        else:
            return {
                "text": f"Normal: {value}% - Operating within limits",
                "icon": "✅"
            }
    
    if path.endswith(".level"):
        level_info = {
            "warning": {"text": "Requires attention - investigate potential issues", "icon": "⚠️"},
            "error": {"text": "Critical - immediate action needed", "icon": "🚨"},
            "info": {"text": "Informational - no action required", "icon": "ℹ️"}
        }
        return level_info.get(value, {"text": "Unknown alert level", "icon": "❓"})
    
    return None

selected_advanced = json_viewer(
    data=advanced_data,
    dynamic_tooltips=advanced_tooltip,
    tooltip_config={
        "placement": "auto",
        "interactive": True,
        "maxWidth": 350,
        "animation": "shift-toward",
        "delay": [100, 50],
        "duration": [300, 200]
    },
    height=350,
    key="advanced_tooltip_demo"
) or None

# Show selected field information from any of the viewers
selected_fields = [selected1, selected2, selected3, selected4, selected_advanced]
active_selection = next((sel for sel in selected_fields if sel), None)

if active_selection:
    st.subheader("Selected Field Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Path:**", active_selection.get("path"))
        st.write("**Value:**", active_selection.get("value"))
    
    with col2:
        if active_selection.get("help_text"):
            st.write("**Help Text:**", active_selection.get("help_text"))
        if active_selection.get("tag"):
            st.write("**Tag:**", active_selection.get("tag"))

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
from streamlit_json_tip import json_viewer

# Static tooltips with custom icon
data = {"name": "John", "age": 30}
help_text = {"name": "The person's full name", "age": "Age in years"}

selected = json_viewer(data=data, help_text=help_text, tooltip_icon="💡")

# Dynamic tooltips with custom icons per field
users = [{"name": "john", "score": 85}, {"name": "jake", "score": 92}]

def dynamic_tooltip_with_icons(path, value, full_data):
    if path.endswith(".name"):
        return {
            "text": f"Name length: {len(value)} characters",
            "icon": "👤"
        }
    elif path.endswith(".score"):
        return {
            "text": f"Performance score: {value}/100",
            "icon": "📊" if value >= 80 else "⚠️"
        }
    return None

selected = json_viewer(data=users, dynamic_tooltips=dynamic_tooltip_with_icons)

# Custom tooltip configuration with global icon
json_viewer(
    data=data,
    help_text=help_text,
    tooltip_icon="❓",              # Global tooltip icon
    tooltip_config={
        "placement": "right",           # Position: top, bottom, left, right, auto
        "animation": "scale",           # Animation: fade, shift-away, scale, etc.
        "delay": [300, 100],           # [show_delay, hide_delay] in ms
        "interactive": True,            # Allow hovering over tooltip
        "maxWidth": 250,               # Max width in pixels
        "sticky": True                 # Tooltip follows cursor
    }
)
''', language='python')