from views.Open import Open
from Tkinter import *
from constants import DBConst
import ConfigParser
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import BaseHTTPServer #without import, py2exe fails to include module for google API use.
import sqlalchemy.sql.default_comparator #needed for py2exe
from db.models import *



def main():
    engine = create_engine(DBConst.conn_str)
    Base.metadata.bind = engine
    root = Tk()
    root.wm_title("DefTools")
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("{0}x{1}+0+0".format(int(w/2), (int(h/2))))
    initSettings()
    initDB()
    open = Open(root)
    root.mainloop()
    return

def initSettings():
    config = ConfigParser.ConfigParser()
    config.read('settings.ini')
    if 'USER' not in config.sections():
        config.add_section('USER')
        config.set('USER', 'default_spreadsheet', '')
        fp = open('settings.ini', 'w+')
        config.write(fp)
        fp.close()
    return

def initDB():
    if not os.path.isfile("./deftools.db"):
        engine = create_engine('sqlite:///deftools.db')
        Base.metadata.create_all(engine)
    return


if __name__ == "__main__":
    main()