"""
Currency Converter Module
Author: Prince Sharma
Description: Real-time currency converter with live exchange rates
"""

import customtkinter as ctk
import threading

# Import colors from main config
from config import COLORS

# Import currency API
try:
    from currency_api import CurrencyAPI
    CURRENCY_API_AVAILABLE = True
except ImportError:
    CURRENCY_API_AVAILABLE = False
    print("Currency API not available, using fallback rates")


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
    
    def refresh_rates(self):
        """Refresh exchange rates"""
        self.status_label.configure(
            text="🔄 Refreshing exchange rates...",
            text_color=COLORS['text_secondary']
        )
        self.load_exchange_rates()
