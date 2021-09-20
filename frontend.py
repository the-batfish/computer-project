import tkinter
from tkinter import font, messagebox, ttk

from PIL import Image, ImageOps, ImageTk

import backend


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
        self.font_small_B = font.Font(family="TkDefaultFont", size=8, slant="italic")
        self.font_error_L = font.Font(family="TkDefaultFont", size=8, slant="italic")

        # Styles
        # Error Label
        error_LabelStyle = ttk.Style()
        error_LabelStyle.configure("small.TLabel", font=self.font_error_L)
        # Username and Password Labels
        login_LabelStyle = ttk.Style()
        login_LabelStyle.configure("big.TLabel", font=self.font_login_L)
        # CheckButtons
        CheckButtonStyle = ttk.Style()
        CheckButtonStyle.configure("small.TCheckbutton", font=self.font_small_B)
        # Big Button
        big_ButtonStyle = ttk.Style()
        big_ButtonStyle.configure("big.TButton", font=self.font_big_B)
        # Small Account Button
        small_ButtonStyle = ttk.Style()
        small_ButtonStyle.configure("small.TButton", font=self.font_small_B)

        # Placing Frames in Root Window
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        #To stop another user from being logged in
        self.logged_in = 0

        self.frames = {}

        for F in (HomePage, LogInPage, RegisterPage, DeletePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="NSEW")

        self.show_frame(HomePage)

    # To display the frame passed as parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        # Sets hidden to 0 since frame is visible
        frame.hidden = 0
        self.geometry(f"{self.winfo_width()+1}x{self.winfo_height()+1}")
        frame.tkraise()
        # Sets hidden of all other frames 0 since the frames are hidden
        for i in self.frames:
            if i != cont:
                self.frames[i].hidden = 1

    # Dynamically Resize Widget Text
    def resize(self, event):
        # Assigns value of x as greater value between window HEIGHT and window WIDTH
        x = (
            event.widget.winfo_height()
            if event.widget.winfo_height() > event.widget.winfo_width()
            else event.widget.winfo_width()
        )
        self.font_login_L["size"] = x // 49
        self.font_big_B["size"] = x // 36
        self.font_small_B["size"] = x // 100
        self.font_error_L["size"] = x // 81


class HomePage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        # App aka tk.TK()
        self.controller = controller

        # Initializing images
        self.image = Image.open("stonks.png")
        self.image = ImageOps.expand(self.image, border=20)  # Adding Borders
        # Recording image sizes
        self.image_size = self.image.size
        # Turning PIL image object into Tk usable objects
        self.logo = ImageTk.PhotoImage(self.image)

        # Configuring Rows and Columns
        for i in range(4):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(i, weight=1)
        self.rowconfigure(5, weight=1)

        # To check if frame is behind another frame
        self.hidden = 0

        # Make Widget Text Resizable
        self.bind("<Configure>", self.resize)

        # Image Label
        self.img_label = ttk.Label(self, image=self.logo)
        self.img_label.grid(row=0, column=1, rowspan=2, columnspan=2)

        # Buttons
        self.to_login = ttk.Button(
            self,
            text="Log In",
            command=lambda: self.controller.show_frame(LogInPage),
            style="big.TButton",
        )
        self.to_login.grid(row=2, column=1, sticky="NSEW")
        self.to_register = ttk.Button(
            self,
            text="Create Account",
            command=lambda: self.controller.show_frame(RegisterPage),
            style="big.TButton",
        )
        self.to_register.grid(row=2, column=2, sticky="NSEW")
        self.to_delete = ttk.Button(
            self,
            text="Delete Account",
            command=lambda: self.controller.show_frame(DeletePage),
            style="big.TButton",
        )
        self.to_delete.grid(row=3, column=1, sticky="NSEW")
        self.quit_app = ttk.Button(
            self, text="Quit App", command=self.controller.destroy, style="big.TButton"
        )
        self.quit_app.grid(row=3, column=2, sticky="NSEW")

    # Dynamically resize fonts and pics
    def resize(self, event):
        # Check if frame is visible
        if self.hidden == 0 and self.controller.logged_in == 0:
            # Keeping picture aspect ratio same when resizing
            ratio = self.image_size[0] / self.image_size[1]
            width = event.height / 1.5
            height = width * (1 / ratio)
            # Original image is preserved in order to act as refernce
            self.logo = ImageTk.PhotoImage(
                self.image.resize((round(width), round(height)), Image.BICUBIC)
            )
            self.img_label.configure(image=self.logo)
            # Dynamically resize fonts using Style
            self.controller.resize(event)


class LogInPage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        # App aka tk.TK()
        self.controller = controller

        # Configuring Rows and Columns
        for i in range(0, 10, 8):
            self.rowconfigure(i, weight=9)
        for i in range(1, 8):
            self.rowconfigure(i, weight=1)
        for i in range(4):
            self.columnconfigure(i, weight=1)

        # To check if frame is behind another frame
        self.hidden = 1

        # Make Widget Text Resizable
        self.bind("<Configure>", self.resize)

        # Styling
        # Fonts
        # Username and Password Entry font
        self.font_login_E = font.Font(family="Avenir Next Condensed", size=14)

        # Initializng Values
        self.username = tkinter.StringVar(value="Enter Username")
        self.password = tkinter.StringVar(value="Enter Password")
        self.show = tkinter.IntVar()

        # Poplating Frame
        # Label And Entry
        # Username Label
        self.user_label = ttk.Label(
            self, text="Username", style="big.TLabel", anchor="w"
        )
        self.user_label.grid(row=1, column=1, sticky="SEW", columnspan=2)
        # Username Entry
        self.user_entry = ttk.Entry(
            self, textvariable=self.username, font=self.font_login_E, foreground="grey"
        )
        self.user_entry.grid(row=2, column=1, sticky="NEW", columnspan=2)

        # Password Label
        self.pass_label = ttk.Label(
            self, text="Password", style="big.TLabel", anchor="w"
        )
        self.pass_label.grid(row=3, column=1, sticky="SEW", columnspan=2)
        # Password Entry
        self.pass_entry = ttk.Entry(
            self, textvariable=self.password, font=self.font_login_E, foreground="grey"
        )
        self.pass_entry.grid(row=4, column=1, sticky="NEW", columnspan=2)

        # Grey text when not focused on Entry
        self.user_entry.bind("<FocusIn>", self.on_focusIn)
        self.user_entry.bind("<FocusOut>", self.on_focusOut)
        self.pass_entry.bind("<FocusIn>", self.on_focusIn)
        self.pass_entry.bind("<FocusOut>", self.on_focusOut)

        # Buttons
        # Show Pass
        self.showPass_checkbutton = ttk.Checkbutton(
            self,
            text="Show Password",
            variable=self.show,
            command=lambda: self.s_or_h(),
            style="small.TCheckbutton",
            compound=tkinter.LEFT,
        )
        self.showPass_checkbutton.grid(row=5, column=2, sticky="SE")
        # Home Page Button
        self.home_button = ttk.Button(
            self,
            text="To Home Page",
            style="small.TButton",
            command=lambda: self.controller.show_frame(HomePage),
        )
        self.home_button.grid(row=5, column=1, sticky="SW")
        # Create Account Button
        self.crAcc_button = ttk.Button(
            self,
            text="Create Account?",
            style="small.TButton",
            command=lambda: self.controller.show_frame(RegisterPage),
        )
        self.crAcc_button.grid(row=6, column=1, sticky="SEW", columnspan=2)
        # Log In Button
        self.logIn_button = ttk.Button(
            self, text="LOG IN", style="big.TButton", command=self.login
        )
        self.logIn_button.grid(row=7, column=1, sticky="NSEW", columnspan=2)

    # Dynamically resize font
    def resize(self, event):
        # Check if frame is visible
        if self.hidden == 0 and self.controller.logged_in == 0:
            # Dynamically resize entry since ttk.Entry does not accept Styles
            x = event.height if event.height > event.width else event.width
            self.font_login_E["size"] = x // 49
            # Dynamically resize fonts using Style
            self.controller.resize(event)

    def on_focusIn(self, event):
        if event.widget == self.user_entry and self.username.get() == "Enter Username":
            self.username.set("")
            self.user_entry.configure(foreground="black")
        elif (
            event.widget == self.pass_entry and self.password.get() == "Enter Password"
        ):
            self.password.set("")
            self.pass_entry.configure(foreground="black", show="*")

    def on_focusOut(self, event):
        if event.widget == self.user_entry and self.username.get() == "":
            self.username.set("Enter Username")
            self.user_entry.configure(foreground="grey")
        elif event.widget == self.pass_entry and self.password.get() == "":
            self.pass_entry.configure(foreground="grey", show="")
            self.password.set("Enter Password")

    # Show or hide password
    def s_or_h(self):
        if self.show.get() == 1:
            self.pass_entry.configure(show="")
        elif self.password.get() == "Enter Password":
            self.pass_entry.configure(show="")
        else:
            self.pass_entry.configure(show="*")

    def login(self):
        boolean, username = backend.login_register(
            self.username.get(), self.password.get(), choice="Log In"
        )
        if boolean == False:
            messagebox.showerror("Error", "Invalid username/password, please check!")
        elif boolean == True:
            self.controller.iconify()
            self.username.set("")
            self.password.set("")  # Minimizes root window when market is shown
            if self.controller.logged_in != 1:
                Market(self, username, self.controller)
            else:
                messagebox.showwarning(
                    "Already Logged In", "Already Logged In, Check Open Windows"
                )


class RegisterPage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        # App aka tk.TK()
        self.controller = controller

        # Configuring Rows and Columns
        for i in range(9):
            self.rowconfigure(i, weight=1)
        for i in range(0, 11, 9):
            self.rowconfigure(i, weight=4)
        for i in range(0, 7):
            self.columnconfigure(i, weight=1)
        for i in range(0, 8, 6):
            self.columnconfigure(i, weight=4)

        # To check if frame is behind another frame
        self.hidden = 1

        # Make Widget Text Resizable
        self.bind("<Configure>", self.resize)

        # Styling
        # Fonts
        self.font_login_E = font.Font(family="Avenir Next Condensed", size=14)

        # Initializing Values
        self.username = tkinter.StringVar(value="Enter Username")
        self.password = tkinter.StringVar(value="Enter Password")
        self.confirm_pass = tkinter.StringVar(value="Re-Enter Password")
        self.show = tkinter.IntVar()
        self.error_msg = tkinter.StringVar()

        # Populating Frame
        # Label And Entry
        # Username Label
        self.user_label = ttk.Label(
            self, text="Enter Username", style="big.TLabel", anchor="w"
        )
        self.user_label.grid(row=3, column=2, sticky="EW", columnspan=1)
        # Username Entry
        self.user_entry = ttk.Entry(
            self, textvariable=self.username, font=self.font_login_E, foreground="grey"
        )
        self.user_entry.grid(row=3, column=4, sticky="EW", columnspan=1)
        # Password Label
        self.pass_label = ttk.Label(
            self, text="Enter Password", style="big.TLabel", anchor="w"
        )
        self.pass_label.grid(row=4, column=2, sticky="EW", columnspan=1)
        # Password Entry
        self.pass_entry = ttk.Entry(
            self, textvariable=self.password, font=self.font_login_E, foreground="grey"
        )
        self.pass_entry.grid(row=4, column=4, sticky="EW", columnspan=1)
        # Password Label
        self.confirmPass_label = ttk.Label(
            self, text="Confirm Password", style="big.TLabel", anchor="w"
        )
        self.confirmPass_label.grid(row=5, column=2, sticky="EW", columnspan=1)
        # Password Entry
        self.confirmPass_entry = ttk.Entry(
            self,
            textvariable=self.confirm_pass,
            font=self.font_login_E,
            foreground="grey",
        )
        self.confirmPass_entry.grid(row=5, column=4, sticky="EW", columnspan=1)
        # Error Label
        self.error_label = ttk.Label(
            self, textvariable=self.error_msg, style="small.TLabel", foreground="red"
        )
        self.error_label.grid(row=6, column=4, sticky="SE")

        # Divider
        for i in range(3, 6):
            ttk.Label(self, text=":", style="big.TLabel", anchor="w").grid(
                row=i, column=3, sticky="EW"
            )

        # Grey text when not focused on Entry
        self.user_entry.bind("<FocusIn>", self.on_focusIn)
        self.user_entry.bind("<FocusOut>", self.on_focusOut)
        self.pass_entry.bind("<FocusIn>", self.on_focusIn)
        self.pass_entry.bind("<FocusOut>", self.on_focusOut)
        self.confirmPass_entry.bind("<FocusIn>", self.on_focusIn)
        self.confirmPass_entry.bind("<FocusOut>", self.on_focusOut)

        # Interactively check entry text
        self.user_entry.bind("<KeyRelease>", self.entry_check)
        self.pass_entry.bind("<KeyRelease>", self.entry_check)
        self.confirmPass_entry.bind("<KeyRelease>", self.entry_check)

        # Buttons
        # Show Pass
        self.showPass_checkbutton = ttk.Checkbutton(
            self,
            text="Show Password",
            variable=self.show,
            command=lambda: self.s_or_h(),
            style="small.TCheckbutton",
            compound=tkinter.LEFT,
        )
        self.showPass_checkbutton.grid(row=6, column=4, sticky="NE")
        # Home Page Button
        self.home_button = ttk.Button(
            self,
            text="To Home Page",
            style="small.TButton",
            command=lambda: self.controller.show_frame(HomePage),
        )
        self.home_button.grid(row=6, column=2, sticky="NW")
        # Back to Log In Button
        # Back to Log In Button use same font as Create Account Button from LogInPage
        self.backToLogIn_button = ttk.Button(
            self,
            text="To Log In?",
            style="small.TButton",
            command=lambda: controller.show_frame(LogInPage),
        )
        self.backToLogIn_button.grid(row=7, column=2, sticky="SEW", columnspan=3)
        # Create Account Button
        # Create Account Button use same font as Log In Button from LogInPage
        self.crAcc_button = ttk.Button(
            self,
            text="CREATE ACCOUNT",
            style="big.TButton",
            command=lambda: self.create_account(),
        )
        self.crAcc_button.grid(row=8, column=2, columnspan=3, sticky="NSEW")

    # Dynamically resize font
    def resize(self, event):
        # Check if frame is visible
        if self.hidden == 0 and self.controller.logged_in == 0:
            # Dynamically resize entry since ttk.Entry does not accept Styles
            x = event.height if event.height > event.width else event.width
            self.font_login_E["size"] = x // 49
            # Dynamically resize fonts using Style
            self.controller.resize(event)

    # Check if passwords meet requirements
    def entry_check(self, event):
        username = self.username.get()
        passwords = (self.password.get(), self.confirm_pass.get())
        if username == "":
            self.error_msg.set("Username Should NOT be Blank")
        elif " " in username:
            self.error_msg.set("Username Should NOT Have Spaces")
        elif len(username) < 5:
            self.error_msg.set("Username Should be More Than 5 Letters")
        elif passwords[0] == "" or passwords[1] == "":
            self.error_msg.set("Password Should NOT be Blank")
        elif " " in passwords[0] or " " in passwords[1]:
            self.error_msg.set("Password Should NOT Have Spaces")
        elif len(passwords[0]) < 5:
            self.error_msg.set("Password Should be More Than 5 Letters")
        elif passwords[0] != passwords[1]:
            self.error_msg.set("Passwords Should Match")
        else:
            self.error_msg.set("")

    def on_focusIn(self, event):
        if event.widget == self.user_entry and self.username.get() == "Enter Username":
            self.username.set("")
            self.user_entry.configure(foreground="black")
        elif (
            event.widget == self.pass_entry and self.password.get() == "Enter Password"
        ):
            self.password.set("")
            self.pass_entry.configure(foreground="black", show="*")
        elif (
            event.widget == self.confirmPass_entry
            and self.confirm_pass.get() == "Re-Enter Password"
        ):
            self.confirm_pass.set("")
            self.confirmPass_entry.configure(foreground="black", show="*")

    def on_focusOut(self, event):
        if event.widget == self.user_entry and self.username.get() == "":
            self.username.set("Enter Username")
            self.user_entry.configure(foreground="grey")
        elif event.widget == self.pass_entry and self.password.get() == "":
            self.pass_entry.configure(foreground="grey", show="")
            self.password.set("Enter Password")
        elif event.widget == self.confirmPass_entry and self.confirm_pass.get() == "":
            self.confirmPass_entry.configure(foreground="grey", show="")
            self.confirm_pass.set("Re-Enter Password")

    # Show or hide password
    def s_or_h(self):
        if self.show.get() == 1:
            self.pass_entry.configure(show="")
            self.confirmPass_entry.configure(show="")
        else:
            self.pass_entry.configure(show="*")
            self.confirmPass_entry.configure(show="*")

        if self.password.get() == "Enter Password":
            self.pass_entry.configure(show="")
        if self.confirm_pass.get() == "Re-Enter Password":
            self.confirmPass_entry.configure(show="")

    # Create Account
    def create_account(self):
        if self.error_msg.get() != "":
            messagebox.showerror("Error", self.error_msg.get())
        else:
            username = self.username.get()
            password = self.confirm_pass.get()
            boolean, username = backend.login_register(
                username, password, choice="Register"
            )
            if boolean == False:
                messagebox.showerror("Error", "Account already exists")
            elif (
                messagebox.askyesno("Log In?", "Would you like to be logged in?")
                == True
            ):
                self.controller.iconify()  # Minimizes root window when market is shown
                self.username.set("")
                self.password.set("")
                self.confirm_pass.set("")
                if self.controller.logged_in != 1:
                    Market(self, username, self.controller)
                else:
                    messagebox.showwarning(
                        "Already Logged In", "Already Logged In, Check Open Windows"
                    )
            else:
                self.username.set("")
                self.password.set("")
                self.confirm_pass.set("")
                self.controller.show_frame(HomePage)


class DeletePage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        # App aka tk.TK()
        self.controller = controller

        # Configuring Rows and Columns
        for i in range(9):
            self.rowconfigure(i, weight=1)
        for i in range(0, 11, 9):
            self.rowconfigure(i, weight=4)
        for i in range(0, 7):
            self.columnconfigure(i, weight=1)
        for i in range(0, 8, 6):
            self.columnconfigure(i, weight=4)

        # To check if frame is behind another frame
        self.hidden = 1

        # Make Widget Text Resizable
        self.bind("<Configure>", self.resize)

        # Styling
        # Fonts
        self.font_login_E = font.Font(family="Avenir Next Condensed", size=14)

        # Initializing Values
        self.username = tkinter.StringVar(value="Enter Username")
        self.password = tkinter.StringVar(value="Enter Password")
        self.confirm_pass = tkinter.StringVar(value="Re-Enter Password")
        self.show = tkinter.IntVar()
        self.error_msg = tkinter.StringVar()

        # Poplating Frame
        # Label And Entry
        # Username Label
        self.user_label = ttk.Label(
            self, text="Enter Username", style="big.TLabel", anchor="w"
        )
        self.user_label.grid(row=3, column=2, sticky="EW", columnspan=1)
        # Username Entry
        self.user_entry = ttk.Entry(
            self, textvariable=self.username, font=self.font_login_E, foreground="grey"
        )
        self.user_entry.grid(row=3, column=4, sticky="EW", columnspan=1)
        # Password Label
        self.pass_label = ttk.Label(
            self, text="Enter Password", style="big.TLabel", anchor="w"
        )
        self.pass_label.grid(row=4, column=2, sticky="EW", columnspan=1)
        # Password Entry
        self.pass_entry = ttk.Entry(
            self, textvariable=self.password, font=self.font_login_E, foreground="grey"
        )
        self.pass_entry.grid(row=4, column=4, sticky="EW", columnspan=1)
        # Password Label
        self.confirmPass_label = ttk.Label(
            self, text="Confirm Password", style="big.TLabel", anchor="w"
        )
        self.confirmPass_label.grid(row=5, column=2, sticky="EW", columnspan=1)
        # Password Entry
        self.confirmPass_entry = ttk.Entry(
            self,
            textvariable=self.confirm_pass,
            font=self.font_login_E,
            foreground="grey",
        )
        self.confirmPass_entry.grid(row=5, column=4, sticky="EW", columnspan=1)
        # Error Label
        self.error_label = ttk.Label(
            self,
            textvariable=self.error_msg,
            text="Remember me",
            style="small.TLabel",
            foreground="red",
        )
        self.error_label.grid(row=6, column=4, sticky="SE")

        # Divider
        for i in range(3, 6):
            ttk.Label(self, text=":", style="big.TLabel", anchor="w").grid(
                row=i, column=3, sticky="EW"
            )

        # Grey text when not focused on Entry
        self.user_entry.bind("<FocusIn>", self.on_focusIn)
        self.user_entry.bind("<FocusOut>", self.on_focusOut)
        self.pass_entry.bind("<FocusIn>", self.on_focusIn)
        self.pass_entry.bind("<FocusOut>", self.on_focusOut)
        self.confirmPass_entry.bind("<FocusIn>", self.on_focusIn)
        self.confirmPass_entry.bind("<FocusOut>", self.on_focusOut)

        # Interactively check entry text
        self.pass_entry.bind("<KeyRelease>", self.entry_check)
        self.confirmPass_entry.bind("<KeyRelease>", self.entry_check)

        # Buttons
        # Show Pass
        self.showPass_checkbutton = ttk.Checkbutton(
            self,
            text="Show Password",
            variable=self.show,
            command=lambda: self.s_or_h(),
            style="small.TCheckbutton",
            compound=tkinter.LEFT,
        )
        self.showPass_checkbutton.grid(row=6, column=4, sticky="NE")
        # Home Page Button
        self.home_button = ttk.Button(
            self,
            text="To Home Page",
            style="small.TButton",
            command=lambda: self.controller.show_frame(HomePage),
        )
        self.home_button.grid(row=6, column=2, sticky="NW")
        # Back to Log In Button
        # Back to Log In Button use same font as Create Account Button from LogInPage
        self.backToLogIn_button = ttk.Button(
            self,
            text="To Log In?",
            style="small.TButton",
            command=lambda: controller.show_frame(LogInPage),
        )
        self.backToLogIn_button.grid(row=7, column=2, sticky="SEW", columnspan=3)
        # Create Account Button
        # Create Account Button use same font as Log In Button from LogInPage
        self.delAcc_button = ttk.Button(
            self,
            text="DELETE ACCOUNT",
            style="big.TButton",
            command=lambda: self.delete(),
        )
        self.delAcc_button.grid(row=8, column=2, columnspan=3, sticky="NSEW")

    # Dynamically resize font
    def resize(self, event):
        # Check if frame is visible
        if self.hidden == 0 and self.controller.logged_in == 0:
            # Dynamically resize entry since ttk.Entry does not accept Styles
            x = event.height if event.height > event.width else event.width
            self.font_login_E["size"] = x // 49
            # Dynamically resize fonts using Style
            self.controller.resize(event)

    # Check if passwords meet requirements
    def entry_check(self, event):
        if self.password.get() != self.confirm_pass.get():
            self.error_msg.set("Passwords Are Not Matching")
        else:
            self.error_msg.set("")

    def on_focusIn(self, event):
        if event.widget == self.user_entry and self.username.get() == "Enter Username":
            self.username.set("")
            self.user_entry.configure(foreground="black")
        elif (
            event.widget == self.pass_entry and self.password.get() == "Enter Password"
        ):
            self.password.set("")
            self.pass_entry.configure(foreground="black", show="*")
        elif (
            event.widget == self.confirmPass_entry
            and self.confirm_pass.get() == "Re-Enter Password"
        ):
            self.confirm_pass.set("")
            self.confirmPass_entry.configure(foreground="black", show="*")

    def on_focusOut(self, event):
        if event.widget == self.user_entry and self.username.get() == "":
            self.username.set("Enter Username")
            self.user_entry.configure(foreground="grey")
        elif event.widget == self.pass_entry and self.password.get() == "":
            self.pass_entry.configure(foreground="grey", show="")
            self.password.set("Enter Password")
        elif event.widget == self.confirmPass_entry and self.confirm_pass.get() == "":
            self.confirmPass_entry.configure(foreground="grey", show="")
            self.confirm_pass.set("Re-Enter Password")

    # Show or hide password
    def s_or_h(self):
        if self.show.get() == 1:
            self.pass_entry.configure(show="")
            self.confirmPass_entry.configure(show="")
        else:
            self.pass_entry.configure(show="*")
            self.confirmPass_entry.configure(show="*")

        if self.password.get() == "Enter Password":
            self.pass_entry.configure(show="")
        if self.confirm_pass.get() == "Re-Enter Password":
            self.confirmPass_entry.configure(show="")

    # Delete Account
    def delete(self):
        if self.error_msg.get() != "":
            messagebox.showerror("Error", self.error_msg.get())
        elif (
            messagebox.askyesno(
                "Are You Sure?", "Are you sure you want to delete the account?"
            )
            == True
        ):
            boolean = backend.del_account(self.username.get(), self.confirm_pass.get())
            if boolean == True:
                messagebox.showinfo("Info", "Account has been deleted sucessfully")
                self.username.set("")
                self.password.set("")
                self.confirm_pass.set("")
                self.controller.show_frame(HomePage)
            else:
                messagebox.showerror("Error", "Wrong username/password")


class Market(tkinter.Toplevel):
    def __init__(self, source, username, controller):
        super().__init__(controller)

        # Configuring window
        self.minsize(500, 500)
        self.geometry("500x500")
        # Bring window to front
        self.lift()

        self.controller = controller
        self.username = username
        self.source = source

        # To Stop Another User From being Logged In
        self.controller.logged_in = 1

        # Initializing Values
        self.balance = tkinter.StringVar()
        self.botcoin = tkinter.StringVar()
        self.esterium = tkinter.StringVar()
        self.binguscoin = tkinter.StringVar()
        self.floppacoin = tkinter.StringVar()
        self.beans = tkinter.StringVar()

        self.set_balance()

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Make root window visible when market window is closed
        self.bind("<Destroy>", self.on_destroy)

        # Populating Frame
        # CryptoCoins Trading
        self.coins = ttk.Notebook(self)
        for i in ("BotCoin", "Esterium", "BingusCoin", "FloppaCoin", "Beans"):
            self.coins.add(
                Coin(self.coins, self, self.controller, self.username, i.lower()),
                text=i,
            )
        self.coins.grid(row=0, column=0, sticky="NSEW")

    def set_balance(self):
        balances = backend.balance(self.username)
        self.balance.set(f"Money: {balances[0]}")
        self.botcoin.set(f"{balances[1]} :Bot Coins")
        self.esterium.set(f"{balances[2]} :Esterium")
        self.binguscoin.set(f"{balances[3]} :Bingus Coins")
        self.floppacoin.set(f"{balances[4]} :Floppa Coin")
        self.beans.set(f"{balances[5]} :Beans")

    def on_destroy(self, event):
        if event.widget == self:
            self.controller.logged_in = 0
            self.controller.geometry(f"{self.controller.winfo_width()+1}x{self.controller.winfo_height()+1}")
            self.controller.deiconify()


class Coin(ttk.Frame):
    def __init__(self, master, toplevel, controller, username, coin):
        super().__init__(master)

        self.toplevel = toplevel
        self.controller = controller
        self.username = username
        self.coin = coin

        # Initializing image
        self.image = Image.open(f"{self.coin}.png")
        # Recording image sizes
        self.image_size = self.image.size
        # Turning PIL image object into Tk usable objects
        self.logo = ImageTk.PhotoImage(self.image)

        # Configuring Rows and Columns
        for i in range(5):
            self.columnconfigure(i, weight=1)
        for i in range(8):
            self.rowconfigure(i, weight=1)

        # Make Widget Text Resizable
        self.bind("<Configure>", self.resize)

        # Font
        self.coin_font = font.Font(family="Avenir Next Condensed", size=14)

        # Initializing Values
        self.coinAmount = tkinter.StringVar(value="1")

        # Validation for Coin Entry
        vcmd = (self.controller.register(self.intValidate), "%S")

        # Balance and Logout Frame
        self.title_labelframe = ttk.LabelFrame(
            self,
            text="".join([" " + i if i == "C" else i for i in self.coin.upper()]),
            borderwidth=0,
            labelanchor="s",
        )
        self.title_labelframe.grid(row=0, column=0, columnspan=5, sticky="NSEW")

        # Configuring Rows and Columns
        for i in range(3):
            self.title_labelframe.columnconfigure(i, weight=1)
        self.title_labelframe.rowconfigure(0, weight=1)

        # Money Label
        self.money_label = ttk.Label(
            self.title_labelframe,
            textvariable=self.toplevel.balance,
            style="small.TLabel",
        )
        self.money_label.grid(row=0, column=0, sticky="NSW")

        # Log Out Button
        self.logOut_button = ttk.Button(
            self.title_labelframe,
            text="Log Out",
            style="small.TButton",
            command=self.toplevel.destroy,
        )
        self.logOut_button.grid(row=0, column=1, sticky="NSEW")

        # Crypto Label
        self.crypto_label = ttk.Label(
            self.title_labelframe,
            textvariable=eval(f"self.toplevel.{self.coin}"),
            style="small.TLabel",
        )
        self.crypto_label.grid(row=0, column=2, sticky="NSE")

        # Populating Main Frame
        # Image Label
        self.img_label = ttk.Label(self, image=self.logo)
        self.img_label.grid(row=1, column=2)

        # Coin Amount Entry
        self.coinAmount_entry = ttk.Entry(
            self,
            textvariable=self.coinAmount,
            font=self.coin_font,
            justify="center",
            validate="key",
            validatecommand=vcmd,
        )
        self.coinAmount_entry.grid(row=3, column=2, sticky="NSEW")

        # Add Coins Button
        self.remove_button = ttk.Button(
            self, text="-", style="big.TButton", command=self.decrease_Amount
        )
        self.remove_button.grid(row=3, column=1, sticky="NSEW")
        # Remove Coins Button
        self.add_button = ttk.Button(
            self, text="+", style="big.TButton", command=self.increase_Amount
        )
        self.add_button.grid(row=3, column=3, sticky="NSEW")

        # Buy Button
        self.buy_button = ttk.Button(
            self, text="BUY", style="big.TButton", command=lambda: self.buy()
        )
        self.buy_button.grid(
            row=4,
            column=2,
            sticky="NSEW",
        )
        # Sell Button
        self.sell_button = ttk.Button(
            self, text="SELL", style="big.TButton", command=lambda: self.sell()
        )
        self.sell_button.grid(row=5, column=2, sticky="NSEW")
        # Show Line Graph
        self.graph_button = ttk.Button(
            self,
            text="Show Stock Graph",
            command=lambda: backend.show_exchange_rate(self.coin),
            style="big.TButton",
        )
        self.graph_button.grid(row=7, column=2, sticky="NSEW")

    def increase_Amount(self, event=None):
        amount = self.coinAmount.get()
        if amount == "":
            self.coinAmount.set("1")
        else:
            self.coinAmount.set(f"{int(amount)+1}")

    def decrease_Amount(self, event=None):
        amount = self.coinAmount.get()
        if amount == "":
            self.coinAmount.set("1")
        elif int(amount) - 1 >= 1:
            self.coinAmount.set(f"{int(amount)-1}")

    def intValidate(self, text):
        if not text.isdigit():
            messagebox.showwarning("Only Digits", "Only Digits Can be Entered")
            return False
        else:
            return True

    def buy(self):
        try:
            amount = int(self.coinAmount.get())
        except ValueError:
            messagebox.showwarning("Empty", "Amount Cannot be Empty")
        else:
            if amount == 0:
                messagebox.showwarning("Zero", "Amount Cannot be Zero")
            elif backend.buy_crypto(amount, self.username, self.coin) == True:
                self.toplevel.set_balance()
                messagebox.showinfo(
                    "Sucessful",
                    f"{amount} {self.title_labelframe['text']}s™ has been ADDED to your account!",
                )
                self.coinAmount.set("1")
            else:
                messagebox.showwarning("Unsucessful", "Insufficient Funds!")

    def sell(self):
        try:
            amount = int(self.coinAmount.get())
        except ValueError:
            messagebox.showwarning("Empty", "Amount Cannot be Empty")
        else:
            if amount == 0:
                messagebox.showwarning("Zero", "Amount Cannot be Zero")
            elif backend.sell_crypto(amount, self.username, self.coin) == True:
                self.toplevel.set_balance()
                messagebox.showinfo(
                    "Sucessful",
                    f"{amount} {self.title_labelframe['text']}s™ has been SOLD from your account!",
                )
                self.coinAmount.set("1")
            else:
                messagebox.showwarning("Unsucessful", "Insufficient Funds!")

    def resize(self, event):
        # Keeping picture aspect ratio same when resizing
        ratio = self.image_size[0] / self.image_size[1]
        width = event.height / 3
        height = width * (1 / ratio)
        x = event.height if event.height > event.width else event.width
        # Original image is preserved in order to act as reference
        if int(width) > 0 and int(height) > 0:
            self.logo = ImageTk.PhotoImage(
                self.image.resize((round(width), round(height)), Image.BICUBIC)
            )
        self.img_label.configure(image=self.logo)
        # Change entry font size
        self.coin_font["size"] = x // 25
        # Change Every Other Font Size
        self.controller.resize(event)


# Starting Gui
app = App()
app.mainloop()
