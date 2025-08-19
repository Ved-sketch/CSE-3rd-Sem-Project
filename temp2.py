import time
import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class GUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Finsight")

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
        self.create_news_items()
        self.root.mainloop()

    def hide_scrollbar(self):
        """Hide the scrollbar"""
        self.main_frame._scrollbar.pack_forget()

    def show_scrollbar(self):
        """Show the scrollbar"""
        self.main_frame._scrollbar.pack(side="right", fill="y")

    def bind_hover_events(self):
        """Bind mouse enter/leave events"""
        # Show scrollbar when hovering over the frame
        self.main_frame.bind("<Enter>", self.on_frame_enter)
        self.main_frame.bind("<Leave>", self.on_frame_leave)

        # Also bind to the scrollbar itself
        self.main_frame._scrollbar.bind("<Enter>", self.on_scrollbar_enter)
        self.main_frame._scrollbar.bind("<Leave>", self.on_scrollbar_leave)

    def on_frame_enter(self, event):
        """Show scrollbar when mouse enters frame"""
        self.show_scrollbar()

    def on_frame_leave(self, event):
        """Hide scrollbar when mouse leaves frame"""
        # Add small delay to prevent flickering
        self.root.after(100, self.check_and_hide_scrollbar)

    def on_scrollbar_enter(self, event):
        """Keep scrollbar visible when hovering over it"""
        pass  # Scrollbar stays visible

    def on_scrollbar_leave(self, event):
        """Hide scrollbar when leaving scrollbar area"""
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

    def create_news_items(self):
        # Sample news items
        news_items = [

            "Market Rally Continues",
            "Tech Giants Report Earnings",
            "Economic Indicators Strong",
            "Cryptocurrency Update",
            "Banking Sector News",
            "Federal Reserve Updates",
            "Global Trade Analysis",
            "Investment Opportunities",
            "Risk Assessment Report",
            "Economic Forecast 2024",
            "Stock Market Volatility",
            "Bond Market Trends",
            "Commodity Price Changes",
            "Currency Exchange Rates",
            "Real Estate Market Update",
            "Energy Sector Analysis",
            "Healthcare Investment News",
            "Technology Stocks Surge",
            "Emerging Markets Report",
            "Financial Regulation Updates",
            "Pension Fund Performance",
            "Insurance Industry News",
            "Startup Funding Rounds",
            "Merger & Acquisition Activity",
            "Corporate Earnings Preview"
        ]

        for item in news_items:
            news_button = ctk.CTkButton(
                self.main_frame,
                text=item,
                height=40,
                font=("Arial", 14),
                command=lambda x=item: self.show_news(x)
            )
            news_button.pack(pady=5, padx=20, fill="x")

    def show_news(self, news_title):
        print(f"Clicked: {news_title}")  # Replace with your news detail logic

    def centring_the_app(self):
        width = 900
        height = 700

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")


GUI()