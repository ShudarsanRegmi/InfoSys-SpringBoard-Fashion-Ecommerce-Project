# InfoSys-SpringBoard Interns Fashion-Ecommerce-Project

## Project Overview  
This project is a **Fashion E-Commerce Website**, designed as part of my internship project. It is a fully functional e-commerce platform with core features such as product browsing, user authentication, shopping cart management, order processing, and admin analytics. The theme of the website is centered around fashion, offering users a seamless and engaging shopping experience.


## Technologies Used

- **Python**: Backend development.
- **Flask**: Web framework to build the web application.
- **SQLAlchemy**: ORM (Object-Relational Mapping) for managing database with SQLite.
- **SQLite3**: Database for storing user information.
- **HTML/CSS**: For frontend pages.
- **JavaScript**: For dynamic page elements and client-side validation.

## Setup Instructions

1. Clone the repository:  
   ```bash  
   git clone https://github.com/ShudarsanRegmi/InfoSys-SpringBoard-Fashion-Ecommerce-Project.git
   cd InfoSys-SpringBoard-Fashion-Ecommerce-Project
   ```  
   
2. **flask db init is used to initialize the migration**:
   ```bash
      flask db migrate
   ```
   >above command is used to create the migration -m flag is used with this command to add the message for example - 
   ```bash
      flask db migrate -m "Initial migration"
   ```

3. **upgrade the database**:
   
   ```bash
      flask db upgrade
   ```
   >the above command is used to apply the migration

4. **Downgrade the DataBase** 
    
   ```bash 
   flask db downgrade
   ```
   
   > the above command is used to revert the migration

## Features  
### User Features:  
- **Home Page:** Displays featured and trending fashion items.  
- **Product Catalog:** Filter and search for products by category, size, and price.  
- **Product Details:** Detailed descriptions, multiple images, and reviews.  
- **Shopping Cart:** Add, update, and remove items before checkout.  
- **Order Processing:** Secure checkout and order confirmation.  

### Admin Features:  
- **Inventory Management:** Add, update, and delete products.  
- **Order Tracking:** View and manage user orders.  
- **Sales Analytics:** Visualizations using Matplotlib for sales trends and inventory analysis.  

---

## Tech Stack  
The project leverages the following technologies:  
- **Frontend:**  
  - HTML  
  - CSS  
  - JavaScript  

- **Backend:**  
  - Python (Flask Framework)  

- **Data Visualization:**  
  - Matplotlib (for generating sales and inventory visualizations)  

- **Database:**  
  - SQLite (or any lightweight relational database)  

---

## Installation  
### Prerequisites:  
Ensure you have Python 3.x installed along with the required libraries.  

### Steps:  
1. Clone the repository:  
   ```bash  
   git clone https://github.com/ShudarsanRegmi/InfoSys-SpringBoard-Fashion-Ecommerce-Project.git
   cd InfoSys-SpringBoard-Fashion-Ecommerce-Project
   ```  

2. Install dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ```  

3. Run the application:  
   ```bash  
   python app.py  
   ```  

4. Open your browser and navigate to:  
   ```
   http://localhost:5000  
   ```  

---

## Usage  
1. **Browse Products:** Explore the catalog and view product details.  
2. **Add to Cart:** Add desired products to the shopping cart.  
3. **Checkout:** Complete the checkout process securely.  
4. **Admin Dashboard:** Analyze sales trends and manage inventory.  

---

## Project Screenshots  
- will be added

---

## Future Enhancements  
- Implement user profiles and purchase history.  
- Add AI-based product recommendations.  
- Integrate with third-party payment gateways.  
- Support for coupons and discount codes.  

---

## License  
This project is licensed under the MIT License.  
---

## Acknowledgments  
- **Mentors:** For guiding us through the project development.  
- **Resources:** Flask Documentation, MDN Web Docs, Matplotlib Tutorials.  

