/*!
* Start Bootstrap - Shop Item v5.0.6 (https://startbootstrap.com/template/shop-item)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-item/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

// Panier simple avec localStorage
function getCart() {
    return JSON.parse(localStorage.getItem('cart') || '[]');
}
function setCart(cart) {
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
}
function addToCart(product) {
    const cart = getCart();
    const found = cart.find(item => item.sku === product.sku && item.option === product.option);
    if (found) {
        found.quantity += product.quantity;
    } else {
        cart.push(product);
    }
    setCart(cart);
}
function updateCartCount() {
    const cart = getCart();
    const count = cart.reduce((sum, item) => sum + item.quantity, 0);
    // Ne met à jour que les badges du panier, pas les badges "Promo"
    document.querySelectorAll('.btn .badge.bg-dark').forEach(el => el.textContent = count);
}
// Ajout listeners sur tous les boutons "Ajouter au panier"
document.addEventListener('DOMContentLoaded', function() {
    updateCartCount();
    document.querySelectorAll('button.btn-outline-dark').forEach(btn => {
        if (btn.textContent.includes('Ajouter au panier')) {
            btn.addEventListener('click', function(e) {
                const parent = btn.closest('.col-md-6, .card-body, .row');
                let sku = parent && parent.querySelector('.small') ? parent.querySelector('.small').textContent.replace('SKU:','').trim() : 'SKU';
                let name = parent && parent.querySelector('h1, h5') ? parent.querySelector('h1, h5').textContent.trim() : 'Produit';
                let price = parent && parent.querySelector('.fs-5 span:not(.text-decoration-line-through)') ? parent.querySelector('.fs-5 span:not(.text-decoration-line-through)').textContent.replace('€','').replace(',','.').trim() : '0';
                let quantity = 1;
                let option = '';
                const inputQty = parent && parent.querySelector('#inputQuantity');
                if (inputQty) quantity = parseInt(inputQty.value) || 1;
                const selectOpt = parent && parent.querySelector('select');
                if (selectOpt) option = selectOpt.options[selectOpt.selectedIndex].text;
                addToCart({sku, name, price: parseFloat(price), quantity, option});
            });
        }
    });
});