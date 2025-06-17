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
// Ajout listeners sur tous les boutons "Ajouter au panier" ou "Add to cart"
document.addEventListener('DOMContentLoaded', function() {
    updateCartCount();
    document.querySelectorAll('button.btn-outline-dark, a.btn-outline-dark').forEach(btn => {
        if (
            btn.textContent.includes('Ajouter au panier') ||
            btn.textContent.includes('Add to cart')
        ) {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                // Trouve le parent qui contient les infos produit
                let parent = btn.closest('.col-md-6') || btn.closest('.card-body') || btn.closest('.row') || btn.closest('.card');
                // Nom du produit
                let name = parent && (parent.querySelector('h1, h5')) ? parent.querySelector('h1, h5').textContent.trim() : 'Produit';
                // SKU
                let sku = parent && parent.querySelector('.small') ? parent.querySelector('.small').textContent.replace('SKU:','').trim() : 'SKU';
                // Prix (prend le dernier span dans .fs-5 ou .fs-5.mb-5/.mb-4)
                let priceSpan = parent && parent.querySelector('.fs-5 span:last-child, .fs-5.mb-5 span:last-child, .fs-5.mb-4 span:last-child');
                let price = priceSpan ? priceSpan.textContent.replace(/[^\d,.]/g,'').replace(',','.').trim() : '0';
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
function renderCart() {
    const cart = JSON.parse(localStorage.getItem('cart') || '[]');
    const cartContent = document.getElementById('cartContent');
    if (!cart.length) {
        cartContent.innerHTML = '<p class="mb-0">Votre panier est vide pour le moment.</p>';
        return;
    }
    let html = '<table class="table"><thead><tr><th>Produit</th><th>Option</th><th>Prix</th><th>Quantité</th><th>Total</th><th></th></tr></thead><tbody>';
    let total = 0;
    cart.forEach((item, i) => {
        const itemTotal = item.price * item.quantity;
        total += itemTotal;
        html += `<tr><td>${item.name}</td><td>${item.option || ''}</td><td>${item.price.toFixed(2)}€</td><td>${item.quantity}</td><td>${itemTotal.toFixed(2)}€</td><td><button class='btn btn-sm btn-danger' onclick='removeCartItem(${i})'>Supprimer</button></td></tr>`;
    });
    html += `</tbody></table><div class='text-end fw-bold'>Total : ${total.toFixed(2)}€</div>`;
    html += `<div class="d-grid mt-3"><a href="/checkout" class="btn btn-success">Payer</a></div>`;
    cartContent.innerHTML = html;
}