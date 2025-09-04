import sqlite3
import customtkinter as ctk

from pprint import pprint
from prettytable import PrettyTable


class App(ctk.CTk):
	def __init__(self):
		super().__init__()
		# window info
		self.title("Simple Scheduler")
		self.geometry("800x600")

		self.lift()
		self.focus_force()
		self.grab_set()

		self.theme_choice = "system"
		ctk.set_appearance_mode(self.theme_choice)

		# configure grid
		self.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)
		self.rowconfigure(0, weight=1)

		self.sidebar_frame = ctk.CTkFrame(self)
		self.sidebar_frame.grid(row=0, column=0, padx=(5, 2.5), pady=5, sticky="nsew")
		self.sidebar_frame.columnconfigure(0, weight=1)
		self.sidebar_frame.rowconfigure((0, 1, 2, 3, 4, 5), weight=0)

		self.sidebar_label = ctk.CTkLabel(self.sidebar_frame, text="Tools")
		self.sidebar_label.grid(row=0, column=0, padx=5, pady=5, sticky="new")
		self.sidebar_label.cget("font").configure(size=14)

		self.add_employee_button = ctk.CTkButton(self.sidebar_frame, text="Add Employee", command=self.add_employee_subwindow)
		self.add_employee_button.grid(row=1, column=0, padx=5, pady=5, sticky="new")

		self.show_employees_button = ctk.CTkButton(self.sidebar_frame, text="Show Employees", command=self.show_employees_subwindow)
		self.show_employees_button.grid(row=2, column=0, padx=5, pady=5, sticky="new")

		self.add_template_button = ctk.CTkButton(self.sidebar_frame, text="Add Template", command=self.add_template_subwindow)
		self.add_template_button.grid(row=3, column=0, padx=5, pady=5, sticky="new")

		self.show_template_button = ctk.CTkButton(self.sidebar_frame, text="Show Template", command=self.show_template_subwindow)
		self.show_template_button.grid(row=4, column=0, padx=5, pady=5, sticky="new")

		self.toggle_theme_button = ctk.CTkButton(self.sidebar_frame, text="Toggle theme", command=self.toggle_theme)
		self.toggle_theme_button.grid(row=5, column=0, padx=5, pady=5, sticky="sew")

		self.main_frame = MainApp(self)
		self.main_frame.grid(row=0, column=1, columnspan=10, padx=(2.5, 5), pady=5, sticky="nsew")
	
	def add_employee_subwindow(self):
		AddEmployee(self)
	
	def show_employees_subwindow(self):
		ShowEmployee(self)
	
	def add_template_subwindow(self):
		AddTemplate(self)
	
	def show_template_subwindow(self):
		ShowTemplate(self)
	
	def toggle_theme(self):
		if self.theme_choice in ["system", "light"]:
			self.theme_choice = "dark"
		elif self.theme_choice == "dark":
			self.theme_choice = "light"
		ctk.set_appearance_mode(self.theme_choice)


class MainApp(ctk.CTkFrame):
	def __init__(self, master=None):
		super().__init__(master)
		self.columnconfigure((0, 1), weight=1)
		self.rowconfigure((0, 1, 2, 3), weight=1)

		self.title_label = ctk.CTkLabel(self, text="Simple Scheduler")
		self.title_label.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="new")
		self.title_label.cget("font").configure(size=14)

		self.select_day_label = ctk.CTkLabel(self, text="Select day")
		self.select_day_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

		self.select_day_combobox = ctk.CTkComboBox(self, values=["Tuesday"])
		self.select_day_combobox.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

		self.leave_frame = ctk.CTkFrame(self)
		self.leave_frame.grid(row=3, column=0, padx=5, pady=5, sticky="new")

		self.leave_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)
		self.leave_frame.rowconfigure((0, 1, 2, 3, 4), weight=1)

		self.leave_label = ctk.CTkLabel(self.leave_frame, text="Who's off?")
		self.leave_label.grid(row=0, column=0, columnspan=5, padx=5, pady=5, sticky="new")

		self.names = self.get_employees()

		self.raw_names = self.get_employees()
		self.names = []

		for name in self.raw_names:
			self.names.append(list(name)[0])
		
		self.employee_name_selector = ctk.CTkComboBox(self.leave_frame, values=self.names)
		self.employee_name_selector.grid(row=1, column=0, columnspan=5, padx=5, pady=5, sticky="ew")

		self.start_hour_selector = ctk.CTkComboBox(self.leave_frame, values=["9", "10", "11", "12", "1", "2", "3", "4", "5", "6", "7", "8"])
		self.start_hour_selector.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

		self.start_minute_selector = ctk.CTkComboBox(self.leave_frame, values=["00", "15", "30", "45"])
		self.start_minute_selector.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

		self.time_divider_label = ctk.CTkLabel(self.leave_frame, text="-")
		self.time_divider_label.grid(row=2, column=2, padx=5, pady=5, sticky="ew")

		self.end_hour_selector = ctk.CTkComboBox(self.leave_frame, values=["9", "10", "11", "12", "1", "2", "3", "4", "5", "6", "7", "8"])
		self.end_hour_selector.grid(row=2, column=3, padx=5, pady=5, sticky="ew")

		self.end_minute_selector = ctk.CTkComboBox(self.leave_frame, values=["00", "15", "30", "45"])
		self.end_minute_selector.grid(row=2, column=4, padx=5, pady=5, sticky="ew")

		self.all_day_checkbox = ctk.CTkCheckBox(self.leave_frame, text="All day?")
		self.all_day_checkbox.grid(row=3, column=0, columnspan=5, padx=5, pady=5, sticky="ew")
	
	def get_employees(self):
		conn = sqlite3.connect("data/employees.db")
		cursor = conn.cursor()

		cursor.execute("SELECT First_Name FROM EMPLOYEES")
		rows = cursor.fetchall()

		conn.close()

		return rows


class AddEmployee(ctk.CTkToplevel):
	def __init__(self, master=None):
		super().__init__(master)
		self.title("Add Employee")
		self.geometry("400x300")

		self.lift()
		self.focus_force()
		self.grab_set()
		
		# configure grid
		self.columnconfigure((0, 1, 2), weight=1)
		self.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
		
		self.label_title = ctk.CTkLabel(self, text="Add Employee")
		self.label_title.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

		self.label_title.cget("font").configure(size=14)
		
		self.label_first_name = ctk.CTkLabel(self, text="First Name")
		self.label_first_name.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

		self.entry_first_name = ctk.CTkEntry(self, placeholder_text="Jane")
		self.entry_first_name.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

		self.label_last_name = ctk.CTkLabel(self, text="Last Name")
		self.label_last_name.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

		self.entry_last_name = ctk.CTkEntry(self, placeholder_text="Doe")
		self.entry_last_name.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

		self.label_position = ctk.CTkLabel(self, text="Position")
		self.label_position.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

		self.position_selector = ctk.CTkComboBox(self, values=["Manager", "Assistant Manager", "Supervisor", "Full-Time", "Part-Time", "Shelver", "Security Full-Time", "Security Part-Time"])
		self.position_selector.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

		self.label_start_time = ctk.CTkLabel(self, text="Start time")
		self.label_start_time.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

		self.start_hour = ctk.CTkComboBox(self, values=["9", "10", "11", "12", "1", "2", "3", "4", "5", "6", "7", "8"])
		self.start_hour.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
		
		self.start_minute = ctk.CTkComboBox(self, values=["00", "15", "30", "45"])
		self.start_minute.grid(row=4, column=2, padx=5, pady=5, sticky="ew")

		self.label_end_time = ctk.CTkLabel(self, text="End time")
		self.label_end_time.grid(row=5, column=0, padx=5, pady=5, sticky="ew")

		self.end_hour = ctk.CTkComboBox(self, values=["9", "10", "11", "12", "1", "2", "3", "4", "5", "6", "7", "8"])
		self.end_hour.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

		self.end_minute = ctk.CTkComboBox(self, values=["00", "15", "30", "45"])
		self.end_minute.grid(row=5, column=2, padx=5, pady=5, sticky="ew")

		self.cancel_button = ctk.CTkButton(self, text="Cancel", command=self.destroy)
		self.cancel_button.grid(row=6, column=0, padx=5, pady=5, sticky="ew")

		self.add_button = ctk.CTkButton(self, text="Add to database", command=self.add_to_db)
		self.add_button.grid(row=6, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
	
	def add_to_db(self):
		if (self.entry_first_name.get() and self.entry_last_name.get()
			and self.position_selector.get() and self.start_hour.get()
			and self.start_minute.get() and self.end_hour.get()
			and self.end_minute.get()):

			first_name = self.entry_first_name.get()
			last_name = self.entry_last_name.get()
			position = self.position_selector.get()
			start_hour = self.start_hour.get()
			start_minute = self.start_minute.get()
			end_hour = self.end_hour.get()
			end_minute = self.end_minute.get()

			conn = sqlite3.connect("data/employees.db")
			cursor = conn.cursor()

			cursor.execute(f"INSERT INTO EMPLOYEES VALUES ('{first_name}', '{last_name}', '{position}', '{start_hour}:{start_minute}', '{end_hour}:{end_minute}')")

			conn.commit()
			conn.close()
			self.destroy()
		else:
			print("Not valid")


class AddTemplate(ctk.CTkToplevel):
	def __init__(self, master=None):
		super().__init__(master)
		self.title("Add Template")
		self.geometry("1000x600")

		self.lift()
		self.focus_force()
		self.grab_set()

		self.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
		self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

		self.label_title = ctk.CTkLabel(self, text="Add Template")
		self.label_title.grid(row=0, column=0, columnspan=7, padx=5, pady=5, sticky="nsew")
		self.label_title.cget("font").configure(size=14)

		self.headers = ["", "9-11", "11-1", "1-2", "2-4", "4-6", "6-8"]
		self.locations = [
			"pick-up window", "floor lead",
			"service point 1", "service point 1",
			"service point 2", "service point 2",
			"meetings/programs",
			"project time"
		]
		self.input_contents = []

		self.raw_names = self.get_employees()
		self.names = [""]

		for name in self.raw_names:
			self.names.append(list(name)[0])

		for h in range(len(self.headers)):
			locations = []
			if h > 0:
				location_label = ctk.CTkLabel(self, text=self.headers[h])
				location_label.grid(row=1, column=h, padx=5, pady=5, sticky="ew")
				location_label.cget("font").configure(size=14)
			for l in range(len(self.locations) - 1):
				if h == 0:
					location_label = ctk.CTkLabel(self, text=self.locations[l])
					location_label.grid(row=l+2, column=h, padx=5, pady=5, sticky="ew")
				else:
					location_entry = ctk.CTkComboBox(self, values=self.names)
					location_entry.grid(row=l+2, column=h, padx=5, pady=5, sticky="ew")
					locations.append(location_entry)
			self.input_contents.append(locations)

		self.cancel_button = ctk.CTkButton(self, text="Cancel", command=self.destroy)
		self.cancel_button.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

		self.add_button = ctk.CTkButton(self, text="Add to database", command=self.add_to_db)
		self.add_button.grid(row=9, column=4, columnspan=3, padx=5, pady=5, sticky="ew")
	
	def add_to_db(self):
		all_names = []
		for hidx, hdata in enumerate(self.input_contents):
			if hidx > 0:
				hour_names = [f"'{n.get()}'" if n.get() != "" else "NULL" for n in hdata]
				all_names.append(hour_names)
		reshaped_names = [list(row) for row in zip(*all_names)]

		conn = sqlite3.connect("data/template.db")
		cursor = conn.cursor()

		for n in reshaped_names:
			cursor.execute(f"INSERT INTO TEMPLATE VALUES ({','.join(n)})")
		
		conn.commit()
		conn.close()
		self.destroy()
	
	def get_employees(self):
		conn = sqlite3.connect("data/employees.db")
		cursor = conn.cursor()

		cursor.execute("SELECT First_Name FROM EMPLOYEES WHERE Position IN ('Manager', 'Assistant Manager', 'Supervisor', 'Full-time', 'Part-time')")
		rows = cursor.fetchall()

		conn.close()

		return rows


class ShowEmployee(ctk.CTkToplevel):
	def __init__(self, master=None):
		super().__init__(master)
		self.title("Show Employees")
		self.geometry("400x500")

		self.lift()
		self.focus_force()
		self.grab_set()

		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)

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


class ShowTemplate(ctk.CTkToplevel):
	def __init__(self, master=None):
		super().__init__(master)
		self.title("Show Template")
		self.geometry("1200x300")

		self.lift()
		self.focus_force()
		self.grab_set()

		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)

		self.preview_text_box = ctk.CTkTextbox(self, wrap="none", font=("Courier", 13))
		self.preview_text_box.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

		self.db_conn = sqlite3.connect("data/template.db")
		self.db_cursor = self.db_conn.cursor()

		self.db_cursor.execute("SELECT * FROM TEMPLATE")
		self.rows = self.db_cursor.fetchall()

		locations = ["pick-up window", "floor lead", "service pt 1", "service pt 1", "service pt 2", "service pt 2", "meetings/programs"]
		hours = ["", "9-11", "11-1", "1-2", "2-4", "4-6", "6-8"]
		
		preview_text = [hours]
		for l in range(len(self.rows)):
			temp_table = []
			temp_table.append(locations[l])
			for n in list(self.rows[l]):
				temp_table.append(n)
			preview_text.append(temp_table)

		for row in preview_text:
			line = ""
			for cell in row:
				if cell is None:
					cell = "None"
				line += str(cell).ljust(20)
			line += "\n\n"
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
	ctk.set_default_color_theme("blue")
	app = App()
	app.mainloop()