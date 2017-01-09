var skills = [ 'design', 'communication', 'sstarter', 'management', 'programming'];
var work = ['klick', 'cgis', 'team2056', 'emc'];
var cl = true;







var library = {};

library.skills = {
	web: '<label>Web Dev</label> HTML, CSS, Javascript, PHP, Angular.js, Backbone.js, Sails.js, Socket.io',
	robotics: '<label>Mechanical Design</label> FIRST Robotics Team for 8 years, SolidWorks, AutoCAD, Autodesk Inventor',
	electrical: '<label>Electrical</label> Circuit design, experience with lab equipment like oscilloscopes and frequency generators ',
	communication: '<label>Interpersonal</label> Strong communication skills, team player, enjoy presenting, high energy and positive attitude',
	sstarter: '<label>Self Starter</label> Several side projects including museum exhibits, micro-brewery branding and website design',
	programming: '<label>Programming</label> C++, java, Linux bash, SQL, Object-oriented C, C#, ASP.net, HTML, CSS',
	psolving: '<label>Problem Solving</label> Strong problem solving skills from much development experience, enjoy analyzing problems',
	management: '<label>Project Management</label> Exemplary leadership skills and ability to lead a project from concept to execution',
	modelling: '<label>Modelling</label> Experience with MatLab, understanding of statistical modelling through Probability and Statistics course',
	design: '<label>Creative Design</label> Adobe Photoshop, Adobe Illustrator, experience making infographics and presentation boards',
	human: '<label>Human Factors</label> task analysis, user testing, usability heuristics, persona creation, ergonomics',

	// web: 'Great expertise in web <b>theming</b> using <b>Bootstrap</b>, <b>CSS3</b>, <b>Adobe Dreamweaver</b> and <b>Adobe Photoshop</b>',
	// present: '<b>Presentation skills</b> strengthened through the creation of many <b>visual</b> presentations on Team 2056',
	// personas: 'Ability to develop <b>personas</b> and <b>user requirements</b> through <b>design class projects</b>',
	// leadership: 'Exemplary <b>leadership</b> skills shown through leading <b>sports teams</b>, <b>musical groups</b> and <b>robotics teams</b>',
	// psolving: 'Strong <b>problem solving</b> skills enhanced through web development for non-profit organizations',
	// design: 'Proficiency with <b>Autodesk Inventor</b>, <b>AutoCAD</b>, and <b>SolidWorks</b> developed through many <b>design projects</b>',
	// programming: 'Capability to use multiple programming languages; <b>C++</b>, <b>java</b>, <b>bash</b>, and <b>PHP</b>',
	// robotics: 'Great familiarity with <b>robotics systems</b> strengthened through eight years on a <b>FIRST Robotics Team</b>',
	// api: 'Very familiar with <b>API</b> development through Web API development in <b>C#</b> and <b>ASP.net</b>',
	// databases: 'Great experience in managing and developing databases using <b>MySQL</b>, <b>Sybase</b>, <b>Excel</b>, and <b>bash</b>',
	// git: 'Much practice in software development through <b>git</b> and <b>GitHub</b>. GitHub account: <b>IsaacHunter</b>',
	// js: 'Very comfortable in developing <b>javascript web apps</b> through development of <b>SLIMS 3.0</b> in <b>Angular.js</b>',
	// team: 'Enjoy working as a part of a <b>team</b>, whether it be on a design project or on a pickup hockey team',
	// sstarter: 'Passionate <b>self starter</b> shown through side projects including <b>museum exhibits</b> and <b>social marketing</b>',
	// algorithms: 'Exposure to <b>efficient algorithm development</b> through <b>algorithm classes</b> and much <b>software development</b>',
	// modeling: 'Understanding of <b>modeling</b> with <b>Excel</b> developed through many engineering <b>design projects</b>'
	extra: ''
};

library.work = {
	fellowship: {
		title: 'Website Manager',
		location: 'Fellowship GTA, Mississauga, ON',
		date: 'Feb 2013 - present',
		content: [
			'Gained experience in content management software Drupal',
			'Designed and developed simple, but professional looking websites',
			'Taught members of Fellowship GTA how to manage content on their new website'
		]
	},
	forestview: {
		title: 'Visual Leader and Webmaster',
		location: 'Forestview Community Church',
		date: '2009 - present',
		content: [
			"Learned how to make complicated systems user friendly by organization and using MySQL databases",
			"Ran Sunday morning effects, videos, and presentations and taught younger members to do the same",
			"Developed the church's website and taught administration how to use and edit website",
			"Formed sermon database and organized a recording and uploading process"
		]
	},
	emc : {
		title: 'Network Test Analyst',
		location: 'EMC Corporation, Burlington, ON',
		date: 'Jan - Apr 2013',
		content: [
			"Set up and automated tests using shell on virtual machines with both UNIX and Windows",
			"Communicated with staff members to organize the lab's virtual machines",
			"Created tutorial documents to explain testing procedures for new hires and co-op students"
		]
	},
	team2056 : {
		title: 'Robotics Team Mentor',
		location: 'FIRST Robotics Team 2056',
		date: '2007 - present',
		content: [
			"Aided in design process which included brainstorming and robot design in Solidworks",
			"Passed on experience in the design and creation of robots to high school students",
			"Led Team 2056 through presentations and essays to eventually win the Chairman's Award",
		]
	},
	gah : {
		title: 'Founder & Web Developer',
		location: 'Give A Hand',
		date: '2010 - 2012',
		content: [
			"Learned how to edit open source software and refine it to a customer's specific standards",
			"Co-created non-profit organization, Give A Hand",
			"Developed website using HTML and phpBulletinBoard software"
		]
	},
	cgis : {
		title: 'Project Manager & Dev',
		location: 'CGIS Spatial Solutions, Perth, ON',
		date: 'Sept - Dec 2013',
		content: [
			"Earned an <b>outstanding</b> evaluation for development of new projects, SLIMS and SLIMS Management 3.0",
			"Used twitter bootstrap and CSS styling to create new designs for SLIMS and SLIMS Management web apps",
			"Transformed SLIMS Management into a responsive web app using Angular JS and other javascript plugins",
			"Shared progress and tracked issues with development team using github and Trello boards"
		]
	},
	klick : {
		title: 'Full-Stack Developer',
		location: 'Klick Health, Toronto, ON',
		date: 'May - Aug 2014',
		content: [
			"Earned an <b>outstanding</b> evaluation for hard work and initiative shown through 50 billable-hour weeks",
			"Led front-end development of various websites and communicated progress to Project Managers",
			"Developed an online store using the Magento back-end with LESS and Javascript"
		]
	}
}

function init () {
	for (var i = 0; i < skills.length; i ++) 
	{
		$('#skills').append('<p class="skills">' + library.skills[skills[i]] + '</p>');
	}

	for (var i = 0; i < work.length; i ++)
	{
		var header = '';
		header += '<div class="date">' + library.work[work[i]].date + '</div>';
		header += '<div class="date-right clearfix"><h2>' + library.work[work[i]].title + '</h2>';
		header += '<h4>' + library.work[work[i]].location + '</h4></div>';

		var worklist = '';

		for (var j = 0; j < library.work[work[i]].content.length; j ++)
		{
			worklist += '<li>' + library.work[work[i]].content[j] + '</li>';
		}

		$('#experience').append('<div class="main-block clearfix">' + header + '<ul>' + worklist + '</ul></div>');

	}

	if (cl) {
		$('#cl').show();
	}
	else {
		$('#cl').hide();
	}
 
}