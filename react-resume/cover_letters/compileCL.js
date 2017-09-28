converter = new showdown.Converter()
text = clContent + "\n\n Sincerely,"
html = converter.makeHtml(text);

$(document).ready(function(){
	$('.cover_letter_content').html(html)
});

