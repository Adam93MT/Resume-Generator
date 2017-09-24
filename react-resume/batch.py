import os
import sys
args = ""

if "f" in sys.argv:
	args += " f"

for file in os.listdir("./job_descriptions"):
    if file.endswith(".txt"):
        file = file.replace(".txt", "")
        print ""
        print file
        os.system("python compile.py \"" + file + "\"" + args)