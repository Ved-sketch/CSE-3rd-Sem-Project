import time
<<<<<<< HEAD
import customtkinter as ctk
=======
import requests
import webbrowser
import customtkinter as ctk
import subprocess
import sys
import os
import yfinance as yf
import threading
import pandas as pd
>>>>>>> 621a76b (Initial commit)

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
ctk.set_window_scaling(1.0)
ctk.set_widget_scaling(2.5)

<<<<<<< HEAD
=======
class StockWidget(ctk.CTkFrame):
    def __init__(self, parent, symbol):
        super().__init__(parent, corner_radius=10, fg_color=("white", "gray20"), width=140, height=80)
        self.symbol = symbol
        
        # Stock symbol
        self.symbol_label = ctk.CTkLabel(
            self, text=symbol, font=("Arial", 14, "bold"),
            text_color=("#1f538d", "#4a9eff")
        )
        self.symbol_label.pack(pady=(8, 2))
        
        # Price
        self.price_label = ctk.CTkLabel(
            self, text="Loading...", font=("Arial", 12)
        )
        self.price_label.pack()
        
        # Change
        self.change_label = ctk.CTkLabel(
            self, text="", font=("Arial", 10)
        )
        self.change_label.pack(pady=(0, 8))
        
        # Load data
        threading.Thread(target=self.load_data, daemon=True).start()
    
    def load_data(self):
        try:
            stock = yf.Ticker(self.symbol)
            hist = stock.history(period="2d")
            
            if not hist.empty and len(hist) >= 2:
                current_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[-2]
                change = current_price - prev_price
                change_percent = (change / prev_price) * 100
                
                # Update UI in main thread
                self.after(0, lambda: self.update_display(current_price, change_percent))
            else:
                self.after(0, lambda: self.update_display("N/A", 0))
                
        except Exception as e:
            print(f"Error loading {self.symbol}: {e}")
            self.after(0, lambda: self.update_display("Error", 0))
    
    def update_display(self, price, change_percent):
        # Update price
        if isinstance(price, (int, float)):
            self.price_label.configure(text=f"${price:.2f}")
        else:
            self.price_label.configure(text=str(price))
        
        # Update change
        if isinstance(change_percent, (int, float)) and change_percent != 0:
            change_text = f"{change_percent:+.2f}%"
            color = ("#16a34a", "#22c55e") if change_percent > 0 else ("#dc2626", "#ef4444")
            arrow = "▲" if change_percent > 0 else "▼"
            self.change_label.configure(
                text=f"{arrow} {change_text}",
                text_color=color
            )
        else:
            self.change_label.configure(text="--")

class NewsItem(ctk.CTkFrame):
    def __init__(self, parent, headline, summary, url, source):
        super().__init__(parent, corner_radius=12, fg_color=("white", "gray20"), width=440)
        # Headline
        self.headline_label = ctk.CTkLabel(
            self, text=headline, font=("Arial", 18, "bold"),
            wraplength=400, anchor="w", justify="left"
        )
        self.headline_label.pack(anchor="w", padx=16, pady=(18, 2))
        # Summary
        self.summary_label = ctk.CTkLabel(
            self, text=summary, font=("Arial", 13),
            wraplength=400, anchor="w", justify="left"
        )
        self.summary_label.pack(anchor="w", padx=16, pady=(0, 6))
        # URL (clickable)
        self.url_label = ctk.CTkLabel(
            self, text="Read more", text_color="blue", cursor="hand2",
            font=("Arial", 12, "underline")
        )
        self.url_label.pack(anchor="w", padx=16, pady=(0, 8))
        self.url_label.bind("<Button-1>", lambda e: webbrowser.open(url))
        # Source (bottom right)
        self.source_label = ctk.CTkLabel(
            self, text=f"Source: {source}", font=("Arial", 10, "italic"),
            text_color="gray"
        )
        self.source_label.pack(anchor="e", padx=16, pady=(0, 8))

>>>>>>> 621a76b (Initial commit)
class GUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Finsight")

        # centring the app
        self.centring_the_app()

        # Main scrollable frame with thin scrollbar
        self.main_frame = ctk.CTkScrollableFrame(
            self.root,
            orientation="vertical",
            width=800,
            height=500,
            corner_radius=15,
            scrollbar_button_color=("gray70", "gray30"),
            scrollbar_button_hover_color=("gray60", "gray40")
        )
        self.main_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Resize and initially hide the scrollbar
        self.main_frame._scrollbar.configure(width=8)
        self.hide_scrollbar()

        # Bind hover events
        self.bind_hover_events()

        self.greeting()
<<<<<<< HEAD

        self.root.mainloop()

    def hide_scrollbar(self):
        """Hide the scrollbar"""
        self.main_frame._scrollbar.pack_forget()

    def show_scrollbar(self):
        """Show the scrollbar"""
        self.main_frame._scrollbar.pack(side="right", fill="y")

    def bind_hover_events(self):
        """Bind mouse enter/leave events"""
=======
        
        self.display_top_stocks()

        self.display_news()

        self.root.mainloop()
    
    def display_news(self):
        try:
            response = requests.get("http://127.0.0.1:5000/news")
            if response.status_code == 200:
                news_list = response.json()
                for news in news_list:
                    headline = news.get("headline", "No Headline")
                    summary = news.get("summary", "No Summary")
                    url = news.get("url", "#")
                    source = news.get("source", "Unknown")
                    item = NewsItem(self.main_frame, headline, summary, url, source)
                    item.pack(pady=8, padx=10)
            else:
                error_label = ctk.CTkLabel(self.main_frame, text="Failed to fetch news.", font=("Arial", 14))
                error_label.pack(pady=20)
        except Exception as e:
            error_label = ctk.CTkLabel(self.main_frame, text=f"Error: {e}", font=("Arial", 14))
            error_label.pack(pady=20)

    def hide_scrollbar(self):
        self.main_frame._scrollbar.pack_forget()

    def show_scrollbar(self):
        self.main_frame._scrollbar.pack(side="right", fill="y")

    def bind_hover_events(self):

>>>>>>> 621a76b (Initial commit)
        # Show scrollbar when hovering over the frame
        self.main_frame.bind("<Enter>", self.on_frame_enter)
        self.main_frame.bind("<Leave>", self.on_frame_leave)

        # Also bind to the scrollbar itself
        self.main_frame._scrollbar.bind("<Enter>", self.on_scrollbar_enter)
        self.main_frame._scrollbar.bind("<Leave>", self.on_scrollbar_leave)

    def on_frame_enter(self, event):
<<<<<<< HEAD
        """Show scrollbar when mouse enters frame"""
        self.show_scrollbar()

    def on_frame_leave(self, event):
        """Hide scrollbar when mouse leaves frame"""
=======
        self.show_scrollbar()

    def on_frame_leave(self, event):

>>>>>>> 621a76b (Initial commit)
        # Add small delay to prevent flickering
        self.root.after(100, self.check_and_hide_scrollbar)

    def on_scrollbar_enter(self, event):
<<<<<<< HEAD
        """Keep scrollbar visible when hovering over it"""
        pass  # Scrollbar stays visible

    def on_scrollbar_leave(self, event):
        """Hide scrollbar when leaving scrollbar area"""
=======
        pass  # Scrollbar stays visible

    def on_scrollbar_leave(self, event):

>>>>>>> 621a76b (Initial commit)
        self.root.after(100, self.check_and_hide_scrollbar)

    def check_and_hide_scrollbar(self):
        """Check if mouse is still in frame area before hiding"""
        try:
            # Get mouse position relative to the frame
            x = self.main_frame.winfo_pointerx() - self.main_frame.winfo_rootx()
            y = self.main_frame.winfo_pointery() - self.main_frame.winfo_rooty()

            # Check if mouse is outside frame boundaries
            if (x < 0 or x > self.main_frame.winfo_width() or
                    y < 0 or y > self.main_frame.winfo_height()):
                self.hide_scrollbar()
        except:
            self.hide_scrollbar()


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
<<<<<<< HEAD
=======

    def display_top_stocks(self):
        """Display top 5 current stocks at the top"""
        # Title
        stocks_title = ctk.CTkLabel(
            self.main_frame, 
            text="📊 Top 5 Stocks", 
            font=("Arial", 20, "bold"),
            text_color=("#1f538d", "#4a9eff")
        )
        stocks_title.pack(pady=(10, 15))
        
        # Container for stocks
        stocks_container = ctk.CTkFrame(self.main_frame, corner_radius=15, fg_color="transparent")
        stocks_container.pack(pady=10, padx=20, fill="x")
        
        # Top 5 popular stocks
        top_stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
        
        # Create horizontal layout for stocks
        stocks_frame = ctk.CTkFrame(stocks_container, fg_color="transparent")
        stocks_frame.pack(fill="x", pady=10)
        
        for i, symbol in enumerate(top_stocks):
            stock_widget = StockWidget(stocks_frame, symbol)
            stock_widget.grid(row=0, column=i, padx=8, pady=5, sticky="ew")
        
        # Configure grid weights for responsive layout
        for i in range(len(top_stocks)):
            stocks_frame.grid_columnconfigure(i, weight=1)
        
        # Add refresh button
        refresh_btn = ctk.CTkButton(
            stocks_container,
            text="🔄 Refresh Stocks",
            command=self.refresh_stocks,
            font=("Arial", 12),
            height=32,
            width=150
        )
        refresh_btn.pack(pady=15)
        
        # Store reference for refresh
        self.stocks_frame = stocks_frame

    def refresh_stocks(self):
        """Refresh stock data"""
        for widget in self.stocks_frame.winfo_children():
            if isinstance(widget, StockWidget):
                widget.price_label.configure(text="Loading...")
                widget.change_label.configure(text="")
                # Reload data
                threading.Thread(target=widget.load_data, daemon=True).start()
>>>>>>> 621a76b (Initial commit)
        

    def centring_the_app(self):

        width = 800
        height = 600

        # get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")

<<<<<<< HEAD
        

GUI()
=======
if __name__ == "__main__":
    # Start the Flask server as a subprocess
    server_process = subprocess.Popen(
        [sys.executable, os.path.join(os.path.dirname(__file__), "app.py")],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    try:
        GUI()
    finally:
        # Terminate the server when GUI closes
        server_process.terminate()

# GUI()
>>>>>>> 621a76b (Initial commit)
