/* window.addEventListener('DOMContentLoaded', () => {
	const currentSession = JSON.parse(localStorage.getItem('currentSession'));
	
	if(currentSession === null) {
		window.location.href = '../forbiden.html'
	}
}) 

const logOutBtn = document.querySelector('#logout-btn');

logOutBtn.addEventListener('click', () => {
	localStorage.setItem('currentSession', null)
}) */