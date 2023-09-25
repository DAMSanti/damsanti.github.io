document.addEventListener('DOMContentLoaded', function () {
    var javaCodeEditorContainer = document.getElementById('javaCodeEditorContainer');
    var htmlFrame = document.getElementById('htmlFrame');
    let selectedPath = '';
    let codeMirrorInstance = null; // Define la variable global aquí
    let sitiojson = "./data/lista-archivos-java.json";

    // Cargar las unidades disponibles al cargar la página
    window.addEventListener('load', () => {
        const unidadSelect = document.getElementById('unidadSelect');
        const hojaSelect = document.getElementById('hojaSelect');
        const archivoSelect = document.getElementById('archivoSelect');

        // Agregar event listener para el cambio de unidad
        unidadSelect.addEventListener('change', loadHojas);

        // Agregar event listener para el cambio de hoja
        hojaSelect.addEventListener('change', loadArchivos); 

        // Agregar event litener para la seleccion de archivo
        archivoSelect.addEventListener('change', loadFile)


        fetch(sitiojson) // Reemplaza con la ruta de tu servidor para obtener la lista de archivos
            .then(response => response.json())
            .then(data => {
                const unidades = [...new Set(data.map(file => file.unidad))];
                unidades.forEach(unidad => {
                    const option = document.createElement('option');
                    option.value = unidad;
                    option.textContent = unidad;
                    unidadSelect.appendChild(option);
                });
            })
            .catch(error => {
                console.error(error);
            });
    });

    // Cargar las hojas disponibles cuando se selecciona una unidad
    function loadHojas() {
        const selectedUnidad = unidadSelect.value;
        hojaSelect.innerHTML = '<option value="">Selecciona una hoja</option>'; // Limpiar las opciones anteriores
        if (selectedUnidad) {
            fetch(sitiojson) // Reemplaza con la ruta de tu servidor para obtener la lista de archivos
                .then(response => response.json())
                .then(data => {
                    const hojas = [...new Set(data.filter(file => file.unidad === selectedUnidad).map(file => file.Hoja))];
                    hojas.forEach(hoja => {
                        const option = document.createElement('option');
                        option.value = hoja;
                        option.textContent = hoja;
                        hojaSelect.appendChild(option);
                    });
                })
                .catch(error => {
                    console.error(error);
                });
        }
    }

    // Cargar los archivos disponibles cuando se selecciona una hoja
    function loadArchivos() {
        const selectedUnidad = unidadSelect.value;
        const selectedHoja = hojaSelect.value;
        archivoSelect.innerHTML = '<option value="">Selecciona un archivo</option>'; // Limpiar las opciones anteriores

        if (selectedUnidad && selectedHoja) {
            fetch(sitiojson) // Reemplaza con la ruta de tu servidor para obtener la lista de archivos
                .then(response => response.json())
                .then(data => {
                    const archivos = data.filter(file => file.unidad === selectedUnidad && file.Hoja === selectedHoja);
                    archivos.forEach(archivo => {
                        // Eliminar la extensión ".java" del nombre del archivo
                        const nombreArchivoSinExtension = archivo.nombre.replace('.java', '');
                    
                        const option = document.createElement('option');
                        option.value = archivo.nombre;
                        option.textContent = nombreArchivoSinExtension;
                        archivoSelect.appendChild(option);
                    });
                })
                .catch(error => {
                    console.error(error);
                });
        }
    }

    // Cargar el archivo Java seleccionado
    function loadFile() {
        // Función para cargar y mostrar el código Java o HTML seleccionado
        unidadSelect.addEventListener('change', loadHojas);
        hojaSelect.addEventListener('change', loadArchivos);
        archivoSelect.addEventListener('change', loadFile);
        const selectedArchivo = archivoSelect.value;
        if (selectedArchivo && selectedArchivo.endsWith('.java')) {
            fetch(sitiojson)
                .then(response => response.json())
                .then(data => {
                    const selectedFileData = data.find(file => file.nombre === selectedArchivo);
                    if (selectedFileData) {
                        selectedPath = selectedFileData.ruta;
                        const fullFilePath = `${selectedPath}${selectedArchivo}`;

                        // Mostrar el editor de CodeMirror y ocultar el iframe
                        javaCodeEditorContainer.style.display = 'block';
                        htmlFrame.style.display = 'none';
                        fetch(fullFilePath)
                            .then(response => response.text())
                            .then(javaCode => {
                                // Crear una instancia de CodeMirror si aún no existe
                                if (!codeMirrorInstance) {
                                    codeMirrorInstance = CodeMirror(javaCodeEditorContainer, {
                                        mode: 'text/x-java',
                                        lineNumbers: true,
                                        readOnly: true,
                                    });
                                }

                                // Después de crear la instancia de CodeMirror
                                if (codeMirrorInstance) {
                                    codeMirrorInstance.setSize(null, '45vh'); // Establecer la altura en 65% de la ventana
                                }

                                // Establecer el código Java
                                codeMirrorInstance.setValue(javaCode);
                            })
                            .catch(error => {
                                console.error(error);
                            });
                    } else {
                        console.error('Datos del archivo no encontrados en el JSON.');
                    }
                })
                .catch(error => {
                    console.error(error);
                });
        } else {
            // Limpiar el contenido del editor de CodeMirror si no se selecciona ningún archivo
            if (codeMirrorInstance) {
                codeMirrorInstance.setValue('');
            }
            // Ocultar el iframe si no se selecciona ningún archivo HTML
            htmlFrame.style.display = 'none';
        }
    }
});