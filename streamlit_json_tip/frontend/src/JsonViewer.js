import React, { useEffect, useState, useCallback, useMemo, useRef } from "react"
import {
  Streamlit,
  withStreamlitConnection,
} from "streamlit-component-lib"
import Tippy from '@tippyjs/react'
import 'tippy.js/dist/tippy.css'
import "./JsonViewer.css"

function JsonViewer(props) {
  const [expandedPaths, setExpandedPaths] = useState(new Set())
  const [isInitialized, setIsInitialized] = useState(false)
  const [isDarkMode, setIsDarkMode] = useState(false)
  const [copyFeedback, setCopyFeedback] = useState(null)
  
  const { 
    data, 
    help_text = {}, 
    tags = {}, 
    tooltip_config = {}, 
    tooltip_icon = "ℹ️", 
    tooltip_icons = {},
    enable_field_selection = true
  } = props.args

  useEffect(() => {
    Streamlit.setFrameHeight()
  })

  useEffect(() => {
    // Detect Streamlit's theme by checking the body class or CSS variables
    const detectTheme = () => {
      const body = document.body
      const computedStyle = getComputedStyle(body)
      
      // Check for Streamlit's dark mode indicators
      const backgroundColor = computedStyle.backgroundColor
      const isDark = backgroundColor === 'rgb(14, 17, 23)' || 
                     backgroundColor === 'rgb(38, 39, 48)' ||
                     body.classList.contains('dark-theme') ||
                     body.classList.contains('stDarkTheme') ||
                     computedStyle.getPropertyValue('--background-color') === '#0e1117'
      
      setIsDarkMode(isDark)
    }

    // Initial theme detection
    detectTheme()

    // Watch for theme changes
    const observer = new MutationObserver(detectTheme)
    observer.observe(document.body, {
      attributes: true,
      attributeFilter: ['class', 'style']
    })

    // Also listen for CSS variable changes
    const handleResize = () => detectTheme()
    window.addEventListener('resize', handleResize)

    return () => {
      observer.disconnect()
      window.removeEventListener('resize', handleResize)
    }
  }, [])

  // Memoize the path calculation to avoid recalculating on every render
  const allPaths = useMemo(() => {
    if (!data) return new Set()
    
    const getAllPaths = (obj, currentPath = "") => {
      const paths = new Set()
      
      if (Array.isArray(obj)) {
        paths.add(currentPath)
        obj.forEach((item, index) => {
          const itemPath = `${currentPath}[${index}]`
          if (typeof item === "object" && item !== null) {
            const childPaths = getAllPaths(item, itemPath)
            childPaths.forEach(path => paths.add(path))
          }
        })
      } else if (typeof obj === "object" && obj !== null) {
        paths.add(currentPath)
        Object.keys(obj).forEach(key => {
          const keyPath = currentPath ? `${currentPath}.${key}` : key
          if (typeof obj[key] === "object" && obj[key] !== null) {
            const childPaths = getAllPaths(obj[key], keyPath)
            childPaths.forEach(path => paths.add(path))
          }
        })
      }
      
      return paths
    }
    
    return getAllPaths(data)
  }, [data])

  useEffect(() => {
    // Auto-expand all nodes by default, but only on first load
    if (data && !isInitialized) {
      setExpandedPaths(allPaths)
      setIsInitialized(true)
    }
  }, [data, isInitialized, allPaths])

  const toggleExpanded = useCallback((path) => {
    // Prevent event from bubbling up and causing unwanted side effects
    setExpandedPaths(prevExpanded => {
      const newExpanded = new Set(prevExpanded)
      if (newExpanded.has(path)) {
        newExpanded.delete(path)
      } else {
        newExpanded.add(path)
      }
      
      // Ensure the frame height is updated after state change but don't trigger component value change
      setTimeout(() => {
        Streamlit.setFrameHeight()
      }, 0)
      
      return newExpanded
    })
  }, [])

  // Ref to store timeout for debouncing
  const fieldClickTimeoutRef = useRef(null)

  const handleFieldClick = useCallback((path, value, event) => {
    // Skip field selection entirely if disabled
    if (!enable_field_selection) {
      return
    }
    
    // Only trigger selection if it's actually a deliberate click on the field content,
    // not accidental clicks on tooltips or other elements
    if (event && (event.target.classList.contains('help-text') || 
                  event.target.closest('.help-text'))) {
      return // Don't trigger selection for tooltip clicks
    }
    
    // Clear any existing timeout
    if (fieldClickTimeoutRef.current) {
      clearTimeout(fieldClickTimeoutRef.current)
    }
    
    // Debounce the field selection to prevent rapid refreshes
    fieldClickTimeoutRef.current = setTimeout(() => {
      Streamlit.setComponentValue({
        path: path,
        value: value,
        help_text: help_text[path] || null,
        tag: tags[path] || null
      })
    }, 500) // 500ms delay to reduce refresh frequency
  }, [help_text, tags, enable_field_selection])

  // Cleanup timeout on unmount
  useEffect(() => {
    return () => {
      if (fieldClickTimeoutRef.current) {
        clearTimeout(fieldClickTimeoutRef.current)
      }
    }
  }, [])

  const handleCopyToClipboard = useCallback(async () => {
    try {
      const jsonString = JSON.stringify(data, null, 2)
      await navigator.clipboard.writeText(jsonString)
      setCopyFeedback('✅ Copied!')
      setTimeout(() => setCopyFeedback(null), 2000)
    } catch (err) {
      setCopyFeedback('❌ Failed to copy')
      setTimeout(() => setCopyFeedback(null), 2000)
      console.error('Failed to copy JSON:', err)
    }
  }, [data])

  const renderValue = (value, path = "") => {
    if (value === null) {
      return <span className="json-null">null</span>
    }
    
    if (typeof value === "boolean") {
      return <span className="json-boolean">{value.toString()}</span>
    }
    
    if (typeof value === "number") {
      return <span className="json-number">{value}</span>
    }
    
    if (typeof value === "string") {
      return <span className="json-string">"{value}"</span>
    }
    
    if (Array.isArray(value)) {
      const isExpanded = expandedPaths.has(path)
      
      return (
        <div className="json-array">
          <div className="json-node-header">
            <span 
              className="expand-arrow"
              onClick={(e) => {
                e.preventDefault()
                e.stopPropagation()
                toggleExpanded(path)
              }}
            >
              {isExpanded ? '▼' : '▶'}
            </span>
            <span className="json-bracket">[</span>
            {!isExpanded && value.length > 0 && (
              <span className="json-summary"> {value.length} items</span>
            )}
            {!isExpanded && <span className="json-bracket">]</span>}
          </div>
          {isExpanded && (
            <div className="json-array-content">
              {value.map((item, index) => {
                const itemPath = `${path}[${index}]`
                return (
                  <div key={index} className="json-array-item">
                    <span className="json-index">{index}:</span>
                    <div 
                      className={`json-field ${enable_field_selection ? 'clickable' : ''}`}
                      onClick={(e) => {
                        e.preventDefault()
                        e.stopPropagation()
                        handleFieldClick(itemPath, item, e)
                      }}
                    >
                      {renderValue(item, itemPath)}
                      {help_text[itemPath] && (
                        <Tippy 
                          content={help_text[itemPath]}
                          theme={isDarkMode ? 'dark' : 'light'}
                          {...tooltip_config}
                        >
                          <span 
                            className="help-text"
                            onClick={(e) => {
                              e.preventDefault()
                              e.stopPropagation()
                            }}
                          >
                            {tooltip_icons[itemPath] || tooltip_icon}
                          </span>
                        </Tippy>
                      )}
                      {tags[itemPath] && (
                        <span className="tag">{tags[itemPath]}</span>
                      )}
                    </div>
                  </div>
                )
              })}
              <div className="json-closing-bracket">
                <span className="json-bracket">]</span>
              </div>
            </div>
          )}
        </div>
      )
    }
    
    if (typeof value === "object" && value !== null) {
      const isExpanded = expandedPaths.has(path)
      const keys = Object.keys(value)
      
      return (
        <div className="json-object">
          <div className="json-node-header">
            <span 
              className="expand-arrow"
              onClick={(e) => {
                e.preventDefault()
                e.stopPropagation()
                toggleExpanded(path)
              }}
            >
              {isExpanded ? '▼' : '▶'}
            </span>
            <span className="json-bracket">{"{"}</span>
            {!isExpanded && keys.length > 0 && (
              <span className="json-summary"> {keys.length} keys</span>
            )}
            {!isExpanded && <span className="json-bracket">{"}"}</span>}
          </div>
          {isExpanded && (
            <div className="json-object-content">
              {keys.map((key) => {
                const keyPath = path ? `${path}.${key}` : key
                return (
                  <div key={key} className="json-object-item">
                    <span className="json-key">"{key}":</span>
                    <div 
                      className={`json-field ${enable_field_selection ? 'clickable' : ''}`}
                      onClick={(e) => {
                        e.preventDefault()
                        e.stopPropagation()
                        handleFieldClick(keyPath, value[key], e)
                      }}
                    >
                      {renderValue(value[key], keyPath)}
                      {help_text[keyPath] && (
                        <Tippy 
                          content={help_text[keyPath]}
                          theme={isDarkMode ? 'dark' : 'light'}
                          {...tooltip_config}
                        >
                          <span className="help-text">
                            {tooltip_icons[keyPath] || tooltip_icon}
                          </span>
                        </Tippy>
                      )}
                      {tags[keyPath] && (
                        <span className="tag">{tags[keyPath]}</span>
                      )}
                    </div>
                  </div>
                )
              })}
              <div className="json-closing-bracket">
                <span className="json-bracket">{"}"}</span>
              </div>
            </div>
          )}
        </div>
      )
    }
    
    return <span>{String(value)}</span>
  }

  if (!data) {
    return <div className={`json-viewer ${isDarkMode ? 'dark-mode' : 'light-mode'}`}>No data provided</div>
  }
  
  return (
    <div className={`json-viewer ${isDarkMode ? 'dark-mode' : 'light-mode'}`}>
      <div className="json-header">
        <Tippy 
          content={copyFeedback || "copy"}
          theme={isDarkMode ? 'dark' : 'light'}
          {...tooltip_config}
        >
          <button 
            className="copy-button"
            onClick={handleCopyToClipboard}
            disabled={!data}
          >
            {copyFeedback || '📋'}
          </button>
        </Tippy>
      </div>
      {renderValue(data)}
    </div>
  )
}

export default withStreamlitConnection(JsonViewer)