"""
Configuration Module
Contains color palette and theme settings for Finsight application
"""

# Enhanced color palette with dark mode support
COLOR_THEMES = {
    # Light theme colors
    'light': {
        'primary': '#6366f1',  # Modern indigo
        'primary_hover': '#5b5bf6',
        'secondary': '#10b981',  # Emerald green
        'secondary_hover': '#059669',
        'accent': '#f59e0b',  # Amber
        'background': '#f8fafc',  # Slate 50
        'surface': '#ffffff',  # White
        'surface_elevated': '#f1f5f9',  # Slate 100
        'card_bg': '#ffffff',
        'card_border': '#e2e8f0',  # Slate 200
        'text_primary': '#0f172a',  # Slate 900
        'text_secondary': '#64748b',  # Slate 500
        'text_tertiary': '#94a3b8',  # Slate 400
        'border': '#e2e8f0',
        'success': '#10b981',
        'success_bg': '#d1fae5',
        'warning': '#f59e0b',
        'warning_bg': '#fef3c7',
        'error': '#ef4444',
        'error_bg': '#fee2e2',
        'info': '#3b82f6',
        'info_bg': '#dbeafe',
        'invested': '#6366f1',
        'returns': '#10b981',
        'shadow': 'rgba(0, 0, 0, 0.1)',
        'shadow_dark': 'rgba(0, 0, 0, 0.2)',
    },
    
    # Dark theme colors
    'dark': {
        'primary': '#818cf8',  # Indigo 400
        'primary_hover': '#6366f1',
        'secondary': '#34d399',  # Emerald 400
        'secondary_hover': '#10b981',
        'accent': '#fbbf24',  # Amber 400
        'background': '#0f172a',  # Slate 900
        'surface': '#1e293b',  # Slate 800
        'surface_elevated': '#334155',  # Slate 700
        'card_bg': '#1e293b',
        'card_border': '#334155',
        'text_primary': '#f8fafc',  # Slate 50
        'text_secondary': '#cbd5e1',  # Slate 300
        'text_tertiary': '#94a3b8',  # Slate 400
        'border': '#334155',
        'success': '#34d399',
        'success_bg': '#064e3b',
        'warning': '#fbbf24',
        'warning_bg': '#451a03',
        'error': '#f87171',
        'error_bg': '#7f1d1d',
        'info': '#60a5fa',
        'info_bg': '#1e3a8a',
        'invested': '#818cf8',
        'returns': '#34d399',
        'shadow': 'rgba(0, 0, 0, 0.3)',
        'shadow_dark': 'rgba(0, 0, 0, 0.5)',
    }
}

class ThemeManager:
    """Manages app theme and provides color utilities"""
    
    def __init__(self):
        self._current_theme = 'light'
        
    @property
    def current_theme(self):
        return self._current_theme
    
    @current_theme.setter 
    def current_theme(self, theme):
        if theme in ['light', 'dark']:
            self._current_theme = theme
    
    def get_color(self, color_name):
        """Get color from current theme"""
        return COLOR_THEMES[self._current_theme].get(color_name, '#000000')
    
    def get_colors(self):
        """Get all colors from current theme"""
        return COLOR_THEMES[self._current_theme]
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        self._current_theme = 'dark' if self._current_theme == 'light' else 'light'
        return self._current_theme

# Global theme manager instance
theme_manager = ThemeManager()

# Backward compatibility - provide COLORS dict that uses current theme
class DynamicColors:
    def __getitem__(self, key):
        return theme_manager.get_color(key)
    
    def get(self, key, default=None):
        color = theme_manager.get_color(key)
        return color if color != '#000000' else default

# Create dynamic COLORS object for backward compatibility
COLORS = DynamicColors()
