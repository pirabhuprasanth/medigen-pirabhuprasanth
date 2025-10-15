# backend/app/routes.py
from flask import Blueprint, jsonify, request
from .models import (
    db, User, Product, Salt, FAQ, Review, Manufacturer, 
    Category, ProductSalt, Substitute, Order, OrderItem
)
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity,
    create_refresh_token, get_jwt
)
from datetime import timedelta
import uuid
from sqlalchemy import or_, and_

api_bp = Blueprint('api_bp', __name__)

# --- Authentication Endpoints ---
@api_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint with JWT token generation"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400
            
        user = User.query.filter(
            or_(User.username == username, User.email == username)
        ).first()
        
        if user and user.check_password(password) and user.is_active:
            # Create tokens
            access_token = create_access_token(
                identity=user.username,
                expires_delta=timedelta(hours=24)
            )
            refresh_token = create_refresh_token(identity=user.username)
            
            return jsonify({
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": user.to_dict(),
                "message": "Login successful"
            }), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401
            
    except Exception as e:
        return jsonify({"error": "Login failed", "details": str(e)}), 500

@api_bp.route('/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"{field} is required"}), 400
        
        # Check if user exists
        existing_user = User.query.filter(
            or_(User.username == data['username'], User.email == data['email'])
        ).first()
        
        if existing_user:
            return jsonify({"error": "Username or email already exists"}), 400
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', '')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            "message": "User registered successfully",
            "user": user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Registration failed", "details": str(e)}), 500

@api_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh JWT token"""
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_token)

@api_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """User logout endpoint"""
    return jsonify({"message": "Successfully logged out"}), 200

@api_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    
    if user:
        return jsonify({"user": user.to_dict()}), 200
    return jsonify({"error": "User not found"}), 404

# --- Product Data Endpoints ---
@api_bp.route('/product/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product_data(product_id):
    """Fetch comprehensive product data for product page"""
    try:
        product = Product.query.get_or_404(product_id)
        
        # 1. Product Details
        product_details = product.to_dict()
        
        # 2. Salt Content with detailed composition
        salt_content = [salt.to_dict() for salt in product.product_salts]
        
        # 3. Substitutes based on similar products
        substitutes_query = Substitute.query.filter_by(product_id=product_id).limit(6)
        substitutes_data = [sub.to_dict() for sub in substitutes_query]
        
        # If no predefined substitutes, find products with similar salts
        if not substitutes_data:
            # Get products with similar salt composition
            similar_products = Product.query.join(ProductSalt).join(Salt).filter(
                Salt.id.in_([ps.salt_id for ps in product.product_salts]),
                Product.id != product_id,
                Product.is_active == True
            ).limit(6).all()
            
            substitutes_data = [{
                'id': p.id,
                'name': p.name,
                'manufacturer': p.manufacturer_info.name if p.manufacturer_info else '',
                'price': float(p.price),
                'strength': p.strength,
                'similarity_score': 0.8
            } for p in similar_products]
        
        # 4. FAQs - both product-specific and salt-specific
        faqs_data = []
        
        # Product-specific FAQs
        product_faqs = FAQ.query.filter_by(product_id=product_id, is_active=True).all()
        faqs_data.extend([faq.to_dict() for faq in product_faqs])
        
        # Salt-specific FAQs
        if product.product_salts:
            salt_ids = [ps.salt_id for ps in product.product_salts]
            salt_faqs = FAQ.query.filter(
                FAQ.salt_id.in_(salt_ids),
                FAQ.is_active == True
            ).limit(10).all()
            faqs_data.extend([faq.to_dict() for faq in salt_faqs])
        
        # 5. Reviews with user details
        reviews_data = [review.to_dict() for review in product.reviews if review.is_active]
        
        # Calculate average rating
        avg_rating = 0
        if reviews_data:
            avg_rating = sum(review['rating'] for review in reviews_data) / len(reviews_data)
        
        # 6. Related products from same category
        related_products = []
        if product.category_id:
            related = Product.query.filter(
                Product.category_id == product.category_id,
                Product.id != product_id,
                Product.is_active == True
            ).limit(4).all()
            related_products = [p.to_dict() for p in related]
        
        return jsonify({
            "product_details": product_details,
            "salt_content": salt_content,
            "substitutes": substitutes_data,
            "faqs": faqs_data,
            "reviews": reviews_data,
            "average_rating": round(avg_rating, 1),
            "total_reviews": len(reviews_data),
            "related_products": related_products
        }), 200
        
    except Exception as e:
        return jsonify({"error": "Failed to fetch product data", "details": str(e)}), 500

@api_bp.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    """Get paginated list of products with filters"""
    try:
        # Query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '')
        category_id = request.args.get('category_id', type=int)
        manufacturer_id = request.args.get('manufacturer_id', type=int)
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        prescription_required = request.args.get('prescription_required', type=bool)
        
        # Build query
        query = Product.query.filter(Product.is_active == True)
        
        # Apply filters
        if search:
            query = query.filter(
                or_(
                    Product.name.ilike(f'%{search}%'),
                    Product.description_general.ilike(f'%{search}%')
                )
            )
        
        if category_id:
            query = query.filter(Product.category_id == category_id)
            
        if manufacturer_id:
            query = query.filter(Product.manufacturer_id == manufacturer_id)
            
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
            
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
            
        if prescription_required is not None:
            query = query.filter(Product.prescription_required == prescription_required)
        
        # Pagination
        products = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            "products": [product.to_dict() for product in products.items],
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": products.total,
                "pages": products.pages,
                "has_next": products.has_next,
                "has_prev": products.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": "Failed to fetch products", "details": str(e)}), 500

@api_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all product categories"""
    try:
        categories = Category.query.all()
        return jsonify({
            "categories": [category.to_dict() for category in categories]
        }), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch categories", "details": str(e)}), 500

@api_bp.route('/manufacturers', methods=['GET'])
def get_manufacturers():
    """Get all manufacturers"""
    try:
        manufacturers = Manufacturer.query.all()
        return jsonify({
            "manufacturers": [manufacturer.to_dict() for manufacturer in manufacturers]
        }), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch manufacturers", "details": str(e)}), 500

# --- Review Endpoints ---
@api_bp.route('/product/<int:product_id>/reviews', methods=['GET'])
@jwt_required()
def get_product_reviews(product_id):
    """Get reviews for a specific product"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        reviews = Review.query.filter(
            Review.product_id == product_id,
            Review.is_active == True
        ).order_by(Review.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            "reviews": [review.to_dict() for review in reviews.items],
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": reviews.total,
                "pages": reviews.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": "Failed to fetch reviews", "details": str(e)}), 500

@api_bp.route('/product/<int:product_id>/reviews', methods=['POST'])
@jwt_required()
def add_product_review(product_id):
    """Add a review for a product"""
    try:
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ['rating', 'comment']):
            return jsonify({"error": "Rating and comment are required"}), 400
        
        if not (1 <= data['rating'] <= 5):
            return jsonify({"error": "Rating must be between 1 and 5"}), 400
        
        # Check if product exists
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404
        
        # Create review
        review = Review(
            product_id=product_id,
            user_id=user.id if user else None,
            rating=data['rating'],
            title=data.get('title', ''),
            comment=data['comment'],
            reviewer_name=data.get('reviewer_name', user.first_name if user else 'Anonymous')
        )
        
        db.session.add(review)
        db.session.commit()
        
        return jsonify({
            "message": "Review added successfully",
            "review": review.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to add review", "details": str(e)}), 500

# --- Search Endpoints ---
@api_bp.route('/search', methods=['GET'])
@jwt_required()
def search_products():
    """Advanced product search"""
    try:
        query = request.args.get('q', '')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        if not query:
            return jsonify({"error": "Search query is required"}), 400
        
        # Search in products, salts, and manufacturers
        products = Product.query.join(ProductSalt).join(Salt).join(Manufacturer).filter(
            or_(
                Product.name.ilike(f'%{query}%'),
                Product.description_general.ilike(f'%{query}%'),
                Salt.name.ilike(f'%{query}%'),
                Manufacturer.name.ilike(f'%{query}%')
            ),
            Product.is_active == True
        ).distinct().paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            "products": [product.to_dict() for product in products.items],
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": products.total,
                "pages": products.pages
            },
            "query": query
        }), 200
        
    except Exception as e:
        return jsonify({"error": "Search failed", "details": str(e)}), 500

# --- Order Management Endpoints ---
@api_bp.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    """Create a new order"""
    try:
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        
        data = request.get_json()
        items = data.get('items', [])
        
        if not items:
            return jsonify({"error": "Order items are required"}), 400
        
        # Calculate total amount
        total_amount = 0
        order_items = []
        
        for item in items:
            product = Product.query.get(item['product_id'])
            if not product:
                return jsonify({"error": f"Product {item['product_id']} not found"}), 404
            
            quantity = item['quantity']
            unit_price = product.price
            item_total = unit_price * quantity
            total_amount += item_total
            
            order_items.append({
                'product_id': product.id,
                'quantity': quantity,
                'unit_price': unit_price,
                'total_price': item_total
            })
        
        # Create order
        order = Order(
            user_id=user.id,
            order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
            total_amount=total_amount,
            shipping_address=data.get('shipping_address', ''),
            payment_method=data.get('payment_method', 'COD'),
            notes=data.get('notes', '')
        )
        
        db.session.add(order)
        db.session.flush()  # Get the order ID
        
        # Create order items
        for item_data in order_items:
            order_item = OrderItem(
                order_id=order.id,
                **item_data
            )
            db.session.add(order_item)
        
        db.session.commit()
        
        return jsonify({
            "message": "Order created successfully",
            "order": order.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create order", "details": str(e)}), 500

@api_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_user_orders():
    """Get current user's orders"""
    try:
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        
        orders = Order.query.filter_by(user_id=user.id).order_by(Order.created_at.desc()).all()
        
        return jsonify({
            "orders": [order.to_dict() for order in orders]
        }), 200
        
    except Exception as e:
        return jsonify({"error": "Failed to fetch orders", "details": str(e)}), 500

# --- Health Check Endpoint ---
@api_bp.route('/health', methods=['GET'])
def health_check():
    """API health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "MediCare API is running",
        "version": "1.0.0"
    }), 200