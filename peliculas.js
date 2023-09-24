let moviesData; // Variable global para almacenar los datos de las películas
let sortColumn = 0; // Columna inicial para ordenar (Título)
let sortOrder = 1; // Orden ascendente por defecto


// Función para crear filas de la tabla
function createTableRow(movie) {
    const row = document.createElement("tr");

    // Columnas de la tabla
    row.innerHTML = `
        <td>${movie.title}</td>
        <td>${movie.year}</td>
        <td>${movie.runtime}</td>
        <td>${movie.genres.join(', ')}</td>
        <td>${movie.director}</td>
        <td>${movie.actors}</td>
        <td>${movie.plot}</td>
        <td><img src="${movie.posterUrl}" alt="${movie.title}" width="100"></td>
    `;

    return row;
}

// Función para llenar la tabla con las películas
function fillTable(data) {
    const tableBody = document.getElementById("movieTableBody");
    tableBody.innerHTML = ""; // Limpiar el cuerpo de la tabla

    data.movies.forEach(movie => {
        const row = createTableRow(movie);
        tableBody.appendChild(row);
    });
}

function sortTable(columnIndex) {
    const table = document.querySelector("table");
    const rows = Array.from(table.rows).slice(1); // Ignora la fila de encabezado

    rows.sort((a, b) => {
        const aValue = a.cells[columnIndex].textContent;
        const bValue = b.cells[columnIndex].textContent;

        if (columnIndex === 1 || columnIndex === 2) {
            return sortOrder * (parseFloat(aValue) - parseFloat(bValue));
        } else {
            return sortOrder * aValue.localeCompare(bValue);
        }
    });

    // Elimina las filas existentes de la tabla
    while (table.rows.length > 1) {
        table.deleteRow(1);
    }

    // Agrega las filas ordenadas de nuevo a la tabla
    rows.forEach((row) => {
        table.appendChild(row);
    });

    // Cambia el orden para la próxima vez que se haga clic
    sortOrder *= -1;
}

// Realizar una solicitud HTTP para obtener el JSON de películas
fetch('./data/lista-peliculas.json')
    .then(response => response.json())
    .then(data => {
        moviesData = data; // Almacenar los datos de las películas en la variable global

        // Llenar la tabla con las películas
        fillTable(data);
    })
    .catch(error => console.error('Error al cargar el JSON de películas:', error));

document.addEventListener("DOMContentLoaded", function () {


});
