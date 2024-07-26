const showApplies = document.querySelectorAll("button[data-show]");

/* Content DOM elements */
const showZones = document.querySelectorAll(".show-sect");
const appliesContent = document.querySelector("#apply");
const modulesContent = document.querySelector("#modules");
const areasContent = document.querySelector("#areas");

/* modal buttons */
const acceptPostulationBtn = document.querySelector(".accept-postulation-btn");
const declinedPostulationBtn = document.querySelector(".decline-postulation-btn");

let selected = 0;

window.addEventListener("DOMContentLoaded", () => {
    loadPostulations();
    loadContent();
});

function loadContent() {
    showApplies.forEach((btn) =>
        btn.addEventListener("click", () => {
            showZones.forEach((zone) => zone.classList.add("d-none"));
            if (btn.dataset.show === "applications") {
                appliesContent.classList.remove("d-none");
				loadPostulations();
            }
            if (btn.dataset.show === "modules") {
                modulesContent.classList.remove("d-none");
            }
            if (btn.dataset.show === "areas") {
                areasContent.classList.remove("d-none");
            }
        })
    );
}

function loadPostulations() {
    axios
        .get("http://localhost:5000/postulations/en%20espera")
        .then((res) => {
            console.log(res.data);
            const postulations = res.data;
            const postulationContainer = document.querySelector(".postulation-space");
            postulationContainer.innerHTML = "";

            postulations.forEach(
                ({ nombre, correo, carrera, cuatrimestre, promedio, tipo, area }) => {
                    const container = document.createElement("tr");
                    container.innerHTML = `
					<td>${nombre}</td>
					<td>${correo}</td>
					<td>${carrera}</td>
					<td>${cuatrimestre}</td>
					<td>${promedio}</td>
					<td>${tipo}</td>
					<td>${area}</td>
					
					<td>
						<button class="btn btn-success btn-modal-accept" data-bs-toggle="modal" data-bs-target="#accept">Aceptar</button>
						<button class="btn btn-danger btn-modal-decline" data-bs-toggle="modal" data-bs-target="#decline">Rechazar</button>
					</td>`;

                    postulationContainer.append(container);

                    document
                        .querySelectorAll(".btn-modal-accept")
                        .forEach((btn) => btn.addEventListener("click", setSelectedId));
                    document
                        .querySelectorAll(".btn-modal-decline")
                        .forEach((btn) => btn.addEventListener("click", setSelectedId));

                    function setSelectedId(e) {
                        const id = e.target.closest("tr").querySelector("td:nth-child(2)").textContent;
                        selected = id;
                    }
                }
            );
        })
        .catch((e) => console.log(e));
}

function setPostulationStatus(email, status) {
    axios.put(`http://localhost:5000/setPostulationStatus/${email}/${status}`)
        .then((res) => {
            console.log(res);
            alert("Cambio exitoso exitosamente");
            loadPostulations();
        })
        .catch((e) => console.log(e));
}

/* make btns for accept/decline work 👍 */
/* get to admin and pass the info from postulaciones to monitores */
/* render the info from the monitors to Modulos and Areas sections */

acceptPostulationBtn.addEventListener('click', () => {
	const newStatus = "aceptada"
	console.log("usuario acceptado", selected)
	setPostulationStatus(selected, newStatus)
})
declinedPostulationBtn.addEventListener('click', () => {
	const newStatus = "rechazada"
	console.log("usuario declinado", selected)
	setPostulationStatus(selected, newStatus)
})

