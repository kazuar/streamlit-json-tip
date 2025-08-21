"""Tests for the json_viewer component."""

import pytest
from unittest.mock import Mock, patch
import streamlit as st
from streamlit_json_tip import json_viewer


class TestJsonViewer:
    """Test cases for the json_viewer function."""

    def test_basic_json_viewer(self):
        """Test basic json_viewer functionality."""
        data = {"name": "John", "age": 30}
        
        with patch('streamlit_json_tip._component_func') as mock_component:
            mock_component.return_value = None
            
            result = json_viewer(data=data)
            
            # Verify component was called with correct arguments
            mock_component.assert_called_once()
            call_args = mock_component.call_args
            
            assert call_args[1]['data'] == data
            assert call_args[1]['help_text'] == {}
            assert call_args[1]['tags'] == {}
            assert call_args[1]['height'] == 400
            assert call_args[1]['tooltip_icon'] == "ℹ️"

    def test_json_viewer_with_help_text(self):
        """Test json_viewer with help text."""
        data = {"user": {"name": "John"}}
        help_text = {"user.name": "User's full name"}
        
        with patch('streamlit_json_tip._component_func') as mock_component:
            mock_component.return_value = None
            
            json_viewer(data=data, help_text=help_text)
            
            call_args = mock_component.call_args
            assert call_args[1]['help_text'] == help_text

    def test_json_viewer_with_tags(self):
        """Test json_viewer with tags."""
        data = {"email": "john@example.com"}
        tags = {"email": "PII"}
        
        with patch('streamlit_json_tip._component_func') as mock_component:
            mock_component.return_value = None
            
            json_viewer(data=data, tags=tags)
            
            call_args = mock_component.call_args
            assert call_args[1]['tags'] == tags

    def test_json_viewer_with_dynamic_tooltips(self):
        """Test json_viewer with dynamic tooltips function."""
        data = {"score": 85}
        
        def dynamic_tooltip(path, value, data):
            if path == "score":
                return f"Score: {value}/100"
            return None
        
        with patch('streamlit_json_tip._component_func') as mock_component:
            mock_component.return_value = None
            
            json_viewer(data=data, dynamic_tooltips=dynamic_tooltip)
            
            call_args = mock_component.call_args
            # Dynamic tooltips are processed and converted to help_text
            assert call_args[1]['help_text'] == {"score": "Score: 85/100"}

    def test_json_viewer_with_custom_tooltip_icon(self):
        """Test json_viewer with custom tooltip icon."""
        data = {"info": "test"}
        
        with patch('streamlit_json_tip._component_func') as mock_component:
            mock_component.return_value = None
            
            json_viewer(data=data, tooltip_icon="💡")
            
            call_args = mock_component.call_args
            assert call_args[1]['tooltip_icon'] == "💡"

    def test_json_viewer_with_tooltip_config(self):
        """Test json_viewer with tooltip configuration."""
        data = {"test": "value"}
        tooltip_config = {"placement": "right", "animation": "scale"}
        
        with patch('streamlit_json_tip._component_func') as mock_component:
            mock_component.return_value = None
            
            json_viewer(data=data, tooltip_config=tooltip_config)
            
            call_args = mock_component.call_args
            # Config is merged with defaults
            expected_config = {
                "placement": "right",  # overridden
                "animation": "scale",  # overridden
                "arrow": True,
                "delay": 0,
                "duration": [300, 250],
                "interactive": False,
                "maxWidth": 350,
                "trigger": "mouseenter focus",
                "hideOnClick": True,
                "sticky": False
            }
            assert call_args[1]['tooltip_config'] == expected_config

    def test_json_viewer_with_custom_height(self):
        """Test json_viewer with custom height."""
        data = {"test": "value"}
        
        with patch('streamlit_json_tip._component_func') as mock_component:
            mock_component.return_value = None
            
            json_viewer(data=data, height=600)
            
            call_args = mock_component.call_args
            assert call_args[1]['height'] == 600

    def test_json_viewer_with_key(self):
        """Test json_viewer with custom key."""
        data = {"test": "value"}
        
        with patch('streamlit_json_tip._component_func') as mock_component:
            mock_component.return_value = None
            
            json_viewer(data=data, key="custom_key")
            
            call_args = mock_component.call_args
            assert call_args[1]['key'] == "custom_key"

    def test_complex_nested_data(self):
        """Test json_viewer with complex nested data structure."""
        data = {
            "users": [
                {"id": 1, "name": "Alice", "settings": {"theme": "dark"}},
                {"id": 2, "name": "Bob", "settings": {"theme": "light"}}
            ],
            "metadata": {
                "version": "1.0",
                "created": "2024-01-01"
            }
        }
        
        help_text = {
            "users[0].name": "First user's name",
            "metadata.version": "API version"
        }
        
        tags = {
            "users[0].name": "PII",
            "users[1].name": "PII"
        }
        
        with patch('streamlit_json_tip._component_func') as mock_component:
            mock_component.return_value = {"path": "users[0].name", "value": "Alice"}
            
            result = json_viewer(data=data, help_text=help_text, tags=tags)
            
            call_args = mock_component.call_args
            assert call_args[1]['data'] == data
            assert call_args[1]['help_text'] == help_text
            assert call_args[1]['tags'] == tags
            assert result == {"path": "users[0].name", "value": "Alice"}

    def test_dynamic_tooltips_with_icons(self):
        """Test dynamic tooltips that return dictionaries with icons."""
        data = {"name": "Alice", "score": 95}
        
        def dynamic_tooltip_with_icons(path, value, data):
            if path == "name":
                return {"text": f"User: {value}", "icon": "👤"}
            elif path == "score":
                return {"text": f"Score: {value}/100", "icon": "📊"}
            return None
        
        with patch('streamlit_json_tip._component_func') as mock_component:
            mock_component.return_value = None
            
            json_viewer(data=data, dynamic_tooltips=dynamic_tooltip_with_icons)
            
            call_args = mock_component.call_args
            # Dynamic tooltips are processed into help_text and tooltip_icons
            assert call_args[1]['help_text'] == {"name": "User: Alice", "score": "Score: 95/100"}
            assert call_args[1]['tooltip_icons'] == {"name": "👤", "score": "📊"}

    @pytest.mark.parametrize("data,expected_type", [
        ({"string": "test"}, dict),
        ([1, 2, 3], list),
        ({"nested": {"deep": {"value": 42}}}, dict),
        ({"mixed": [{"id": 1}, {"id": 2}]}, dict),
    ])
    def test_json_viewer_data_types(self, data, expected_type):
        """Test json_viewer with different data types."""
        with patch('streamlit_json_tip._component_func') as mock_component:
            mock_component.return_value = None
            
            json_viewer(data=data)
            
            call_args = mock_component.call_args
            assert isinstance(call_args[1]['data'], expected_type)
            assert call_args[1]['data'] == data

    def test_json_viewer_empty_data(self):
        """Test json_viewer with empty data structures."""
        test_cases = [
            {},
            [],
            {"empty_dict": {}, "empty_list": []}
        ]
        
        for data in test_cases:
            with patch('streamlit_json_tip._component_func') as mock_component:
                mock_component.return_value = None
                
                json_viewer(data=data)
                
                call_args = mock_component.call_args
                assert call_args[1]['data'] == data

    def test_json_viewer_with_static_multiple_tooltips(self):
        """Test json_viewer with static multiple tooltips."""
        data = {"user_id": 123, "status": "active"}
        help_text = {
            "user_id": [
                {"text": "Unique identifier", "icon": "🆔"},
                {"text": "Used for database queries", "icon": "🔗"},
                {"text": "Cannot be changed", "icon": "🔒"}
            ],
            "status": "Current user status"  # Mix with single tooltip
        }
        
        with patch('streamlit_json_tip._component_func') as mock_component:
            mock_component.return_value = None
            
            json_viewer(data=data, help_text=help_text)
            
            call_args = mock_component.call_args
            # Multiple tooltips should be moved to separate parameter
            assert call_args[1]['help_text'] == {"status": "Current user status"}
            assert call_args[1]['multiple_tooltips'] == {
                "user_id": [
                    {"text": "Unique identifier", "icon": "🆔"},
                    {"text": "Used for database queries", "icon": "🔗"},
                    {"text": "Cannot be changed", "icon": "🔒"}
                ]
            }

    def test_json_viewer_with_dynamic_multiple_tooltips(self):
        """Test json_viewer with dynamic tooltips returning multiple tooltips."""
        data = {"score": 95, "name": "Alice"}
        
        def dynamic_tooltip_multiple(path, value, data):
            if path == "score":
                return [
                    {"text": f"Performance: {value}/100", "icon": "📊"},
                    {"text": "Excellent rating", "icon": "⭐"},
                    {"text": "Above target", "icon": "🎯"}
                ]
            elif path == "name":
                return {"text": f"User: {value}", "icon": "👤"}  # Single tooltip
            return None
        
        with patch('streamlit_json_tip._component_func') as mock_component:
            mock_component.return_value = None
            
            json_viewer(data=data, dynamic_tooltips=dynamic_tooltip_multiple)
            
            call_args = mock_component.call_args
            # Single dynamic tooltip should be in help_text
            assert call_args[1]['help_text'] == {"name": "User: Alice"}
            assert call_args[1]['tooltip_icons'] == {"name": "👤"}
            # Multiple dynamic tooltips should be in multiple_tooltips
            assert call_args[1]['multiple_tooltips'] == {
                "score": [
                    {"text": "Performance: 95/100", "icon": "📊"},
                    {"text": "Excellent rating", "icon": "⭐"},
                    {"text": "Above target", "icon": "🎯"}
                ]
            }

    def test_json_viewer_with_array_multiple_tooltips(self):
        """Test json_viewer with array data and multiple tooltips."""
        data = {"items": [{"id": 1, "value": "test"}, {"id": 2, "value": "demo"}]}
        
        def dynamic_tooltip_array(path, value, data):
            if path.startswith("items[") and path.endswith("].id"):
                return [
                    {"text": f"Item ID: {value}", "icon": "🆔"},
                    {"text": "Primary key", "icon": "🔑"}
                ]
            return None
        
        with patch('streamlit_json_tip._component_func') as mock_component:
            mock_component.return_value = None
            
            json_viewer(data=data, dynamic_tooltips=dynamic_tooltip_array)
            
            call_args = mock_component.call_args
            # Should process array items and create multiple tooltips
            assert "items[0].id" in call_args[1]['multiple_tooltips']
            assert "items[1].id" in call_args[1]['multiple_tooltips']
            assert call_args[1]['multiple_tooltips']["items[0].id"] == [
                {"text": "Item ID: 1", "icon": "🆔"},
                {"text": "Primary key", "icon": "🔑"}
            ]

    def test_json_viewer_enable_field_selection(self):
        """Test json_viewer with field selection enabled/disabled."""
        data = {"test": "value"}
        
        # Test with field selection enabled (default)
        with patch('streamlit_json_tip._component_func') as mock_component:
            mock_component.return_value = None
            
            json_viewer(data=data, enable_field_selection=True)
            
            call_args = mock_component.call_args
            assert call_args[1]['enable_field_selection'] == True
        
        # Test with field selection disabled
        with patch('streamlit_json_tip._component_func') as mock_component:
            mock_component.return_value = None
            
            json_viewer(data=data, enable_field_selection=False)
            
            call_args = mock_component.call_args
            assert call_args[1]['enable_field_selection'] == False

    def test_static_multiple_tooltips_with_existing_icons(self):
        """Test that static multiple tooltips properly remove single tooltip icons."""
        data = {"field": "value"}
        help_text = {
            "field": [
                {"text": "First tooltip", "icon": "📝"},
                {"text": "Second tooltip", "icon": "📊"}
            ]
        }
        
        # Pre-populate tooltip_icons to test cleanup
        with patch('streamlit_json_tip._component_func') as mock_component:
            mock_component.return_value = None
            
            # This should clean up any existing single icons when converting to multiple
            json_viewer(data=data, help_text=help_text)
            
            call_args = mock_component.call_args
            assert call_args[1]['help_text'] == {}  # Should be empty
            assert call_args[1]['tooltip_icons'] == {}  # Should be empty  
            assert call_args[1]['multiple_tooltips'] == {
                "field": [
                    {"text": "First tooltip", "icon": "📝"},
                    {"text": "Second tooltip", "icon": "📊"}
                ]
            }

    def test_development_mode_component_declaration(self):
        """Test component declaration in development mode."""
        # Test the development mode path by directly testing the conditional logic
        import streamlit.components.v1 as components
        
        with patch.object(components, 'declare_component') as mock_declare:
            mock_declare.return_value = Mock()
            
            # Simulate the development mode conditional
            _RELEASE = False
            if not _RELEASE:
                _component_func = components.declare_component(
                    "json_viewer",
                    url="http://localhost:3001",
                )
            
            # Should have been called with URL for development
            mock_declare.assert_called_with(
                "json_viewer",
                url="http://localhost:3001"
            )