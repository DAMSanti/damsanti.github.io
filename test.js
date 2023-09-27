// Función para generar dinámicamente las opciones del desplegable de unidades
function generarOpcionesUnidades() {
    const asignaturaSelect = document.getElementById("asignaturaSelect");
    const unidadSelect = document.getElementById("unidadSelect");
    const asignaturaValue = asignaturaSelect.value;

    unidadSelect.innerHTML = ""; // Limpiamos las opciones anteriores

    // Generamos las opciones de unidades en función de la asignatura seleccionada
    for (let i = 1; i <= 10; i++) { // Puedes ajustar el rango según tus necesidades
        const option = document.createElement("option");
        const unidadNumber = i < 10 ? `0${i}` : `${i}`;
        option.value = unidadNumber;
        option.textContent = `Unidad ${unidadNumber} de ${asignaturaValue}`;
        unidadSelect.appendChild(option);
    }
}

// Llamamos a la función para generar las opciones de unidades cuando cambia la asignatura
document.getElementById("asignaturaSelect").addEventListener("change", generarOpcionesUnidades);

// Función para mostrar el PDF seleccionado
function mostrarPDF() {
    const asignatura = document.getElementById("asignaturaSelect").value;
    const unidad = document.getElementById("unidadSelect").value;
    const pdfContainer = document.getElementById("pdfContainer");

    const pdfURL = `/apuntes/${asignatura}Unidad${unidad}.pdf`;

    // Verificar si el archivo existe antes de mostrarlo
    fetch(pdfURL)
        .then(response => {
            if (response.status === 200) {
                // Si el archivo existe, mostrarlo en un iframe
                pdfContainer.innerHTML = `<iframe src="${pdfURL}" width="100%" height="500px"></iframe>`;
            } else {
                // Si el archivo no existe, mostrar un mensaje de error
                pdfContainer.innerHTML = "El archivo PDF no existe.";
            }
        })
        .catch(error => {
            console.error("Error al cargar el PDF:", error);
            pdfContainer.innerHTML = "Hubo un error al cargar el PDF.";
        });
}
