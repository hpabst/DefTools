from Tkinter import *
from ttk import Frame, Button, Style, Entry, Scale
from models.rclc_reader import RCLCReader
from sqlalchemy.orm import Session


class Open(Frame):

    def __init__(self, parent, **kw):
        Frame.__init__(self, **kw)
        self.parent = parent
        self.initUI()
        return

    def initUI(self):
        self.pack(fill=BOTH, expand=True)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)

        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

        self.lblCsv = Label(self, text="Enter CSV Export:")
        self.lblCsv.grid(sticky=W, pady=4, padx=5)

        self.txtCsv = Text(self)
        self.txtCsv.grid(row=1, column=0, columnspan=2, rowspan=4, padx=5, sticky=E+W+N+S)

        self.btnSubmit = Button(self, text="Submit", command=self.submit_text)
        self.btnSubmit.grid(row=5, column=4, padx=5)

        self.btnCancel = Button(self, text="Cancel")
        self.btnCancel.grid(row=5, column=3)
        return


    def submit_text(self):
        text = self.txtCsv.get("1.0", END)
        reader = RCLCReader()
        session = Session()
        db_objects = reader.read_csv_text(text, session)
        session.commit()
        return
