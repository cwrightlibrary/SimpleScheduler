import calendar
from datetime import datetime
import sqlite3

import customtkinter as ctk

class App(ctk.CTk):
	def __init__(self):
		super().__init__()
		self.title("Simple Scheduler")
		self.geometry("500x250")
		self.resizable(False, False)

		self.lift()
		self.focus_force()
		self.grab_set()

		self.tuesday_employees = self.get_employees("tuesday")
		self.tuesday_template = self.get_template("tuesday")

		self.changes = []
		
		self.months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
		self.current_days = 0; self.current_month = 0
		self.current_year = 0; self.current_weekday = 0

		self.get_current_date()

		self.date_string = f"{self.current_weekday}, {self.current_month} {str(self.current_day)}, {self.current_year}"

		self.grid_columnconfigure((0, 1, 2), weight=1)
		self.grid_rowconfigure((0, 1, 2, 3), weight=1)

		self.title_label = ctk.CTkLabel(
			self,
			text="Simple Scheduler",
			font=ctk.CTkFont(size=20, weight="bold")
		)
		self.title_label.grid(
			row=0, column=0, columnspan=3,
			padx=10, pady=10, sticky="new"
		)

		self.date_label = ctk.CTkLabel(
			self,
			text=self.date_string,
			font=ctk.CTkFont(size=16, weight="bold")
		)
		self.date_label.grid(
			row=1, column=0, columnspan=3,
			padx=10, pady=10, sticky="nsew"
		)

		self.month_options = ctk.CTkOptionMenu(
			self,
			values=self.months,
			command=self.update_current_date
		)
		self.month_options.grid(
			row=2, column=0,
			padx=10, pady=10, sticky="ew"
		)
		self.month_options.set(self.current_month)

		self.day_options = ctk.CTkOptionMenu(
			self,
			values=self.current_days,
			command=self.update_current_date
		)
		self.day_options.grid(
			row=2, column=1,
			padx=10, pady=10, sticky="ew"
		)
		self.day_options.set(self.current_day)

		self.year_options = ctk.CTkOptionMenu(
			self,
			values=[str(self.current_year + i) for i in range(6)],
			command=self.update_current_date
		)
		self.year_options.grid(
			row=2, column=2,
			padx=10, pady=10, sticky="ew"
		)
		self.year_options.set(self.current_year)

		self.create_template_button = ctk.CTkButton(
			self,
			text="Create Template",
			height=40,
			command=self.create_template
		)
		self.create_template_button.grid(
			row=3, column=1,
			padx=10, pady=10, sticky="ew"
		)

		self.create_schedule_button = ctk.CTkButton(
			self,
			text="Create Schedule",
			height=40,
			command=self.create_schedule
		)
		self.create_schedule_button.grid(
			row=3, column=2,
			padx=10, pady=10, sticky="ew"
		)
	
	def get_employees(self, day: str):
		conn = sqlite3.connect("data/employees.db")
		cursor = conn.cursor()

		cursor.execute("SELECT * FROM EMPLOYEES")
		rows = cursor.fetchall()

		employees = []
		for row in rows:
			employees.append(list(row))
		
		return employees

	def get_template(self, date: str):
		conn = sqlite3.connect("data/template.db")
		cursor = conn.cursor()

		cursor.execute("SELECT * FROM TEMPLATE")
		rows = cursor.fetchall()

		template = []
		for row in rows:
			template.append(list(row))
		
		return template
	
	def get_current_date(self):
		year = datetime.now().year
		month = self.months[datetime.now().month - 1]
		day = datetime.now().day

		amount_days = {m: calendar.monthrange(year, m)[1] for m in range(1, 13)}
		current_days_total = amount_days[self.months.index(month) + 1]

		self.current_days = [str(i + 1) for i in range(current_days_total)]

		self.current_year = year
		self.current_month = month
		self.current_day = day

		self.current_weekday = datetime.strptime(
			f"{self.current_month} {str(self.current_day)}, {self.current_year}",
			"%B %d, %Y"
		).strftime("%A")
	
	def update_current_date(self, data):
		selected_year = self.year_options.get()
		selected_month = self.month_options.get()
		selected_day = self.day_options.get()

		amount_days = {m: calendar.monthrange(selected_year, m)[1] for m in range(1, 13)}
		current_days_total = amount_days[self.months.index(selected_month) + 1]

		self.current_days = [str(i + 1) for i in range(current_days_total)]

		self.current_year = selected_year
		self.current_month = selected_month
		self.current_day = selected_day

		self.current_weekday = datetime.strptime(
			f"{self.current_month} {str(self.current_day)}, {self.current_year}",
			"%B %d, %Y"
		).strftime("%A")

		self.date_string = f"{self.current_weekday}, {self.current_month} {str(self.current_day)}, {self.current_year}"

		self.date_label.configure(text=self.date_string)
		self.day_options.configure(values=self.current_days)
	
	def get_changes(self):
		from scratch import changes_list
		self.changes = changes_list
	
	def create_schedule(self):
		self.get_changes()
		print("Yet to implement...")
		for change in self.changes:
			print(change)
	
	def create_template(self):
		self.get_changes()
		print("Yet to implement...")
		for change in self.changes:
			print(change)

if __name__ == "__main__":
	app = App()
	app.mainloop()