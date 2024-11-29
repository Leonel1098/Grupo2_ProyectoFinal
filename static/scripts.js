const allSideMenu = document.querySelectorAll('#sidebar .side-menu.top li a');

allSideMenu.forEach(item => {
    const li = item.parentElement;

    item.addEventListener('click', function () {
        allSideMenu.forEach(i => {
            i.parentElement.classList.remove('active');
        })
        li.classList.add('active');
    })
});


// Funciones para manejar la paginación
document.getElementById("prev-page").addEventListener("click", () => {
    if (currentPage > 1) {
        currentPage--;
        updateTable(document.getElementById("search-input").value);
    }
});

document.getElementById("next-page").addEventListener("click", () => {
    const totalPages = Math.ceil(employees.length / rowsPerPage);
    if (currentPage < totalPages) {
        currentPage++;
        updateTable(document.getElementById("search-input").value);
    }
});

// Cambiar el número de filas por página
document.getElementById("rows-per-page").addEventListener("change", (event) => {
    rowsPerPage = parseInt(event.target.value);
    currentPage = 1;  // Resetear a la primera página
    updateTable(document.getElementById("search-input").value);
});

// Evento de búsqueda
document.getElementById("search-input").addEventListener("input", (event) => {
    updateTable(event.target.value);
});

// Inicializar la tabla al cargar la página
updateTable();