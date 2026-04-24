import tkinter as tk
from tkinter import messagebox

def show_alert(service_name, risk_level):
    root = tk.Tk()
    root.withdraw()

    message = f"{service_name} stopped!\nRisk Level: {risk_level}"
    messagebox.showwarning("Service Alert", message)

    root.destroy()