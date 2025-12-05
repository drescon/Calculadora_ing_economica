import tkinter as tk
from tkinter import ttk

from app.views.credit_frame import CreditFrame
from app.views.compound_frame import CompoundFrame
from app.views.annuity_frame import AnnuityFrame

class MainWindow(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Simulador Financiero Integral")
        self.geometry("1050x750")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        self.credit_tab = CreditFrame(notebook, controller)
        self.compound_tab = CompoundFrame(notebook, controller)
        self.annuity_tab = AnnuityFrame(notebook, controller)

        notebook.add(self.credit_tab, text="Crédito | Amortización")
        notebook.add(self.compound_tab, text="Interés Compuesto")
        notebook.add(self.annuity_tab, text="Anualidades Anticipadas")