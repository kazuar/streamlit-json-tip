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
    height : int, optional
        Height of the component in pixels (default: 400)
    key : str, optional
        An optional key that uniquely identifies this component
        
    Returns
    -------
    dict
        The selected field information or None
    """
    component_value = _component_func(
        data=data,
        help_text=help_text or {},
        tags=tags or {},
        height=height,
        key=key,
        default=None
    )
    
    return component_value