from Tkinter import *
from ttk import Frame, Button, Style, Entry, Scale
from models.rclc_reader import RCLCReader
from sqlalchemy.orm import Session
import ConfigParser


class Open(Frame):

    def __init__(self, parent, **kw):
        Frame.__init__(self, **kw)
        self.parent = parent
        self.initUI()
        return

    def initUI(self):
        config = ConfigParser.ConfigParser()
        config.read('settings.ini')
        default_sheet = config.get('USER', 'default_spreadsheet')
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
        self.btnSubmit.grid(row=6, column=4, padx=5)

        self.btnCancel = Button(self, command=quit, text="Quit")
        self.btnCancel.grid(row=6, column=3)

        self.lblSheet = Label(self, text="Enter google sheets URL:")
        self.lblSheet.grid(row=5, sticky=W, pady=4, padx=4)

        self.sheetUrl = Entry(self)
        self.sheetUrl.grid(row=6, columnspan=3, sticky=W+E, padx=5, pady=5)
        self.sheetUrl.insert(0, default_sheet)
        return


    def submit_text(self):
        text = self.txtCsv.get("1.0", END)
        reader = RCLCReader()
        session = Session()
        db_objects = reader.read_csv_text(text, session)
        session.commit()
        return
