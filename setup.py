import sys
from cx_Freeze import setup, Executable

include_files = ["autorun.inf"]
base = None

if sys.platform == "win32":
    base = "win32GUI"

setup(name="run this", version="0.1", description="don't run this",
      options={"build.exe": {"include_files": include_files}},
      executables=[Executable("client.py", base=base)])
