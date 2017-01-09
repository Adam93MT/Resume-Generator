# resume
My HTML resume

#Requirements
- [Prince XML](http://www.princexml.com)


# To Generate
1) Write all possible content in `resources/jsonContent.json`

2) Create a `tagMap.csv` file that maps the Keywords to look for in a job description to all your tags

3) Add tags to your resume content file where applicable

4) Paste a job description into `<job title>.txt` file and save it in `job_descriptions/`

5) run command `python generateResume.py "<job title>"`

6) Prince will automatically generate your PDF resume tailored to that job description

You may need to tweak some things to make it your own
