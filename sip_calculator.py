"""
SIP Calculator Module
Author: Parth Hada
Description: Systematic Investment Plan Calculator with visualization
"""

import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Import colors from main config
from config import COLORS


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
