import os
import json
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Load product data
def load_products():
    with open('data/products.json', 'r') as f:
        return json.load(f)

@app.route('/')
def index():
    products = load_products()
    search_query = request.args.get('search', '').lower()
    category = request.args.get('category', '')
    
    # Filter products based on search and category
    filtered_products = products
    if search_query:
        filtered_products = [p for p in filtered_products if search_query in p['name'].lower() or search_query in p['description'].lower()]
    if category:
        filtered_products = [p for p in filtered_products if p['category'] == category]
    
    # Get unique categories for filter
    categories = list(set(p['category'] for p in products))
    
    return render_template('index.html', 
                         products=filtered_products, 
                         categories=categories,
                         search_query=search_query,
                         selected_category=category)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    products = load_products()
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return redirect(url_for('index'))
    return render_template('product_detail.html', product=product)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = int(request.form.get('product_id'))
    quantity = int(request.form.get('quantity', 1))
    
    # Initialize cart in session if it doesn't exist
    if 'cart' not in session:
        session['cart'] = []
    
    # Check if product already in cart
    cart = session['cart']
    existing_item = next((item for item in cart if item['product_id'] == product_id), None)
    
    if existing_item:
        existing_item['quantity'] += quantity
    else:
        products = load_products()
        product = next((p for p in products if p['id'] == product_id), None)
        if product:
            cart.append({
                'product_id': product_id,
                'name': product['name'],
                'price': product['price'],
                'image': product['image'],
                'quantity': quantity
            })
    
    session['cart'] = cart
    session.modified = True
    
    return redirect(request.referrer or url_for('index'))

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = int(request.form.get('product_id'))
    
    if 'cart' in session:
        session['cart'] = [item for item in session['cart'] if item['product_id'] != product_id]
        session.modified = True
    
    return redirect(request.referrer or url_for('index'))

@app.route('/update_cart', methods=['POST'])
def update_cart():
    product_id = int(request.form.get('product_id'))
    quantity = int(request.form.get('quantity'))
    
    if 'cart' in session:
        cart = session['cart']
        for item in cart:
            if item['product_id'] == product_id:
                if quantity > 0:
                    item['quantity'] = quantity
                else:
                    cart.remove(item)
                break
        session['cart'] = cart
        session.modified = True
    
    return redirect(request.referrer or url_for('index'))

@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('index'))

@app.context_processor
def inject_cart():
    cart = session.get('cart', [])
    cart_total = sum(item['price'] * item['quantity'] for item in cart)
    cart_count = sum(item['quantity'] for item in cart)
    return dict(cart=cart, cart_total=cart_total, cart_count=cart_count)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
