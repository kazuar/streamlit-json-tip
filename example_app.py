import streamlit as st
from streamlit_json_tip import json_viewer

st.set_page_config(page_title="JSON Viewer with Tooltips", layout="wide")

st.title("🔍 Streamlit JSON Tip - Interactive JSON Viewer")

st.markdown("""
This component provides an interactive JSON viewer with tooltips and tags for individual fields.
Click on the ℹ️ icons to see tooltips, and click on any field to select it.

**Test the expand/collapse functionality** - it should NOT refresh the page or reset other inputs!
""")

# Add input fields to test that expand/collapse doesn't cause page refresh
st.subheader("🧪 State Preservation Test")
col1, col2, col3 = st.columns(3)

with col1:
    user_input = st.text_input("Type something here:", placeholder="This should not reset when expanding/collapsing JSON")
    counter = st.number_input("Counter:", value=0, step=1)

with col2:
    selected_option = st.selectbox("Choose an option:", ["Option 1", "Option 2", "Option 3"])
    slider_value = st.slider("Slider value:", 0, 100, 50)

with col3:
    checkbox_state = st.checkbox("Check me")
    radio_choice = st.radio("Radio buttons:", ["A", "B", "C"])

# Display current state
if user_input or counter != 0 or selected_option != "Option 1" or slider_value != 50 or checkbox_state or radio_choice != "A":
    st.success(f"✅ State preserved: Input='{user_input}', Counter={counter}, Select='{selected_option}', Slider={slider_value}, Checkbox={checkbox_state}, Radio='{radio_choice}'")
else:
    st.info("👆 Interact with the controls above, then expand/collapse JSON nodes below to test state preservation")

st.markdown("---")

# Sample data
data = {
    "user": {
        "name": "Alice Johnson",
        "email": "alice@company.com",
        "id": 12345,
        "role": "admin",
        "last_login": "2024-01-15T10:30:00Z",
        "preferences": {
            "theme": "dark",
            "notifications": True,
            "language": "en"
        },
        "permissions": ["read", "write", "admin"]
    },
    "system": {
        "version": "2.1.0",
        "environment": "production",
        "uptime": 99.9,
        "memory_usage": 0.78,
        "cpu_usage": 0.45
    },
    "metrics": {
        "requests_per_second": 1250,
        "response_time_ms": 45,
        "error_rate": 0.001,
        "active_connections": 892
    },
    "config": {
        "database": {
            "host": "db.company.com",
            "port": 5432,
            "ssl": True,
            "pool_size": 20
        },
        "redis": {
            "host": "cache.company.com", 
            "port": 6379,
            "timeout": 5000
        },
        "features": {
            "new_ui": True,
            "beta_features": False,
            "analytics": True
        }
    }
}

# Help text for tooltips (including multiple tooltips example)
help_text = {
    "user.name": "Full name of the user",
    "user.email": "Primary email address for notifications",
    "user.id": [
        {"text": "Unique user identifier in the system", "icon": "🆔"},
        {"text": "Used for database lookups and API calls", "icon": "🔗"},
        {"text": "Cannot be changed after account creation", "icon": "🔒"}
    ],
    "user.role": "User's permission level (admin, user, guest)",
    "user.last_login": "Timestamp of user's last login",
    "user.preferences.theme": "UI theme preference (light/dark)",
    "user.preferences.notifications": "Whether user receives notifications",
    "user.preferences.language": "User's preferred language code",
    "user.permissions": "List of user's system permissions",
    "system.version": "Current application version",
    "system.environment": "Deployment environment",
    "system.uptime": [
        {"text": "System uptime percentage", "icon": "⏱️"},
        {"text": "Target: >99.9% for production", "icon": "🎯"},
        {"text": "Current status: Excellent", "icon": "✅"}
    ],
    "system.memory_usage": "Current memory usage as decimal (0.78 = 78%)",
    "system.cpu_usage": "Current CPU usage as decimal",
    "metrics.requests_per_second": "Average requests handled per second",
    "metrics.response_time_ms": "Average response time in milliseconds",
    "metrics.error_rate": "Error rate as decimal (0.001 = 0.1%)",
    "metrics.active_connections": "Number of active client connections",
    "config.database.host": "Database server hostname",
    "config.database.port": "Database connection port",
    "config.database.ssl": "Whether SSL encryption is enabled",
    "config.database.pool_size": "Maximum database connection pool size",
    "config.redis.host": "Redis cache server hostname",
    "config.redis.port": "Redis server port",
    "config.redis.timeout": "Connection timeout in milliseconds",
    "config.features.new_ui": "Whether new UI is enabled",
    "config.features.beta_features": "Whether beta features are enabled",
    "config.features.analytics": "Whether analytics tracking is enabled"
}

# Tags for categorizing fields
tags = {
    "user.name": "PII",
    "user.email": "PII", 
    "user.id": "ID",
    "user.role": "AUTH",
    "user.permissions": "AUTH",
    "system.version": "INFO",
    "system.environment": "CONFIG",
    "system.uptime": "METRIC", 
    "system.memory_usage": "METRIC",
    "system.cpu_usage": "METRIC",
    "metrics.requests_per_second": "METRIC",
    "metrics.response_time_ms": "METRIC", 
    "metrics.error_rate": "METRIC",
    "metrics.active_connections": "METRIC",
    "config.database.host": "CONFIG",
    "config.database.port": "CONFIG",
    "config.database.ssl": "SECURITY",
    "config.redis.host": "CONFIG",
    "config.redis.port": "CONFIG",
    "config.features.new_ui": "FEATURE",
    "config.features.beta_features": "FEATURE",
    "config.features.analytics": "FEATURE"
}

# Dynamic tooltips function
def dynamic_tooltip(path, value, data):
    """Generate contextual tooltips based on field path and value."""
    
    # User-related fields with contextual info
    if path.startswith("user."):
        user_name = data.get("user", {}).get("name", "Unknown")
        
        if path.endswith(".name"):
            return {
                "text": f"👤 User profile: {len(value)} characters long",
                "icon": "👤"
            }
        elif path.endswith(".role"):
            role_info = {
                "admin": {"icon": "👑", "desc": "Full system access"},
                "user": {"icon": "👤", "desc": "Standard user access"},
                "guest": {"icon": "👁️", "desc": "Read-only access"}
            }
            info = role_info.get(value, {"icon": "❓", "desc": "Unknown role"})
            return {
                "text": f"{info['desc']} for {user_name}",
                "icon": info["icon"]
            }
        elif path.endswith(".permissions"):
            return {
                "text": f"🔐 {user_name} has {len(value)} permission(s): {', '.join(value)}",
                "icon": "🔐"
            }
        elif path.endswith(".last_login"):
            return {
                "text": f"🕒 {user_name}'s last activity: {value}",
                "icon": "🕒"
            }
    
    # System metrics with status indicators
    elif path.startswith("system."):
        if "usage" in path:
            percentage = f"{value * 100:.1f}%"
            if value > 0.9:
                return {"text": f"🔴 Critical usage: {percentage}", "icon": "🔴"}
            elif value > 0.7:
                return {"text": f"🟡 High usage: {percentage}", "icon": "🟡"}
            else:
                return {"text": f"🟢 Normal usage: {percentage}", "icon": "🟢"}
        elif path.endswith(".uptime"):
            # Example of dynamic multiple tooltips
            if value >= 99.9:
                return [
                    {"text": f"Excellent uptime: {value}%", "icon": "🟢"},
                    {"text": "SLA compliance: Met", "icon": "✅"},
                    {"text": "No action needed", "icon": "👍"}
                ]
            elif value >= 99.0:
                return [
                    {"text": f"Good uptime: {value}%", "icon": "🟡"},
                    {"text": "SLA compliance: At risk", "icon": "⚠️"}
                ]
            else:
                return [
                    {"text": f"Poor uptime: {value}%", "icon": "🔴"},
                    {"text": "SLA compliance: Failed", "icon": "❌"},
                    {"text": "Immediate action required", "icon": "🚨"}
                ]
    
    # Performance metrics
    elif path.startswith("metrics."):
        if path.endswith(".error_rate"):
            if value > 0.01:  # > 1%
                return {"text": f"🚨 High error rate: {value * 100:.2f}%", "icon": "🚨"}
            elif value > 0.005:  # > 0.5%
                return {"text": f"⚠️ Elevated error rate: {value * 100:.3f}%", "icon": "⚠️"}
            else:
                return {"text": f"✅ Normal error rate: {value * 100:.3f}%", "icon": "✅"}
        elif path.endswith(".response_time_ms"):
            if value > 100:
                return {"text": f"🐌 Slow response: {value}ms", "icon": "🐌"}
            elif value > 50:
                return {"text": f"🟡 Moderate response: {value}ms", "icon": "🟡"}
            else:
                return {"text": f"⚡ Fast response: {value}ms", "icon": "⚡"}
    
    # Configuration with security notes
    elif path.startswith("config."):
        if path.endswith(".ssl"):
            if value:
                return {"text": "🔒 SSL encryption enabled", "icon": "🔒"}
            else:
                return {"text": "⚠️ SSL encryption disabled", "icon": "⚠️"}
        elif path.endswith(".port"):
            return {"text": f"🔌 Network port: {value}", "icon": "🔌"}
    
    return None

st.subheader("📊 Interactive JSON Viewer")
st.markdown("🎯 **Try this:** Fill out the form above, then expand/collapse JSON nodes below. Your form data should remain intact!")
st.markdown("📋 **New:** Click the copy button in the top-right corner of the JSON viewer to copy the raw JSON data to your clipboard!")
st.markdown("💡 **Multiple Tooltips:** Some fields now have multiple tooltip icons - hover over each one for different information!")

# Add field selection toggle
field_selection_enabled = st.checkbox(
    "Enable field selection", 
    value=False, 
    help="When enabled, clicking on field values will trigger selection (may cause page refresh). When disabled, no refreshes occur."
)

if not field_selection_enabled:
    st.info("💡 Field selection is disabled - clicking on values won't refresh the page!")

# Create columns for layout
col1, col2 = st.columns([2, 1])

with col1:
    # Display the JSON viewer
    selected = json_viewer(
        data=data,
        help_text=help_text,
        tags=tags,
        dynamic_tooltips=dynamic_tooltip,
        tooltip_config={
            "placement": "auto",
            "animation": "fade",
            "delay": [200, 100],
            "interactive": True,
            "maxWidth": 400
        },
        enable_field_selection=field_selection_enabled,  # Control field selection
        height=600,
        key="json_viewer_demo"  # Add a key for better state management
    )

with col2:
    st.subheader("🎛️ Field Selection")
    
    if selected:
        st.success("✅ Field Selected!")
        st.json({
            "Path": selected['path'],
            "Value": selected['value'],
            "Type": type(selected['value']).__name__,
            "Help": selected.get('help_text', 'No help available'),
            "Tag": selected.get('tag', 'No tag')
        })
    else:
        st.info("👆 Click on any field to see details")
    
    st.subheader("📈 Stats")
    st.metric("Total Fields", len(help_text))
    st.metric("Tagged Fields", len(tags))
    st.metric("Dynamic Tooltips", "✅ Enabled")
    
    st.subheader("📋 Copy Feature")
    st.info("Click the 📋 button in the JSON viewer to copy the raw JSON data to your clipboard!")

# Instructions
st.subheader("🧪 How to Test State Preservation")
st.markdown("""
1. **Fill out the form** at the top of the page (text input, counter, dropdown, etc.)
2. **Expand and collapse** different sections in the JSON viewer below
3. **Verify** that your form inputs remain unchanged

If the expand/collapse arrows cause the page to refresh, your form data would be lost. 
This demonstrates that the component properly handles internal state without triggering Streamlit reruns.
""")

# Feature examples section
st.subheader("🚀 Features Demonstrated")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **🏷️ Field Tags**
    - PII: Personal data
    - AUTH: Authentication 
    - CONFIG: Configuration
    - METRIC: Performance metrics
    - SECURITY: Security settings
    - FEATURE: Feature flags
    """)

with col2:
    st.markdown("""
    **💡 Dynamic Tooltips**
    - Context-aware help text
    - Custom icons per field
    - Value-based conditions
    - Cross-field references
    - Status indicators
    - **🔄 Multiple tooltips per field**
    """)

with col3:
    st.markdown("""
    **🎨 Interactive Features**
    - Expand/collapse nodes
    - Click to select fields
    - Professional tooltips
    - Syntax highlighting
    - Responsive design
    - **📋 Copy to clipboard**
    """)

st.markdown("---")
st.markdown("*Built with ❤️ using Streamlit and Tippy.js*")