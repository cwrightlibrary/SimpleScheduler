import customtkinter as ctk

class App(ctk.CTk):
  def __init__(self):
    super().__init__()
    self.title("UI Testing")
    self.geometry("800x600")

    self.lift()
    self.focus_force()
    self.grab_set()

    self.theme_choice = "system"
    ctk.set_appearance_mode(self.theme_choice)


if __name__ == "__main__":
  app = App()
  app.mainloop()