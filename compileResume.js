R = resumeContent;

$( document ).ready(function() {

// ------------------------ Tagline ------------------------
t = 3;
$('.main-header .tagline').html(R.tagline[t]);

// ------------------------ Objective ------------------------
$('#objective .content').text(R.objective);

// ------------------------ Summary  ------------------------
for (i = 0;  i<  R.summary.length; i++) {
	$("#summary ul").append("<li>" + R.summary[i] + "</li>");
}

// ------------------------ Experience  ------------------------
for (j = 0; j < R.experience.length; j++) {

	job = "<article class=\"job\" id=\"" + R.experience[j].company.toLowerCase() + "\"><div class=\"resume-content\">";
	
	job += "<div class=\"subsection-header\">";
	job += "<span class=\"title subsection-title\">" + R.experience[j].position + "</span>";
	job += "<span class=\"title subsection-company\"><a href=\"http://www." + R.experience[j].url + "\">" + R.experience[j].company + "</a></span>";
	job += "<span class=\"subsection-location\"> <span class =\"subsection-location-before\"> in </span> " + R.experience[j].location + "</span>";
	job += "<span class=\"subsection-duration\">" + R.experience[j].term + "</span>";
	job += "</div>";

	job += "<ul class=\"list resume-list\">";
	for (t = 0; t < R.experience[j].responsibilities.length; t++) {
		if (R.experience[j].responsibilities[t].task !== "")
			job += "<li class=\"resume-item\">" + R.experience[j].responsibilities[t].task + "</li>";
	}
	job += "</div> </article>"
	$("#experience").append(job);
}

// ------------------------ Projects   ------------------------
for (var p = 0; p < R.projects.length; p++){
	proj = "<article class=\"project\" id=\"" + R.projects[p].id + "\">";
	proj +=	"<div class=\"resume-content\">";
	proj += "<div class=\"subsection-header\">";
	proj += "<span class=\"title subsection-title\">" + R.projects[p].name + "</span>";
	proj += "<span class=\"subsection-duration\">" + R.projects[p].term + "</span>";
	proj += "</div>";
	proj += "<div class=\"content\">" + R.projects[p].description + "</div>";
	
	if (R.projects[p].responsibilities.length > 0) {
		proj += "<ul class=\"list project-list\">";

		for (r = 0; r < R.projects[p].responsibilities.length; r++){ 
			proj += "<li>" + R.projects[p].responsibilities[r].task + "</li>" 
		}
	}
	proj += "</ul></div></article>";
	$("#projects").append(proj);
}



// ------------------------ Skills  ------------------------
// Full Width, Left or Right?
rspace = $("#experience").height() - $("#projects").height();
if ( rspace >= 168)
	$('#skills').addClass('skills-rightcol');
else if ( rspace <= -102 )
	$('#skills').addClass('skills-leftcol');
else
	$('#skills').addClass('skills-fullwidth');	

for (var s = 0; s < R.skills.length; s++){
	skl_id = R.skills[s].toLowerCase().replace(/\s+/g, '');
	skl = "<li class=\" resume-item\" id=\"" + skl_id + "\">";
	skl += "<div class=\"app-logo\"></div><p class=\"app-name\">" + R.skills[s] + "</p>";
	skl += "</li>";

	$("#skills .skills-list").append(skl);
}

console.log("\n Compiled \n")
});






























