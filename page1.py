import time
import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
ctk.set_window_scaling(1.0)
ctk.set_widget_scaling(2.5)

class GUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Finsight")

        # centring the app
        self.centring_the_app()


        # Main Frame
        self.main_frame = ctk.CTkScrollableFrame(
            self.root,
            orientation="vertical",
            width = 800,
            height = 300,
            corner_radius=15
        )
        self.main_frame.pack(pady=5,padx=5)

        self.greeting()
        
        self.root.mainloop()

    def greeting(self):
        current_time = time.strftime("%H:%M")
        if current_time > "6" and current_time < "12":
            message = "Good Morning!"
        elif current_time > '12' and current_time < '19':
            message = "Good Afternoon"
        else:
            message = "Working Late?"
        
        label = ctk.CTkLabel(self.main_frame, text=message, font=("Times New Roman", 22))
        label.pack(pady=40)
        

    def centring_the_app(self):

        width = 800
        height = 600

        # get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")

        

GUI()