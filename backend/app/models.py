# backend/app/models.py
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    reviews = db.relationship('Review', backref='user', lazy=True)
    orders = db.relationship('Order', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_active': self.is_active
        }

class Manufacturer(db.Model):
    """Manufacturer model for normalization"""
    __tablename__ = 'manufacturers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False, index=True)
    country = db.Column(db.String(100))
    established_year = db.Column(db.Integer)
    website = db.Column(db.String(255))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='manufacturer_info', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'country': self.country,
            'established_year': self.established_year,
            'website': self.website
        }

class Category(db.Model):
    """Product category model"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Self-referential relationship for subcategories
    children = db.relationship('Category', backref=db.backref('parent', remote_side=[id]))
    products = db.relationship('Product', backref='category', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'parent_id': self.parent_id
        }

class Salt(db.Model):
    """Salt/Active ingredient model"""
    __tablename__ = 'salts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False, index=True)
    chemical_formula = db.Column(db.String(100))
    molecular_weight = db.Column(db.Float)
    description = db.Column(db.Text)
    therapeutic_class = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    faqs = db.relationship('FAQ', backref='salt', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'chemical_formula': self.chemical_formula,
            'molecular_weight': self.molecular_weight,
            'description': self.description,
            'therapeutic_class': self.therapeutic_class
        }

class Product(db.Model):
    """Product model for medicines"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    sku = db.Column(db.String(50), unique=True, nullable=False, index=True)
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturers.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    price = db.Column(db.Numeric(10, 2), nullable=False)
    mrp = db.Column(db.Numeric(10, 2))  # Maximum Retail Price
    discount_percentage = db.Column(db.Float, default=0.0)
    description_general = db.Column(db.Text)
    uses = db.Column(db.Text)
    how_it_works = db.Column(db.Text)
    how_to_use = db.Column(db.Text)
    side_effects = db.Column(db.Text)
    precautions = db.Column(db.Text)
    interactions = db.Column(db.Text)
    dosage_form = db.Column(db.String(100))  # Tablet, Capsule, Syrup, etc.
    strength = db.Column(db.String(100))     # 300mg, 500ml, etc.
    pack_size = db.Column(db.String(50))     # 10 tablets, 100ml, etc.
    prescription_required = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)
    stock_quantity = db.Column(db.Integer, default=0)
    reorder_level = db.Column(db.Integer, default=10)
    expiry_date = db.Column(db.Date)
    manufacturing_date = db.Column(db.Date)
    batch_number = db.Column(db.String(50))
    storage_conditions = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    reviews = db.relationship('Review', backref='product', lazy=True)
    product_salts = db.relationship('ProductSalt', backref='product', lazy=True)
    substitute_products = db.relationship('Substitute', foreign_keys='Substitute.product_id', backref='main_product', lazy=True)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'sku': self.sku,
            'manufacturer': self.manufacturer_info.name if self.manufacturer_info else None,
            'category': self.category.name if self.category else None,
            'price': float(self.price) if self.price else 0,
            'mrp': float(self.mrp) if self.mrp else 0,
            'discount_percentage': self.discount_percentage,
            'description_general': self.description_general,
            'uses': self.uses.split(';') if self.uses else [],
            'how_it_works': self.how_it_works,
            'how_to_use': self.how_to_use,
            'side_effects': self.side_effects.split(';') if self.side_effects else [],
            'precautions': self.precautions.split(';') if self.precautions else [],
            'interactions': self.interactions.split(';') if self.interactions else [],
            'dosage_form': self.dosage_form,
            'strength': self.strength,
            'pack_size': self.pack_size,
            'prescription_required': self.prescription_required,
            'is_active': self.is_active,
            'stock_quantity': self.stock_quantity,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'manufacturing_date': self.manufacturing_date.isoformat() if self.manufacturing_date else None,
            'batch_number': self.batch_number,
            'storage_conditions': self.storage_conditions
        }

class ProductSalt(db.Model):
    """Association table for Product and Salt with composition details"""
    __tablename__ = 'product_salts'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    salt_id = db.Column(db.Integer, db.ForeignKey('salts.id'), nullable=False)
    strength = db.Column(db.String(100), nullable=False)  # e.g., "300mg", "500IU"
    percentage = db.Column(db.Float)  # Percentage composition
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    salt = db.relationship('Salt', backref='product_salts')

    def to_dict(self):
        return {
            'salt_name': self.salt.name,
            'strength': self.strength,
            'percentage': self.percentage,
            'description': self.salt.description
        }

class Substitute(db.Model):
    """Substitute products model"""
    __tablename__ = 'substitutes'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    substitute_product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    similarity_score = db.Column(db.Float, default=0.0)  # How similar are the products
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    substitute_product = db.relationship('Product', foreign_keys=[substitute_product_id])

    def to_dict(self):
        return {
            'id': self.substitute_product.id,
            'name': self.substitute_product.name,
            'manufacturer': self.substitute_product.manufacturer_info.name,
            'price': float(self.substitute_product.price),
            'strength': self.substitute_product.strength,
            'similarity_score': self.similarity_score
        }

class FAQ(db.Model):
    """Frequently Asked Questions model"""
    __tablename__ = 'faqs'
    
    id = db.Column(db.Integer, primary_key=True)
    salt_id = db.Column(db.Integer, db.ForeignKey('salts.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100))  # Usage, Side Effects, Dosage, etc.
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category
        }

class Review(db.Model):
    """Product reviews model"""
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    title = db.Column(db.String(255))
    comment = db.Column(db.Text)
    reviewer_name = db.Column(db.String(100), default='Anonymous')
    verified_purchase = db.Column(db.Boolean, default=False)
    helpful_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'title': self.title,
            'comment': self.comment,
            'reviewer_name': self.reviewer_name,
            'verified_purchase': self.verified_purchase,
            'helpful_count': self.helpful_count,
            'date': self.created_at.strftime('%Y-%m-%d')
        }

class Order(db.Model):
    """Order model"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    status = db.Column(db.String(50), default='pending')  # pending, confirmed, shipped, delivered, cancelled
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    shipping_address = db.Column(db.Text)
    payment_method = db.Column(db.String(50))
    payment_status = db.Column(db.String(50), default='pending')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='order', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'status': self.status,
            'total_amount': float(self.total_amount),
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'created_at': self.created_at.isoformat()
        }

class OrderItem(db.Model):
    """Order items model"""
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'product_name': self.product.name,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price),
            'total_price': float(self.total_price)
        }