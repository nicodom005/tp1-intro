
function obtenerIdUsuario() {
    var params = new URLSearchParams(window.location.search);
    var idUsuario = params.get('id'); 

    return idUsuario;
}


// Array para almacenar los productos en el carrito
let cart = [];

// Función para agregar un producto al carrito
function addToCart(productName, price) {
    cart.push({ name: productName, price: price });
    updateCart();
}

// Función para actualizar el contenido del carrito
function updateCart() {
    const cartItems = document.getElementById('cart-items');
    cartItems.innerHTML = '';

    if (cart.length === 0) {
        cartItems.innerHTML = '<p>Tu carrito está vacío.</p>';
    } else {
        cart.forEach((item, index) => {
            const productElement = document.createElement('div');
            productElement.classList.add('cart-item');
            productElement.innerHTML = `
                <p>${item.name} - $${item.price.toFixed(2)}</p>
                <button onclick="removeFromCart(${index})">Eliminar</button>
            `;
            cartItems.appendChild(productElement);
        });
    }
}


// Función para eliminar un producto del carrito
function removeFromCart(index) {
    cart.splice(index, 1);
    updateCart();
}

// Event listener para el botón de "Proceder al pago"
document.getElementById('checkout').addEventListener('click', () => {
    if (cart.length === 0) {
        alert('Tu carrito está vacío.');
    } else {
        // Lógica para proceder al pago
        alert('Gracias por tu compra!');
        cart = [];
        updateCart();
    }
});

// Función para agregar productos al carrito
function addToCart(name, price) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    let item = { name: name, price: price };
    cart.push(item);
    localStorage.setItem('cart', JSON.stringify(cart));
}
