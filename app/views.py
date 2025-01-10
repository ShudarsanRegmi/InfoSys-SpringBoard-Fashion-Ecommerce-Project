from flask import Blueprint, render_template, get_flashed_messages, redirect, url_for, request, jsonify, session, flash
from flask_login import login_required, current_user
from .models import db, CartItem, Wishlist
from .forms import UpdateUserForm
import logging
bp = Blueprint('views', __name__)


# Dummy Product Data (for rendering)
products = [
    {
        'id': 1,
        'name': 'Classic White Shirt',
        'price': 1999,
        'image': 'static/Products/white.jpeg',
        'description': 'A timeless classic for any wardrobe, perfect for both formal and casual occasions.',
        'details': [
            'Made from 100% premium cotton.',
            'Breathable and comfortable for all-day wear.',
            'Available in multiple sizes for the perfect fit.',
            'Machine washable and easy to maintain.',
            'Perfect for office, events, and everyday use.'
        ],
        'stock': 2,
        'category': 'Clothing',
        'type': 'Shirt'
    },
    {
        'id': 2,
        'name': 'Denim Jacket',
        'price': 3499,
        'image': 'static/Products/dDenim Jacket.jpeg',
        'description': 'A stylish denim jacket that adds an edgy touch to your outfit.',
        'details': [
            'Durable and soft denim fabric.',
            'Slim-fit design with button closure.',
            'Features side pockets and a classic collar.',
            'Perfect for layering in any season.',
            'Hand-wash recommended for extended durability.'
        ],
        'stock': 2,
        'category': 'Clothing',
        'type': 'Jacket'
    },
    {
        'id': 3,
        'name': 'Summer Floral Dress',
        'price': 2799,
        'image': 'static/Products/dSummer Floral Dress.jpeg',
        'description': 'A breezy floral dress ideal for summer outings and vacations.',
        'details': [
            'Lightweight, flowy material for comfort.',
            'Beautiful floral prints with vibrant colors.',
            'Adjustable straps for a customized fit.',
            'Perfect for brunches, picnics, or beach outings.',
            'Machine washable and fade-resistant.'
        ],
        'stock': 2,
        'category': 'Clothing',
        'type': 'Dress'
    },
    {
        'id': 4,
        'name': 'Leather Wallet',
        'price': 1299,
        'image': 'static/Products/Leather Wallet.jpeg',
        'description': 'A sleek and functional leather wallet for everyday use.',
        'details': [
            'Crafted from genuine leather for durability.',
            'Multiple compartments for cards and cash.',
            'Compact design to fit in any pocket.',
            'Available in black and brown colors.',
            'A great gift for friends and family.'
        ],
        'stock': 2,
        'category': 'Accessories',
        'type': 'Wallet'
    },
    {
        'id': 5,
        'name': 'Running Shoes',
        'price': 3999,
        'image': 'static/Products/shoes.jpeg',
        'description': 'High-performance running shoes for athletes and fitness enthusiasts.',
        'details': [
            'Breathable mesh upper for ventilation.',
            'Cushioned sole for maximum comfort.',
            'Slip-resistant outsole for stability.',
            'Lightweight design for enhanced speed.',
            'Available in various sizes and colors.'
        ],
        'stock': 0,
        'category': 'Footwear',
        'type': 'Shoes'
    },
    {
        'id': 6,
        'name': 'Silk Tie Set',
        'price': 999,
        'image': 'static/Products/tie.jpeg',
        'description': 'A premium silk tie set for formal occasions.',
        'details': [
            'Includes matching pocket square.',
            'Made from high-quality silk fabric.',
            'Perfect for weddings, parties, and office wear.',
            'Easy to clean and maintain.'
        ],
        'stock': 5,
        'category': 'Accessories',
        'type': 'Tie'
    },
    {
        'id': 7,
        'name': 'Smartwatch',
        'price': 7999,
        'image': 'static/Products/smartwatch.jpeg',
        'description': 'A feature-packed smartwatch for health and connectivity.',
        'details': [
            'Tracks heart rate, steps, and sleep patterns.',
            'Water-resistant and durable design.',
            'Syncs with your smartphone for notifications.',
            'Available in multiple strap colors.'
        ],
        'stock': 3,
        'category': 'Electronics',
        'type': 'Watch'
    },
    {
        'id': 8,
        'name': 'Backpack',
        'price': 2499,
        'image': 'static/Products/backpack.jpeg',
        'description': 'A stylish and spacious backpack for work or travel.',
        'details': [
            'Made from water-resistant material.',
            'Multiple compartments for organized storage.',
            'Comfortable shoulder straps.',
            'Available in multiple colors.'
        ],
        'stock': 4,
        'category': 'Accessories',
        'type': 'Bag'
    },
    {
        'id': 9,
        'name': 'Wireless Earbuds',
        'price': 3499,
        'image': 'static/Products/earbuds.jpeg',
        'description': 'Premium wireless earbuds with noise cancellation.',
        'details': [
            'Superior sound quality with deep bass.',
            'Long battery life for all-day use.',
            'Comes with a compact charging case.',
            'Sweat and splash resistant.'
        ],
        'stock': 6,
        'category': 'Electronics',
        'type': 'Earbuds'
    },
    {
        'id': 10,
        'name': 'Yoga Mat',
        'price': 1299,
        'image': 'static/Products/yogamat.jpeg',
        'description': 'Non-slip yoga mat for fitness and relaxation.',
        'details': [
            'Made from eco-friendly materials.',
            'Offers excellent grip and cushioning.',
            'Lightweight and easy to carry.',
            'Ideal for yoga, Pilates, and workouts.'
        ],
        'stock': 7,
        'category': 'Fitness',
        'type': 'Mat'
    },
    {
        'id': 11,
        'name': 'Formal Black Blazer',
        'price': 4999,
        'image': 'static/Products/blazer.jpeg',
        'description': 'A tailored blazer for formal events and office wear.',
        'details': [
            'Made from high-quality fabric.',
            'Slim-fit design with classic lapels.',
            'Available in multiple sizes.',
            'Dry clean recommended.'
        ],
        'stock': 2,
        'category': 'Clothing',
        'type': 'Blazer'
    },
    {
        'id': 12,
        'name': 'Gaming Mouse',
        'price': 1999,
        'image': 'static/Products/gaming_mouse.jpeg',
        'description': 'Ergonomic gaming mouse with customizable buttons.',
        'details': [
            'Adjustable DPI for precision.',
            'RGB lighting for a cool aesthetic.',
            'Compatible with all major operating systems.',
            'Plug-and-play setup.'
        ],
        'stock': 8,
        'category': 'Electronics',
        'type': 'Mouse'
    },
    {
        'id': 13,
        'name': 'Cotton Bedsheet',
        'price': 1499,
        'image': 'static/Products/bedsheet.jpeg',
        'description': 'A soft and comfortable bedsheet for a good night’s sleep.',
        'details': [
            'Made from 100% cotton.',
            'Available in vibrant patterns.',
            'Machine washable and durable.',
            'Perfect for all bed sizes.'
        ],
        'stock': 10,
        'category': 'Home',
        'type': 'Bedsheet'
    },
    {
        'id': 14,
        'name': 'Bluetooth Speaker',
        'price': 2599,
        'image': 'static/Products/speaker.jpeg',
        'description': 'Compact Bluetooth speaker with superior sound quality.',
        'details': [
            'Long battery life and quick charging.',
            'Supports hands-free calls.',
            'Water-resistant and durable.',
            'Compatible with all Bluetooth devices.'
        ],
        'stock': 5,
        'category': 'Electronics',
        'type': 'Speaker'
    },
    {
        'id': 15,
        'name': 'Wrist Watch',
        'price': 3499,
        'image': 'static/Products/wristwatch.jpeg',
        'description': 'A classic wristwatch with an elegant design.',
        'details': [
            'Quartz movement for precise timekeeping.',
            'Stainless steel strap.',
            'Water-resistant up to 50 meters.',
            'Available in gold and silver tones.'
        ],
        'stock': 3,
        'category': 'Accessories',
        'type': 'Watch'
    }
]

@bp.route("/")
@bp.route('/home')
@login_required
def home():
    print("going to render homepage...")
    return render_template('home.html', products=products)


@bp.route('/product/<int:product_id>')
def product_details(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product is None:
        return "Product not found", 404
    return render_template('product.html', product=product)


@bp.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    get_flashed_messages()
    form = UpdateUserForm(obj=current_user)  # Prepopulate form with current_user data
    if form.validate_on_submit():
        form.populate_obj(current_user)  # Update user object with form data
        db.session.commit()
        return redirect(url_for('views.home'))
    return render_template('update_user.html', form=form)


@bp.route('/auth_error')
def auth_error():
    return render_template('notAuthorized.html')


@bp.route('/add_to_cart/<product_id>', methods=['POST'])
def add_to_cart(product_id):
    # Ensure product_id is an integer
    try:
        product_id = int(product_id)
    except ValueError:
        return "Invalid product ID", 400

    # Initialize cart in session if not already present
    if 'cart' not in session:
        session['cart'] = {}

    # Initialize cart to hold products as integers
    cart = {int(k): v for k, v in session['cart'].items()}

    # Get the product from the products list
    product = next((p for p in products if p['id'] == product_id), None)

    if product:
        # If product is already in the cart, increment the quantity, but not exceeding stock
        if product_id in cart:
            if cart[product_id] < product['stock']:
                cart[product_id] += 1  # Increment quantity by 1
            else:
                # If the cart quantity reaches stock, don't increase it further
                cart[product_id] = product['stock']
        else:
            # Add the product to the cart with a quantity of 1 if it's not already in the cart
            cart[product_id] = 1

    # Save the updated cart back to the session
    session['cart'] = cart

    # Redirect to the product details page or referrer
    return redirect(request.referrer)


@bp.route("/cart")
def cart():
    cart = session.get("cart", {})
    cart_items = []
    total_price = 0  # Initialize total price
    total_items = 0  # Initialize total items count

    # Loop through the cart to get each product and calculate totals
    for product_id, quantity in cart.items():
        product_id = int(product_id)

        product = next((p for p in products if p["id"] == product_id), None)
        if product:
            product_copy = product.copy()
            product_copy["quantity"] = quantity
            cart_items.append(product_copy)

            # Calculate total price for this product
            total_price += product["price"] * quantity
            total_items += quantity  # Add quantity to total items

    # Pass total price and total items to the template
    return render_template("cart.html", cart_items=cart_items, total_price=total_price, total_items=total_items)

@bp.route("/update_quantity/<int:product_id>", methods=["POST"])
def update_quantity(product_id):
    cart = session.get("cart", {})
    try:
        # Parse new quantity from request data
        new_quantity = int(request.json.get('quantity', 1))
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': 'Invalid quantity'}), 400

    product = next((p for p in products if p['id'] == product_id), None)

    if not product:
        return jsonify({'success': False, 'message': 'Product not found'}), 404

    if new_quantity > product['stock']:
        new_quantity = product['stock']  # Cap quantity to available stock

    if new_quantity < 1:
        cart.pop(str(product_id), None)  # Remove product if quantity is 0 or less
    else:
        cart[str(product_id)] = new_quantity

    session['cart'] = cart

    # Calculate new total price and total items
    total_price = sum(product["price"] * quantity for product_id, quantity in cart.items() if (product := next((p for p in products if p["id"] == int(product_id)), None)))
    total_items = sum(cart.values())  # Total items is the sum of all quantities

    return jsonify({'success': True, 'new_quantity': new_quantity, 'total_price': total_price, 'total_items': total_items})

@bp.route('/remove-from-cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        session['cart'] = cart
        flash("Item removed from cart!", "success")
    return redirect(url_for('views.cart'))

@bp.route('/add_to_wishlist/<int:product_id>', methods=['POST'])
@login_required
def add_to_wishlist(product_id):
    # Find the product (Assuming 'products' is a list or query of products)
    product = next((p for p in products if p['id'] == product_id), None)
    
    if not product:
        # If product not found, flash an error message and redirect
        flash('Product not found', 'danger')
        return redirect(url_for('views.product_details', product_id=product_id))

    # Check if product already exists in wishlist
    existing_item = Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if existing_item:
        # If product already in wishlist, flash a message and redirect
        flash('Product already in wishlist', 'info')
        return redirect(url_for('views.product_details', product_id=product_id))

    # Add the product to the wishlist
    wishlist_item = Wishlist(user_id=current_user.id, product_id=product_id)
    db.session.add(wishlist_item)
    db.session.commit()

    # Flash success message and redirect
    flash('Product added to wishlist!', 'success')
    return redirect(url_for('views.product_details', product_id=product_id))


@bp.route('/wishlist')
@login_required
def view_wishlist():
    wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).all()
    products_in_wishlist = []
    for item in wishlist_items:
        product = next((p for p in products if p['id'] == item.product_id), None)
        if product:
            products_in_wishlist.append(product)
    
    return render_template('wishlist.html', products=products_in_wishlist)

@bp.route('/remove-from-wishlist/<int:product_id>', methods=['POST'])
@login_required
def remove_from_wishlist(product_id):
    wishlist_item = Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if wishlist_item:
        db.session.delete(wishlist_item)
        db.session.commit()
        flash("Item removed from wishlist!", "success")
    else:
        flash("Item not found in wishlist.", "error")
    
    return redirect(url_for('views.view_wishlist'))
@bp.route('/search')
def search():
    query = request.args.get('query', '').lower()  # Get the search query from the URL parameters
    query_words = query.split()  # Split the query into individual words
    
    if query:
        results = []
        
        # Loop through each product and check if it matches the individual words or combined query
        for p in products:
            try:
                # Combine product attributes into one string for easier matching
                product_str = (
                    str(p.get('name', '')).lower() + ' ' + 
                    str(p.get('description', '')).lower() + ' ' + 
                    str(p.get('brand', '')).lower() + ' ' + 
                    str(p.get('colour', '')).lower() + ' ' + 
                    str(p.get('category', '')).lower() + ' ' + 
                    str(p.get('target_user', '')).lower() + ' ' + 
                    str(p.get('type', '')).lower()
                )
                
                # Check for exact matches for each word in the query
                individual_match = all(word in product_str.split() for word in query_words)
                
                # Check if the entire query (combined) exists in the product attributes (combined search)
                combined_match = query in product_str
                
                if individual_match or combined_match:
                    results.append(p)
            except Exception as e:
                print(f"Error processing product: {p}. Error: {e}")
                continue  # Skip any products that cause an error
                
    else:
        results = []  # No results if query is empty
    
    return render_template('search_results.html', query=query, results=results)
@bp.route('/category/<category>')
def category(category):
    category = category.lower()
    results = [p for p in products if p['category'].lower() == category]
    return render_template('category_results.html', category=category.capitalize(), results=results)