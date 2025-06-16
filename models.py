from datetime import datetime

def init_models(db):
    """Initialize all database models with the db instance"""
    
    class Product(db.Model):
        __tablename__ = 'products'
        
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(200), nullable=False)
        description = db.Column(db.Text, nullable=False)
        price = db.Column(db.Numeric(10, 2), nullable=False)
        category = db.Column(db.String(100), nullable=False)
        image = db.Column(db.String(500), nullable=False)
        stock = db.Column(db.Integer, nullable=False, default=0)
        rating = db.Column(db.Numeric(3, 2), nullable=False, default=0.0)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        
        def to_dict(self):
            return {
                'id': self.id,
                'name': self.name,
                'description': self.description,
                'price': float(self.price),
                'category': self.category,
                'image': self.image,
                'stock': self.stock,
                'rating': float(self.rating),
                'created_at': self.created_at.isoformat() if self.created_at else None,
                'updated_at': self.updated_at.isoformat() if self.updated_at else None
            }
        
        def __repr__(self):
            return f'<Product {self.name}>'

    class User(db.Model):
        __tablename__ = 'users'
        
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password_hash = db.Column(db.String(256))
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        
        def __repr__(self):
            return f'<User {self.username}>'

    class CartItem(db.Model):
        __tablename__ = 'cart_items'
        
        id = db.Column(db.Integer, primary_key=True)
        session_id = db.Column(db.String(255), nullable=False)
        product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
        quantity = db.Column(db.Integer, nullable=False, default=1)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        
        # Relationship
        product = db.relationship('Product', backref='cart_items')
        
        def __repr__(self):
            return f'<CartItem {self.product_id} x{self.quantity}>'
    
    return Product, User, CartItem