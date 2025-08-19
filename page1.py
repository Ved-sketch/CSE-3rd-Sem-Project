import time
import requests
import webbrowser
import customtkinter as ctk
import subprocess
import sys
import os

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
ctk.set_window_scaling(1.0)
ctk.set_widget_scaling(2.5)

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

        # Show scrollbar when hovering over the frame
        self.main_frame.bind("<Enter>", self.on_frame_enter)
        self.main_frame.bind("<Leave>", self.on_frame_leave)

        # Also bind to the scrollbar itself
        self.main_frame._scrollbar.bind("<Enter>", self.on_scrollbar_enter)
        self.main_frame._scrollbar.bind("<Leave>", self.on_scrollbar_leave)

    def on_frame_enter(self, event):
        self.show_scrollbar()

    def on_frame_leave(self, event):

        # Add small delay to prevent flickering
        self.root.after(100, self.check_and_hide_scrollbar)

    def on_scrollbar_enter(self, event):
        pass  # Scrollbar stays visible

    def on_scrollbar_leave(self, event):

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
        

    def centring_the_app(self):

        width = 800
        height = 600

        # get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")

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