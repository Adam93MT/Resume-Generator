import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import registerServiceWorker from './registerServiceWorker';
// import Prince from "prince";


ReactDOM.render(
	<App />, 
	document.getElementById('root')
);
registerServiceWorker();

// Prince()
//     .inputs("../public/index.html")
//     .output("test.pdf")
//     .execute();