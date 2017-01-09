import sys
import os
import csv
import json
from pprint import pprint

fileName = str(sys.argv[0])
jobTitle = str(sys.argv[1])

jobDescriptionFile = "job_descriptions/" + jobTitle + ".txt"
jobDescription = open(jobDescriptionFile, 'r').read().lower()


ShowCourses = False
CourseDescriptions = False

keywords = []
tags = []	
tagMap = []

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
			# print str(tags[-t]) + str(tagCount[-t])
		# if t == 1:
		# 	print tags[t] + " " + word + " " + str(wordCount)

# for t,tag in enumerate(tags):
# 	print str(tag) + "[" + str(t) + "] : " + str(tagCount[t])

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

# Iterate through the resume setions & select appropriate text
toSave = {}
if not(os.path.isfile(jobTitle + '.json')):
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
			# blurbWeight = [0] * len(resumeContent[item])
			# for b,blurb in enumerate(resumeContent[item]):
			# 	for tag in blurb["tags"]:
			# 		if tag in tags:
			# 			idx = tags.index(tag)
			# 		if tagCount[idx] > 0:
			# 			blurbWeight[b] += tagCount[idx]
			# 	print str(blurb["blurb"]) + " " + str(blurbWeight[b]) + "\n"
			for x in xrange(0,4):
				# max_idx = blurbWeight.index(max(blurbWeight))
				SummaryToSave.append(resumeContent[item][x]["blurb"])
				# blurbWeight[max_idx] = 0
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
				for x in xrange(0,4):
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
				del projRank[projRank.index(x)]
			projRank = [projRank[0], projRank[1]]

			i = 0
			for p,proj in enumerate(resumeContent[item]):
				projectsToSave[i] = {}

				if p in defaultProjects or p in projRank:
					projectsToSave[i]["id"] = proj["id"]
					projectsToSave[i]["name"] = proj["name"]
					projectsToSave[i]["term"] = proj["term"]
					projectsToSave[i]["description"] = proj["description"]
					
					if "responsibilities" in proj:
						projectsToSave[i]["responsibilities"] = []
						for x in xrange(0,2):
							if max(taskWeight[p]) == 0:
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
						for x in xrange(0,4):
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
			for x in xrange(0,10):
				max_idx = skillWeight.index(max(skillWeight))
				skillsToSave.append(resumeContent[item][max_idx])
				skillWeight[max_idx] = 0

			toSave[item] = skillsToSave

		elif item == "clubs":
			toSave[item] = resumeContent[item]
# else:
# 	with open(jobTitle + '.json', 'r') as infile:
# 		toSave = json.load(infile)

				
toSave["showCourses"] = ShowCourses
toSave["courseDescriptions"] = CourseDescriptions

# Save the file
with open('resources/data.json', 'w') as outfile:
    json.dump(toSave, outfile, indent=4, sort_keys=True)
with open('resources/data.json', 'r') as og:
	data = og.read()
with open('resources/data.js', 'w') as outfile:
	outfile.write("resumeContent = " + data)

pdfName = "compiled/Adam Thompson Resume - " + jobTitle.title() + ".pdf"
pdfName = pdfName.replace(" ", "\ ")

# Compile pdf Resume
os.system("prince --javascript -s resume-style.css resume.html " + pdfName)

with open("job_descriptions/" + jobTitle + '.json', 'w') as outfile:
	json.dump(toSave, outfile, indent=4, sort_keys=True)





