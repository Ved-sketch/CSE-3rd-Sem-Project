<<<<<<< HEAD
label.grid(row=0, column=0, sticky="ew", pady=40)
=======
def __init__(self, parent, headline, summary, url, source):
        super().__init__(parent, corner_radius=12, fg_color=("white", "gray20"))
        # Headline
        self.headline_label = ctk.CTkLabel(self, text=headline, font=("Arial", 18, "bold"), wraplength=700, anchor="w")
        self.headline_label.pack(anchor="w", padx=16, pady=(10, 2))
        # Summary
        self.summary_label = ctk.CTkLabel(self, text=summary, font=("Arial", 13), wraplength=700, anchor="w")
        self.summary_label.pack(anchor="w", padx=16, pady=(0, 6))
        # URL (clickable)
        self.url_label = ctk.CTkLabel(self, text="Read more", text_color="blue", cursor="hand2", font=("Arial", 12, "underline"))
        self.url_label.pack(anchor="w", padx=16, pady=(0, 8))
        self.url_label.bind("<Button-1>", lambda e: webbrowser.open(url))
        # Source (bottom right)
        self.source_label = ctk.CTkLabel(self, text=f"Source: {source}", font=("Arial", 10, "italic"), text_color="gray")
        self.source_label.pack(anchor="e", padx=16, pady=(0, 8))
>>>>>>> 621a76b (Initial commit)
