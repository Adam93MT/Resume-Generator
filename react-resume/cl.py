import sys
import os

fileName = str(sys.argv[0])
try:
	jobTitle = str(sys.argv[1])
except:
	jobTitle = "google ux iot"

def removeFirstPage(name):
	from PyPDF2 import PdfFileWriter, PdfFileReader
	infile = PdfFileReader(name, 'rb')
	output = PdfFileWriter()
	for x in xrange(infile.getNumPages()):
		if x is not(0):
			output.addPage(infile.getPage(x))
	with open(name, 'wb') as f:
	   output.write(f)

print "Compiling Cover Letter"
clName = "cover_letters/Adam Thompson - " + jobTitle.title() + ".pdf"
clName = clName.replace(" ", "\ ")

mdtext = ""
with open('cover_letters/' + jobTitle + '.md', 'r') as mdfile:
	for line in mdfile:
		newline = line.strip()
		if newline:
			newline = newline.replace("\'", "\\'")
			mdtext += newline + "\\n\\n"

# Since Prince doesn't do AJAX, 
# we need to save the .md file as a js variable which is loaded at runtime
with open('cover_letters/tmpcl.js', 'w') as tmpmdfile:
	tmpmdfile.write("clContent = '" + mdtext + "'")

# os.system("prince --javascript -s src/style/resume.css cover_letters/coverLetter.html " + clName)
# removeFirstPage(clName.replace("\ ", " "))