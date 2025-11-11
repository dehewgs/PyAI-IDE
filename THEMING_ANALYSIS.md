# PyAI IDE - Theming System Analysis and Issues

## Current State Analysis

### Issues Identified

1. **Hardcoded Colors in Components**
   - CodeEditor: Hardcoded Monokai theme colors (#272822, #f8f8f2)
   - ConsolePanel: Hardcoded dark theme colors (#1e1e1e, #d4d4d4)
   - Line numbers: Hardcoded colors (39, 40, 34), (117, 113, 94)
   - Syntax highlighting: Hardcoded colors for keywords, strings, comments, etc.

2. **Theme Manager Limitations**
   - Only provides basic QSS stylesheets
   - Doesn't handle component-specific theming
   - No theme persistence
   - No theme configuration file support
   - Limited color palette management

3. **Inconsistent Theming**
   - CodeEditor uses Monokai theme regardless of app theme
   - ConsolePanel always uses dark colors
   - Syntax highlighter colors don't adapt to theme
   - Line number colors hardcoded

4. **Missing Features**
   - No theme configuration system
   - No color palette management
   - No theme switching for already-created components
   - No custom theme support
   - No theme preview

5. **UI Component Issues**
   - Dialogs don't have themed stylesheets
   - Project/Model panels don't have themed stylesheets
   - No consistent spacing/padding across themes
   - No hover/focus state styling

## Proposed Solutions

### 1. Enhanced Theme Manager
- Support multiple theme profiles (dark, light, custom)
- Centralized color palette management
- Theme configuration files (JSON/YAML)
- Dynamic theme switching with component updates
- Theme persistence to config

### 2. Component-Aware Theming
- Each component registers with theme manager
- Components receive theme updates via signals
- Syntax highlighter adapts to theme
- Editor colors adapt to theme

### 3. Color Palette System
- Define color palettes for each theme
- Semantic color names (primary, secondary, background, etc.)
- Easy customization and extension

### 4. Theme Configuration
- JSON-based theme definitions
- Support for custom themes
- Theme inheritance/composition
- Easy distribution of themes

### 5. UI Consistency
- All dialogs themed consistently
- All panels themed consistently
- Proper spacing and padding
- Hover/focus states defined

## Implementation Plan

1. Create enhanced ThemeManager with palette support
2. Create ThemeConfig class for theme definitions
3. Update CodeEditor to use theme colors
4. Update ConsolePanel to use theme colors
5. Update SyntaxHighlighter to use theme colors
6. Create theme configuration files
7. Update all dialogs with theming
8. Add theme switching signal/slot system
9. Add theme persistence
10. Create theme preview/selector dialog
