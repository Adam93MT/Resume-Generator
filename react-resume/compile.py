import sys
import os
import csv
import json
import urllib2

RESOURCE_PATH = "./src/resource/"
JD_PATH = "./job_descriptions/"

# jsonPath = "http://adamthompson.ca/Resume/resumeContent.json"
jsonPath = "http://localhost:9999/Resume-Generator/react-resume/src/resource/resumeContent.json"
jsonfile = urllib2.urlopen(jsonPath)
resumeContent = json.load(jsonfile)

if 'default' in sys.argv:
	with open(RESOURCE_PATH + "tmpdata.json", 'w') as outfile:
	    json.dump(resumeContent, outfile, indent=4, sort_keys=True)
	sys.exit()

# Setup and load files
fileName = str(sys.argv[0])
try:
	jobTitle = str(sys.argv[1])
except:
	jobTitle = "google ux iot"

try:
	arg2 = sys.argv[2]
except:
	arg2 = False

jobDescriptionFile = JD_PATH + jobTitle + ".txt"
if not(os.path.isfile(jobDescriptionFile)):
	jobDescriptionFile = JD_PATH + "archive/" + jobTitle + ".txt"

try:
	jobDescription = open(jobDescriptionFile, 'r').read().lower()
except Exception as e:
	print "Can't load file"
	raise e

# Settings
MAX_BULLETS = 4
MAX_BULLETS_PROJ = 3
MAX_JOBS = 3
MAX_SKILLS = 11

ShowCourses = False
CourseDescriptions = False
SmartSections = ['skills']

# Setup some global vars
keywords = []
tags = []	
tagMap = []

# A hack to remove Prince's watermark
def removeFirstPage(name):
	from PyPDF2 import PdfFileWriter, PdfFileReader
	infile = PdfFileReader(name, 'rb')
	output = PdfFileWriter()
	for x in xrange(infile.getNumPages()):
		if x is not(0):
			output.addPage(infile.getPage(x))
	with open(name, 'wb') as f:
	   output.write(f)

# A list iterator
def iterateTags(tagsList):
	weightListElement = 0
	for tag in tagsList:
		if tag in tags:
			idx = tags.index(tag)
		else:
			idx = -1
		weightListElement += tagCount[idx]
	return weightListElement

# Parse Job Description file
with open(RESOURCE_PATH + 'tagMap.csv', 'rb') as csvfile:
	CSVreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in CSVreader:
		if row[0] == "TAGS":
			tags = row
			del tags[0]
		else:
			keywords.append(row[0])
			tagMap.append([])
			i = len(keywords) - 1;
			for j in xrange(1,len(row)):
				if row[j] == "x":
					tagMap[i].append(j-1)
				elif row[j] == "-":
					tagMap[i].append(-(j-1))

# 
tagCount = [0] * len(tags)
for w,word in enumerate(keywords):
	word = word.lower()
	wordCount = jobDescription.count(word)
	for t in tagMap[w]:
		if wordCount > 0:
			tagCount[t] += wordCount
		if t < 0:
			tagCount[-t] -= 10

# print ", ".join(tags)
# Iterate through the resume setions & select appropriate text
toSave = {}
if not(os.path.isfile(JD_PATH + "json/" + jobTitle + '.json')) or ("f" in sys.argv):
	if "f" in sys.argv:
		print "Forcing JSON Rebuild"
	else:
		print "Building JSON"

	for item in resumeContent:
		if item == 'bio':
			toSave[item] = resumeContent[item]
		# Summary
		elif item == "summary":
			# Decide which Summary elememts to use
			SummaryToSave = []
			for x in xrange(0,MAX_BULLETS):
				SummaryToSave.append(resumeContent[item][x]['text'])
			toSave[item] = SummaryToSave

		# Experience
		elif item == "experience":
			jobsToSave = [None] * len(resumeContent[item])
			for j,job in enumerate(resumeContent[item]):
				jobsToSave[j] = {}
				taskWeight = [0] * len(job["responsibilities"])

				jobsToSave[j]["company"] = (job["company"])
				jobsToSave[j]["url"] = (job["url"])
				jobsToSave[j]["term"] = (job["term"])
				jobsToSave[j]["location"] = (job["location"])
				jobsToSave[j]["position"] = (job["position"])

				# Decide which responsibilities to highlight
				for t, task in enumerate(job["responsibilities"]):
					for tag in task['tags']:
						if tag in tags:
							idx = tags.index(tag)
						if tagCount[idx] > 0:
							taskWeight[t] += tagCount[idx]

				jobsToSave[j]["responsibilities"] = []
				for x in xrange(0,MAX_BULLETS):
					if item in SmartSections:
						max_idx = taskWeight.index(max(taskWeight))
						if max(taskWeight) == 0:
							break
						jobsToSave[j]["responsibilities"].append(job["responsibilities"][max_idx]['text'])
						taskWeight[max_idx] = 0
					else:
						jobsToSave[j]["responsibilities"].append(job["responsibilities"][x]['text'])
			toSave[item] = jobsToSave
		
		# Projects
		elif item == "projects":
			projectsToSave = [None] * len(resumeContent[item])
			projWeight = [0] * len(resumeContent[item])
			taskWeight = [0] * len(resumeContent[item])
			# Assign weights to each project
			for p,proj in enumerate(resumeContent[item]):
				if "tags" in proj:
					projWeight[p] = iterateTags(proj["tags"])
				elif "responsibilities" in proj:
					taskWeight[p] = [0] * len(proj["responsibilities"])
					for t, task in enumerate(proj["responsibilities"]):
						taskWeight[p][t] = iterateTags(task["tags"])
					projWeight[p] = sum(taskWeight[p])/float(len(proj["responsibilities"]))

			# Which projects to put in
			projRank = []
			max_idx = 0
			for x in enumerate(projWeight):
				max_idx = projWeight.index(max(projWeight))
				projRank.append(max_idx)
				projWeight[max_idx] = 0
			defaultProjects = [0,1] # Indexes of always-in projects
			for x in defaultProjects:
				try:
					del projRank[projRank.index(x)]
				except:
					print len(projRank)
			projRank = [projRank[0], projRank[1]]

			i = 0
			for p,proj in enumerate(resumeContent[item]):
				projectsToSave[i] = {}

				if p in defaultProjects or p in projRank:
					projectsToSave[i]["id"] = proj["id"]
					projectsToSave[i]["name"] = proj["name"]
					projectsToSave[i]["term"] = proj["term"]
					projectsToSave[i]["description"] = proj["description"]
					projectsToSave[i]["url"] = proj["url"]
					
					if len(proj["responsibilities"]) > 0:
						projectsToSave[i]["responsibilities"] = []
						for x in xrange(0, MAX_BULLETS_PROJ):
							if item in SmartSections:
								if max(taskWeight[p]) == 0 and projectsToSave[i]["responsibilities"] <= 3:
									break
								max_idx = taskWeight[p].index(max(taskWeight[p]))
								projectsToSave[i]["responsibilities"].append(proj["responsibilities"][max_idx]['text'])
								taskWeight[p][max_idx] = 0
							else: 
								projectsToSave[i]["responsibilities"].append(proj["responsibilities"][x]['text'])
					else:
						projectsToSave[i]["responsibilities"] = []
					i += 1
			toSave[item] = projectsToSave
		
		# Education
		elif item == "education":
			eduToSave = [None] * len(resumeContent[item])
			for s,school in enumerate(resumeContent[item]):
				if s > 0 and not("french" in jobDescription):
					del eduToSave[s]
					break
				eduToSave[s] = {}
				eduToSave[s]["id"] = school["id"]
				eduToSave[s]["url"] = school["url"]
				eduToSave[s]["school"] = school["school"]
				eduToSave[s]["program"] = school["program"]
				eduToSave[s]["degree"] = school["degree"]
				eduToSave[s]["minor"] = school["minor"]

				if ShowCourses:
					courseWeight = [0] * len(school["courses"])
					for c,course in enumerate(school["courses"]):
						courseWeight[c] = iterateTags(course["tags"])
					if len(school["courses"]) > 0 and max(courseWeight) > 0:
						eduToSave[s]["courses"] = [None] * 4
						for x in xrange(0,MAX_BULLETS):
							if max(courseWeight) == 0:
								break
							eduToSave[s]["courses"][x] = {}
							max_idx = courseWeight.index(max(courseWeight))
							eduToSave[s]["courses"][x]["name"] = (school["courses"][max_idx]["name"])
							eduToSave[s]["courses"][x]["code"] = (school["courses"][max_idx]["code"])
							if CourseDescriptions: 
								eduToSave[s]["courses"][x]["description"] = (school["courses"][max_idx]["description"])
							courseWeight[max_idx] = 0
					
			toSave[item] = eduToSave
		
		# Skills
		elif item == "skills":
			skillsToSave = []
			skillWeight = [0] * len(resumeContent[item])
			for s,skill in enumerate(resumeContent[item]):
				skillWeight[s] = iterateTags(skill[1])
				# print str(skill[0]) + " " + str(skillWeight[s])
			for x in xrange(0,MAX_SKILLS):
				if item in SmartSections:
					max_idx = skillWeight.index(max(skillWeight))
					skillsToSave.append(resumeContent[item][max_idx][0])
					skillWeight[max_idx] = 0
				else:
					skillsToSave.append(resumeContent[item][x][0])

			toSave[item] = skillsToSave

		elif item == "clubs":
			toSave[item] = resumeContent[item]
else:
	print "JSON Already Exists. Refreshing."
	with open(JD_PATH + "json/" + jobTitle + '.json', 'r') as infile:
		toSave = json.load(infile)
				
toSave["showCourses"] = ShowCourses
toSave["courseDescriptions"] = CourseDescriptions


# -------------------- EXPORTING ------------------- #

# # Prep the pdf filename
pdfName = "Adam Thompson Resume - " + jobTitle.title() + ".pdf"
pdfName = pdfName.replace(" ", "\ ")

# Save the json file
with open(RESOURCE_PATH + "tmpdata.json", 'w') as outfile:
    json.dump(toSave, outfile, indent=4, sort_keys=True)

print "Printing PDF" 
# Have to use apple script to print
os.system("osascript printPDF.scpt " + pdfName)

# save the html
# with open(RESOURCE_PATH + 'tmphtml.html', 'w') as outfile:
# 	outfile.write(html_source)	

# Run Prince
# os.system("prince --javascript " + RESOURCE_PATH + "tmphtml.html " + pdfName)

# Save a Word file
# if ("word" in sys.argv[2:]):
	# import pandoc
	# from selenium import webdriver
	# browser = webdriver.Firefox()
	# url = 'resume.html'
	# browser.get(url)
	# html_source = browser.page_source
	# print html_source
	# with open('tmphtml.html', 'w') as outfile:
	# 	outfile.write(html_source)
	# pandoc.convert_file('tmphtml.html', 'docx', outputfile=jobTitle.title()+".docx")	

# Compile pdf Resume
# def exportPrince():
# 	os.system("prince --javascript -s resume-style.css resume.html " + pdfName)
# 	# Once the pdf is compiled, remove the first page that has the watermark
	# removeFirstPage(pdfName.replace("\ ", " "))

# -------------------- CLEANUP ------------------- #
# Move the txt file to archive
os.rename(jobDescriptionFile, JD_PATH + 'archive/' + jobTitle + ".txt")

# Save the json file for future reference
with open(JD_PATH + "json/" + jobTitle + '.json', 'w') as outfile:
	json.dump(toSave, outfile, indent=4, sort_keys=True)


# -------------------- COVER LETTER ------------------- #
# Do we need to build a cover letter too?
if ("cl" in sys.argv): 
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

	os.system("prince --javascript -s resume-style.css coverLetter.html " + clName)
	removeFirstPage(clName.replace("\ ", " "))
