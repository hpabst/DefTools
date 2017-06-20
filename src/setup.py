from distutils.core import setup
import py2exe

data_files = [("", ["client_id.json", "client_secret.json"]),
              ("", ["cacerts.txt"])]
setup(console=['DefTools.py'], data_files=data_files)