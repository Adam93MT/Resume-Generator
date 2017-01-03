import sys
import os
import csv
import json
from pprint import pprint

fileName = str(sys.argv[0])
jobDescriptionFile = str(sys.argv[1])
jobTitle = jobDescriptionFile

ShowCourses = True
CourseDescriptions = False

keywords = []
tags = []
tagMap = []

with open('resources/skillsMap.csv', 'rb') as csvfile:
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
# print keywords
# print '\n'
# print tags
# print '\n'
# print tagMap

jobDescription = open(jobDescriptionFile, 'r').read().lower()

tagCount = [0] * len(tags)
for w in xrange(0,len(keywords)-1):
	word = keywords[w].lower()
	wordCount = jobDescription.count(word)
	for t in xrange(0,len(tagMap[w]) - 1):
		tagCount[t] += wordCount

with open('resources/resumeContent.json') as jsonfile:    
    resumeContent = json.load(jsonfile)
	# JSON must be in proper format

# Iterate through the resume setions & select appropriate text
toSave = {}
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
		blurbWeight = [0] * len(resumeContent[item])
		for b,blurb in enumerate(resumeContent[item]):
			for tag in blurb["tags"]:
				if tag in tags:
					idx = tags.index(tag)
				if tagCount[idx] > 0:
					blurbWeight[b] += tagCount[idx]
		for x in xrange(0,4):
			max_idx = blurbWeight.index(max(blurbWeight))
			SummaryToSave.append(resumeContent[item][max_idx]["blurb"])
			blurbWeight[max_idx] = 0
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
				isInName = 0
				for n,name in enumerate(job["position"]):
					if name.lower() in jobTitle.lower() and not(isInName):
						isInName = 1
						jobsToSave[j]["position"] = (job["position"][n])
						break
					if topTag.lower() in name.lower() and not(isInName):
						isInName = 1
						jobsToSave[j]["position"] = (job["position"][n])
				if not(isInName):
					jobsToSave[j]["position"] = (job["position"][0])
					break
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
		for p,proj in enumerate(resumeContent[item]):
			projectsToSave[p] = {}
			projWeight = [0] * len(proj["responsibilities"])

			if "id" in proj:
				projectsToSave[p]["id"] = proj["id"]
			projectsToSave[p]["name"] = proj["name"]
			projectsToSave[p]["term"] = proj["term"]
			projectsToSave[p]["description"] = proj["description"]

			for t, task in enumerate(proj["responsibilities"]):
				for tag in task["tags"]:
					if tag in tags:
						idx = tags.index(tag)
					if tagCount[idx] > 0:
						projWeight[t] += tagCount[idx]
			
			if len(projWeight) > 0: # if there are tags
				projectsToSave[p]["responsibilities"] = []
				for x in xrange(0,8):
					if max(projWeight) == 0:
						break
					max_idx = projWeight.index(max(projWeight))
					projectsToSave[p]["responsibilities"].append(proj["responsibilities"][max_idx]["task"])
					projWeight[max_idx] = 0
		
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
					for tag in course["tags"]:
						if tag in tags:
							idx = tags.index(tag)
						if tagCount[idx] > 0:
							courseWeight[c] += tagCount[idx]
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
			for tag in skill[1]:
				if tag in tags:
					idx = tags.index(tag)
				if tagCount[idx] > 0:
					skillWeight[s] += tagCount[idx]
			if str(skill).lower() in jobDescription:
				skillWeight[s] += 100

		for x in xrange(0,10):
			max_idx = skillWeight.index(max(skillWeight))
			skillsToSave.append(resumeContent[item][max_idx][0])
			skillWeight[max_idx] = 0

		toSave[item] = skillsToSave

# Save the file
with open('resources/data.json', 'w') as outfile:
    json.dump(toSave, outfile, indent=4, sort_keys=True)
with open('resources/data.json', 'r') as og:
	data = og.read()
with open('resources/data.js', 'w') as outfile:
	outfile.write("resumeContent = " + data)

# Compile pdf Resume
os.system("prince --javascript -s resume-style.css resume.html Adam\ Thompson\ -\ Resume.pdf")






















