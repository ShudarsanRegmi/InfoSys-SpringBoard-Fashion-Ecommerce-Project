from flask import Blueprint, render_template, get_flashed_messages, redirect, url_for, Response, flash, request, session, jsonify
from flask_login import login_required, current_user
from .models import db, Wishlist,Order,CartItem,OrderItems
from .forms import UpdateUserForm
from .decorators import is_delivery_person, is_admin
from .constants import STATES_CITY, PRODUCTS
bp = Blueprint('views', __name__)
from .models import Product, Order
import os
from datetime import datetime,timezone
import logging
from werkzeug.utils import secure_filename
from .methods import send_thankyou_email

OrderItem = OrderItems

@bp.route("/")
@bp.route('/home')
@login_required
def home():
    if current_user.isDeliveryPerson():
        return redirect(url_for('views.dashboard'))
    
    if current_user.isAdmin():
        return redirect(url_for('admin.index'))
    
    global PRODUCTS
    PRODUCTS = Product.query.all()
    return render_template('home.html', products=PRODUCTS)


@bp.route('/product/<int:product_id>')
@login_required
def product_details(product_id):
    product = Product.query.get(product_id)
    PRODUCTS = Product.query.all()
    if product is None:
        return "Product not found", 404
    similar_products = [_ for _ in PRODUCTS if ((_.category == product.category or _.type == product.type or _.target_user == product.target_user) and _.id != product.id) ]
    
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
            return redirect(url_for('views.profile'))
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


@bp.route('/add_to_wishlist/<int:product_id>', methods=['POST'])
@login_required
def add_to_wishlist(product_id):
    # Find the product 
    product = Product.query.get(product_id)

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
        product = Product.query.get(item.product_id)
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
    product = Product.query.get(product_id)
    if not product:
        return "Product not found", 404

    # Check if the item already exists in the user's cart
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()

    if cart_item:
        # If the product is already in the cart, update the quantity
        if cart_item.quantity < product.stock_quantity:
            cart_item.quantity += 1
        else:
            flash("Stock limit reached!", "warning")
    else:
        # Add new product to the cart
        cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=1)
        db.session.add(cart_item)

    db.session.commit()
    # flash("Product added to cart!", "success")
    return redirect(request.referrer)


@bp.route('/cart')
def cart():
    if not current_user.is_authenticated:
        flash("Please log in to view your cart.", "warning")
        return redirect(url_for('auth.login'))

    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total_amount = sum(item.quantity * item.product.price for item in cart_items)
    total_items = sum(item.quantity for item in cart_items)

    return render_template(
        'cart.html',
        cart_items=cart_items,
        total_price=total_amount,
        total_items=total_items
    )

@bp.route("/update_quantity/<int:product_id>", methods=["POST"])
@login_required
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
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
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
    total_price = sum(item.quantity * next((p for p in PRODUCTS if p['id'] == item.product_id), {}).get('price', 0)
                      for item in CartItem.query.filter_by(user_id=current_user.id).all())
    total_items = sum(item.quantity for item in CartItem.query.filter_by(user_id=current_user.id).all())

    return jsonify({'success': True, 'new_quantity': cart_item.quantity, 'total_price': total_price, 'total_items': total_items})


@bp.route('/remove-from-cart/<int:product_id>', methods=['POST'])
@login_required
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


@bp.route('/search')
@login_required
def search():
    query = request.args.get('query', '').lower()  # Get the search query from the URL parameters
    query_words = query.split()  # Split the query into individual words

    PRODUCTS = Product.query.all()
    
    if query:
        results = []
        
        # Loop through each product and check if it matches the individual words or combined query
        for p in PRODUCTS:
            try:
                # Combine product attributes into one string for easier matching
                product_str = str(p.name).lower() + ' ' + str(p.description).lower() + ' ' + str(p.brand).lower() + ' ' + str(p.colour).lower() + ' ' + str(p.category).lower() + ' ' + str(p.target_user).lower() + ' ' + str(p.type).lower()
                
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
    PRODUCTS = Product.query.all()
    results = [p for p in PRODUCTS if p.category.lower() == category.lower()]
    return render_template('category_results.html', category=category.capitalize(), results=results)

@bp.route('/deliver')
@login_required
@is_delivery_person
def deliver():
    return Response("Delivered", status=200)

@bp.route('/partner_dash')
@login_required
@is_delivery_person
def dashboard():
     # Use current_user which represents the logged-in delivery person
    delivery_person = current_user
    pincode = delivery_person.pincode  # Get pincode from current_user

    # Fetch new orders that haven't been assigned (deliver_person is None) and match the pincode
    new_orders = Order.query.filter(Order.delivery_person_id.is_(None), Order.pincode == pincode, Order.status == "Pending").all()

    # Fetch orders assigned to this delivery person, 
    assigned_orders = Order.query.filter(Order.delivery_person_id == current_user.id, Order.status == 'Pending').all()

    # Fetch orders cancelled by this delivery person
    cancelled_orders = Order.query.filter(Order.delivery_person_id == current_user.id, Order.status == 'Cancelled').all()

    # Fetch delivered orders (status 'Delivered Successfully') for this delivery person
    delivered_orders = Order.query.filter(Order.delivery_person_id == current_user.id, Order.status == 'Delivered').all()

    return render_template('partner_home.html',
                           new_orders=new_orders,
                           assigned_orders=assigned_orders,
                           delivered_orders=delivered_orders,
                           cancelled_orders=cancelled_orders)


@bp.route('/update_status/<int:order_id>', methods=['POST'])
@is_delivery_person
def update_status(order_id):
    order = Order.query.filter_by(id = order_id).first()

    if order:
        new_status = request.form['status']
        order.status = new_status

        # If the order was not assigned (deliver_person is None), assign it to the current delivery person
        if order.delivery_person_id is None:
            order.delivery_person_id = current_user.id

        # Handle the case when the order is successfully delivered
        if order.status == 'Delivered':
            order.delivery_date = datetime.now(timezone.utc)
            # def send_thankyou_email(to_email, user_name, rating_url = None):
            send_thankyou_email(order_id)  # Send a thank you email
            # Move the order to the delivered orders section
            # Optionally, remove it from the assigned orders (this is handled by the dashboard query)

        # Commit the changes to the database
        db.session.commit()


    return redirect(url_for('views.dashboard'))  # Redirect back to the dashboard





# @bp.route('/rate_product/<int:order_id>', methods=['GET', 'POST'])
# @login_required
# def rate_product(order_id):
#     # Fetch the order using the order_id
#     order = Order.query.get_or_404(order_id)

#     # Fetch the product associated with the order
#     product = Product.query.get_or_404(order.product_id)

#     if request.method == 'POST':
#         try:
#             # Get the user's rating from the form (rating is expected to be between 1 and 5)
#             rating = request.form['rating']  # Assumes the form will send a 'rating' field as 1, 2, 3, 4, or 5
#             customer_rating = int(rating)  # Convert rating to integer

#             # Check if the product has already been rated
#             if product.rating == 'not rated':
#                 # If not rated yet, store the customer's rating
#                 product.rating = str(customer_rating)
#             else:
#                 # If rated, calculate the new average rating
#                 current_rating = float(product.rating)
#                 new_rating = (current_rating + customer_rating) / 2
#                 product.rating = str(new_rating)

#             # Commit the changes to the database
#             db.session.commit()

#             # Flash success message and redirect to the product page or a thank-you page
#             flash(f"Thank you for rating! Your rating of {customer_rating} has been saved.", "success")
#             return redirect(url_for('auth.login'))

#         except Exception as e:
#             db.session.rollback()
#             print(f"Error occurred while rating the product: {e}")
#             flash("An error occurred while submitting your rating. Please try again later.", "danger")
#             return redirect(url_for('views.view_product', id=product.id))

#     return render_template('rate_product.html', product=product,order=order)

@bp.route('/rate_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def rate_product(product_id):
    # Fetch the order using the order_id
    # order = Order.query.get_or_404(order_id)

    # Fetch the product associated with the order
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        try:
            # Get the user's rating from the form (rating is expected to be between 1 and 5)
            rating = request.form['rating']  # Assumes the form will send a 'rating' field as 1, 2, 3, 4, or 5
            customer_rating = int(rating)  # Convert rating to integer

            # Check if the product has already been rated
            if not product.rating or product.rating == 'not rated':  # Handles None or 'not rated'
                # If not rated yet, store the customer's rating
                product.rating = str(customer_rating)
            else:
                # If rated, calculate the new average rating
                print("Product rating = " + product.rating)
                current_rating = float(product.rating)
                new_rating = (current_rating + customer_rating) / 2
                product.rating = str(new_rating)

            # Commit the changes to the database
            db.session.commit()

            # Flash success message and redirect to the product page or a thank-you page
            flash(f"Thank you for rating! Your rating of {customer_rating} has been saved.", "success")
            return redirect(url_for('auth.login'))

        except Exception as e:
            db.session.rollback()
            print(f"Error occurred while rating the product: {e}")
            flash("An error occurred while submitting your rating. Please try again later.", "danger")
            # return redirect(url_for('views.view_product', id=product.id))

    return render_template('rate_product.html', product=product)

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html')


# Team 2 Merge

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
        product = Product.query.get(cart_item.product_id)
        if product:
            cart_items.append({
                'id': cart_item.product_id,
                'name': product.name,
                'price': product.price,
                'quantity': cart_item.quantity
            })
            subtotal += product.price * cart_item.quantity

    shipping = 40
    tax = subtotal * 5/100  # 5% tax
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

    address_line_1 = request.form.get('address_line_1')
    state = request.form.get('state')
    city = request.form.get('city')
    pincode = request.form.get('pincode')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')

    # Fetch the product ID and quantity from the cart
    cart_items_db = CartItem.query.filter_by(user_id=user.id).all()
    if not cart_items_db:
        flash('Your cart is empty!', 'danger')
        return redirect(url_for('views.checkout'))

    
    # Create a new order
    new_order = Order(customer_id=user.id, customer_name=firstname+" "+lastname, address_line_1=address_line_1, state=state, city=city, pincode=pincode, price=0, status="Pending", mail=email)
    db.session.add(new_order)
    db.session.commit()  # Commit order immediately to get order ID
    db.session.refresh(new_order)  # Refresh to get the latest order ID

    for cart_item in cart_items_db:
        # Fetch the product from the dummy data using product_id from the cart
        product = Product.query.get(cart_item.product_id)
        if not product:
            flash(f"Product with ID {cart_item.product_id} not found.", 'danger')
            continue

        # Calculate total cost for the product
        total_cost = product.price * cart_item.quantity


        new_order.price += total_cost

        # Create an OrderItem entry for this order
        order_item = OrderItem(OrderID=new_order.id, ProductID=cart_item.product_id, UserID=user.id, Quantity=cart_item.quantity, Price=total_cost)
        
        db.session.add(order_item)
        db.session.commit()  # Commit order item immediately
        db.session.refresh(order_item)  # Refresh order item

        #decrease the stock levels of the products
        
        product.stock_quantity -= cart_item.quantity

    # Clear the user's cart after order placement
    CartItem.query.filter_by(user_id=user.id).delete()
    db.session.commit()

    # flash('Order(s) placed successfully and your cart has been emptied!', 'success')

    return jsonify({"success": True})


@bp.route('/my_orders')
@login_required
def my_orders():
    # Fetch all orders for the current user
    orders = db.session.query(Order).filter(Order.customer_id == current_user.id).all()

    # Create a structured data format for orders with their items
    orders_with_items = []
    for order in orders:
        order_items = OrderItem.query.filter_by(OrderID=order.id).all()
        items_data = [{'name': item.product.name, 'quantity': item.Quantity} for item in order_items]

        orders_with_items.append({
            'id': order.id,
            'status': order.status,
            'price': order.price,
            'order_items': items_data
        })

    return render_template('my_orders.html', orders=orders_with_items)

@bp.route('/cancel_order/<int:order_id>', methods=['POST'])
@login_required
def cancel_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.customer_id != current_user.id:
        flash('You can only cancel your own orders.', 'danger')
        return redirect(url_for('views.my_orders'))

    # Update the order status to 'Cancelled'
    order.status = 'Cancelled'

    #increace the stock levels of the products
    order_items = OrderItem.query.filter_by(OrderID=order_id).all()
    for order_item in order_items:
        product = Product.query.get(order_item.ProductID)
        product.stock_quantity += order_item.Quantity

    db.session.commit()

    # flash('Order has been cancelled successfully.', 'success')
    return redirect(url_for('views.my_orders'))


@bp.route('/order/<int:order_id>')
@login_required
def view_order_items(order_id):
    order = Order.query.filter_by(id=order_id, customer_id=current_user.id).first()
    if not order:
        flash("Order not found or unauthorized access.", "danger")
        return redirect(url_for('views.my_orders'))
    
    order_items = OrderItem.query.filter_by(OrderID=order.id).all()
    return render_template('view_order_items.html', order=order, order_items=order_items)

@bp.route('/order/<int:order_id>/remove_item/<int:item_id>', methods=['POST'])
@login_required
def remove_order_item(order_id, item_id):
    order = Order.query.filter_by(id=order_id, customer_id=current_user.id).first()
    if not order:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('views.view_order_items', order_id=order_id))
    
    order_item = OrderItem.query.filter_by(OrderItemID=item_id, OrderID=order.id).first()
    if not order_item:
        flash("Item not found.", "danger")
        return redirect(url_for('views.view_order_items', order_id=order_id))
    
    # Increase stock quantity of the product
    product = Product.query.get(order_item.ProductID)
    if product:
        product.stock_quantity += order_item.Quantity
    
    db.session.delete(order_item)
    db.session.commit()

    #deleting the order if no items left
    if not OrderItem.query.filter_by(OrderID=order.id).all():
        db.session.delete(order)
        db.session.commit()
        return redirect(url_for('views.my_orders'))
    
    return redirect(url_for('views.view_order_items', order_id=order_id))
