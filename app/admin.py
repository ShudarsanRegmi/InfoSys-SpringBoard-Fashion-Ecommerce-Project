from flask import Blueprint, request, jsonify, get_flashed_messages, redirect, url_for
from datetime import datetime
from flask_login import login_required, current_user
from .models import db, User, Product
from .decorators import is_admin
from .forms import AddItemForm


# Define the admin blueprint
admin = Blueprint('admin', __name__)

# Define the route to add shop items
@admin.route('/add-shop-items', methods=['POST'])
def add_shop_items():
    form = AddItemForm(meta={'csrf': False})  # Disable CSRF for API requests

    if not form.validate_on_submit():
        return jsonify({'message': 'Validation failed', 'errors': form.errors}), 400

    try:
        # Create a new product from form data
        new_product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            stock_quantity=form.stock_quantity.data,
            brand=form.brand.data,
            category=form.category.data,
            updated_at=form.updated_at.data if form.updated_at.data else datetime.utcnow(),
            rating=form.rating.data,
            ratting=form.ratting.data
        )

        # Add the product to the database
        db.session.add(new_product)
        db.session.commit()

        return jsonify({'message': 'Product added successfully'}), 201
    except Exception as e:
        db.session.rollback()  # Rollback transaction in case of error
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500
    finally:
        db.session.close()  # Ensure the session is closed


# Define the route to remove shop items
@admin.route('/remove-shop-items/<int:product_id>', methods=['DELETE'])
@login_required
def remove_shop_items(product_id):
    try:
        # Query the product by ID
        product = Product.query.get(product_id)

        # Check if the product exists
        if not product:
            return jsonify({'message': 'Product not found'}), 404

        # Remove the product from the database
        db.session.delete(product)
        db.session.commit()

        return jsonify({'message': 'Product removed successfully'}), 200
    except Exception as e:
        db.session.rollback()  # Rollback transaction in case of error
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500
    finally:
        db.session.close()  # Ensure the session is closed

@admin.route('/approveDelivery')
@login_required
@is_admin
def approve_delivery():

    delivery_user_request = User.query.filter_by(role='delivery', approved = False).all()

    get_flashed_messages()
    

    return redirect(url_for('views.home'))


@admin.route('/make_me_admin')
@login_required
def make_me_admin():
    if not current_user.isAdmin():
        current_user.role = 'admin'
        db.session.commit()
    return redirect(url_for('views.home'))
