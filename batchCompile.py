import os
for file in os.listdir("./job_descriptions"):
    if file.endswith(".txt"):
        file = file.replace(".txt", "")
        print ""
        print file
        os.system("python generateResume.py \"" + file + "\"")