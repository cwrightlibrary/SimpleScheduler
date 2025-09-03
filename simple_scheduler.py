import sqlite3
import customtkinter as ctk

from prettytable import PrettyTable


class App(ctk.CTk):
	def __init__(self):
		super().__init__()
		# window info
		self.title("Simple Scheduler")
		self.geometry("800x600")

		self.theme_choice = "system"
		ctk.set_appearance_mode(self.theme_choice)

		# configure grid
		self.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)
		self.rowconfigure(0, weight=1)

		self.sidebar_frame = ctk.CTkFrame(self)
		self.sidebar_frame.grid(row=0, column=0, padx=(5, 2.5), pady=5, sticky="nsew")
		self.sidebar_frame.columnconfigure(0, weight=1)
		self.sidebar_frame.rowconfigure((0, 1, 2), weight=1)

		self.sidebar_label = ctk.CTkLabel(self.sidebar_frame, text="Tools")
		self.sidebar_label.grid(row=0, column=0, padx=5, pady=5, sticky="new")
		self.sidebar_label.cget("font").configure(size=14)

		# add employee button to open the sub-window
		self.add_employee_button = ctk.CTkButton(self.sidebar_frame, text="Add Employee", command=self.add_employee_subwindow)
		self.add_employee_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

		self.toggle_theme_button = ctk.CTkButton(self.sidebar_frame, text="Toggle theme", command=self.toggle_theme)
		self.toggle_theme_button.grid(row=2, column=0, padx=5, pady=5, sticky="sew")

		self.main_frame = ctk.CTkFrame(self)
		self.main_frame.grid(row=0, column=1, columnspan=10, padx=(2.5, 5), pady=5, sticky="nsew")
		self.main_frame.columnconfigure((0, 1, 2, 3), weight=1)
		self.main_frame.rowconfigure((0, 1, 2, 3), weight=1)

		self.title_label = ctk.CTkLabel(self.main_frame, text="Simple Scheduler")
		self.title_label.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="new")
		self.title_label.cget("font").configure(size=14)
	
	def add_employee_subwindow(self):
		AddEmployee(self)
	
	def toggle_theme(self):
		if self.theme_choice in ["system", "light"]:
			self.theme_choice = "dark"
		elif self.theme_choice == "dark":
			self.theme_choice = "light"
		ctk.set_appearance_mode(self.theme_choice)


class AddEmployee(ctk.CTkToplevel):
	def __init__(self, master=None):
		super().__init__(master)
		self.title("Add Employee")
		self.geometry("400x300")

		# database object
		self.db_conn = sqlite3.connect("data/employees.db")
		self.db_cursor = self.db_conn.cursor()
		self.db_cursor.execute("DROP TABLE IF EXISTS EMPLOYEES")

		# create the database table
		self.db_create_table_query = """
			CREATE TABLE EMPLOYEES (
				First_Name CHAR(25) NOT NULL,
				Last_Name CHAR(25) NOT NULL,
				Position CHAR(25) NOT NULL,
				Start_Time CHAR(5) NOT NULL,
				End_Time CHAR(5) NOT NULL
			);
		"""
		self.db_cursor.execute(self.db_create_table_query)
		
		# configure grid
		self.columnconfigure((0, 1, 2), weight=1)
		self.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
		
		self.label_title = ctk.CTkLabel(self, text="Add Employee")
		self.label_title.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

		self.label_title.cget("font").configure(size=14)
		
		self.label_first_name = ctk.CTkLabel(self, text="First Name")
		self.label_first_name.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

		self.entry_first_name = ctk.CTkEntry(self, placeholder_text="Chris")
		self.entry_first_name.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

		self.label_last_name = ctk.CTkLabel(self, text="Last Name")
		self.label_last_name.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

		self.entry_last_name = ctk.CTkEntry(self, placeholder_text="Wright")
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

		self.cancel_button = ctk.CTkButton(self, text="Cancel", command=self.cancel_command)
		self.cancel_button.grid(row=6, column=0, padx=5, pady=5, sticky="ew")

		self.add_button = ctk.CTkButton(self, text="Add to database", command=self.add_to_db)
		self.add_button.grid(row=6, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
	
	def cancel_command(self):
		self.db_conn.close()
		self.destroy()
	
	def add_to_db(self):
		if self.entry_first_name.get() and self.entry_last_name.get() and self.position_selector.get() and self.start_hour.get() and self.start_minute.get() and self.end_hour.get() and self.end_minute.get():
			first_name = self.entry_first_name.get()
			last_name = self.entry_last_name.get()
			position = self.position_selector.get()
			start_hour = self.start_hour.get()
			start_minute = self.start_minute.get()
			end_hour = self.end_hour.get()
			end_minute = self.end_minute.get()
			self.db_cursor.execute(f"INSERT INTO EMPLOYEES VALUES ('{first_name}', '{last_name}', '{position}', '{start_hour}:{start_minute}', '{end_hour}:{end_minute}')")
			self.db_cursor.execute("SELECT * FROM EMPLOYEES")
			for row in self.db_cursor.fetchall():
				print(row)
		else:
			print("Not valid")


if __name__ == "__main__":
  ctk.set_default_color_theme("blue")
  app = App()
  app.mainloop()