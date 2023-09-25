document.addEventListener('DOMContentLoaded', function () {
    var salida = document.getElementById('salida');
    var input = document.getElementById('input');
    var consoleText = ''; // Variable para mantener el texto de la consola

    
function appendToConsole(text) {
    // Agregar el texto al contenido de la consola
    consoleText += text + '\n';
    salida.textContent = consoleText;
    // Desplazar el scroll al final
    salida.scrollTop = salida.scrollHeight;
}
function executeCommand(command) {
    // Convertir el comando a minúsculas para que sea insensible a mayúsculas/minúsculas
    command = command.toLowerCase();

    if (command === '?' || command === 'help') {
        appendToConsole('Comando ejecutado: ' + command);
        // Si se ingresa "?" o "help", muestra las instrucciones en la consola
        appendToConsole('Si quieres ejecutar el codigo escribe "Run"');
    } else {
        // Aquí debes agregar la lógica para otros comandos.
        // Por ahora, simplemente muestra un mensaje genérico si no se reconoce el comando.
        appendToConsole('Comando no reconocido. Ingresa "?" o "help" para ver las instrucciones.');
    }

    // Establecer un temporizador para borrar el mensaje después de 3 segundos
    setTimeout(function () {
    appendToConsole('');
    }, 1000);

    input.focus();
}
       
    
    if (input) {
    input.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            var command = input.value;
            executeCommand(command);
            input.value = ''; // Limpiar el campo de entrada después de ejecutar el comando
        }
        });
    }
});

