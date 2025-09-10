import customtkinter as ctk
import tkinter as tk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Simple Scheduler")
        self.geometry("1000x600")

        self.lift()
        self.focus_force()
        self.grab_set()

        self.theme_choice = "Light"
        ctk.set_appearance_mode(self.theme_choice)

        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Custom Menubar
        self.create_menubar(self.theme_choice)

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.title_label = ctk.CTkLabel(
            self.sidebar_frame, text="Simple Scheduler", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.grid(row=1, column=0, padx=20, pady=(20, 10))

        self.instructions_text = """Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos."""
        self.instructions_label = ctk.CTkLabel(
            self.sidebar_frame, text=self.instructions_text, wraplength=200, justify=ctk.LEFT
        )
        self.instructions_label.grid(row=2, column=0, padx=20, pady=10)

        self.appearance_mode_label  = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionmenu = ctk.CTkOptionMenu(
            self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event
        )
        self.appearance_mode_optionmenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text="UI Scaling", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionmenu = ctk.CTkOptionMenu(
            self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event
        )
        self.scaling_optionmenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        self.scaling_optionmenu.set("100%")

        # Tabview
        self.tabview_options = ["Date", "Leave", "Programs & Meetings"]
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=1, columnspan=2, padx=20, pady=20, sticky="nsew")
        self.tabview.add("Date")
        self.tabview.add("Leave")
        self.tabview.add("Programs & Meetings")

        # Navigation buttons
        self.previous_button = ctk.CTkButton(self, text="Previous", command=self.previous_tabview)
        self.previous_button.grid(row=1, column=1, padx=20, pady=20, sticky="sw")

        self.next_button = ctk.CTkButton(self, text="Next", command=self.next_tabview)
        self.next_button.grid(row=1, column=2, padx=20, pady=20, sticky="se")

    def create_menubar(self, theme: str):
        # Colors based on theme
        if theme == "Dark":
            bg_color = "#2b2b2b"
            fg_color = "white"
            hover_color = "#3c3c3c"
        else:
            bg_color = "white"
            fg_color = "black"
            hover_color = "#e5e5e5"

        # Remove previous menubar if it exists
        if hasattr(self, "top_bar"):
            self.top_bar.destroy()
            if hasattr(self, "dropdown_frame"):
                self.dropdown_frame.destroy()

        # Top menubar frame
        self.top_bar = ctk.CTkFrame(self, height=30, fg_color=bg_color)
        self.top_bar.grid(row=0, column=0, columnspan=3, sticky="ew")

        # File menu button
        self.file_button = ctk.CTkButton(
            self.top_bar, text="File", fg_color=bg_color, hover_color=hover_color, text_color=fg_color,
            command=self.toggle_dropdown
        )
        self.file_button.pack(side="left", padx=5)

        # Dropdown frame (hidden initially)
        self.dropdown_frame = ctk.CTkFrame(self, fg_color=bg_color, border_width=1, border_color=fg_color)
        self.dropdown_visible = False

        # Dropdown buttons
        self.export_button = ctk.CTkButton(
            self.dropdown_frame, text="Export Schedule", fg_color=bg_color, hover_color=hover_color, text_color=fg_color,
            command=lambda: print("Yet to implement exporting...")
        )
        self.export_button.pack(fill="x")

        self.exit_button = ctk.CTkButton(
            self.dropdown_frame, text="Exit", fg_color=bg_color, hover_color=hover_color, text_color=fg_color,
            command=self.quit
        )
        self.exit_button.pack(fill="x")

    def toggle_dropdown(self):
        if self.dropdown_visible:
            self.dropdown_frame.place_forget()
            self.dropdown_visible = False
        else:
            x = self.file_button.winfo_rootx() - self.winfo_rootx()
            y = self.top_bar.winfo_height()
            self.dropdown_frame.place(x=x, y=y)
            self.dropdown_visible = True

    def change_appearance_mode_event(self, new_appearance_mode: str):
        self.theme_choice = new_appearance_mode
        ctk.set_appearance_mode(self.theme_choice)
        self.create_menubar(self.theme_choice)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def previous_tabview(self):
        index = self.tabview.index(self.tabview.get())
        if index > 0:
            self.tabview.set(self.tabview_options[index - 1])

    def next_tabview(self):
        index = self.tabview.index(self.tabview.get())
        if index < len(self.tabview_options) - 1:
            self.tabview.set(self.tabview_options[index + 1])

if __name__ == "__main__":
    app = App()
    app.mainloop()
