import time
import customtkinter as ctk
import requests
import threading
import re
from urllib.parse import urlparse
from datetime import datetime
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
import math

# Import our currency API
try:
    from currency_api import CurrencyAPI
    CURRENCY_API_AVAILABLE = True
except ImportError:
    CURRENCY_API_AVAILABLE = False
    print("Currency API not available, using fallback rates")

ctk.set_appearance_mode("Light")  # Force light mode for purple theme
ctk.set_default_color_theme("blue")
ctk.set_window_scaling(1.0)
ctk.set_widget_scaling(1.0)

# Custom color palette inspired by Groww
COLORS = {
    'primary': '#5367ff',  # Purple-blue
    'secondary': '#00d09c',  # Teal/Green
    'background': '#f5f7ff',  # Light purple background
    'card_bg': '#ffffff',  # White cards
    'text_primary': '#1c1c1e',  # Dark text
    'text_secondary': '#6e7191',  # Gray text
    'border': '#e4e7f5',  # Light border
    'success': '#00d09c',  # Green
    'warning': '#f59e0b',  # Orange
    'invested': '#5367ff',  # Purple for invested
    'returns': '#00d09c',  # Teal for returns
}

class SIPCalculator(ctk.CTkFrame):
    """SIP (Systematic Investment Plan) Calculator Widget"""
    
    def __init__(self, parent):
        super().__init__(parent, corner_radius=20, fg_color=COLORS['background'])
        
        # SIP Calculator Title with purple theme
        title = ctk.CTkLabel(
            self,
            text="💰 SIP Calculator",
            font=("Segoe UI", 24, "bold"),
            text_color=COLORS['text_primary']
        )
        title.pack(pady=(25, 5))
        
        # Subtitle
        subtitle = ctk.CTkLabel(
            self,
            text="Calculate your Systematic Investment Plan returns",
            font=("Segoe UI", 12),
            text_color=COLORS['text_secondary']
        )
        subtitle.pack(pady=(0, 20))
        
        # Input frame with white card background
        input_frame = ctk.CTkFrame(self, fg_color=COLORS['card_bg'], corner_radius=15)
        input_frame.pack(pady=10, padx=30, fill="x")
        
        # Configure grid
        input_frame.grid_columnconfigure(1, weight=1)
        
        # Monthly Investment with Groww style
        monthly_label = ctk.CTkLabel(
            input_frame, 
            text="Monthly Investment", 
            font=("Segoe UI", 13),
            text_color=COLORS['text_secondary']
        )
        monthly_label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 5))
        
        self.monthly_entry = ctk.CTkEntry(
            input_frame, 
            placeholder_text="₹ 5000", 
            width=200,
            height=40,
            font=("Segoe UI", 14),
            border_width=2,
            border_color=COLORS['border'],
            fg_color="white"
        )
        self.monthly_entry.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")
        self.monthly_entry.insert(0, "5000")
        
        # Duration in years
        duration_label = ctk.CTkLabel(
            input_frame, 
            text="Investment Period (Years)", 
            font=("Segoe UI", 13),
            text_color=COLORS['text_secondary']
        )
        duration_label.grid(row=2, column=0, sticky="w", padx=20, pady=(10, 5))
        
        self.duration_entry = ctk.CTkEntry(
            input_frame, 
            placeholder_text="10", 
            width=200,
            height=40,
            font=("Segoe UI", 14),
            border_width=2,
            border_color=COLORS['border'],
            fg_color="white"
        )
        self.duration_entry.grid(row=3, column=0, padx=20, pady=(0, 15), sticky="w")
        self.duration_entry.insert(0, "10")
        
        # Expected Annual Return
        return_label = ctk.CTkLabel(
            input_frame, 
            text="Expected Return Rate (% p.a.)", 
            font=("Segoe UI", 13),
            text_color=COLORS['text_secondary']
        )
        return_label.grid(row=4, column=0, sticky="w", padx=20, pady=(10, 5))
        
        self.return_entry = ctk.CTkEntry(
            input_frame, 
            placeholder_text="12%", 
            width=200,
            height=40,
            font=("Segoe UI", 14),
            border_width=2,
            border_color=COLORS['border'],
            fg_color="white"
        )
        self.return_entry.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="w")
        self.return_entry.insert(0, "12")
        
        # Calculate button with Groww green style
        calc_button = ctk.CTkButton(
            input_frame,
            text="Calculate",
            command=self.calculate_sip,
            font=("Segoe UI", 14, "bold"),
            height=45,
            width=200,
            fg_color=COLORS['secondary'],
            hover_color="#00b87c",
            corner_radius=10
        )
        calc_button.grid(row=6, column=0, padx=20, pady=(10, 25), sticky="w")
        
        # Results frame with light background
        self.results_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=COLORS['primary'],
            scrollbar_button_hover_color=COLORS['primary']
        )
        self.results_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Initial placeholder with Groww style
        placeholder = ctk.CTkLabel(
            self.results_frame,
            text="👆 Enter your investment details above and click Calculate",
            font=("Segoe UI", 13),
            text_color=COLORS['text_secondary']
        )
        placeholder.pack(pady=50)
    
    def calculate_sip(self):
        """Calculate SIP returns and display results"""
        try:
            # Get input values
            monthly_investment = float(self.monthly_entry.get() or 5000)
            duration_years = float(self.duration_entry.get() or 10)
            annual_return = float(self.return_entry.get() or 12)
            
            # Calculate SIP
            monthly_return = annual_return / 100 / 12
            total_months = duration_years * 12
            
            # Future Value formula for SIP
            if monthly_return > 0:
                future_value = monthly_investment * (((1 + monthly_return) ** total_months - 1) / monthly_return) * (1 + monthly_return)
            else:
                future_value = monthly_investment * total_months
            
            total_invested = monthly_investment * total_months
            total_returns = future_value - total_invested
            
            # Clear results frame
            for widget in self.results_frame.winfo_children():
                widget.destroy()
            
            # Display results with Groww-style cards
            results_title = ctk.CTkLabel(
                self.results_frame,
                text="Investment Summary",
                font=("Segoe UI", 20, "bold"),
                text_color=COLORS['text_primary']
            )
            results_title.pack(pady=(20, 25))
            
            # Create stylish results cards with Groww theme
            results_container = ctk.CTkFrame(self.results_frame, fg_color="transparent")
            results_container.pack(pady=10, padx=20, fill="x")
            
            # Invested Amount Card - Purple theme
            invested_card = ctk.CTkFrame(
                results_container, 
                corner_radius=15, 
                fg_color=COLORS['card_bg'],
                border_width=2,
                border_color=COLORS['border']
            )
            invested_card.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
            
            ctk.CTkLabel(
                invested_card, 
                text="Invested amount", 
                font=("Segoe UI", 12),
                text_color=COLORS['text_secondary']
            ).pack(pady=(20, 5))
            
            ctk.CTkLabel(
                invested_card, 
                text=f"₹{total_invested:,.0f}", 
                font=("Segoe UI", 26, "bold"),
                text_color=COLORS['invested']
            ).pack(pady=(0, 20))
            
            # Returns Card - Teal theme
            returns_card = ctk.CTkFrame(
                results_container, 
                corner_radius=15, 
                fg_color=COLORS['card_bg'],
                border_width=2,
                border_color=COLORS['border']
            )
            returns_card.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
            
            ctk.CTkLabel(
                returns_card, 
                text="Est. returns", 
                font=("Segoe UI", 12),
                text_color=COLORS['text_secondary']
            ).pack(pady=(20, 5))
            
            ctk.CTkLabel(
                returns_card, 
                text=f"₹{total_returns:,.0f}", 
                font=("Segoe UI", 26, "bold"),
                text_color=COLORS['returns']
            ).pack(pady=(0, 20))
            
            # Total Value Card - Purple theme
            future_card = ctk.CTkFrame(
                results_container, 
                corner_radius=15, 
                fg_color=COLORS['card_bg'],
                border_width=2,
                border_color=COLORS['border']
            )
            future_card.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
            
            ctk.CTkLabel(
                future_card, 
                text="Total value", 
                font=("Segoe UI", 12),
                text_color=COLORS['text_secondary']
            ).pack(pady=(20, 5))
            
            ctk.CTkLabel(
                future_card, 
                text=f"₹{future_value:,.0f}", 
                font=("Segoe UI", 26, "bold"),
                text_color=COLORS['primary']
            ).pack(pady=(0, 20))
            
            # Configure grid columns to be equal width
            for i in range(3):
                results_container.grid_columnconfigure(i, weight=1, uniform="results")
            
            # Create visualization
            self.create_sip_chart(monthly_investment, duration_years, annual_return, total_invested, future_value)
            
        except ValueError:
            # Show error
            for widget in self.results_frame.winfo_children():
                widget.destroy()
            
            error_label = ctk.CTkLabel(
                self.results_frame,
                text="❌ Please enter valid numbers",
                font=("Arial", 14),
                text_color=("red", "#ff6b6b")
            )
            error_label.pack(pady=30)
    
    def create_sip_chart(self, monthly_investment, duration_years, annual_return, total_invested, future_value):
        """Create SIP growth visualization chart with Groww theme"""
        try:
            # Create chart frame with Groww card style
            chart_frame = ctk.CTkFrame(
                self.results_frame, 
                corner_radius=15, 
                fg_color=COLORS['card_bg'],
                border_width=2,
                border_color=COLORS['border']
            )
            chart_frame.pack(pady=25, padx=20, fill="both", expand=True)
            
            # Chart title with Groww style
            chart_title = ctk.CTkLabel(
                chart_frame,
                text="Growth Visualization",
                font=("Segoe UI", 16, "bold"),
                text_color=COLORS['text_primary']
            )
            chart_title.pack(pady=(20, 10))
            
            # Create matplotlib figure
            fig, ax = plt.subplots(figsize=(11, 5))
            fig.patch.set_facecolor('#ffffff')
            
            # Calculate year-wise values
            years = list(range(1, int(duration_years) + 1))
            invested_values = [monthly_investment * 12 * year for year in years]
            
            monthly_return = annual_return / 100 / 12
            future_values = []
            
            for year in years:
                months = year * 12
                if monthly_return > 0:
                    fv = monthly_investment * (((1 + monthly_return) ** months - 1) / monthly_return) * (1 + monthly_return)
                else:
                    fv = monthly_investment * months
                future_values.append(fv)
            
            # Set Groww-style colors
            ax.set_facecolor('#fafbff')
            
            # Plot bars with Groww colors
            width = 0.38
            x_pos = np.arange(len(years))
            
            bars1 = ax.bar(
                x_pos - width/2, invested_values, width, 
                label='Invested amount', 
                color='#d4d9ff',  # Light purple
                alpha=0.9,
                edgecolor='#5367ff',
                linewidth=1.8
            )
            bars2 = ax.bar(
                x_pos + width/2, future_values, width, 
                label='Est. returns', 
                color='#b3f5e9',  # Light teal
                alpha=0.9,
                edgecolor='#00d09c',
                linewidth=1.8
            )
            
            # Styling with Groww theme
            ax.set_xlabel('Years', color=COLORS['text_primary'], fontsize=12, fontweight='600', labelpad=10)
            ax.set_ylabel('Amount (₹)', color=COLORS['text_primary'], fontsize=12, fontweight='600', labelpad=10)
            ax.set_xticks(x_pos)
            ax.set_xticklabels([f'{y}Y' for y in years], fontsize=10)
            
            # Enhanced legend with Groww style
            legend = ax.legend(
                loc='upper left',
                facecolor='white', 
                edgecolor=COLORS['border'], 
                fontsize=11,
                framealpha=1,
                shadow=False
            )
            legend.get_frame().set_linewidth(1.5)
            
            # Format y-axis
            def format_currency(x, p):
                if x >= 10000000:  # 1 Crore
                    return f'₹{x/10000000:.1f}Cr'
                elif x >= 100000:  # 1 Lakh
                    return f'₹{x/100000:.1f}L'
                elif x >= 1000:
                    return f'₹{x/1000:.0f}K'
                else:
                    return f'₹{x:.0f}'
            
            ax.yaxis.set_major_formatter(plt.FuncFormatter(format_currency))
            ax.tick_params(colors=COLORS['text_secondary'], labelsize=10)
            ax.grid(True, alpha=0.2, linestyle='-', linewidth=0.8, color='#e0e4f5', axis='y')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color(COLORS['border'])
            ax.spines['bottom'].set_color(COLORS['border'])
            
            # Tight layout
            fig.tight_layout()
            
            # Embed chart
            canvas = FigureCanvasTkAgg(fig, chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=(5, 20))
            
        except Exception as e:
            print(f"Error creating SIP chart: {e}")

class CurrencyConverter(ctk.CTkFrame):
    """Currency Converter Widget with Real-time Exchange Rates - Groww Theme"""
    
    def __init__(self, parent):
        super().__init__(parent, corner_radius=20, fg_color=COLORS['background'])
        
        # Store reference to root window
        self.root = parent.winfo_toplevel()
        
        # Initialize currency API
        if CURRENCY_API_AVAILABLE:
            self.currency_api = CurrencyAPI()
        else:
            self.currency_api = None
        
        # Currency data
        self.currencies = {
            "USD": "US Dollar",
            "EUR": "Euro", 
            "GBP": "British Pound",
            "JPY": "Japanese Yen",
            "CAD": "Canadian Dollar",
            "AUD": "Australian Dollar",
            "CHF": "Swiss Franc",
            "CNY": "Chinese Yuan",
            "INR": "Indian Rupee",
            "SGD": "Singapore Dollar",
            "KRW": "South Korean Won",
            "BRL": "Brazilian Real",
            "MXN": "Mexican Peso"
        }
        
        # Fallback exchange rates (used if API fails)
        self.fallback_rates = {
            "USD": 1.0,
            "EUR": 0.85,
            "GBP": 0.73,
            "JPY": 110.0,
            "CAD": 1.25,
            "AUD": 1.35,
            "CHF": 0.92,
            "CNY": 6.45,
            "INR": 83.2,
            "SGD": 1.35,
            "KRW": 1300.0,
            "BRL": 5.2,
            "MXN": 17.5
        }
        
        self.current_rates = {}
        self.setup_ui()
        self.load_exchange_rates()
        
    def setup_ui(self):
        """Setup Currency Converter UI with side-by-side layout"""
        # Title with Groww style
        title = ctk.CTkLabel(
            self,
            text="💱 Currency Converter",
            font=("Segoe UI", 24, "bold"),
            text_color=COLORS['text_primary']
        )
        title.pack(pady=(25, 5))
        
        # Subtitle
        subtitle = ctk.CTkLabel(
            self,
            text="Convert between different currencies with live rates",
            font=("Segoe UI", 12),
            text_color=COLORS['text_secondary']
        )
        subtitle.pack(pady=(0, 10))
        
        # API status
        self.status_label = ctk.CTkLabel(
            self,
            text="🔄 Loading exchange rates...",
            font=("Segoe UI", 11),
            text_color=COLORS['text_secondary']
        )
        self.status_label.pack(pady=(0, 15))
        
        # Main container for side-by-side layout
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(pady=10, padx=30, fill="both", expand=True)
        
        # Configure grid for 50-50 split
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)
        
        # LEFT SIDE - Input Card
        input_card = ctk.CTkFrame(
            main_container, 
            fg_color=COLORS['card_bg'], 
            corner_radius=15,
            border_width=2,
            border_color=COLORS['border']
        )
        input_card.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        
        # Card title
        input_title = ctk.CTkLabel(
            input_card,
            text="Enter Details",
            font=("Segoe UI", 16, "bold"),
            text_color=COLORS['text_primary']
        )
        input_title.pack(pady=(20, 15))
        
        # Amount input
        amount_label = ctk.CTkLabel(
            input_card, 
            text="Amount", 
            font=("Segoe UI", 13),
            text_color=COLORS['text_secondary']
        )
        amount_label.pack(anchor="w", padx=20, pady=(10, 5))
        
        self.amount_entry = ctk.CTkEntry(
            input_card, 
            placeholder_text="Enter amount", 
            height=45,
            font=("Segoe UI", 16),
            border_width=2,
            border_color=COLORS['border'],
            fg_color="white"
        )
        self.amount_entry.pack(padx=20, pady=(0, 15), fill="x")
        self.amount_entry.insert(0, "100")
        self.amount_entry.bind("<KeyRelease>", self.on_amount_change)
        
        # From currency
        from_label = ctk.CTkLabel(
            input_card, 
            text="From", 
            font=("Segoe UI", 13),
            text_color=COLORS['text_secondary']
        )
        from_label.pack(anchor="w", padx=20, pady=(10, 5))
        
        self.from_currency = ctk.CTkComboBox(
            input_card,
            values=list(self.currencies.keys()),
            height=40,
            font=("Segoe UI", 14),
            border_width=2,
            border_color=COLORS['border'],
            button_color=COLORS['primary'],
            button_hover_color=COLORS['primary'],
            dropdown_hover_color=COLORS['background'],
            command=self.on_currency_change
        )
        self.from_currency.set("USD")
        self.from_currency.pack(padx=20, pady=(0, 15), fill="x")
        
        # Swap button
        swap_button = ctk.CTkButton(
            input_card,
            text="⇄ Swap",
            command=self.swap_currencies,
            height=35,
            font=("Segoe UI", 13),
            fg_color="transparent",
            text_color=COLORS['primary'],
            hover_color=COLORS['background'],
            border_width=2,
            border_color=COLORS['border']
        )
        swap_button.pack(pady=10, padx=20, fill="x")
        
        # To currency
        to_label = ctk.CTkLabel(
            input_card, 
            text="To", 
            font=("Segoe UI", 13),
            text_color=COLORS['text_secondary']
        )
        to_label.pack(anchor="w", padx=20, pady=(10, 5))
        
        self.to_currency = ctk.CTkComboBox(
            input_card,
            values=list(self.currencies.keys()),
            height=40,
            font=("Segoe UI", 14),
            border_width=2,
            border_color=COLORS['border'],
            button_color=COLORS['primary'],
            button_hover_color=COLORS['primary'],
            dropdown_hover_color=COLORS['background'],
            command=self.on_currency_change
        )
        self.to_currency.set("INR")
        self.to_currency.pack(padx=20, pady=(0, 15), fill="x")
        
        # Convert button with Groww green
        convert_button = ctk.CTkButton(
            input_card,
            text="Convert",
            command=self.convert_currency,
            font=("Segoe UI", 14, "bold"),
            height=45,
            fg_color=COLORS['secondary'],
            hover_color="#00b87c",
            corner_radius=10
        )
        convert_button.pack(padx=20, pady=(10, 25), fill="x")
        
        # RIGHT SIDE - Results frame
        self.results_frame = ctk.CTkFrame(
            main_container,
            fg_color="transparent"
        )
        self.results_frame.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
        
        # Initial placeholder
        self.show_initial_placeholder()
        
        # Initial conversion
        self.convert_currency()
    
    def show_initial_placeholder(self):
        """Show initial placeholder in results area"""
        placeholder_card = ctk.CTkFrame(
            self.results_frame,
            fg_color=COLORS['card_bg'],
            corner_radius=15,
            border_width=2,
            border_color=COLORS['border']
        )
        placeholder_card.pack(fill="both", expand=True, pady=(0, 0))
        
        # Placeholder content
        ctk.CTkLabel(
            placeholder_card,
            text="💰",
            font=("Segoe UI", 48)
        ).pack(pady=(80, 20))
        
        ctk.CTkLabel(
            placeholder_card,
            text="Your Result",
            font=("Segoe UI", 18, "bold"),
            text_color=COLORS['text_primary']
        ).pack(pady=5)
        
        ctk.CTkLabel(
            placeholder_card,
            text="Will appear here",
            font=("Segoe UI", 13),
            text_color=COLORS['text_secondary']
        ).pack(pady=(0, 80))
    
    def load_exchange_rates(self):
        """Load exchange rates in background"""
        def fetch_rates():
            try:
                if self.currency_api:
                    self.current_rates = self.currency_api.get_exchange_rates("USD")
                    self.root.after(0, lambda: self.status_label.configure(
                        text="✅ Live exchange rates loaded",
                        text_color=COLORS['success']
                    ))
                else:
                    self.current_rates = self.fallback_rates
                    self.root.after(0, lambda: self.status_label.configure(
                        text="⚠️ Using fallback rates (API unavailable)",
                        text_color=COLORS['warning']
                    ))
                
                # Auto-convert if amount is entered
                self.root.after(0, self.convert_currency)
                
            except Exception as e:
                self.current_rates = self.fallback_rates
                self.root.after(0, lambda: self.status_label.configure(
                    text="❌ Failed to load rates, using fallback",
                    text_color="#dc2626"
                ))
        
        threading.Thread(target=fetch_rates, daemon=True).start()
    
    def on_amount_change(self, event=None):
        """Auto-convert when amount changes"""
        # Add small delay to avoid too many conversions while typing
        if hasattr(self, '_conversion_timer'):
            self.root.after_cancel(self._conversion_timer)
        self._conversion_timer = self.root.after(500, self.convert_currency)
    
    def on_currency_change(self, choice=None):
        """Auto-convert when currency selection changes"""
        self.convert_currency()
    
    def swap_currencies(self):
        """Swap from and to currencies"""
        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()
        
        self.from_currency.set(to_curr)
        self.to_currency.set(from_curr)
        
        self.convert_currency()
    
    def convert_currency(self):
        """Convert currency and display result"""
        try:
            amount_text = self.amount_entry.get().strip()
            if not amount_text:
                amount = 1.0
            else:
                # Remove any non-numeric characters except decimal point
                amount_text = ''.join(c for c in amount_text if c.isdigit() or c == '.')
                amount = float(amount_text) if amount_text else 1.0
                
            from_curr = self.from_currency.get()
            to_curr = self.to_currency.get()
            
            # Convert currency
            if self.currency_api and CURRENCY_API_AVAILABLE:
                converted_amount = self.currency_api.convert_currency(amount, from_curr, to_curr)
            else:
                # Fallback conversion via USD
                usd_amount = amount / self.current_rates.get(from_curr, 1)
                converted_amount = usd_amount * self.current_rates.get(to_curr, 1)
            
            # Clear results
            for widget in self.results_frame.winfo_children():
                widget.destroy()
            
            # Main result card with Groww style - fills the right side
            result_card = ctk.CTkFrame(
                self.results_frame, 
                corner_radius=15, 
                fg_color=COLORS['card_bg'],
                border_width=2, 
                border_color=COLORS['border']
            )
            result_card.pack(fill="both", expand=True)
            
            # Result title inside card
            result_title = ctk.CTkLabel(
                result_card,
                text="Result",
                font=("Segoe UI", 16, "bold"),
                text_color=COLORS['text_primary']
            )
            result_title.pack(pady=(20, 25))
            
            # Format numbers appropriately
            if converted_amount >= 1000:
                converted_str = f"{converted_amount:,.2f}"
            else:
                converted_str = f"{converted_amount:.4f}"
                
            if amount >= 1000:
                amount_str = f"{amount:,.2f}"
            else:
                amount_str = f"{amount:.4f}"
            
            # From amount section
            from_section = ctk.CTkFrame(result_card, fg_color="transparent")
            from_section.pack(pady=(15, 10))
            
            ctk.CTkLabel(
                from_section,
                text=amount_str,
                font=("Segoe UI", 28, "bold"),
                text_color=COLORS['primary']
            ).pack(side="left", padx=3)
            
            ctk.CTkLabel(
                from_section,
                text=from_curr,
                font=("Segoe UI", 20, "bold"),
                text_color=COLORS['text_secondary']
            ).pack(side="left", padx=3)
            
            # Equals symbol with icon
            ctk.CTkLabel(
                result_card,
                text="↓",
                font=("Segoe UI", 32, "bold"),
                text_color=COLORS['text_secondary']
            ).pack(pady=15)
            
            # To amount section - highlighted
            to_section = ctk.CTkFrame(result_card, fg_color="transparent")
            to_section.pack(pady=(10, 20))
            
            ctk.CTkLabel(
                to_section,
                text=converted_str,
                font=("Segoe UI", 36, "bold"),
                text_color=COLORS['success']
            ).pack(side="left", padx=3)
            
            ctk.CTkLabel(
                to_section,
                text=to_curr,
                font=("Segoe UI", 22, "bold"),
                text_color=COLORS['success']
            ).pack(side="left", padx=3)
            
            # Exchange rate info
            if from_curr != to_curr:
                rate = self.current_rates.get(to_curr, 1) / self.current_rates.get(from_curr, 1)
                
                rate_info_frame = ctk.CTkFrame(
                    result_card, 
                    corner_radius=8,
                    fg_color=COLORS['background']
                )
                rate_info_frame.pack(pady=(20, 15), padx=20, fill="x")
                
                rate_text = f"1 {from_curr} = {rate:.6f} {to_curr}"
                rate_label = ctk.CTkLabel(
                    rate_info_frame,
                    text=rate_text,
                    font=("Segoe UI", 11),
                    text_color=COLORS['text_secondary']
                )
                rate_label.pack(pady=10)
            
            # Add popular rates at bottom
            self.show_compact_popular_rates(result_card)
            
        except (ValueError, ZeroDivisionError):
            # Show error for invalid input
            for widget in self.results_frame.winfo_children():
                widget.destroy()
            
            error_label = ctk.CTkLabel(
                self.results_frame,
                text="❌ Please enter a valid amount",
                font=("Arial", 14),
                text_color=("red", "#ff6b6b")
            )
            error_label.pack(pady=30)
    
    def show_compact_popular_rates(self, parent_card):
        """Show compact popular rates in the result card"""
        # Popular rates title
        rates_title = ctk.CTkLabel(
            parent_card,
            text="Popular Rates",
            font=("Segoe UI", 13, "bold"),
            text_color=COLORS['text_primary']
        )
        rates_title.pack(pady=(15, 10))
        
        # Get popular currencies (limited to 3 for compact view)
        if self.currency_api and CURRENCY_API_AVAILABLE:
            popular_rates = self.currency_api.get_popular_rates()
        else:
            popular_currencies = ["EUR", "GBP", "JPY"]
            popular_rates = {curr: self.current_rates.get(curr, 1) for curr in popular_currencies}
        
        # Display compact rates
        for curr, rate in list(popular_rates.items())[:3]:
            rate_item = ctk.CTkFrame(
                parent_card,
                fg_color=COLORS['background'],
                corner_radius=8
            )
            rate_item.pack(pady=3, padx=15, fill="x")
            
            # Format rate
            if rate >= 100:
                rate_str = f"{rate:.2f}"
            elif rate >= 1:
                rate_str = f"{rate:.4f}"
            else:
                rate_str = f"{rate:.6f}"
            
            rate_label = ctk.CTkLabel(
                rate_item,
                text=f"1 USD = {rate_str} {curr}",
                font=("Segoe UI", 10),
                text_color=COLORS['text_secondary']
            )
            rate_label.pack(pady=8, padx=10)
    
    def show_popular_rates(self):
        """Show popular exchange rates with Groww theme"""
        rates_title = ctk.CTkLabel(
            self.results_frame,
            text="Popular Exchange Rates",
            font=("Segoe UI", 16, "bold"),
            text_color=COLORS['text_primary']
        )
        rates_title.pack(pady=(25, 15))
        
        rates_container = ctk.CTkFrame(self.results_frame, fg_color="transparent")
        rates_container.pack(fill="x", padx=20)
        
        # Get popular currencies
        if self.currency_api and CURRENCY_API_AVAILABLE:
            popular_rates = self.currency_api.get_popular_rates()
        else:
            popular_currencies = ["EUR", "GBP", "JPY", "CAD", "AUD", "CHF"]
            popular_rates = {curr: self.current_rates.get(curr, 1) for curr in popular_currencies}
        
        # Display rates in a grid with Groww cards
        for i, (curr, rate) in enumerate(list(popular_rates.items())[:6]):
            row = i // 3
            col = i % 3
            
            # Create Groww-style rate card
            rate_card = ctk.CTkFrame(
                rates_container, 
                corner_radius=12,
                fg_color=COLORS['card_bg'],
                border_width=2,
                border_color=COLORS['border']
            )
            rate_card.grid(row=row, column=col, padx=8, pady=8, sticky="ew")
            
            # Currency pair label
            pair_label = ctk.CTkLabel(
                rate_card, 
                text=f"USD/{curr}", 
                font=("Segoe UI", 11),
                text_color=COLORS['text_secondary']
            )
            pair_label.pack(pady=(15, 5))
            
            # Format rate display
            if rate >= 100:
                rate_str = f"{rate:.2f}"
            elif rate >= 1:
                rate_str = f"{rate:.4f}"
            else:
                rate_str = f"{rate:.6f}"
            
            # Rate value with purple color
            rate_label = ctk.CTkLabel(
                rate_card, 
                text=rate_str, 
                font=("Segoe UI", 20, "bold"),
                text_color=COLORS['primary']
            )
            rate_label.pack(pady=5)
            
            # Currency name
            name_label = ctk.CTkLabel(
                rate_card, 
                text=self.currencies.get(curr, curr), 
                font=("Segoe UI", 9), 
                text_color=COLORS['text_secondary']
            )
            name_label.pack(pady=(0, 15))
        
        # Configure grid columns to be equal
        for i in range(3):
            rates_container.grid_columnconfigure(i, weight=1, uniform="rates")
        
        # Add refresh button
        refresh_btn = ctk.CTkButton(
            self.results_frame,
            text="🔄 Refresh Rates",
            command=self.refresh_rates,
            font=("Arial", 12),
            height=35,
            width=150
        )
        refresh_btn.pack(pady=15)
    
    def refresh_rates(self):
        """Refresh exchange rates"""
        self.status_label.configure(
            text="🔄 Refreshing exchange rates...",
            text_color=("gray", "lightgray")
        )
        self.load_exchange_rates()

class GUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Finsight - Enhanced Financial Hub")
        
        # Initialize news articles list for better refresh handling
        self.news_articles = []

        # centring the app
        self.centring_the_app()
        
        # Create navigation frame
        self.create_navigation()

        # Main content frame
        self.content_frame = ctk.CTkFrame(self.root)
        self.content_frame.pack(pady=(0, 10), padx=10, fill="both", expand=True)

        # Show dashboard by default
        self.show_dashboard()

        self.root.mainloop()
    
    def create_navigation(self):
        """Create navigation bar"""
        nav_frame = ctk.CTkFrame(self.root, height=60)
        nav_frame.pack(pady=10, padx=10, fill="x")
        nav_frame.pack_propagate(False)
        
        # App title
        title_label = ctk.CTkLabel(
            nav_frame,
            text="📊 Finsight",
            font=("Arial", 20, "bold"),
            text_color=("#1f538d", "#4a9eff")
        )
        title_label.pack(side="left", padx=20, pady=15)
        
        # Navigation buttons
        nav_buttons_frame = ctk.CTkFrame(nav_frame, fg_color="transparent")
        nav_buttons_frame.pack(side="right", padx=20, pady=10)
        
        self.dashboard_btn = ctk.CTkButton(
            nav_buttons_frame,
            text="🏠 Dashboard",
            command=self.show_dashboard,
            width=120,
            height=35
        )
        self.dashboard_btn.pack(side="left", padx=5)
        
        self.sip_btn = ctk.CTkButton(
            nav_buttons_frame,
            text="🧮 SIP Calculator",
            command=self.show_sip_calculator,
            width=120,
            height=35
        )
        self.sip_btn.pack(side="left", padx=5)
        
        self.currency_btn = ctk.CTkButton(
            nav_buttons_frame,
            text="💱 Currency",
            command=self.show_currency_converter,
            width=120,
            height=35
        )
        self.currency_btn.pack(side="left", padx=5)
    
    def clear_content(self):
        """Clear current content"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Show main dashboard"""
        self.clear_content()
        
        # Update button states
        self.dashboard_btn.configure(state="disabled")
        self.sip_btn.configure(state="normal")
        self.currency_btn.configure(state="normal")
        
        # Create scrollable main frame
        self.main_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            orientation="vertical",
            corner_radius=15
        )
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.greeting()
        self.create_stock_widgets()
        self.load_news()
    
    def show_sip_calculator(self):
        """Show SIP Calculator"""
        self.clear_content()
        
        # Update button states
        self.dashboard_btn.configure(state="normal")
        self.sip_btn.configure(state="disabled")
        self.currency_btn.configure(state="normal")
        
        # Create SIP calculator
        sip_calculator = SIPCalculator(self.content_frame)
        sip_calculator.pack(fill="both", expand=True, padx=10, pady=10)
    
    def show_currency_converter(self):
        """Show Currency Converter"""
        self.clear_content()
        
        # Update button states
        self.dashboard_btn.configure(state="normal")
        self.sip_btn.configure(state="normal")
        self.currency_btn.configure(state="disabled")
        
        # Create currency converter
        currency_converter = CurrencyConverter(self.content_frame)
        currency_converter.pack(fill="both", expand=True, padx=10, pady=10)

    def greeting(self):
        current_time = time.strftime("%H:%M")
        if current_time > "06:00" and current_time < "12:00":
            message = "Good Morning!"
        elif current_time > '12:00' and current_time < '19:00':
            message = "Good Afternoon"
        else:
            message = "Working Late?"
        
        label = ctk.CTkLabel(self.main_frame, text=message, font=("Times New Roman", 22))
        label.pack(pady=30)
        
        # Add Finsight subtitle
        subtitle = ctk.CTkLabel(
            self.main_frame, 
            text="Welcome to Finsight - Your Complete Financial Intelligence Hub 📊", 
            font=("Arial", 16),
            text_color=("#2563eb", "#3b82f6")
        )
        subtitle.pack(pady=(0, 20))

    def create_stock_widgets(self):
        """Create stock price widgets and market charts"""
        # Create main container for financial widgets
        financial_container = ctk.CTkFrame(self.main_frame, corner_radius=15)
        financial_container.pack(pady=20, padx=20, fill="x")
        
        # Title for financial section
        finance_title = ctk.CTkLabel(
            financial_container, 
            text="📈 Live Market Data & Charts", 
            font=("Arial", 18, "bold"),
            text_color=("#1f538d", "#4a9eff")
        )
        finance_title.pack(pady=(15, 10))
        
        # Create market summary
        self.create_market_summary(financial_container)
        
        # Create stock price widgets frame
        self.create_stock_price_widgets(financial_container)
        
        # Create market chart
        self.create_market_chart(financial_container)

    def create_market_summary(self, parent):
        """Create market summary with major indices"""
        summary_frame = ctk.CTkFrame(parent, corner_radius=10)
        summary_frame.pack(pady=10, padx=15, fill="x")
        
        summary_title = ctk.CTkLabel(
            summary_frame,
            text="🏛️ Market Indices",
            font=("Arial", 16, "bold")
        )
        summary_title.pack(pady=(10, 5))
        
        # Create indices grid
        indices_grid = ctk.CTkFrame(summary_frame, fg_color="transparent")
        indices_grid.pack(pady=10, padx=10, fill="x")
        
        # Major market indices
        indices = {
            "^GSPC": "S&P 500",
            "^DJI": "Dow Jones",
            "^IXIC": "NASDAQ"
        }
        
        self.index_widgets = {}
        for i, (symbol, name) in enumerate(indices.items()):
            # Create index widget
            index_widget = ctk.CTkFrame(indices_grid, corner_radius=8, width=240, height=70)
            index_widget.grid(row=0, column=i, padx=10, pady=5, sticky="ew")
            index_widget.grid_propagate(False)
            
            # Index name
            name_label = ctk.CTkLabel(
                index_widget,
                text=name,
                font=("Arial", 12, "bold")
            )
            name_label.pack(pady=(8, 2))
            
            # Index value
            value_label = ctk.CTkLabel(
                index_widget,
                text="Loading...",
                font=("Arial", 11)
            )
            value_label.pack()
            
            # Index change
            change_label = ctk.CTkLabel(
                index_widget,
                text="",
                font=("Arial", 10)
            )
            change_label.pack(pady=(0, 8))
            
            self.index_widgets[symbol] = {
                'value_label': value_label,
                'change_label': change_label
            }
        
        # Configure grid weights
        for i in range(3):
            indices_grid.grid_columnconfigure(i, weight=1)
        
        # Load index data
        threading.Thread(target=self.load_index_data, daemon=True).start()

    def load_index_data(self):
        """Load market indices data"""
        try:
            for symbol in self.index_widgets.keys():
                try:
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period="2d")
                    
                    if not hist.empty and len(hist) >= 2:
                        current_value = hist['Close'].iloc[-1]
                        prev_value = hist['Close'].iloc[-2]
                        change = current_value - prev_value
                        change_percent = (change / prev_value) * 100
                        
                        self.root.after(0, lambda s=symbol, v=current_value, c=change_percent:
                                       self.update_index_widget(s, v, c))
                        
                except Exception as e:
                    print(f"Error loading index {symbol}: {e}")
                    
        except Exception as e:
            print(f"Error in load_index_data: {e}")

    def update_index_widget(self, symbol, value, change_percent):
        """Update market index widget"""
        if symbol in self.index_widgets:
            widget_info = self.index_widgets[symbol]
            
            # Update value
            value_text = f"{value:.2f}" if isinstance(value, (int, float)) else str(value)
            widget_info['value_label'].configure(text=value_text)
            
            # Update change
            if isinstance(change_percent, (int, float)):
                change_text = f"{change_percent:+.2f}%"
                color = ("#16a34a", "#22c55e") if change_percent > 0 else ("#dc2626", "#ef4444")
                arrow = "▲" if change_percent > 0 else "▼"
                widget_info['change_label'].configure(
                    text=f"{arrow} {change_text}",
                    text_color=color
                )

    def create_stock_price_widgets(self, parent):
        """Create live stock price widgets"""
        # Stock widgets container
        stock_container = ctk.CTkFrame(parent, corner_radius=10)
        stock_container.pack(pady=10, padx=15, fill="x")
        
        stock_title = ctk.CTkLabel(
            stock_container,
            text="💰 Popular Stocks",
            font=("Arial", 16, "bold")
        )
        stock_title.pack(pady=(10, 5))
        
        # Create a frame for stock widgets grid
        stocks_grid = ctk.CTkFrame(stock_container, fg_color="transparent")
        stocks_grid.pack(pady=10, padx=10, fill="x")
        
        # Popular stocks to display
        popular_stocks = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "NVDA"]
        
        # Create stock widgets in a grid (3 columns, 2 rows)
        self.stock_widgets = {}
        for i, symbol in enumerate(popular_stocks):
            row = i // 3
            col = i % 3
            
            # Create individual stock widget
            stock_widget = ctk.CTkFrame(stocks_grid, corner_radius=8, width=220, height=80)
            stock_widget.grid(row=row, column=col, padx=8, pady=5, sticky="ew")
            stock_widget.grid_propagate(False)
            
            # Stock symbol
            symbol_label = ctk.CTkLabel(
                stock_widget,
                text=symbol,
                font=("Arial", 14, "bold"),
                text_color=("#1f538d", "#4a9eff")
            )
            symbol_label.pack(pady=(8, 2))
            
            # Price label (will be updated with real data)
            price_label = ctk.CTkLabel(
                stock_widget,
                text="Loading...",
                font=("Arial", 12)
            )
            price_label.pack()
            
            # Change label (will show percentage change)
            change_label = ctk.CTkLabel(
                stock_widget,
                text="",
                font=("Arial", 10)
            )
            change_label.pack(pady=(0, 8))
            
            self.stock_widgets[symbol] = {
                'price_label': price_label,
                'change_label': change_label,
                'widget': stock_widget
            }
        
        # Configure grid weights
        for i in range(3):
            stocks_grid.grid_columnconfigure(i, weight=1)
        
        # Load stock data in background
        threading.Thread(target=self.load_stock_data, daemon=True).start()
        
        # Add refresh button for stock data
        refresh_stocks_btn = ctk.CTkButton(
            stock_container,
            text="🔄 Refresh Stock Prices",
            command=self.refresh_stock_data,
            font=("Arial", 12),
            height=32,
            width=200
        )
        refresh_stocks_btn.pack(pady=(10, 15))

    def create_market_chart(self, parent):
        """Create market chart using matplotlib"""
        # Chart container
        chart_container = ctk.CTkFrame(parent, corner_radius=10)
        chart_container.pack(pady=15, padx=15, fill="both", expand=True)
        
        chart_title = ctk.CTkLabel(
            chart_container,
            text="📊 S&P 500 Chart (Last 30 Days)",
            font=("Arial", 16, "bold")
        )
        chart_title.pack(pady=(10, 5))
        
        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.fig.patch.set_facecolor('#212121' if ctk.get_appearance_mode() == "Dark" else '#f0f0f0')
        
        # Initial placeholder chart
        self.ax.plot([1, 2, 3, 4, 5], [1, 4, 2, 3, 5], color='#4a9eff', linewidth=2)
        self.ax.set_title('Loading S&P 500 Data...', color='white' if ctk.get_appearance_mode() == "Dark" else 'black')
        self.ax.set_facecolor('#2b2b2b' if ctk.get_appearance_mode() == "Dark" else 'white')
        
        # Embed chart in tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, chart_container)
        self.canvas.draw()
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Load chart data in background
        threading.Thread(target=self.load_chart_data, daemon=True).start()

    def load_stock_data(self):
        """Load real-time stock data"""
        try:
            for symbol in self.stock_widgets.keys():
                try:
                    # Get stock info
                    stock = yf.Ticker(symbol)
                    info = stock.info
                    hist = stock.history(period="2d")
                    
                    if not hist.empty and len(hist) >= 2:
                        current_price = hist['Close'].iloc[-1]
                        prev_price = hist['Close'].iloc[-2]
                        change = current_price - prev_price
                        change_percent = (change / prev_price) * 100
                        
                        # Update UI in main thread
                        self.root.after(0, lambda s=symbol, p=current_price, c=change_percent: 
                                       self.update_stock_widget(s, p, c))
                    else:
                        # Fallback to basic info
                        current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
                        if current_price:
                            self.root.after(0, lambda s=symbol, p=current_price: 
                                           self.update_stock_widget(s, p, 0))
                        
                except Exception as e:
                    print(f"Error loading {symbol}: {e}")
                    self.root.after(0, lambda s=symbol: self.update_stock_widget(s, "Error", 0))
                    
        except Exception as e:
            print(f"Error in load_stock_data: {e}")

    def update_stock_widget(self, symbol, price, change_percent):
        """Update individual stock widget with real data"""
        if symbol in self.stock_widgets:
            widget_info = self.stock_widgets[symbol]
            
            # Update price
            if isinstance(price, (int, float)):
                price_text = f"${price:.2f}"
                widget_info['price_label'].configure(text=price_text)
            else:
                widget_info['price_label'].configure(text=str(price))
            
            # Update change
            if isinstance(change_percent, (int, float)) and change_percent != 0:
                change_text = f"{change_percent:+.2f}%"
                color = ("#16a34a", "#22c55e") if change_percent > 0 else ("#dc2626", "#ef4444")
                arrow = "▲" if change_percent > 0 else "▼"
                widget_info['change_label'].configure(
                    text=f"{arrow} {change_text}",
                    text_color=color
                )
            else:
                widget_info['change_label'].configure(text="--")

    def load_chart_data(self):
        """Load S&P 500 chart data"""
        try:
            # Get S&P 500 data
            sp500 = yf.Ticker("^GSPC")
            hist = sp500.history(period="1mo")  # Last 30 days
            
            if not hist.empty:
                # Schedule chart update in main thread
                self.root.after(0, lambda: self.update_chart(hist))
            else:
                self.root.after(0, lambda: self.show_chart_error("No data available"))
                
        except Exception as e:
            self.root.after(0, lambda: self.show_chart_error(f"Error: {str(e)}"))

    def update_chart(self, data):
        """Update the market chart with real data"""
        try:
            # Clear previous plot
            self.ax.clear()
            
            # Set style based on appearance mode
            is_dark = ctk.get_appearance_mode() == "Dark"
            bg_color = '#2b2b2b' if is_dark else 'white'
            text_color = 'white' if is_dark else 'black'
            grid_color = '#404040' if is_dark else '#e0e0e0'
            
            self.ax.set_facecolor(bg_color)
            
            # Plot the closing prices
            dates = data.index
            closes = data['Close']
            
            # Create the line plot
            self.ax.plot(dates, closes, color='#4a9eff', linewidth=2.5, alpha=0.9)
            
            # Fill area under the curve
            self.ax.fill_between(dates, closes, alpha=0.2, color='#4a9eff')
            
            # Styling
            self.ax.set_title('S&P 500 Index - Last 30 Days', 
                            color=text_color, fontsize=14, fontweight='bold', pad=20)
            self.ax.set_xlabel('Date', color=text_color, fontsize=12)
            self.ax.set_ylabel('Price ($)', color=text_color, fontsize=12)
            
            # Grid
            self.ax.grid(True, alpha=0.3, color=grid_color)
            
            # Format axes
            self.ax.tick_params(colors=text_color, labelsize=10)
            
            # Format dates on x-axis
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
            self.ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
            
            # Rotate date labels
            plt.setp(self.ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
            
            # Add current price annotation
            current_price = closes.iloc[-1]
            self.ax.annotate(f'${current_price:.2f}', 
                           xy=(dates[-1], current_price),
                           xytext=(10, 10), textcoords='offset points',
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='#4a9eff', alpha=0.8),
                           color='white', fontweight='bold')
            
            # Tight layout
            self.fig.tight_layout()
            
            # Redraw canvas
            self.canvas.draw()
            
        except Exception as e:
            print(f"Error updating chart: {e}")
            self.show_chart_error(f"Chart update error: {str(e)}")

    def show_chart_error(self, error_msg):
        """Show error message on chart"""
        try:
            self.ax.clear()
            self.ax.text(0.5, 0.5, f"📊 Chart Error\n{error_msg}", 
                        transform=self.ax.transAxes, ha='center', va='center',
                        fontsize=12, color='red')
            self.ax.set_facecolor('#2b2b2b' if ctk.get_appearance_mode() == "Dark" else 'white')
            self.canvas.draw()
        except:
            pass

    def load_news(self):
        """Load financial news articles in a separate thread"""
        # Show loading message
        self.loading_label = ctk.CTkLabel(
            self.main_frame, 
            text="📈 Loading latest financial news & market updates...", 
            font=("Arial", 16),
            text_color=("#1f538d", "#4a9eff")
        )
        self.loading_label.pack(pady=15)
        
        # Fetch news in background thread to prevent UI freezing
        threading.Thread(target=self.fetch_and_display_news, daemon=True).start()

    def fetch_and_display_news(self):
        """Fetch financial/stock news from API and display in UI"""
        try:
            # Using MarketWatch RSS feed (verified working)
            marketwatch_url = "https://api.rss2json.com/v1/api.json?rss_url=https://feeds.marketwatch.com/marketwatch/realtimeheadlines/"
            
            response = requests.get(marketwatch_url, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'ok':
                    # Schedule UI update in main thread
                    self.root.after(0, lambda: self.display_financial_news(data))
                else:
                    self.root.after(0, lambda: self.show_error("Failed to retrieve financial news data"))
            else:
                self.root.after(0, lambda: self.show_error(f"API returned status code: {response.status_code}"))
                
        except requests.exceptions.Timeout:
            self.root.after(0, lambda: self.show_error("Request timed out. Please check your internet connection."))
        except requests.exceptions.ConnectionError:
            self.root.after(0, lambda: self.show_error("Connection error. Please check your internet connection."))
        except Exception as e:
            self.root.after(0, lambda: self.show_error(f"Error fetching financial news: {str(e)}"))

    def display_financial_news(self, data):
        """Display financial news articles in the UI"""
        # Remove loading message
        if hasattr(self, 'loading_label'):
            self.loading_label.destroy()
        
        # Add financial news header
        news_header = ctk.CTkLabel(
            self.main_frame, 
            text="📰 Latest Financial News & Market Updates", 
            font=("Arial", 20, "bold"),
            text_color=("#1f538d", "#4a9eff")
        )
        news_header.pack(pady=(20, 10))
        self.news_articles.append(news_header)
        
        # Display news articles
        articles = data.get('items', [])[:8]  # Show top 8 financial articles
        
        for i, article in enumerate(articles):
            # Create frame for each article with financial styling
            article_frame = ctk.CTkFrame(
                self.main_frame, 
                corner_radius=12,
                border_width=1,
                border_color=("#d4d4d8", "#3f3f46")
            )
            article_frame.pack(pady=8, padx=15, fill="x")
            self.news_articles.append(article_frame)
            
            # Article title
            title = article.get('title', 'No title')
            # Clean up title
            if len(title) > 100:
                title = title[:100] + "..."
                
            title_label = ctk.CTkLabel(
                article_frame, 
                text=title, 
                font=("Arial", 15, "bold"),
                wraplength=720,
                justify="left",
                text_color=("#1a1a1a", "#ffffff")
            )
            title_label.pack(pady=(15, 8), padx=15, anchor="w")
            
            # Article description/content
            description = article.get('description', '') or article.get('content', '')
            if not description:
                description = "Click to read full article..."
            
            # Clean up description (remove HTML tags)
            description = re.sub(r'<[^>]+>', '', description)
            if len(description) > 200:
                description = description[:200] + "..."
                
            desc_label = ctk.CTkLabel(
                article_frame, 
                text=description, 
                font=("Arial", 13),
                wraplength=720,
                justify="left",
                text_color=("#4a5568", "#a0aec0")
            )
            desc_label.pack(pady=(0, 8), padx=15, anchor="w")
            
            # Create a frame for metadata (date, source, link)
            meta_frame = ctk.CTkFrame(article_frame, fg_color="transparent")
            meta_frame.pack(fill="x", padx=15, pady=(0, 15))
            
            # Publication date
            pub_date = article.get('pubDate', '')
            if pub_date:
                try:
                    # Handle different date formats
                    if 'T' in pub_date:
                        date_obj = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
                    else:
                        date_obj = datetime.strptime(pub_date[:19], "%Y-%m-%d %H:%M:%S")
                    
                    formatted_date = date_obj.strftime("%b %d, %Y • %I:%M %p")
                except:
                    formatted_date = pub_date[:16] if len(pub_date) > 16 else pub_date
                    
                date_label = ctk.CTkLabel(
                    meta_frame,
                    text=f"🕒 {formatted_date}",
                    font=("Arial", 11),
                    text_color=("#718096", "#a0aec0")
                )
                date_label.pack(side="left", pady=2)
            
            # Source information
            source = article.get('author', 'Financial News')
            if source:
                source_label = ctk.CTkLabel(
                    meta_frame,
                    text=f"📰 {source}",
                    font=("Arial", 11),
                    text_color=("#718096", "#a0aec0")
                )
                source_label.pack(side="right", pady=2)

        # Add refresh button
        self.news_refresh_button = ctk.CTkButton(
            self.main_frame,
            text="🔄 Refresh Financial News",
            command=self.refresh_news,
            font=("Arial", 14, "bold"),
            height=40,
            corner_radius=20
        )
        self.news_refresh_button.pack(pady=20)
        self.news_articles.append(self.news_refresh_button)

    def refresh_news(self):
        """Refresh the financial news"""
        # Remove existing news articles only
        for article_widget in self.news_articles:
            try:
                article_widget.destroy()
            except:
                pass
        
        self.news_articles.clear()
        
        # Reload news
        self.load_news()

    def refresh_stock_data(self):
        """Refresh all stock and index data"""
        # Update stock widgets to show loading
        if hasattr(self, 'stock_widgets'):
            for symbol, widget_info in self.stock_widgets.items():
                widget_info['price_label'].configure(text="Updating...")
                widget_info['change_label'].configure(text="")
        
        # Update index widgets to show loading  
        if hasattr(self, 'index_widgets'):
            for symbol, widget_info in self.index_widgets.items():
                widget_info['value_label'].configure(text="Updating...")
                widget_info['change_label'].configure(text="")
        
        # Reload data in background
        threading.Thread(target=self.load_stock_data, daemon=True).start()
        threading.Thread(target=self.load_index_data, daemon=True).start()
        threading.Thread(target=self.load_chart_data, daemon=True).start()

    def show_error(self, error_message):
        """Display error message for financial news"""
        # Remove loading message if exists
        if hasattr(self, 'loading_label'):
            self.loading_label.destroy()
            
        error_label = ctk.CTkLabel(
            self.main_frame, 
            text=f"❌ {error_message}\n\n💡 Please check your internet connection and try again.", 
            font=("Arial", 14),
            text_color=("red", "#ff6b6b"),
            justify="center"
        )
        error_label.pack(pady=20)
        self.news_articles.append(error_label)
        
        # Add retry button
        retry_button = ctk.CTkButton(
            self.main_frame,
            text="🔄 Retry Loading Financial News",
            command=self.retry_load_news,
            font=("Arial", 12),
            height=35
        )
        retry_button.pack(pady=10)
        self.news_articles.append(retry_button)
    
    def retry_load_news(self):
        """Retry loading financial news"""
        # Remove existing news articles
        for article_widget in self.news_articles:
            try:
                article_widget.destroy()
            except:
                pass
        
        self.news_articles.clear()
        
        # Reload news
        self.load_news()

    def centring_the_app(self):
        width = 1000
        height = 700

        # get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    GUI()