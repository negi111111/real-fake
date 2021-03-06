'use strict';

function predict(prediction) {
	const request = new XMLHttpRequest();
	request.onreadystatechange = function() {
		if (request.readyState === XMLHttpRequest.DONE) {
			if (request.status === 200) {
				const response = JSON.parse(request.responseText);
				console.info(response);
				window.location.replace(response.new_url);
			} else {
				console.error(request.statusText);
			}
		}
	};
	request.open('POST', '/predict/');
	request.setRequestHeader('Content-Type', 'application/json');
	request.send(`{"prediction": ${prediction}}`);
}

function skip(count) {
	for (let i = 0; i < count; ++i) {
		predict(null);
	}
}

document.addEventListener('keydown', (event) => {
	switch (event.keyCode) {
		case 82:
			predict(true);
			break;
		case 70:
			predict(false);
			break;
		case 83:
			predict(null);
			break;
	}
});
