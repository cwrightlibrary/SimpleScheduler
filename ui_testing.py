import customtkinter as ctk
import sqlite3
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
		
		self.create_menubar(self.theme_choice)

		self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
		self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
		self.sidebar_frame.grid_rowconfigure(4, weight=1)

		self.title_label = ctk.CTkLabel(self.sidebar_frame, text="Simple Scheduler", font=ctk.CTkFont(size=20, weight="bold"))
		self.title_label.grid(row=1, column=0, padx=20, pady=(20, 10))

		self.instructions_text = """Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos."""
		self.instructions_label = ctk.CTkLabel(self.sidebar_frame, text=self.instructions_text, wraplength=200, justify=ctk.LEFT)
		self.instructions_label.grid(row=2, column=0, padx=20, pady=10)

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
		self.tabview.grid(row=0, column=1, columnspan=2, padx=20, pady=20, sticky="nsew")
		self.tabview.add("Date")
		self.tabview.add("Leave")
		self.tabview.add("Programs & Meetings")

		self.previous_button = ctk.CTkButton(self, text="Previous", command=self.previous_tabview)
		self.previous_button.grid(row=1, column=1, padx=20, pady=20, sticky="sw")

		self.next_button = ctk.CTkButton(self, text="Next", command=self.next_tabview)
		self.next_button.grid(row=1, column=2, padx=20, pady=20, sticky="se")
	
	def create_menubar(self, theme: str):
		if theme == "Dark":
			bg_color = "#2b2b2b"
			fg_color = "white"
			active_bg = "#3c3c3c"
			active_fg = "white"
		else:
			bg_color = "white"
			fg_color = "black"
			active_bg = "#e5e5e5"
			active_fg = "black"
		
		self.menubar = tk.Menu(self, tearoff=0, bg=bg_color, fg=fg_color, activebackground=active_bg, activeforeground=active_fg, relief="flat")
		self.config(menu=self.menubar)

		self.file_menu = tk.Menu(self.menubar, tearoff=0, bg=bg_color, fg=fg_color, activebackground=active_bg, activeforeground=active_fg, relief="flat")
		self.menubar.add_cascade(label="File", menu=self.file_menu)

		self.file_menu.add_command(label="Add Employee", command=self.add_employee_subwindow)
		self.file_menu.add_command(label="Add Template", command=self.add_template_subwindow)

		self.file_menu.add_separator()

		self.file_menu.add_command(label="Export Schedule", command=lambda: print("Yet to implement exporting..."))

		self.file_menu.add_separator()

		self.file_menu.add_command(label="Exit", command=self.quit)

		self.view_menu = tk.Menu(self.menubar, tearoff=0, bg=bg_color, fg=fg_color, activebackground=active_bg, activeforeground=active_fg, relief="flat")
		self.menubar.add_cascade(label="View", menu=self.view_menu)

		self.view_menu.add_command(label="Show Employees", command=self.show_employees_subwindow)
		self.view_menu.add_command(label="Show Template", command=self.show_template_subwindow)

		self.help_menu = tk.Menu(self.menubar, tearoff=0, bg=bg_color, fg=fg_color, activebackground=active_bg, activeforeground=active_fg, relief="flat")
		self.menubar.add_cascade(label="Help", menu=self.help_menu)
		
		self.help_menu.add_command(label="About", command=self.show_about)
	
	def add_employee_subwindow(self):
		pass

	def add_template_subwindow(self):
		pass

	def show_employees_subwindow(self):
		ShowEmployees()

	def show_template_subwindow(self):
		pass

	def show_about(self):
		pass
	
	def change_appearance_mode_event(self, new_appearance_mode: str):
		self.theme_choice = new_appearance_mode
		ctk.set_appearance_mode(self.theme_choice)
		
		self.create_menubar(self.theme_choice)
	
	def change_scaling_event(self, new_scaling: str):
		new_scaling_float = int(new_scaling.replace("%", "")) / 100
		ctk.set_widget_scaling(new_scaling_float)
	
	def previous_tabview(self):
		if self.tabview.index(self.tabview.get()) > 0:
			self.tabview.set(self.tabview_options[self.tabview.index(self.tabview.get()) - 1])

	def next_tabview(self):
		if self.tabview.index(self.tabview.get()) < len(self.tabview_options) - 1:
			self.tabview.set(self.tabview_options[self.tabview.index(self.tabview.get()) + 1])


class ShowEmployees(ctk.CTkToplevel):
	def __init__(self, master=None):
		super().__init__(master)
		self.title("Employees")
		self.geometry("400x500")

		self.lift()
		self.focus_force()
		self.grab_set()

		self.grid_columnconfigure(0, weight=1)
		self.grid_rowconfigure(0, weight=1)

		self.preview_text_box = ctk.CTkTextbox(self, wrap="none")
		self.preview_text_box.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

		self.db_conn = sqlite3.connect("data/employees.db")
		self.db_cursor = self.db_conn.cursor()

		self.db_cursor.execute("SELECT * FROM EMPLOYEES")
		self.rows = self.db_cursor.fetchall()

		for row in self.rows:
			row_info = list(row)
			line = f"{row_info[0]} {row_info[1]}, {row_info[2]} ({row_info[3]}-{row_info[4]})\n"
			self.preview_text_box.insert("end", line)
		
		self.preview_text_box.configure(state="disabled")
		
		self.db_conn.close()


def init_db(db_type):
	db_loc = f"data/{db_type}.db"
	conn = sqlite3.connect(db_loc)
	cursor = conn.cursor()

	query = {
		"employees": """
				CREATE TABLE IF NOT EXISTS EMPLOYEES (
						First_Name CHAR(25) NOT NULL,
						Last_Name CHAR(25) NOT NULL,
						Position CHAR(25) NOT NULL,
						Start_Time CHAR(5) NOT NULL,
						End_Time CHAR(5) NOT NULL
				);
		""",
		"template": """
				CREATE TABLE IF NOT EXISTS TEMPLATE (
						NINE_ELEVEN CHAR(50),
						ELEVEN_ONE CHAR(50),
						ONE_TWO CHAR(50),
						TWO_FOUR CHAR(50),
						FOUR_SIX CHAR(50),
						SIX_EIGHT CHAR(50)
				);
		"""
	}

	cursor.execute(query[db_type])

	conn.commit()
	conn.close()

if __name__ == "__main__":
	init_db("employees")
	init_db("template")
	app = App()
	app.mainloop()