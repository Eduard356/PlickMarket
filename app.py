import os
import json
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# configure the database
database_url = os.environ.get("DATABASE_URL")
if database_url:
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
else:
    # Fallback for development
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plickmarket.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# initialize the app with the extension
db.init_app(app)

# Initialize models once
from models import init_models
Product, User, CartItem = init_models(db)

# Initialize database and create tables
with app.app_context():    
    db.create_all()
    
    # Check if products already exist and populate from JSON if needed
    if Product.query.count() == 0:
        try:
            with open('data/products.json', 'r') as f:
                json_products = json.load(f)
            
            for product_data in json_products:
                product = Product(
                    name=product_data['name'],
                    description=product_data['description'],
                    price=product_data['price'],
                    category=product_data['category'],
                    image=product_data['image'],
                    stock=product_data.get('stock', 10),
                    rating=product_data.get('rating', 4.5)
                )
                db.session.add(product)
            
            db.session.commit()
            print(f"Initialized database with {len(json_products)} products")
        except FileNotFoundError:
            print("No products.json file found, starting with empty database")

# Load product data from database
def load_products():
    products = Product.query.all()
    return [product.to_dict() for product in products]

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
    product_id_str = request.form.get('product_id')
    quantity_str = request.form.get('quantity', '1')
    
    if not product_id_str:
        return redirect(request.referrer or url_for('index'))
    
    try:
        product_id = int(product_id_str)
        quantity = int(quantity_str)
    except (ValueError, TypeError):
        return redirect(request.referrer or url_for('index'))
    
    session_id = session.get('session_id', request.remote_addr or 'anonymous')
    
    # Ensure session has an ID
    if 'session_id' not in session:
        session['session_id'] = session_id
    
    # Check if item already exists in cart
    existing_item = CartItem.query.filter_by(
        session_id=session_id, 
        product_id=product_id
    ).first()
    
    if existing_item:
        existing_item.quantity += quantity
    else:
        cart_item = CartItem(
            session_id=session_id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
    
    db.session.commit()
    return redirect(request.referrer or url_for('index'))

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id_str = request.form.get('product_id')
    if not product_id_str:
        return redirect(request.referrer or url_for('index'))
    
    try:
        product_id = int(product_id_str)
    except (ValueError, TypeError):
        return redirect(request.referrer or url_for('index'))
    
    session_id = session.get('session_id', request.remote_addr or 'anonymous')
    
    cart_item = CartItem.query.filter_by(
        session_id=session_id, 
        product_id=product_id
    ).first()
    
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
    
    return redirect(request.referrer or url_for('index'))

@app.route('/update_cart', methods=['POST'])
def update_cart():
    product_id_str = request.form.get('product_id')
    quantity_str = request.form.get('quantity')
    
    if not product_id_str or not quantity_str:
        return redirect(request.referrer or url_for('index'))
    
    try:
        product_id = int(product_id_str)
        quantity = int(quantity_str)
    except (ValueError, TypeError):
        return redirect(request.referrer or url_for('index'))
    
    session_id = session.get('session_id', request.remote_addr or 'anonymous')
    
    cart_item = CartItem.query.filter_by(
        session_id=session_id, 
        product_id=product_id
    ).first()
    
    if quantity > 0:
        if cart_item:
            cart_item.quantity = quantity
        else:
            cart_item = CartItem(
                session_id=session_id,
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(cart_item)
    elif cart_item:
        db.session.delete(cart_item)
    
    db.session.commit()
    return redirect(request.referrer or url_for('index'))

@app.route('/clear_cart')
def clear_cart():
    session_id = session.get('session_id', request.remote_addr or 'anonymous')
    
    CartItem.query.filter_by(session_id=session_id).delete()
    db.session.commit()
    
    return redirect(url_for('index'))

@app.context_processor
def inject_cart():
    session_id = session.get('session_id', request.remote_addr or 'anonymous')
    cart_items = CartItem.query.filter_by(session_id=session_id).all()
    
    cart = []
    cart_total = 0
    cart_count = 0
    
    for item in cart_items:
        cart_data = {
            'product_id': item.product_id,
            'name': item.product.name,
            'price': float(item.product.price),
            'image': item.product.image,
            'quantity': item.quantity
        }
        cart.append(cart_data)
        cart_total += float(item.product.price) * item.quantity
        cart_count += item.quantity
    
    return dict(cart=cart, cart_total=cart_total, cart_count=cart_count)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
