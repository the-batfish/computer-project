import tkinter
from tkinter import ttk, font
from PIL import ImageTk, Image


class App(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configuring Root  Window
        self.title("Crypto Stonks")
        self.minsize(500, 500)
        self.pic = ImageTk.PhotoImage(Image.open("stonks.png"))
        self.iconphoto(True, self.pic)

        # Styling
        # Fonts
        self.font_login_L = font.Font(family="Monaco", size=14)
        self.font_big_B = font.Font(family="Avenir Next", size=30)
        # Create Account Button font
        self.font_small_B = font.Font(
            family="TkDefaultFont", size=8, slant="italic")
        self.font_error_L = font.Font(
            family="TkDefaultFont", size=8, slant="italic")

        # Styles
        # Username and Password Labels
        login_LabelStyle = ttk.Style()
        login_LabelStyle.configure("login.TLabel", font=self.font_login_L)
        # Log In Button
        big_ButtonStyle = ttk.Style()
        big_ButtonStyle.configure("big.TButton", font=self.font_big_B)
        # Create Account Button
        small_ButtonStyle = ttk.Style()
        small_ButtonStyle.configure("small.TButton", font=self.font_small_B)
        # Error Label
        error_LabelStyle = ttk.Style()
        error_LabelStyle.configure(
            "error.TLabel", font=self.font_error_L, foreground="red")

        # Placing Frames in Root Window
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}

        for F in (LogInPage, RegisterPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="NSEW")

        self.show_frame(LogInPage)

    # To display the current frame passed as parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    # Dynamically Resize Widget Text
    def resize(self, event):
        x = event.widget.winfo_height() if event.widget.winfo_height(
        ) > event.widget.winfo_width() else event.widget.winfo_width()
        self.font_login_L["size"] = x//49
        self.font_big_B["size"] = x//25
        self.font_small_B["size"] = x//81
        self.font_error_L["size"] = x//81

class HomePage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Configuring Rows and Columns
        for i in range(1,3):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(i, weight=1)
        self.rowconfigure(3, weight=1)

class LogInPage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)

        # Configuring Rows and Columns
        for i in range(1, 10, 8):
            self.rowconfigure(i, weight=9)
        for i in range(2, 9):
            self.rowconfigure(i, weight=1)
        for i in range(6):
            self.columnconfigure(i, weight=1)

        # Make Widget Text Resizable
        self.bind("<Configure>", self.resize)

        # Styling
        # Fonts
        # Username and Password Entry font
        self.font_login_E = font.Font(family="Avenir Next Condensed", size=14)

        # Poplating Frame
        # Entry and error Lable values
        self.username = tkinter.StringVar()
        self.password = tkinter.StringVar()
        self.error_msg = tkinter.StringVar()
        self.error_msg.set("Test")

        # Label And Entry
        # Username Label
        user_label = ttk.Label(self, text="Username",
                               style="login.TLabel", anchor="w")
        user_label.grid(row=2, column=2, sticky="SEW", columnspan=2)
        # Username Entry
        user_entry = ttk.Entry(
            self, textvariable=self.username, font=self.font_login_E)
        user_entry.grid(row=3, column=2, sticky="NEW", columnspan=2)
        # Password Label
        pass_label = ttk.Label(self, text="Password",
                               style="login.TLabel", anchor="w")
        pass_label.grid(row=4, column=2, sticky="SEW", columnspan=2)
        # Password Entry
        pass_entry = ttk.Entry(
            self, textvariable=self.password, show="*", font=self.font_login_E)
        pass_entry.grid(row=5, column=2, sticky="NEW", columnspan=2)
        # Error Label
        error_label = ttk.Label(
            self, textvariable=self.error_msg, text="Remember me", style="error.TLabel")
        error_label.grid(row=6, column=3, sticky="SE")

        # Buttons
        # Create Account Button
        crAcc_button = ttk.Button(self, text="Create Account?", style="small.TButton",
                                  command=lambda: controller.show_frame(RegisterPage))
        crAcc_button.grid(row=7, column=2, sticky="SEW", columnspan=2)
        # Log In Button
        logIn_button = ttk.Button(self, text="LOG IN", style="big.TButton")
        logIn_button.grid(row=8, column=2, sticky="NSEW", columnspan=2)

    # Dynamically resize font

    def resize(self, event):
        # Dynamically resize entry since ttk.Entry does not accept Styles
        x = event.height if event.height > event.width else event.width
        self.font_login_E["size"] = x//49
        app.resize(event)  # Dynamically resize fonts using Style


class RegisterPage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)

        # Configuring Rows and Columns
        for i in range(1, 10):
            self.rowconfigure(i, weight=1)
        for i in range(1, 11, 9):
            self.rowconfigure(i, weight=4)
        for i in range(1, 8):
            self.columnconfigure(i, weight=1)
        for i in range(1, 8, 6):
            self.columnconfigure(i, weight=4)

        # Make Widget Text Resizable
        self.bind("<Configure>", self.resize)

        # Styling
        # Fonts
        self.font_login_E = font.Font(family="Avenir Next Condensed", size=14)

        # Poplating Frame
        # Entry and error Label values
        self.username = tkinter.StringVar()
        self.password = tkinter.StringVar()
        self.confirm_pass = tkinter.StringVar()
        self.error_msg = tkinter.StringVar()
        

        # Label And Entry
        # Username Label
        user_label = ttk.Label(self, text="Enter Username",
                               style="login.TLabel", anchor="w")
        user_label.grid(row=4, column=3, sticky="EW", columnspan=1)
        # Username Entry
        user_entry = ttk.Entry(
            self, textvariable=self.username, font=self.font_login_E)
        user_entry.grid(row=4, column=5, sticky="EW", columnspan=1)
        # Password Label
        pass_label = ttk.Label(self, text="Enter Password",
                               style="login.TLabel", anchor="w")
        pass_label.grid(row=5, column=3, sticky="EW", columnspan=1)
        # Password Entry
        pass_entry = ttk.Entry(
            self, textvariable=self.password, show="*", font=self.font_login_E)
        pass_entry.grid(row=5, column=5, sticky="EW", columnspan=1)
        # Password Label
        confirmPass_label = ttk.Label(
            self, text="Confirm Password", style="login.TLabel", anchor="w")
        confirmPass_label.grid(row=6, column=3, sticky="EW", columnspan=1)
        # Password Entry
        confirmPass_entry = ttk.Entry(
            self, textvariable=self.confirm_pass, show="*", font=self.font_login_E)
        confirmPass_entry.grid(row=6, column=5, sticky="EW", columnspan=1)
        # Error Label
        error_label = ttk.Label(
            self, textvariable=self.error_msg, text="Remember me", style="error.TLabel")
        error_label.grid(row=7, column=5, sticky="NE")

        # Divider
        for i in range(4, 7):
            ttk.Label(self, text=":", style="login.TLabel",
                      anchor="w").grid(row=i, column=4, sticky="NSW")

        # Buttons
        # Back to Log In Button
        # Back to Log In Button use same font as Create Account Button from LogInPage
        backToLogIn_button = ttk.Button(self, text="Back To Log In?", style="small.TButton",
                                        command=lambda: controller.show_frame(LogInPage))
        backToLogIn_button.grid(row=7, column=3, sticky="SEW", columnspan=3)
        # Create Account Button
        # Create Account Button use same font as Log In Button from LogInPage
        crAcc_button = ttk.Button(
            self, text="CREATE ACCOUNT", style="big.TButton")
        crAcc_button.grid(row=8, column=3, columnspan=3, sticky="NSEW")

    # Dynamically resize font
    def resize(self, event):
        # Dynamically resize entry since ttk.Entry does not accept Styles
        x = event.height if event.height > event.width else event.width
        self.font_login_E["size"] = x//49
        app.resize(event)  # Dynamically resize fonts using Style


# Starting Gui
app = App()
app.mainloop()
    