R = resumeContent;
$( document).ready(function() {
	$.getJSON("resources/data.json", function(data) {
		R = data;
		console.log("AJAX");
	})
	.fail(function() {
		console.log('No AJAX')
		R = resumeContent;
	}).always(function() {
		console.log("Compiling...")
		compileResume(R);
	});
});

function compileResume(R) {
	R_Col_Height = 0;
	L_Col_Height = 0;

	// ------------------------ Tagline ------------------------
	$('.main-header .tagline').html(R.tagline);

	// ------------------------ Objective ------------------------
	// $('#objective .content').text(R.objective);
	// L_Col_Height += $('#objective').height();

	// ------------------------ Summary  ------------------------
	for (i = 0;  i<  R.summary.length; i++) {
		$("#summary .resume-content ul").append("<li>" + R.summary[i] + "</li>");
	}
	$("#summary").addClass('col-left')
	R_Col_Height += $('#summary').height();

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
			if (t > 4)
				break
			if (R.experience[j].responsibilities[t].task !== "")
				job += "<li class=\"resume-item\">" + R.experience[j].responsibilities[t] + "</li>";
		}
		job += "</div> </article>"
		$("#experience").append(job);
		if (j > 1) {
			break
		}
	}
	$('#experience').addClass('col-left')
	L_Col_Height += $("#experience").height();

	// ------------------------ Projects   ------------------------
	for (var p = 0; p < R.projects.length; p++){
		proj = "<article class=\"project\" id=\"" + R.projects[p].id + "\">";
		proj +=	"<div class=\"resume-content\">";
		proj += "<div class=\"subsection-header\">";
		proj += "<span class=\"title subsection-title\">" + R.projects[p].name + "</span>";
		proj += "<span class=\"subsection-duration\">" + R.projects[p].term + "</span>";
		proj += "</div>";
		proj += "<div class=\"content\">" + R.projects[p].description + "</div>";
		
		if (R.projects[p].responsibilities) {
			proj += "<ul class=\"list project-list\">";

			for (r = 0; r < R.projects[p].responsibilities.length; r++){ 
				if (R.projects[p].responsibilities[r].task !== "" && r <= 4) {
					proj += "<li>" + R.projects[p].responsibilities[r] + "</li>";
				} 
			}
		}
		proj += "</ul></div></article>";
		$("#projects").append(proj);

		if (p > 2) {
			break
		}
	}
	$('#projects').addClass('col-right')
	$('#projects').insertBefore('#experience')
	R_Col_Height += $("#projects").height();


	// ------------------------ Skills  ------------------------
	// Full Width, Left or Right?
	// rspace = L_Col_Height - R_Col_Height;
	// if ( rspace >= 144)
	// 	$('#skills').addClass('skills-rightcol');
	// else if ( rspace <= -96 )
	// 	$('#skills').addClass('skills-leftcol');
	// else
		$('#skills').addClass('skills-fullwidth');	

	for (var s = 0; s < R.skills.length; s++){
		skl_id = R.skills[s][1][0].toLowerCase().replace(/\s+/g, ''); // The first tag is the skill id
		skl = "<li class=\" resume-item\" id=\"" + skl_id + "\">";
		skl += "<div class=\"app-logo\"></div><p class=\"app-name\">" + R.skills[s][0] + "</p>";
		skl += "</li>";

		$("#skills .skills-list").append(skl);
	}

	// if (rspace < 0) {
	// 	$("#skills").css("margin-top","-4px");
	// }


	// ------------------------ Education ------------------------
	for (var e = 0; e < R.education.length; e++){
		edu = "<article class=\"school\" id=\"" + R.education[e].id + "\">";
		edu += "<div class=\"resume-content\">"
		edu += "<div class=\"subsection-header\">";
		edu += "<span class=\"title subsection-school\">";
		if (R.education[e].url)
			edu += "<a href=\"http://www." + R.education[e].url + "\">"
		edu += R.education[e].school;
		if (R.education[e].url) 
			edu += "</a>";
		edu += "</span>";

		if (R.showCourses) {
			edu += "<span class=\"title subsection-degree\">"
			// if (getFullYear() >= 2017) {
				edu += R.education[e].degree + " ";
			// }
			edu += R.education[e].program + ", ";
			edu += "<span class=\"minor\">";
			edu += "Minor in " + R.education[e].minor;
			edu += "</span></span></div>"

			// if show_courses &&
			edu += "<ul class=\"list course-list "
			if (R.courseDescriptions) {
				edu += "titles-only\">"
				for (c in R.education[e].courses) {
					edu +="<li class=\"course\">"
					edu +="<span class=\"title course-title\">";
					edu += R.education[e].courses[c].name + "</span>";
					edu += "<span class=\"course-code\"> ("
					edu += R.education[e].courses[c].code + ")</span>";
					edu += "<div class=\"list-description\">"
					edu += R.education[e].courses[c].description + "</div></li>";
				}
				edu += "</ul>";
			}
		}
		else {
			edu += "</div><div class=\"content\">"
			edu += R.education[e].degree + " " 
			edu += R.education[e].program + ", "//<br/>"
			edu += R.education[e].minor + " minor"
			$("#education").addClass("edu-one-line")
			// $("#education").addClass("edu-club-line")
			// $("#clubs").addClass("edu-club-line")

		}
		edu += "</div></article>"
		$("#education").append(edu);
	}

	// ------------------------ Clubs & Groups ------------------------
	for (var g = 0; g < R.clubs.length; g++) {
		clb = "<article class=\"club\" id=\"" + R.clubs[g].id + "\">"
		clb += "<div class=\"resume-content\">"
		clb += "<div class=\"subsection-header\">"
		clb += "<span class=\"title subsection-clubname\">"
		clb += R.clubs[g].name
		clb += "</span><span class=\"subsection-duration\">"
		clb += R.clubs[g].term
		clb += "</span></div>"
		clb += "<div class=\"content\">"
		clb += R.clubs[g].description
		clb += "</div></div></article>"

		$("#clubs").append(clb)
		$("#clubs").addClass("col-right")

	}

	console.log("Compiled.")
}


