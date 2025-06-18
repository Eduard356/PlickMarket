// MercadoLibre Clone - JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips and popovers
    initializeBootstrapComponents();
    
    // Add smooth scrolling
    addSmoothScrolling();
    
    // Initialize search functionality
    initializeSearch();
    
    // Initialize cart functionality
    initializeCart();
    
    // Add loading states
    initializeLoadingStates();
    
    // Initialize animations
    initializeAnimations();
});

/**
 * Initialize Bootstrap components
 */
function initializeBootstrapComponents() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

/**
 * Add smooth scrolling to anchor links
 */
function addSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            // Skip if href is just '#' or empty
            if (!href || href === '#') {
                return;
            }
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Initialize search functionality
 */
function initializeSearch() {
    const searchInput = document.querySelector('input[name="search"]');
    const searchForm = document.querySelector('form[action*="index"]');
    
    if (searchInput && searchForm) {
        // Add search suggestions (placeholder for future enhancement)
        searchInput.addEventListener('input', function() {
            // This could be enhanced with live search suggestions
            console.log('Search query:', this.value);
        });
        
        // Prevent empty searches
        searchForm.addEventListener('submit', function(e) {
            const query = searchInput.value.trim();
            if (query.length < 2) {
                e.preventDefault();
                searchInput.focus();
                showAlert('Por favor ingresa al menos 2 caracteres para buscar', 'warning');
            }
        });
    }
}

/**
 * Initialize cart functionality
 */
function initializeCart() {
    // Add to cart buttons
    document.querySelectorAll('form[action*="add_to_cart"]').forEach(form => {
        form.addEventListener('submit', function(e) {
            const button = this.querySelector('button[type="submit"]');
            if (button) {
                // Show loading state
                const originalText = button.innerHTML;
                button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Agregando...';
                button.disabled = true;
                
                // Simulate processing time (remove this in production)
                setTimeout(() => {
                    // Reset button after form submission
                    button.innerHTML = originalText;
                    button.disabled = false;
                }, 1000);
            }
        });
    });
    
    // Update cart count animation
    const cartCount = document.getElementById('cart-count');
    if (cartCount && cartCount.textContent !== '0') {
        cartCount.classList.add('animate__animated', 'animate__pulse');
    }
    
    // Quantity input validation
    document.querySelectorAll('input[name="quantity"]').forEach(input => {
        input.addEventListener('change', function() {
            const min = parseInt(this.min) || 1;
            const max = parseInt(this.max) || 999;
            const value = parseInt(this.value);
            
            if (value < min) {
                this.value = min;
                showAlert('La cantidad mínima es ' + min, 'warning');
            } else if (value > max) {
                this.value = max;
                showAlert('La cantidad máxima disponible es ' + max, 'warning');
            }
        });
    });
}

/**
 * Initialize loading states for forms
 */
function initializeLoadingStates() {
    // Add loading states to all forms
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton && !submitButton.disabled) {
                // Add loading spinner to button
                const originalText = submitButton.innerHTML;
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Procesando...';
                submitButton.disabled = true;
                
                // Store original text for potential restoration
                submitButton.setAttribute('data-original-text', originalText);
            }
        });
    });
}

/**
 * Initialize animations
 */
function initializeAnimations() {
    // Fade in animation for product cards
    const productCards = document.querySelectorAll('.product-card');
    
    // Intersection Observer for scroll animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    productCards.forEach(card => {
        observer.observe(card);
    });
    
    // Hover effects for product cards
    productCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

/**
 * Show alert messages
 */
function showAlert(message, type = 'info') {
    // Create alert element
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alert.style.cssText = 'top: 100px; right: 20px; z-index: 9999; min-width: 300px;';
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Add to body
    document.body.appendChild(alert);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alert && alert.parentNode) {
            alert.remove();
        }
    }, 5000);
}

/**
 * Format currency
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('es-AR', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2
    }).format(amount);
}

/**
 * Validate email format
 */
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Handle modal forms
 */
document.addEventListener('DOMContentLoaded', function() {
    // Login form handling
    const loginForm = document.querySelector('#loginModal form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = this.querySelector('#email').value;
            const password = this.querySelector('#password').value;
            
            if (!validateEmail(email)) {
                showAlert('Por favor ingresa un email válido', 'danger');
                return;
            }
            
            if (password.length < 6) {
                showAlert('La contraseña debe tener al menos 6 caracteres', 'danger');
                return;
            }
            
            // Simulate login
            showAlert('Función de login no implementada en esta demo', 'info');
        });
    }
    
    // Register form handling
    const registerForm = document.querySelector('#registerModal form');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const name = this.querySelector('#registerName').value;
            const email = this.querySelector('#registerEmail').value;
            const password = this.querySelector('#registerPassword').value;
            const confirmPassword = this.querySelector('#confirmPassword').value;
            
            if (name.length < 2) {
                showAlert('El nombre debe tener al menos 2 caracteres', 'danger');
                return;
            }
            
            if (!validateEmail(email)) {
                showAlert('Por favor ingresa un email válido', 'danger');
                return;
            }
            
            if (password.length < 6) {
                showAlert('La contraseña debe tener al menos 6 caracteres', 'danger');
                return;
            }
            
            if (password !== confirmPassword) {
                showAlert('Las contraseñas no coinciden', 'danger');
                return;
            }
            
            // Simulate registration
            showAlert('Función de registro no implementada en esta demo', 'info');
        });
    }
});

/**
 * Shopping cart utilities
 */
const Cart = {
    // Update cart display
    updateDisplay: function() {
        const cartCount = document.getElementById('cart-count');
        const cartItems = JSON.parse(localStorage.getItem('cart') || '[]');
        const totalItems = cartItems.reduce((sum, item) => sum + item.quantity, 0);
        
        if (cartCount) {
            cartCount.textContent = totalItems;
            cartCount.style.display = totalItems > 0 ? 'inline' : 'none';
        }
    },
    
    // Add item to cart (client-side for demo purposes)
    addItem: function(productId, name, price, image, quantity = 1) {
        let cart = JSON.parse(localStorage.getItem('cart') || '[]');
        const existingItem = cart.find(item => item.productId === productId);
        
        if (existingItem) {
            existingItem.quantity += quantity;
        } else {
            cart.push({
                productId: productId,
                name: name,
                price: price,
                image: image,
                quantity: quantity
            });
        }
        
        localStorage.setItem('cart', JSON.stringify(cart));
        this.updateDisplay();
        showAlert('Producto agregado al carrito', 'success');
    },
    
    // Remove item from cart
    removeItem: function(productId) {
        let cart = JSON.parse(localStorage.getItem('cart') || '[]');
        cart = cart.filter(item => item.productId !== productId);
        localStorage.setItem('cart', JSON.stringify(cart));
        this.updateDisplay();
        showAlert('Producto eliminado del carrito', 'info');
    },
    
    // Clear cart
    clear: function() {
        localStorage.removeItem('cart');
        this.updateDisplay();
        showAlert('Carrito vaciado', 'info');
    }
};

// Initialize cart display
document.addEventListener('DOMContentLoaded', function() {
    // Cart.updateDisplay(); // Commented out since we're using server-side cart
    
    // Add keyboard navigation support
    document.addEventListener('keydown', function(e) {
        // ESC key closes modals
        if (e.key === 'Escape') {
            const openModal = document.querySelector('.modal.show');
            if (openModal) {
                const modal = bootstrap.Modal.getInstance(openModal);
                if (modal) {
                    modal.hide();
                }
            }
        }
        
        // Ctrl+F focuses search
        if (e.ctrlKey && e.key === 'f') {
            e.preventDefault();
            const searchInput = document.querySelector('input[name="search"]');
            if (searchInput) {
                searchInput.focus();
                searchInput.select();
            }
        }
    });
});

/**
 * Lazy loading for images
 */
function initializeLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

/**
 * Print functionality
 */
function printPage() {
    window.print();
}




/**
 * Share functionality
 */
function shareProduct(productName, productUrl) {
    if (navigator.share) {
        navigator.share({
            title: productName,
            text: `Mira este producto: ${productName}`,
            url: productUrl
        });
    } else {
        // Fallback: copy to clipboard
        navigator.clipboard.writeText(productUrl).then(() => {
            showAlert('Enlace copiado al portapapeles', 'success');
        });
    }
}

// Export functions for global use
window.Cart = Cart;
window.showAlert = showAlert;
window.formatCurrency = formatCurrency;
window.validateEmail = validateEmail;
window.shareProduct = shareProduct;
window.printPage = printPage;
