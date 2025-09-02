import sqlite3
import customtkinter as ctk

from prettytable import PrettyTable


class App(ctk.CTk):
	def __init__(self):
		super().__init__()
		self.title("Simple Schedule")
		self.geometry("600x400")

		# configure grid
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)

		# add employee button to open the sub-window
		self.add_employee_button = ctk.CTkButton(self, text="Add Employee", command=self.add_employee_subwindow)
		self.add_employee_button.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
	
	def add_employee_subwindow(self):
		AddEmployee(self)


class AddEmployee(ctk.CTkToplevel):
	def __init__(self, master=None):
		super().__init__(master)
		self.title("Add Employee")
		self.geometry("400x300")
		
		# configure grid
		self.columnconfigure((0, 1, 2), weight=1)
		self.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
		
		self.label_title = ctk.CTkLabel(self, text="Add Employee")
		self.label_title.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
		
		self.label_first_name = ctk.CTkLabel(self, text="First Name")
		self.label_first_name.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

		self.entry_first_name = ctk.CTkEntry(self, placeholder_text="Chris")
		self.entry_first_name.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

		self.label_last_name = ctk.CTkLabel(self, text="Last Name")
		self.label_last_name.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

		self.entry_last_name = ctk.CTkEntry(self, placeholder_text="Wright")
		self.entry_last_name.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

		self.label_start_time = ctk.CTkLabel(self, text="Start time")
		self.label_start_time.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

		self.start_hour = ctk.CTkComboBox(self, values=["9", "10", "11", "12", "1", "2", "3", "4", "5", "6", "7", "8"])
		self.start_hour.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
		
		self.start_minute = ctk.CTkComboBox(self, values=["00", "15", "30", "45"])
		self.start_minute.grid(row=3, column=2, padx=10, pady=10, sticky="ew")

		self.label_end_time = ctk.CTkLabel(self, text="End time")
		self.label_end_time.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

		self.end_hour = ctk.CTkComboBox(self, values=["9", "10", "11", "12", "1", "2", "3", "4", "5", "6", "7", "8"])
		self.end_hour.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

		self.end_minute = ctk.CTkComboBox(self, values=["00", "15", "30", "45"])
		self.end_minute.grid(row=4, column=2, padx=10, pady=10, sticky="ew")

		self.close_button = ctk.CTkButton(self, text="Close", command=self.destroy)
		self.close_button.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

		self.save_button = ctk.CTkButton(self, text="Save", command=self.add_to_db)
		self.save_button.grid(row=5, column=1, columnspan=2, padx=10, pady=10, sticky="ew")
	
	def add_to_db(self):
		if self.entry_first_name.get() and self.entry_last_name.get() and self.start_hour.get() and self.start_minute.get() and self.end_hour.get() and self.end_minute.get():
			first_name = self.entry_first_name.get()
			last_name = self.entry_last_name.get()
			start_hour = self.start_hour.get()
			start_minute = self.start_minute.get()
			end_hour = self.end_hour.get()
			end_minute = self.end_minute.get()
			print(f"Name: {first_name} {last_name}")
			print(f"Start time: {start_hour}:{start_minute}")
			print(f"End time: {end_hour}:{end_minute}")
		else:
			print("Not valid")


if __name__ == "__main__":
  ctk.set_appearance_mode("System")
  ctk.set_default_color_theme("blue")
  app = App()
  app.mainloop()