import customtkinter as ctk

class App(ctk.CTk):
	def __init__(self):
		super().__init__()
		self.title("Simple Scheduler")
		self.geometry("1000x600")

		self.lift()
		self.focus_force()
		self.grab_set()

		self.theme_choice = "system"
		ctk.set_appearance_mode(self.theme_choice)

		self.grid_columnconfigure((1, 2), weight=1)
		self.grid_rowconfigure(0, weight=0)
		self.grid_rowconfigure(1, weight=1)

		self.menu_frame = ctk.CTkFrame(self, height=40, corner_radius=0)
		self.menu_frame.grid(row=0, column=0, columnspan=3, sticky="new")

		self.file_menu = ctk.CTkOptionMenu(self.menu_frame, values=["Save"], fg_color="lightgray", text_color="black", anchor="w", corner_radius=0)
		self.file_menu.grid(row=0, column=0, padx=(0, 5), pady=0, sticky="ew")
		self.file_menu.set("File")

		self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
		self.sidebar_frame.grid(row=1, column=0, rowspan=4, sticky="nsew")
		self.sidebar_frame.grid_rowconfigure(4, weight=1)

		self.title_label = ctk.CTkLabel(self.sidebar_frame, text="Simple Scheduler", font=ctk.CTkFont(size=20, weight="bold"))
		self.title_label.grid(row=1, column=0, padx=20, pady=(20, 10))

		self.instructions_text = """Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos."""
		self.instructions_label = ctk.CTkLabel(self.sidebar_frame, text=self.instructions_text, wraplength=200, justify=ctk.LEFT)
		self.instructions_label.grid(row=1, column=0, padx=20, pady=10)

		self.appearance_mode_label  = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode", anchor="w")
		self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
		self.appearance_mode_optionmenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
		self.appearance_mode_optionmenu.grid(row=6, column=0, padx=20, pady=(10, 10))

		self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text="UI Scaling", anchor="w")
		self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
		self.scaling_optionmenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
		self.scaling_optionmenu.grid(row=8, column=0, padx=20, pady=(10, 20))
		self.scaling_optionmenu.set("100%")

		self.tabview_options = ["Date", "Leave", "Programs & Meetings"]

		self.tabview = ctk.CTkTabview(self)
		self.tabview.grid(row=1, column=1, columnspan=2, padx=20, pady=20, sticky="nsew")
		self.tabview.add("Date")
		self.tabview.add("Leave")
		self.tabview.add("Programs & Meetings")

		self.previous_button = ctk.CTkButton(self, text="Previous", command=self.previous_tabview)
		self.previous_button.grid(row=2, column=1, padx=20, pady=20, sticky="sw")

		self.next_button = ctk.CTkButton(self, text="Next", command=self.next_tabview)
		self.next_button.grid(row=2, column=2, padx=20, pady=20, sticky="se")
	
	def change_appearance_mode_event(self, new_appearance_mode: str):
		ctk.set_appearance_mode(new_appearance_mode)
	
	def change_scaling_event(self, new_scaling: str):
		new_scaling_float = int(new_scaling.replace("%", "")) / 100
		ctk.set_widget_scaling(new_scaling_float)
	
	def previous_tabview(self):
		if self.tabview.index(self.tabview.get()) > 0:
			self.tabview.set(self.tabview_options[self.tabview.index(self.tabview.get()) - 1])

	def next_tabview(self):
		if self.tabview.index(self.tabview.get()) < len(self.tabview_options) - 1:
			self.tabview.set(self.tabview_options[self.tabview.index(self.tabview.get()) + 1])


if __name__ == "__main__":
	app = App()
	app.mainloop()