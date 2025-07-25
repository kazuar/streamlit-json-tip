import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "json_viewer",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("json_viewer", path=build_dir)

def json_viewer(
    data,
    help_text=None,
    tags=None,
    dynamic_tooltips=None,
    tooltip_config=None,
    height=400,
    key=None
):
    """
    Display a JSON viewer with optional help text and tags for each field.
    
    Parameters
    ----------
    data : dict
        The JSON data to display
    help_text : dict, optional
        Dictionary mapping field paths to help text
    tags : dict, optional
        Dictionary mapping field paths to tags/labels
    dynamic_tooltips : function, optional
        Function that takes (field_path, field_value, full_data) and returns tooltip text
    tooltip_config : dict, optional
        Configuration for Tippy.js tooltips. Available options:
        - placement: str, default "top" (top, bottom, left, right, auto)
        - arrow: bool, default True
        - animation: str, default "fade" (fade, shift-away, shift-toward, scale, perspective)
        - delay: int|list, default 0 (delay in ms, or [show_delay, hide_delay])
        - duration: int|list, default [300, 250] (animation duration)
        - interactive: bool, default False (allow hovering over tooltip)
        - maxWidth: int, default 350 (max width in pixels)
        - trigger: str, default "mouseenter focus" (events that trigger tooltip)
        - hideOnClick: bool, default True
        - sticky: bool, default False (tooltip follows cursor)
    height : int, optional
        Height of the component in pixels (default: 400)
    key : str, optional
        An optional key that uniquely identifies this component
        
    Returns
    -------
    dict
        The selected field information or None
        
    Examples
    --------
    # Static tooltips
    json_viewer(data, help_text={"user.name": "The user's display name"})
    
    # Dynamic tooltips
    def dynamic_tooltip(path, value, data):
        if path.endswith(".name"):
            return f"Name length: {len(value)} characters"
        return None
    
    json_viewer(data, dynamic_tooltips=dynamic_tooltip)
    
    # Custom tooltip configuration
    json_viewer(
        data=data,
        help_text=help_text,
        tooltip_config={
            "placement": "right",
            "animation": "scale", 
            "delay": [500, 0],
            "interactive": True,
            "maxWidth": 200
        }
    )
    """
    # Pre-compute dynamic tooltips if function provided
    computed_help_text = help_text.copy() if help_text else {}
    
    if dynamic_tooltips and callable(dynamic_tooltips):
        def _collect_tooltips(obj, current_path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    field_path = f"{current_path}.{key}" if current_path else key
                    tooltip = dynamic_tooltips(field_path, value, data)
                    if tooltip:
                        computed_help_text[field_path] = tooltip
                    _collect_tooltips(value, field_path)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    field_path = f"{current_path}[{i}]"
                    tooltip = dynamic_tooltips(field_path, item, data)
                    if tooltip:
                        computed_help_text[field_path] = tooltip
                    _collect_tooltips(item, field_path)
        
        _collect_tooltips(data)
    
    # Set default tooltip configuration
    default_tooltip_config = {
        "placement": "top",
        "arrow": True,
        "animation": "fade",
        "delay": 0,
        "duration": [300, 250],
        "interactive": False,
        "maxWidth": 350,
        "trigger": "mouseenter focus",
        "hideOnClick": True,
        "sticky": False
    }
    
    # Merge user config with defaults
    final_tooltip_config = default_tooltip_config.copy()
    if tooltip_config:
        final_tooltip_config.update(tooltip_config)
    
    component_value = _component_func(
        data=data,
        help_text=computed_help_text,
        tags=tags or {},
        tooltip_config=final_tooltip_config,
        height=height,
        key=key,
        default=None
    )
    
    return component_value