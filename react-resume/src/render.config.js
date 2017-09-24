 var path = require('path');
 
  module.exports = { 
    entry: {
      "index": {
         path: path.join(__filename, './../base.pug'),
         options: {
           "context": {path: path.join(__filename, "./../../lib/component"), props: {id: "1"}}
         }   
       }   
    },  
    output: {
      filename: "[name].html",
      path: path.join(__filename, "./../")
    }
  };