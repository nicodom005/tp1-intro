
function obtenerIdUsuario() {
    var params = new URLSearchParams(window.location.search);
    var idUsuario = params.get('id'); 

    return idUsuario;
}

// Función para agregar productos al carrito
function addToCart(name, price) {
    let cart = JSON.parse(localStorage.getItem('carrito')) || [];
    let item = { nombre: name, precio: price };
    cart.push(item);
    localStorage.setItem('carrito', JSON.stringify(cart));
    console.log('Carrito actualizado:', cart); 
    alert('Producto agregado al carrito');
}

// Función para cargar el carrito y mostrar los productos
function loadCart() {
    const cart = JSON.parse(localStorage.getItem('carrito')) || [];
    console.log('Cargando carrito:', cart); 
    const cartItems = document.getElementById('carrito-items');
    cartItems.innerHTML = '';

    let subtotal = 0;

    cart.forEach((item, index) => {
        console.log('Item en carrito:', item); 
        const div = document.createElement('div');
        div.classList.add('carrito-item');
        div.innerHTML = `
            <div>
                <h4>${item.nombre}</h4>
                <p>Precio: $${item.precio.toFixed(2)}</p>
                <button onclick="removeFromCart(${index})">Eliminar</button>
            </div>
        `;
        cartItems.appendChild(div);
        subtotal += item.precio;
    });

    //const impuestos = subtotal * 0.21; //Suponiendo  un impuesto del 21%
    //const total = subtotal + impuestos;

    document.getElementById('subtotal').innerText = ` $${subtotal.toFixed(2)}`;
    //document.getElementById('impuestos').innerText = ` $${impuestos.toFixed(2)}`;
    document.getElementById('total').innerText = ` $${subtotal.toFixed(2)}`;
}

// Función para eliminar productos del carrito
function removeFromCart(index) {
    let cart = JSON.parse(localStorage.getItem('carrito')) || [];
    cart.splice(index, 1);
    localStorage.setItem('carrito', JSON.stringify(cart));
    loadCart();
}

// Función para procesar el pago
function procesarPago() {
    const carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    if (carrito.length === 0) {
        alert('El carrito está vacío.');
        return;
    }

    var idUsuario = obtenerIdUsuario();

    fetch('http://127.0.0.1:5000/procesar_pago/' + idUsuario, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(carrito)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            localStorage.removeItem('carrito');
            alert('Compra realizada exitosamente');
            loadCart();
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Hubo un error al procesar el pago.');
    });
}

// Cargar el carrito al cargar la página del carrito
if (document.getElementById('carrito-items')) {
    window.onload = loadCart;
}



// Funcion para el carrusel
document.addEventListener('DOMContentLoaded', function() {
    let indiceDiapositiva = 0;
    const diapositivas = document.querySelector('.diapositivas');
    const imagenesDiapositivas = document.querySelectorAll('.diapositivas img');
    const puntos = document.querySelectorAll('.indicadores-carrusel .punto');
    const anterior = document.querySelector('.controles-carrusel .anterior');
    const siguiente = document.querySelector('.controles-carrusel .siguiente');

    function mostrarDiapositiva(indice) {
        const anchoDiapositiva = imagenesDiapositivas[0].clientWidth;
        diapositivas.style.transform = `translateX(${-anchoDiapositiva * indice}px)`;
        puntos.forEach(punto => punto.classList.remove('activo'));
        puntos[indice].classList.add('activo');
    }

    function siguienteDiapositiva() {
        indiceDiapositiva = (indiceDiapositiva + 1) % imagenesDiapositivas.length;
        mostrarDiapositiva(indiceDiapositiva);
    }

    function anteriorDiapositiva() {
        indiceDiapositiva = (indiceDiapositiva - 1 + imagenesDiapositivas.length) % imagenesDiapositivas.length;
        mostrarDiapositiva(indiceDiapositiva);
    }

    puntos.forEach(punto => {
        punto.addEventListener('click', () => {
            indiceDiapositiva = parseInt(punto.getAttribute('data-slide'));
            mostrarDiapositiva(indiceDiapositiva);
        });
    });

    anterior.addEventListener('click', anteriorDiapositiva);
    siguiente.addEventListener('click', siguienteDiapositiva);

    // Reproducción automática
    setInterval(siguienteDiapositiva, 5000); // Cambia de imagen cada 5 segundos
});




