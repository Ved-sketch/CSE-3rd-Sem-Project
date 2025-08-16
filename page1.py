import time
import customtkinter

class GUI:
    def __init__(self):
        self.root = customtkinter.CTk()
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("blue")

        # centring the app
        self.centring_the_app()

        # Main Frame
        main_frame = customtkinter.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True)

        # Canvas and Scrollbar (customtkinter)
        self.canvas = customtkinter.CTkCanvas(main_frame, bg="black", highlightthickness=0)
        scrollbar = customtkinter.CTkScrollbar(main_frame, orientation="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Inner frame inside the canvas (customtkinter)
        self.inner_frame = customtkinter.CTkFrame(self.canvas, fg_color="black")
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Update scrollregion when widgets are added
        self.inner_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.greeting()
        
        self.root.mainloop()

    def greeting(self):
        current_time = time.strftime("%H:%M")
        if(current_time > "6" and current_time < "12"):
            message = "Good Morning!"
        elif(current_time > '12' and current_time < '19'):
            message = "Good Afternoon"
        else:
            message = "Working Late?"

        label = customtkinter.CTkLabel(self.inner_frame, text = message, font=("Times New Roman",16))
        label.pack(pady=20)

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