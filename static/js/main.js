// Main JavaScript for Solana Pay frontend

// Initialize AngularJS app
var app = angular.module('app', []);

// Cart controller (placeholder for shopping cart functionality)
app.controller('cart-ctrl', function($scope) {
    $scope.cart = [];
    $scope.total = 0;
    
    // Add item to cart
    $scope.addToCart = function(item) {
        $scope.cart.push(item);
        $scope.updateTotal();
    };
    
    // Remove item from cart
    $scope.removeFromCart = function(index) {
        $scope.cart.splice(index, 1);
        $scope.updateTotal();
    };
    
    // Update cart total
    $scope.updateTotal = function() {
        $scope.total = $scope.cart.reduce(function(sum, item) {
            return sum + (item.price * item.quantity);
        }, 0);
    };
});

// Utility functions
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const menuToggle = document.querySelector('.js-menu-toggle');
    const menu = document.querySelector('.site-menu');
    
    if (menuToggle && menu) {
        menuToggle.addEventListener('click', function(e) {
            e.preventDefault();
            menu.classList.toggle('show');
        });
    }
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Form validation helpers
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
    
    function validateSolanaAddress(address) {
        // Basic Solana address validation (base58, 32-44 characters)
        if (!address) return true; // Optional field
        const base58Regex = /^[1-9A-HJ-NP-Za-km-z]{32,44}$/;
        return base58Regex.test(address);
    }
    
    // Add validation to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const emailInputs = form.querySelectorAll('input[type="email"]');
            const walletInputs = form.querySelectorAll('input[name="wallet_key"]');
            
            emailInputs.forEach(function(input) {
                if (input.value && !validateEmail(input.value)) {
                    e.preventDefault();
                    showError('Please enter a valid email address');
                }
            });
            
            walletInputs.forEach(function(input) {
                if (input.value && !validateSolanaAddress(input.value)) {
                    e.preventDefault();
                    showError('Please enter a valid Solana wallet address');
                }
            });
        });
    });
    
    function showError(message) {
        // Create or update error message
        let errorDiv = document.getElementById('error-message');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.id = 'error-message';
            errorDiv.className = 'text-danger';
            const form = document.querySelector('form');
            if (form) {
                form.insertBefore(errorDiv, form.firstChild);
            }
        }
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        
        // Hide after 5 seconds
        setTimeout(function() {
            errorDiv.style.display = 'none';
        }, 5000);
    }
    
    // Initialize tooltips if Bootstrap is loaded
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Authentication helpers
    window.authHelpers = {
        getToken: function() {
            return localStorage.getItem('auth_token');
        },
        
        setToken: function(token) {
            localStorage.setItem('auth_token', token);
        },
        
        removeToken: function() {
            localStorage.removeItem('auth_token');
        },
        
        isAuthenticated: function() {
            const token = this.getToken();
            if (!token) return false;
            
            // Check if token is expired (simple JWT parsing)
            try {
                const payload = JSON.parse(atob(token.split('.')[1]));
                return payload.exp > Date.now() / 1000;
            } catch (e) {
                return false;
            }
        },
        
        logout: function() {
            this.removeToken();
            window.location.href = '/login';
        }
    };
    
    // Add auth headers to fetch requests
    const originalFetch = window.fetch;
    window.fetch = function(url, options = {}) {
        if (url.startsWith('/api/') && window.authHelpers.isAuthenticated()) {
            options.headers = options.headers || {};
            options.headers['Authorization'] = 'Bearer ' + window.authHelpers.getToken();
        }
        return originalFetch(url, options);
    };
});

// Loading spinner utility
function showLoader() {
    const loader = document.createElement('div');
    loader.id = 'global-loader';
    loader.innerHTML = `
        <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
                    background: rgba(0,0,0,0.5); display: flex; justify-content: center; 
                    align-items: center; z-index: 9999;">
            <div style="background: white; padding: 20px; border-radius: 10px; text-align: center;">
                <div style="border: 4px solid #f3f3f3; border-top: 4px solid #14F195; 
                           border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; 
                           margin: 0 auto 15px;"></div>
                <p>Processing...</p>
            </div>
        </div>
        <style>
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    `;
    document.body.appendChild(loader);
}

function hideLoader() {
    const loader = document.getElementById('global-loader');
    if (loader) {
        loader.remove();
    }
}

// Export utilities for use in other scripts
window.solanaPay = {
    showLoader: showLoader,
    hideLoader: hideLoader,
    authHelpers: window.authHelpers
};