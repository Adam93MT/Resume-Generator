var fs = require('fs'),
    args = require('system').args,
    page = require('webpage').create();
 
page.content = fs.read(args[1]);
page.viewportSize = {width: 600, height: 600};
page.paperSize = {
    format: 'Letter',
    orientation: 'portrait',
    // margin: '1cm'
    // footer: {
    //     height: '1cm',
    //     contents: phantom.callback(function (pageNum, numPages) {
    //         return '<div style="text-align: right; font-size: 12px;">' + pageNum + ' / ' + numPages + '</div>';
    //     })
    }
};
 
window.setTimeout(function() {
    page.render(args[1]);
    phantom.exit();
}, 250);