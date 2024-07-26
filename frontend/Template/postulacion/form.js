const nameInp = document.querySelector("#name");
const lnameInp = document.querySelector("#lname");
const emailInp = document.querySelector("#email");
const careerInp = document.querySelector("#program");
const cuatrimestreInp = document.querySelector("#current_level");
const promedioInp = document.querySelector("#average");
const typeInp = document.querySelector("#tutoring_type");
const areaInp = document.querySelector("#tutoring_area");
const adminAreaInp = document.querySelector("#admin_area");

const form = document.querySelector("form");

form.addEventListener("submit", (e) => {
    e.preventDefault();
	
	axios.post("http://localhost:5000/add_postulacion", {
			name: nameInp.value,
			lname: lnameInp.value,
			email: emailInp.value,
			career: careerInp.value,
			avg: parseInt(cuatrimestreInp.value),
			cicle: parseInt(promedioInp.value),
			id_materia: parseInt(typeInp.value),
			carrer: parseInt(areaInp.value) || 0,
			apply_admin: parseInt(adminAreaInp.value) || 0,
		})
		.then(function (response) {
			console.log(response);
			if(response.statusText == 'OK') {
				alert('postulacion registrada exitosamente')
				window.location.href = '../index.html'
			}
		})
		.catch(function (error) { console.log(error); }); 
});

/* Verificar si el correo ya existe antes de añadir la postulacion */
/* Cambiar el input de promedio para que acepte decimales */
/* Cambiar el campo de tipo de monitoria para que acepte "administrativa" ó "academica" */
