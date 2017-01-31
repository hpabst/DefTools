from views.Open import Open
from Tkinter import *
from constants import DBConst
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import *



def main():
    DBConst.engine = create_engine('sqlite:///db/deftools.db')
    Base.metadata.bind = DBConst.engine
    DBSession = sessionmaker(bind=DBConst.engine)
    DBConst.session = DBSession()
    root = Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("{0}x{1}+0+0".format(int(w/2), (int(h/2))))
    open = Open(root)
    root.mainloop()
    DBConst.session.commit()
    return


if __name__ == "__main__":
    main()