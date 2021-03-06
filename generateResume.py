import sys
import os
import csv
import json
from pprint import pprint

fileName = str(sys.argv[0])
jobTitle = str(sys.argv[1])
try:
	arg2 = sys.argv[2]
except:
	arg2 = False

jobDescriptionFile = "job_descriptions/" + jobTitle + ".txt"
if not(os.path.isfile(jobDescriptionFile)):
	jobDescriptionFile = "job_descriptions/applied/" + jobTitle + ".txt"
try:
	jobDescription = open(jobDescriptionFile, 'r').read().lower()
except Exception as e:
	print "Can't load file"
	raise e

MAX_BULLETS = 4
MAX_BULLETS_PROJ = 3
MAX_JOBS = 3
MAX_SKILLS = 10

ShowCourses = False
CourseDescriptions = False

keywords = []
tags = []	
tagMap = []

def removeFirstPage(name):
	from PyPDF2 import PdfFileWriter, PdfFileReader
	infile = PdfFileReader(name, 'rb')
	output = PdfFileWriter()
	for x in xrange(infile.getNumPages()):
		if x is not(0):
			output.addPage(infile.getPage(x))
	with open(name, 'wb') as f:
	   output.write(f)

# Parse Job Description
with open('resources/tagMap.csv', 'rb') as csvfile:
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

tagCount = [0] * len(tags)
for w,word in enumerate(keywords):
	word = word.lower()
	wordCount = jobDescription.count(word)
	for t in tagMap[w]:
		if wordCount > 0:
			tagCount[t] += wordCount
		if t < 0:
			tagCount[-t] -= 10

with open('resources/resumeContent.json') as jsonfile:    
    resumeContent = json.load(jsonfile)
	# JSON must be in proper format

def iterateTags(tagsList):
	weightListElement = 0
	for tag in tagsList:
		if tag in tags:
			idx = tags.index(tag)
		else:
			idx = -1
		weightListElement += tagCount[idx]
	return weightListElement

# print ", ".join(tags)
# Iterate through the resume setions & select appropriate text
toSave = {}
if not(os.path.isfile("job_descriptions/json/" + jobTitle + '.json')) or ("f" in sys.argv):
	if "f" in sys.argv:
		print "Forcing re-parse"
	for item in resumeContent:
		# Tagline
		if item == "tagline":
			toSave[item] = resumeContent[item][0]
		# Objective
		elif item == "objective":
			toSave[item] = resumeContent[item]
		# Summary
		elif item == "summary":
			# Decide which Summary elememts to use
			SummaryToSave = []
			for x in xrange(0,MAX_BULLETS):
				SummaryToSave.append(resumeContent[item][x]["blurb"])
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

				# Decide what the job title should be
				if (not(isinstance(job["position"], (str, unicode) ) and len(job["position"]) > 1 )):
					topTag = tags[tagCount.index(max(tagCount))]
					nameIsSet = False
					for n,name in enumerate(job["position"]):
						if name.lower() in jobTitle.lower():
							jobsToSave[j]["position"] = (job["position"][n])
							nameIsSet = True
							break
						elif topTag.lower() in name.lower() and not(nameIsSet):
							jobsToSave[j]["position"] = (job["position"][n])
							break
					if not("position" in jobsToSave[j]):
						jobsToSave[j]["position"] = (job["position"][0])
				else:
					jobsToSave[j]["position"] = (job["position"])

				# Decide which responsibilities to highlight
				for t, task in enumerate(job["responsibilities"]):
					for tag in task["tags"]:
						if tag in tags:
							idx = tags.index(tag)
						if tagCount[idx] > 0:
							taskWeight[t] += tagCount[idx]

				jobsToSave[j]["responsibilities"] = []
				for x in xrange(0,MAX_BULLETS):
					max_idx = taskWeight.index(max(taskWeight))
					if max(taskWeight) == 0:
						break
					jobsToSave[j]["responsibilities"].append(job["responsibilities"][max_idx]["task"])
					taskWeight[max_idx] = 0
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
					
					if "responsibilities" in proj:
						projectsToSave[i]["responsibilities"] = []
						for x in xrange(0, MAX_BULLETS_PROJ):
							if max(taskWeight[p]) == 0 and projectsToSave[i]["responsibilities"] <= 3:
									break
							max_idx = taskWeight[p].index(max(taskWeight[p]))
							projectsToSave[i]["responsibilities"].append(proj["responsibilities"][max_idx]["task"])
							taskWeight[p][max_idx] = 0
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
				max_idx = skillWeight.index(max(skillWeight))
				skillsToSave.append(resumeContent[item][max_idx][0])
				skillWeight[max_idx] = 0

			toSave[item] = skillsToSave

		elif item == "clubs":
			toSave[item] = resumeContent[item]
else:
	print "Data Already Exists. Rebuilding."
	with open("job_descriptions/json/" + jobTitle + '.json', 'r') as infile:
		toSave = json.load(infile)
				
toSave["showCourses"] = ShowCourses
toSave["courseDescriptions"] = CourseDescriptions

# Save the file
with open('resources/tmpdata.json', 'w') as outfile:
    json.dump(toSave, outfile, indent=4, sort_keys=True)
with open('resources/tmpdata.json', 'r') as og:
	data = og.read()
with open('resources/tmpdata.js', 'w') as outfile:
	outfile.write("resumeContent = " + data)

pdfName = "compiled/Adam Thompson Resume - " + jobTitle.title() + ".pdf"
pdfName = pdfName.replace(" ", "\ ")

# Compile pdf Resume
os.system("prince --javascript -s resume-style.css resume.html " + pdfName)
# Once the pdf is compiled, remove the first page that has the watermark
removeFirstPage(pdfName.replace("\ ", " "))

with open("job_descriptions/json/" + jobTitle + '.json', 'w') as outfile:
	json.dump(toSave, outfile, indent=4, sort_keys=True)


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

	# Since Prince doesn't do AJAX, we need to save the .md file as a js variable which is loaded at runtime
	with open('cover_letters/tmpcl.js', 'w') as tmpmdfile:
		tmpmdfile.write("clContent = '" + mdtext + "'")

	os.system("prince --javascript -s resume-style.css coverLetter.html " + clName)
	removeFirstPage(clName.replace("\ ", " "))
