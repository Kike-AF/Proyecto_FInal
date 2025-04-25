// Borrar el mensaje de flash despues de 5 segundos y añadir la clase "fade" para que se desvanezca
setTimeout(function() {
    var flash = document.getElementById('flash-message');
    if (flash) {
        flash.classList.remove('show');
        flash.classList.add('fade'); 
        setTimeout(()=> flash.remove(), 400); // Espera 400ms para eliminar el elemento después de que se desvanezca
    }
}, 5000);