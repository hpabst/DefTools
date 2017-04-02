from Tkinter import *
from ttk import Frame, Button, Style, Entry, Scale
from models.rclc_reader import RCLCReader
from models.gsheets_writer import GSheetsWriter
from sqlalchemy.orm import Session
import ConfigParser
import re
import tkMessageBox
import sys
import traceback

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

        self.lblTsv = Label(self, text="Enter TSV Export:")
        self.lblTsv.grid(sticky=W, pady=4, padx=5)

        self.txtTsv = Text(self)
        self.txtTsv.grid(row=1, column=0, columnspan=2, rowspan=4, padx=5, sticky=E+W+N+S)

        self.btnSubmit = Button(self, text="Submit", command=self.submit_text)
        self.btnSubmit.grid(row=6, column=4, padx=5)

        self.btnUpload = Button(self, text="Upload to GS", command = self.upload_db)
        self.btnUpload.grid(row=6, column=3, padx=5)

        self.btnCancel = Button(self, command=quit, text="Quit")
        self.btnCancel.grid(row=6, column=2, padx=5)

        self.lblSheet = Label(self, text="Enter google sheets URL:")
        self.lblSheet.grid(row=5, sticky=W, pady=4, padx=4)

        self.sheetUrl = Entry(self)
        self.sheetUrl.grid(row=6, columnspan=2, sticky=W+E, padx=5, pady=5)
        self.sheetUrl.insert(0, default_sheet)
        return


    def submit_text(self):
        text = self.txtTsv.get("1.0", END)
        reader = RCLCReader()
        session = Session()
        try:
            db_objects, failed_lines = reader.read_tsv_text(text, session)
            session.commit()
            if len(failed_lines) > 0:
                errormsg = "{0} lines raised an error when reading data:\n".format(len(failed_lines))
                for line in failed_lines:
                    errormsg += line
                tkMessageBox.showerror("Error", errormsg)
            else:
                tkMessageBox.showinfo("Data Submission Complete", "All data has been submitted to DB successfully.")
        except Exception as e:
            ex_type, ex, tb = sys.exc_info()
            tkMessageBox.showerror("Error", "An error occured in reading the data: {0} {1}.\nTraceback: {2}.".format(e.message, str(e), traceback.format_tb(tb)))
        return


    def upload_db(self):
        session = Session()
        id_regex = "/spreadsheets/d/([a-zA-Z0-9-_]+)"
        id = re.search(id_regex, self.sheetUrl.get())
        if len(id.groups()) == 0:
            tkMessageBox.showerror("Error", "A valid google sheet ID could not be determined.")
        else:
            try:
                writer = GSheetsWriter(spreadsheet_id=id.group(1))
                writer.update_loot_spreadsheet(session)
            except Exception as e:
                tkMessageBox.showerror("Error", "An error occurred in uploading to google sheets: {0}".format(e.message))
            tkMessageBox.showinfo("", "Loot data has been uploaded to google spreadsheet.")
        return
