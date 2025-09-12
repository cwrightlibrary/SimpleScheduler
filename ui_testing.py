import calendar
import customtkinter as ctk
import sqlite3
import tkinter as tk

from datetime import datetime

class App(ctk.CTk):
	def __init__(self):
		super().__init__()
		self.title("Simple Scheduler")
		self.base_width = 1000
		self.base_height = 750
		self.current_scale = 1.0
		self.apply_scale(self.current_scale)

		self.lift()
		self.focus_force()
		self.grab_set()

		self.theme_choice = "System"
		ctk.set_appearance_mode(self.theme_choice)

		self.employees_names = self.get_employee_names()

		self.grid_columnconfigure((1, 2), weight=1)
		self.grid_rowconfigure(0, weight=1)
		
		self.create_menubar(self.theme_choice)

		self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
		self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
		self.sidebar_frame.grid_rowconfigure(4, weight=1)

		self.title_label = ctk.CTkLabel(self.sidebar_frame, text="Simple Scheduler", font=ctk.CTkFont(size=20, weight="bold"))
		self.title_label.grid(row=1, column=0, padx=20, pady=(20, 10))

		self.instructions_text = """Here's a quick tutorial on how to create a schedule.\n\nFirst, in the Date tab, select your date. It'll automatically detect if that date falls on a weekend (including Friday). If it is a weekend, just select who's weekend it is.\n\nNext, in the Leave tab, select an employee's name and enter the hours they're off or check all day. Add or remove as many as you need.\n\nSimilarly, in the Programs & Meetings tab, add or remove as many programs or meetings that you need, assigning all involved employees.\n\nFinally, in the Review tab, just make sure everything is looks right and click Export Schedule to create your schedule as a Word document."""
		self.instructions_label = ctk.CTkLabel(self.sidebar_frame, text=self.instructions_text, wraplength=200, justify=ctk.LEFT)
		self.instructions_label.grid(row=2, column=0, padx=20, pady=10)

		self.appearance_mode_label  = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode", anchor="w")
		self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
		self.appearance_mode_optionmenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
		self.appearance_mode_optionmenu.grid(row=6, column=0, padx=20, pady=(10, 10))
		self.appearance_mode_optionmenu.set(self.theme_choice)

		self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text="UI Scaling", anchor="w")
		self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
		self.scaling_optionmenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
		self.scaling_optionmenu.grid(row=8, column=0, padx=20, pady=(10, 20))
		self.scaling_optionmenu.set("100%")

		self.tabview_options = ["Date", "Leave", "Programs & Meetings", "Review"]

		self.tabview = ctk.CTkTabview(self)
		self.tabview.grid(row=0, column=1, columnspan=2, padx=20, pady=20, sticky="nsew")

		self.tabview.add("Date")
		self.tabview.add("Leave")
		self.tabview.add("Programs & Meetings")
		self.tabview.add("Review")

		self.months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

		self.get_current_date_info()

		self.draw_date_tabview()
		self.draw_leave_tabview()
		self.draw_programs_meetings_tabview()
		self.draw_review_tabview()

		self.tabview.set("Date")

		self.previous_button = ctk.CTkButton(self, text="Previous", height=40, font=ctk.CTkFont(size=16), command=self.previous_tabview)
		self.previous_button.grid(row=1, column=1, padx=20, pady=20, sticky="sw")
		self.previous_button.configure(state="disabled")

		self.next_button = ctk.CTkButton(self, text="Next", height=40, font=ctk.CTkFont(size=16), command=self.next_tabview)
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

		self.file_menu.add_command(label="Export Schedule", command=self.export_schedule)

		self.file_menu.add_separator()

		self.file_menu.add_command(label="Exit", command=self.quit)

		self.view_menu = tk.Menu(self.menubar, tearoff=0, bg=bg_color, fg=fg_color, activebackground=active_bg, activeforeground=active_fg, relief="flat")
		self.menubar.add_cascade(label="View", menu=self.view_menu)

		self.view_menu.add_command(label="Show Employees", command=self.show_employees_subwindow)

		self.help_menu = tk.Menu(self.menubar, tearoff=0, bg=bg_color, fg=fg_color, activebackground=active_bg, activeforeground=active_fg, relief="flat")
		self.menubar.add_cascade(label="Help", menu=self.help_menu)
		
		self.help_menu.add_command(label="About", command=self.show_about)
	
	def add_employee_subwindow(self):
		pass

	def add_template_subwindow(self):
		pass

	def show_employees_subwindow(self):
		ShowEmployees(self)

	def show_about(self):
		AboutWindow(self)
	
	def change_appearance_mode_event(self, new_appearance_mode: str):
		self.theme_choice = new_appearance_mode
		ctk.set_appearance_mode(self.theme_choice)
	
	def change_scaling_event(self, new_scaling: str):
		new_scaling_float = int(new_scaling.replace("%", "")) / 100
		self.apply_scale(new_scaling_float)
		ctk.set_widget_scaling(new_scaling_float)

	def apply_scale(self, scale_factor):
		self.current_scale = scale_factor

		new_width = int(self.base_width * scale_factor)
		new_height = int(self.base_height * scale_factor)
		self.geometry(f"{new_width}x{new_height}")
	
	def draw_date_tabview(self):
		self.tabview.tab("Date").grid_columnconfigure((0, 1, 2), weight=1)
		self.tabview.tab("Date").grid_rowconfigure((3, 4), weight=1)

		self.date_label = ctk.CTkLabel(self.tabview.tab("Date"), text="Select the Date", font=ctk.CTkFont(size=20, weight="bold"))
		self.date_label.grid(row=0, column=0, columnspan=3, padx=10, pady=(80, 10), sticky="nsew")

		self.current_date = f"{self.current_weekday}, {self.current_month} {str(self.current_day)}, {self.current_year}"

		self.month_picker = ctk.CTkOptionMenu(self.tabview.tab("Date"), values=self.months, command=self.update_date_label)
		self.month_picker.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
		self.month_picker.set(self.current_month)

		self.day_picker = ctk.CTkOptionMenu(self.tabview.tab("Date"), values=self.current_days, command=self.update_date_label)
		self.day_picker.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
		self.day_picker.set(str(self.current_day))

		self.year_picker = ctk.CTkOptionMenu(self.tabview.tab("Date"), values=["2025", "2026", "2027", "2028", "2029", "2030"], command=self.update_date_label)
		self.year_picker.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

		self.weekend_label = ctk.CTkLabel(self.tabview.tab("Date"), text="Who's weekend?")
		self.weekend_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

		self.weekend_picker = ctk.CTkOptionMenu(self.tabview.tab("Date"), values=["Michelle's Weekend", "Rod's Weekend", "Lea's Weekend"], width=200)
		self.weekend_picker.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
		self.weekend_picker.configure(state="disabled")

		self.current_date_tip_label = ctk.CTkLabel(self.tabview.tab("Date"), text="You've selected")
		self.current_date_tip_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="sew")

		self.current_date_label = ctk.CTkLabel(self.tabview.tab("Date"), text=self.current_date, font=ctk.CTkFont(size=20, weight="bold"))
		self.current_date_label.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="new")
	
	def update_date_label(self, new_info: str):
		self.current_month = self.month_picker.get()
		self.current_day = self.day_picker.get()
		self.current_year = self.year_picker.get()
		self.current_weekday = datetime.strptime(f"{self.current_month} {str(self.current_day)}, {self.current_year}", "%B %d, %Y").strftime("%A")

		self.current_date = f"{self.current_weekday}, {self.current_month} {str(self.current_day)}, {self.current_year}"
		self.current_date_label.configure(text=self.current_date)

		if self.current_weekday in ["Friday", "Saturday", "Sunday"]:
			self.weekend_picker.configure(state="normal")
		else:
			self.weekend_picker.configure(state="disabled")
		
		if self.current_weekday in ["Friday", "Saturday"]:
			self.hour_values = ["9", "10", "11", "12", "1", "2", "3", "4", "5", "6"]
		elif self.current_weekday == "Sunday":
			self.hour_values = ["2", "3", "4", "5", "6"]
		else:
			self.hour_values = ["9", "10", "11", "12", "1", "2", "3", "4", "5", "6", "7", "8"]
		self.start_hour_leave_picker.configure(values=self.hour_values)
	
	def draw_leave_tabview(self):
		self.tabview.tab("Leave").grid_columnconfigure((0, 1, 2, 3), weight=1)
		self.tabview.tab("Leave").grid_rowconfigure((3, 4), weight=1)

		self.leave_label = ctk.CTkLabel(self.tabview.tab("Leave"), text="Who's Off Today?", font=ctk.CTkFont(size=20, weight="bold"))
		self.leave_label.grid(row=0, column=0, columnspan=4, padx=10, pady=(80, 10), sticky="nsew")

		self.employee_leave_picker = ctk.CTkOptionMenu(self.tabview.tab("Leave"), values=self.employees_names)
		self.employee_leave_picker.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="")

		self.hour_values = []
		if self.current_weekday in ["Friday", "Saturday"]:
			self.hour_values = ["9", "10", "11", "12", "1", "2", "3", "4", "5", "6"]
		elif self.current_weekday == "Sunday":
			self.hour_values = ["2", "3", "4", "5", "6"]
		else:
			self.hour_values = ["9", "10", "11", "12", "1", "2", "3", "4", "5", "6", "7", "8"]
		
		self.start_hour_leave_label = ctk.CTkLabel(self.tabview.tab("Leave"), text="Start time")
		self.start_hour_leave_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

		self.start_hour_leave_picker = ctk.CTkOptionMenu(self.tabview.tab("Leave"), values=self.hour_values)
		self.start_hour_leave_picker.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
		
		self.start_minute_leave_picker = ctk.CTkOptionMenu(self.tabview.tab("Leave"), values=["00", "15", "30", "45"])
		self.start_minute_leave_picker.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

	def draw_programs_meetings_tabview(self):
		self.tabview.tab("Programs & Meetings").grid_columnconfigure((0, 1, 2), weight=1)
		self.tabview.tab("Programs & Meetings").grid_rowconfigure((3, 4), weight=1)

		self.programs_meetings_label = ctk.CTkLabel(self.tabview.tab("Programs & Meetings"), text="Today's Programs & Meetings", font=ctk.CTkFont(size=20, weight="bold"))
		self.programs_meetings_label.grid(row=0, column=0, columnspan=3, padx=10, pady=(80, 10), sticky="nsew")
	
	def get_employee_names(self):
		db_conn = sqlite3.connect("data/employees.db")
		db_cursor = db_conn.cursor()

		db_cursor.execute("SELECT First_name, Last_name FROM EMPLOYEES")
		rows = db_cursor.fetchall()

		employees_names = []

		for row in rows:
			name = " ".join(row)
			employees_names.append(name)
		
		return employees_names
	
	def draw_review_tabview(self):
		self.tabview.tab("Review").grid_columnconfigure((0, 1, 2), weight=1)
		self.tabview.tab("Review").grid_rowconfigure((3, 4), weight=1)

		self.review_label = ctk.CTkLabel(self.tabview.tab("Review"), text="Everything Good?", font=ctk.CTkFont(size=20, weight="bold"))
		self.review_label.grid(row=0, column=0, columnspan=3, padx=10, pady=(80, 10), sticky="nsew")
	
	def previous_tabview(self):
		new_tab = self.tabview_options[(self.tabview.index(self.tabview.get()) - 1) % len(self.tabview_options)]
		
		if self.tabview.index(self.tabview.get()) - 1 == 0:
			self.previous_button.configure(state="disabled")
		else:
			self.previous_button.configure(state="normal")
		
		self.next_button.configure(text="Next", command=self.next_tabview)

		self.tabview._segmented_button_callback(new_tab)
		self.tabview.set(new_tab)

	def next_tabview(self):
		new_tab = self.tabview_options[(self.tabview.index(self.tabview.get()) + 1) % len(self.tabview_options)]

		if self.tabview.index(self.tabview.get()) + 1 == len(self.tabview_options) - 1:
			self.next_button.configure(text="Export Schedule", command=self.export_schedule)
		else:
			self.next_button.configure(text="Next", command=self.next_tabview)
		
		self.previous_button.configure(state="normal")

		self.tabview._segmented_button_callback(new_tab)
		self.tabview.set(new_tab)
	
	def get_current_date_info(self):		
		year = datetime.now().year
		month = self.months[datetime.now().month - 1]
		day = datetime.now().day

		amount_days = {m: calendar.monthrange(year, m)[1] for m in range(1, 13)}
		current_days_total = amount_days[datetime.now().month]
		
		self.current_days = [str(i + 1) for i in range(current_days_total)]

		self.current_month = month
		self.current_day = day
		self.current_year = year
		self.current_weekday = datetime.strptime(f"{self.current_month} {str(self.current_day)}, {self.current_year}", "%B %d, %Y").strftime("%A")

		self.current_date = f"{self.current_weekday}, {self.current_month} {str(self.current_day)}, {self.current_year}"
	
	def export_schedule(self):
		print("Yet to implement exporting...")


class ShowEmployees(ctk.CTkToplevel):
	def __init__(self, master: ctk.CTk):
		super().__init__(master)
		self.title("Employees")
		self.geometry("600x700")

		self.lift()
		self.focus_force()
		self.grab_set()

		self.update_idletasks()
		x = master.winfo_x() + (master.winfo_width() // 2) - (self.winfo_width() // 2)
		y = master.winfo_y() + (master.winfo_height() // 2) - (self.winfo_height() // 2)
		self.geometry(f"+{x}+{y}")

		self.db_conn = sqlite3.connect("data/employees.db")
		self.db_cursor = self.db_conn.cursor()

		self.db_cursor.execute("SELECT * FROM EMPLOYEES ORDER BY CASE Position WHEN 'Manager' THEN 1 WHEN 'Assistant Manager' THEN 2 WHEN 'Supervisor' THEN 3 WHEN 'Full-time' THEN 4 WHEN 'Part-time' THEN 5 WHEN 'Shelver' THEN 6 WHEN 'Security Full-time' THEN 7 WHEN 'Security Part-time' THEN 8 ELSE 9 END;")
		self.rows = self.db_cursor.fetchall()

		rows_len_tup = tuple(range(len(self.rows) + 1))

		self.grid_columnconfigure((0, 1, 2), weight=1)
		self.grid_rowconfigure(rows_len_tup, weight=1)

		position_label = ctk.CTkLabel(self, text="Position")
		position_label.grid(row=0, column=0, padx=(5, 2), pady=(5, 2))
		position_label.cget("font").configure(weight="bold")

		name_label = ctk.CTkLabel(self, text="Name")
		name_label.grid(row=0, column=1, padx=5, pady=(5, 2))
		name_label.cget("font").configure(weight="bold")

		hours_label = ctk.CTkLabel(self, text="Hours")
		hours_label.grid(row=0, column=2, padx=(2, 5), pady=(5, 2))
		hours_label.cget("font").configure(weight="bold")

		for i, row in enumerate(self.rows):
			row_info = list(row)
			position = row_info[2]
			name = f"{row_info[0]} {row_info[1]}"
			hours = f"{row_info[3]}-{row_info[4]}"

			position_entry = ctk.CTkEntry(self, placeholder_text=position, placeholder_text_color=("black", "white"))
			position_entry.configure(state="disabled")

			name_entry = ctk.CTkEntry(self, placeholder_text=name, placeholder_text_color=("black", "white"), width=250)
			name_entry.configure(state="disabled")

			hours_entry = ctk.CTkEntry(self, placeholder_text=hours, placeholder_text_color=("black", "white"), width=100)
			hours_entry.configure(state="disabled")

			if i == 0:
				position_entry.grid(row=i + 1, column=0, padx=(5, 2), pady=(5, 2))
				name_entry.grid(row=i + 1, column=1, padx=2, pady=(5, 2))
				hours_entry.grid(row=i + 1, column=2, padx=2, pady=(5, 2))
			elif i == len(self.rows) + 1:
				position_entry.grid(row=i + 1, column=0, padx=(5, 2), pady=(2, 5))
				name_entry.grid(row=i + 1, column=1, padx=2, pady=(2, 5))
				hours_entry.grid(row=i + 1, column=2, padx=(2, 5), pady=(2, 5))
			else:
				position_entry.grid(row=i + 1, column=0, padx=(5, 2), pady=2)
				name_entry.grid(row=i + 1, column=1, padx=2, pady=2)
				hours_entry.grid(row=i + 1, column=2, padx=2, pady=2)
		
		self.db_conn.close()


class AboutWindow(ctk.CTkToplevel):
	def __init__(self, master: ctk.CTk):
		super().__init__(master)
		self.title("About Simple Scheduler")
		self.geometry("400x250")
		self.resizable(False, False)

		self.lift()
		self.focus_force()
		self.grab_set()

		self.update_idletasks()
		x = master.winfo_x() + (master.winfo_width() // 2) - (self.winfo_width() // 2)
		y = master.winfo_y() + (master.winfo_height() // 2) - (self.winfo_height() // 2)
		self.geometry(f"+{x}+{y}")

		title = ctk.CTkLabel(self, text="Simple Scheduler", font=ctk.CTkFont(size=20, weight="bold"))
		title.pack(pady=(20, 10))

		version = ctk.CTkLabel(self, text="Version 0.1")
		version.pack(pady=(10, 0))

		author = ctk.CTkLabel(self, text="Developed by Chris Wright")
		author.pack(pady=0)

		date = ctk.CTkLabel(self, text="September 10, 2025")
		date.pack(pady=(0, 10))

		description = ctk.CTkLabel(self, text="A lightweight scheduling app to help you create a daily staff schedule.", wraplength=350, justify="center")
		description.pack(pady=20)


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