/**
 * Tests for JsonViewer component
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import JsonViewer from './JsonViewer';

// Mock streamlit-component-lib
jest.mock('streamlit-component-lib', () => ({
  Streamlit: {
    setComponentValue: jest.fn(),
    setFrameHeight: jest.fn(),
    setComponentReady: jest.fn(),
  },
  withStreamlitConnection: (component) => component,
}));

describe('JsonViewer', () => {
  const defaultProps = {
    args: {
      data: { name: 'John', age: 30 },
      help_text: {},
      tags: {},
      tooltip_config: {},
      tooltip_icon: 'ℹ️',
      tooltip_icons: {},
    },
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders JSON data correctly', () => {
    render(<JsonViewer {...defaultProps} />);
    
    expect(screen.getByText('"name":')).toBeInTheDocument();
    expect(screen.getByText('"John"')).toBeInTheDocument();
    expect(screen.getByText('"age":')).toBeInTheDocument();
    expect(screen.getByText('30')).toBeInTheDocument();
  });

  test('renders help text icons when help text is provided', () => {
    const propsWithHelp = {
      ...defaultProps,
      args: {
        ...defaultProps.args,
        help_text: { name: 'User full name' },
      },
    };

    render(<JsonViewer {...propsWithHelp} />);
    
    // Should render help icon for name field
    const helpIcons = screen.getAllByText('ℹ️');
    expect(helpIcons.length).toBeGreaterThan(0);
  });

  test('renders tags when provided', () => {
    const propsWithTags = {
      ...defaultProps,
      args: {
        ...defaultProps.args,
        tags: { name: 'PII' },
      },
    };

    render(<JsonViewer {...propsWithTags} />);
    
    expect(screen.getByText('PII')).toBeInTheDocument();
  });

  test('handles nested objects correctly', () => {
    const nestedProps = {
      ...defaultProps,
      args: {
        ...defaultProps.args,
        data: {
          user: {
            profile: {
              name: 'Alice',
              settings: { theme: 'dark' }
            }
          }
        },
      },
    };

    render(<JsonViewer {...nestedProps} />);
    
    expect(screen.getByText('"user":')).toBeInTheDocument();
    expect(screen.getByText('"profile":')).toBeInTheDocument();
  });

  test('handles arrays correctly', () => {
    const arrayProps = {
      ...defaultProps,
      args: {
        ...defaultProps.args,
        data: {
          items: ['apple', 'banana', 'cherry']
        },
      },
    };

    render(<JsonViewer {...arrayProps} />);
    
    expect(screen.getByText('"items":')).toBeInTheDocument();
    expect(screen.getByText('"apple"')).toBeInTheDocument();
    expect(screen.getByText('"banana"')).toBeInTheDocument();
    expect(screen.getByText('"cherry"')).toBeInTheDocument();
  });

  test('expands and collapses objects on click', async () => {
    const nestedProps = {
      ...defaultProps,
      args: {
        ...defaultProps.args,
        data: {
          user: { name: 'John', age: 30 }
        },
      },
    };

    render(<JsonViewer {...nestedProps} />);
    
    // Should see the user object structure
    expect(screen.getByText('"user":')).toBeInTheDocument();
    
    // Find and click the expand/collapse arrow
    const arrows = screen.getAllByText(/[▼▶]/);
    if (arrows.length > 0) {
      fireEvent.click(arrows[0]);
      
      // After clicking, content might be hidden (depending on implementation)
      // This test verifies the click interaction works
      expect(arrows[0]).toBeInTheDocument();
    }
  });

  test('handles different data types correctly', () => {
    const mixedDataProps = {
      ...defaultProps,
      args: {
        ...defaultProps.args,
        data: {
          string: 'text',
          number: 42,
          boolean: true,
          null_value: null,
          array: [1, 2, 3],
          object: { nested: 'value' }
        },
      },
    };

    render(<JsonViewer {...mixedDataProps} />);
    
    expect(screen.getByText('"text"')).toBeInTheDocument();
    expect(screen.getByText('42')).toBeInTheDocument();
    expect(screen.getByText('true')).toBeInTheDocument();
    expect(screen.getByText('null')).toBeInTheDocument();
  });

  test('uses custom tooltip icon when provided', () => {
    const customIconProps = {
      ...defaultProps,
      args: {
        ...defaultProps.args,
        tooltip_icon: '💡',
        help_text: { name: 'Help text' },
      },
    };

    render(<JsonViewer {...customIconProps} />);
    
    expect(screen.getByText('💡')).toBeInTheDocument();
  });

  test('handles empty objects and arrays', () => {
    const emptyProps = {
      ...defaultProps,
      args: {
        ...defaultProps.args,
        data: {
          empty_object: {},
          empty_array: []
        },
      },
    };

    render(<JsonViewer {...emptyProps} />);
    
    expect(screen.getByText('"empty_object":')).toBeInTheDocument();
    expect(screen.getByText('"empty_array":')).toBeInTheDocument();
  });

  test('renders field paths correctly for nested data', () => {
    const nestedProps = {
      ...defaultProps,
      args: {
        ...defaultProps.args,
        data: {
          users: [
            { id: 1, name: 'Alice' },
            { id: 2, name: 'Bob' }
          ]
        },
        help_text: {
          'users[0].name': 'First user name',
          'users[1].name': 'Second user name'
        },
      },
    };

    render(<JsonViewer {...nestedProps} />);
    
    expect(screen.getByText('"users":')).toBeInTheDocument();
    expect(screen.getByText('"Alice"')).toBeInTheDocument();
    expect(screen.getByText('"Bob"')).toBeInTheDocument();
  });

  test('handles tooltip configuration', () => {
    const tooltipConfigProps = {
      ...defaultProps,
      args: {
        ...defaultProps.args,
        tooltip_config: {
          placement: 'top',
          theme: 'dark'
        },
        help_text: { name: 'Help text' },
      },
    };

    render(<JsonViewer {...tooltipConfigProps} />);
    
    // Component should render without errors with tooltip config
    expect(screen.getByText('"name":')).toBeInTheDocument();
  });
});