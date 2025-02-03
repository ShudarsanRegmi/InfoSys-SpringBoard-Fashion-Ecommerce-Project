from flask import Blueprint, render_template, get_flashed_messages, redirect, url_for, Response, flash, request, session, jsonify
from flask_login import login_required, current_user
from .models import db, Wishlist,Order,CartItem,OrderItem
from .forms import UpdateUserForm
from .decorators import is_delivery_person
from .constants import STATES_CITY
from datetime import datetime,timezone
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
        'stock': 1000,
        'category': 'Clothing',
        'brand':'Wrogn',
        'colour': 'White',
        'target_user':'Men',
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
        'brand':'Levis',
        'colour': 'Blue',
        'target_user':'Men',
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
        'brand':'Zara',
        'colour': 'orange',
        'target_user':['Women','girls'],
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
        'brand':'Puma',
        'colour': 'Brown',
        'target_user':'Men',
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
        'brand':'Campus',
        'colour': 'Blue',
        'target_user':'Men',
        'type': 'Shoes'
    },
    # Additional 10 dummy products
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
        'brand':'levis',
        'colour': 'White',
        'target_user':'Men',
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
        'brand':'Apple',
        'colour': 'Black',
        'target_user':'Unisex',
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
        'brand':'Safari',
        'colour': 'Black',
        'target_user':['Unisex'],
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
        'brand':'Boat',
        'colour': 'Black',
        'target_user':['Unisex'],
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
        'brand':'Boldfit',
        'colour': 'Pink',
        'target_user':'Unisex',
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
        'brand':'levis',
        'colour': 'Black',
        'target_user':['Men'],
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
        'brand':'Asus',
        'colour': 'Black',
        'target_user':['Unisex'],
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
        'brand':'levis',
        'colour': 'Red',
        'target_user':'Unisex',
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
        'brand': 'OnePlus',
        'colour': 'Black',
        'target_user':'Unisex',
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
        'brand': 'Boat',
        'colour': 'Brown',
        'target_user':['Unisex'],
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
    # Fetch similar products based on category and type
    similar_products = [p for p in products if (p['category'] == product['category'] or p['type'] == product['type']) and p['id'] != product_id]

    return render_template('product.html', product=product, similar_products=similar_products)


@bp.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    get_flashed_messages()
    form = UpdateUserForm(obj=current_user)  # Populate the form with the current user's data
    if form.state.data in STATES_CITY:
        form.city.choices = [(city, city) for city in STATES_CITY[form.state.data]]
    else:
        form.city.choices = []

    if request.method == 'POST' and form.validate_on_submit():
        try:
            current_user.firstname = form.firstname.data
            current_user.lastname = form.lastname.data
            current_user.address_line_1 = form.address_line_1.data
            current_user.state = form.state.data
            current_user.city = form.city.data
            current_user.role = form.role.data
            current_user.pincode = form.pincode.data

            db.session.commit()
            flash('Details updated successfully!', 'success')
            return redirect(url_for('auth.update_user'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')

    return render_template(
        'update_user.html',
        form=form,
        STATES_CITY=STATES_CITY
    )


@bp.route('/auth_error')
def auth_error():
    return render_template('notAuthorized.html')



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

@bp.route('/deliver')
@is_delivery_person
def deliver():
    return Response("Delivered", status=200)


@bp.route('/add_to_wishlist/<int:product_id>', methods=['POST'])
@login_required
def add_to_wishlist(product_id):
    # Find the product 
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


@bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if not current_user.is_authenticated:
        flash("Please log in to add items to the cart.", "warning")
        return redirect(url_for('auth.login'))

    # Get the product details
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return "Product not found", 404

    # Check if the item already exists in the user's cart
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()

    if cart_item:
        # If the product is already in the cart, update the quantity
        if cart_item.quantity < product['stock']:
            cart_item.quantity += 1
        else:
            flash("Stock limit reached!", "warning")
    else:
        # Add new product to the cart
        cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=1)
        db.session.add(cart_item)

    db.session.commit()
    flash("Product added to cart!", "success")
    return redirect(request.referrer)

@bp.route('/cart')
def cart():
    if not current_user.is_authenticated:
        flash("Please log in to view your cart.", "warning")
        return redirect(url_for('auth.login'))

    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    items_in_cart = []
    total_price = 0
    total_items = 0

    for item in cart_items:
        # Match with the dummy products
        product = next((p for p in products if p['id'] == item.product_id), None)
        if product:
            product_copy = product.copy()
            product_copy['quantity'] = item.quantity
            items_in_cart.append(product_copy)
            total_price += product['price'] * item.quantity
            total_items += item.quantity

    return render_template(
        'cart.html',
        cart_items=items_in_cart,
        total_price=total_price,
        total_items=total_items
    )


@bp.route("/update_quantity/<int:product_id>", methods=["POST"])
def update_quantity(product_id):
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'message': 'Please log in to update your cart.'}), 403

    # Get the cart item for the user and product
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if not cart_item:
        return jsonify({'success': False, 'message': 'Item not found in cart'}), 404

    try:
        new_quantity = int(request.json.get('quantity', 1))
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': 'Invalid quantity'}), 400

    # Check if the new quantity exceeds stock
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({'success': False, 'message': 'Product not found'}), 404

    if new_quantity > product['stock']:
        return jsonify({'success': False, 'message': f'Stock limit reached. Maximum available: {product["stock"]}'}), 400

    # Update or delete the cart item
    if new_quantity < 1:
        db.session.delete(cart_item)
    else:
        cart_item.quantity = new_quantity

    db.session.commit()

    # Calculate total price and total items
    total_price = sum(item.quantity * next((p for p in products if p['id'] == item.product_id), {}).get('price', 0)
                      for item in CartItem.query.filter_by(user_id=current_user.id).all())
    total_items = sum(item.quantity for item in CartItem.query.filter_by(user_id=current_user.id).all())

    return jsonify({'success': True, 'new_quantity': cart_item.quantity, 'total_price': total_price, 'total_items': total_items})

@bp.route('/remove-from-cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    if not current_user.is_authenticated:
        flash("Please log in to modify your cart.", "warning")
        return redirect(url_for('auth.login'))

    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        flash("Item removed from cart!", "success")
    return redirect(url_for('views.cart'))

@bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items_db = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items_db:
        flash('Your cart is empty!', 'danger')
        return redirect(url_for('views.cart'))

    # Fetch products and calculate costs from cart
    cart_items = []
    subtotal = 0
    for cart_item in cart_items_db:
        product = next((p for p in products if p["id"] == cart_item.product_id), None)
        if product:
            cart_items.append({
                'id': cart_item.product_id,
                'name': product['name'],
                'price': product['price'],
                'quantity': cart_item.quantity
            })
            subtotal += product['price'] * cart_item.quantity

    shipping = subtotal
    tax = subtotal * 1
    total = subtotal + shipping + tax

    # Pass data to the template
    return render_template(
        'checkout.html',
        cart_items=cart_items,
        subtotal=round(subtotal, 2),
        shipping=round(shipping, 2),
        tax=round(tax, 2),
        total=round(total, 2)
    )


@bp.route('/place_order', methods=['POST'])
@login_required
def place_order():
    user = current_user
    # Extract address information from the form
    address_line_1 = request.form.get('address_line_1')
    state = request.form.get('state')
    city = request.form.get('city')
    pincode = request.form.get('pincode')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')

    # Fetch cart items
    cart_items_db = CartItem.query.filter_by(user_id=user.id).all()
    if not cart_items_db:
        flash('Your cart is empty!', 'danger')
        return redirect(url_for('views.cart'))

    created_orders = []

    for cart_item in cart_items_db:
        product = next((p for p in products if p["id"] == cart_item.product_id), None)
        if not product:
            flash(f"Product with ID {cart_item.product_id} not found.", 'danger')
            continue

        total_cost = product['price'] * cart_item.quantity

        # Create a new order
        new_order = Order(
            user_id=user.id,
            product_id=cart_item.product_id,
            address_line_1=address_line_1,
            state=state,
            city=city,
            pincode=pincode,
            total_cost=total_cost,
            status="Pending"
        )

        db.session.add(new_order)
        db.session.commit()

        created_orders.append(new_order)

        # Add order item details
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=total_cost,
            product_name=product['name'],
            product_image=product['image']
        )
        db.session.add(order_item)
        db.session.commit()

    # Clear the user's cart after placing the order
    CartItem.query.filter_by(user_id=user.id).delete()
    db.session.commit()

    flash('Order placed successfully!', 'success')

    return jsonify({"success": True})




@bp.route('/my_orders')
@login_required
def my_orders():
    # Fetch all orders for the current user
    orders = (
        db.session.query(Order)
        .filter(Order.user_id == current_user.id)
        .all()
    )

    # Organizing data to group items under respective orders
    orders_data = []
    for order in orders:
        # Find the product associated with this order from the dummy product data
        product = next((p for p in products if p['id'] == order.product_id), None)

        # Fetch related OrderItem details
        order_items = db.session.query(OrderItem).filter(OrderItem.order_id == order.id).all()

        total_quantity = sum(item.quantity for item in order_items)
        total_price = order.total_cost  # Ensure total_cost is stored in the Order model

        if product:
            orders_data.append({
                "order": order,
                "product": product,
                "total_quantity": total_quantity,
                "total_price": total_price
            })

    return render_template('my_orders.html', orders_data=orders_data)





@bp.route('/cancel_order/<int:order_id>', methods=['POST'])
@login_required
def cancel_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('You can only cancel your own orders.', 'danger')
        return redirect(url_for('views.my_orders'))

    # Update the order status to 'Cancelled'
    order.status = 'Cancelled'
    db.session.commit()

    flash('Order has been cancelled successfully.', 'success')
    return redirect(url_for('views.my_orders'))
