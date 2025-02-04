
STATES_CITY = {
    "":["select a state first"],
    "Andhra Pradesh": ["Amaravati", "Visakhapatnam", "Vijayawada", "Guntur", "Tirupati"],
    "Arunachal Pradesh": ["Itanagar", "Pasighat", "Tawang", "Ziro", "Bomdila"],
    "Assam": ["Guwahati", "Silchar", "Dibrugarh", "Jorhat", "Tezpur"],
    "Bihar": ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Darbhanga"],
    "Chhattisgarh": ["Raipur", "Bilaspur", "Durg", "Raigarh", "Korba"],
    "Goa": ["Panaji", "Vasco da Gama", "Mapusa", "Margao", "Ponda"],
    "Gujarat": ["Gandhinagar", "Ahmedabad", "Surat", "Vadodara", "Rajkot"],
    "Haryana": ["Chandigarh", "Faridabad", "Gurgaon", "Panipat", "Rohtak"],
    "Himachal Pradesh": ["Shimla", "Manali", "Dharamshala", "Solan", "Kullu"],
    "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Bokaro", "Hazaribag"],
    "Karnataka": ["Bengaluru", "Mysuru", "Mangalore", "Hubli-Dharwad", "Belgaum"],
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Trivandrum", "Kollam"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Jabalpur", "Gwalior", "Ujjain"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad"],
    "Manipur": ["Imphal", "Churachandpur", "Ukhrul", "Thoubal", "Jiribam"],
    "Meghalaya": ["Shillong", "Tura", "Jowai", "Nongstoin", "Williamnagar"],
    "Mizoram": ["Aizawl", "Lunglei", "Silchar", "Champhai", "Saiha"],
    "Nagaland": ["Kohima", "Dimapur", "Mokokchung", "Wokha", "Zunheboto"],
    "Odisha": ["Bhubaneswar", "Cuttack", "Puri", "Rourkela", "Sambalpur"],
    "Punjab": ["Chandigarh", "Ludhiana", "Amritsar", "Jalandhar", "Patiala"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Jaisalmer", "Ajmer"],
    "Sikkim": ["Gangtok", "Pelling", "Lachung", "Yuksom", "Mangan"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem"],
    "Telangana": ["Hyderabad", "Warangal", "Karimnagar", "Nizamabad", "Khammam"],
    "Tripura": ["Agartala", "Durgapur", "Udaipur", "Kailashahar", "Belonia"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Varanasi", "Agra", "Ghaziabad"],
    "Uttarakhand": ["Dehradun", "Haridwar", "Rishikesh", "Nainital", "Mussoorie"],
    "West Bengal": ["Kolkata", "Durgapur", "Asansol", "Siliguri", "Haldia"],
    "Andaman and Nicobar Islands": ["Port Blair", "Havelock Island", "Neil Island", "Diglipur", "Mayabunder"],
    "Chandigarh": ["Chandigarh"],
    "Delhi": ["Delhi"],
    "Puducherry": ["Puducherry", "Karaikal", "Mahe", "Yanam"],
    "Ladakh": ["Leh", "Kargil", "Zanskar", "Nubra Valley", "Pangong Tso"],
    "Jammu and Kashmir": ["Srinagar", "Jammu", "Leh", "Kargil", "Anantnag"]
}

# Dummy Product Data (for rendering)
PRODUCTS = [
    {
        'name': 'Classic White Shirt',
        'price': 1999,
        'stock_quantity': 412,
        'brand': 'Wrogn',
        'size': 'M',
        'target_user': 'Men',
        'type': 'Shirt',
        'image': 'defaults/white.jpeg',
        'description': 'A timeless classic for any wardrobe, perfect for both formal and casual occasions.',
        'details': "Made from 100% premium cotton. Breathable and comfortable for all-day wear. Available in multiple sizes for the perfect fit. Machine washable and easy to maintain. Perfect for office, events, and everyday use.",
        'colour': 'White',
        'category': 'Clothing'
    },
    {
        'name': 'Denim Jacket',
        'price': 3499,
        'stock_quantity': 721,
        'brand': 'Levis',
        'size': 'M',
        'target_user': 'Men',
        'type': 'Jacket',
        'image': 'defaults/dDenim Jacket.jpeg',
        'description': 'A stylish denim jacket that adds an edgy touch to your outfit.',
        'details': "Durable and soft denim fabric. Slim-fit design with button closure. Features side pockets and a classic collar. Perfect for layering in any season. Hand-wash recommended for extended durability.",
        'colour': 'Blue',
        'category': 'Clothing'
    },
    {
        'name': 'Summer Floral Dress',
        'price': 2799,
        'stock_quantity': 620,
        'brand': 'Zara',
        'size': 'S',
        'target_user': 'Womens',
        'type': 'Dress',
        'image': 'defaults/dSummer Floral Dress.jpeg',
        'description': 'A breezy floral dress ideal for summer outings and vacations.',
        'details': "Lightweight, flowy material for comfort. Beautiful floral prints with vibrant colors. Adjustable straps for a customized fit. Perfect for brunches, picnics, or beach outings. Machine washable and fade-resistant.",
        'colour': 'Orange',
        'category': 'Clothing'
    },
    {
        'name': 'Leather Wallet',
        'price': 1299,
        'stock_quantity': 522,
        'brand': 'Puma',
        'size': 'Regular',
        'target_user': 'Men',
        'type': 'Wallet',
        'image': 'defaults/Leather Wallet.jpeg',
        'description': 'A sleek and functional leather wallet for everyday use.',
        'details': "Crafted from genuine leather for durability. Multiple compartments for cards and cash. Compact design to fit in any pocket. Available in black and brown colors. A great gift for friends and family.",
        'colour': 'Brown',
        'category': 'Accessories'
    },
    {
        'name': 'Running Shoes',
        'price': 3999,
        'stock_quantity': 490,
        'brand': 'Campus',
        'size': '8',
        'target_user': 'Men',
        'type': 'Shoes',
        'image': 'defaults/shoes.jpeg',
        'description': 'High-performance running shoes for athletes and fitness enthusiasts.',
        'details': "Breathable mesh upper for ventilation. Cushioned sole for maximum comfort. Slip-resistant outsole for stability. Lightweight design for enhanced speed. Available in various sizes and colors.",
        'colour': 'Blue',
        'category': 'Footwear'
    },
    {
        'name': 'Smart Watch',
        'price': 4999,
        'stock_quantity': 415,
        'brand': 'Fastrack',
        'size': 'One Size',
        'target_user': 'Men',
        'type': 'Watch',
        'image': 'defaults/smart_watch.jpeg',
        'description': 'A rugged sports watch with advanced tracking features.',
        'details': "Water-resistant up to 50 meters. Digital display with multiple functions. Shock-resistant design. Ideal for fitness tracking and outdoor activities.",
        'colour': 'Black',
        'category': 'Accessories'
    },
    {
        'name': 'Casual Sneakers',
        'price': 2999,
        'stock_quantity': 524,
        'brand': 'Nike',
        'size': '9',
        'target_user': 'Men',
        'type': 'Shoes',
        'image': 'defaults/sneakers.jpeg',
        'description': 'Comfortable sneakers perfect for daily casual wear.',
        'details': "Soft cushioning for all-day comfort. Stylish and lightweight design. Available in multiple colors. Durable rubber sole for extra grip.",
        'colour': 'White',
        'category': 'Footwear'
    },
    {
        'name': 'Formal Black Trousers',
        'price': 2199,
        'stock_quantity': 613,
        'brand': 'Raymond',
        'size': 'L',
        'target_user': 'Men',
        'type': 'Trousers',
        'image': 'defaults/formal_trousers.jpeg',
        'description': 'Perfectly tailored black trousers for formal occasions.',
        'details': "Premium fabric with a smooth finish. Classic straight fit for professional attire. Wrinkle-resistant and machine washable.",
        'colour': 'Black',
        'category': 'Clothing'
    },
    {
        'name': 'Stylish Handbag',
        'price': 3599,
        'stock_quantity': 722,
        'brand': 'Lavie',
        'size': 'Medium',
        'target_user': 'Women',
        'type': 'Bag',
        'image': 'defaults/handbag.jpeg',
        'description': 'A trendy handbag for all your essentials.',
        'details': "Spacious compartments with secure zip closure. Made from high-quality faux leather. Elegant design suitable for both work and casual outings.",
        'colour': 'Red',
        'category': 'Accessories'
    },
    {
        'name': 'Wireless Earbuds',
        'price': 5999,
        'stock_quantity': 813,
        'brand': 'boAt',
        'size': 'One Size',
        'target_user': 'Unisex',
        'type': 'Earbuds',
        'image': 'defaults/earbuds.jpeg',
        'description': 'True wireless earbuds with superior sound quality.',
        'details': "Bluetooth 5.0 connectivity. Long battery life with quick charging. Noise-canceling feature for immersive audio experience.",
        'colour': 'Black',
        'category': 'Electronics'
    },
    {
        'name': 'Smartphone Stand',
        'price': 999,
        'stock_quantity': 948,
        'brand': 'AmazonBasics',
        'size': 'Adjustable',
        'target_user': 'Unisex',
        'type': 'Stand',
        'image': 'defaults/phone_stand.jpeg',
        'description': 'A versatile stand for smartphones and tablets.',
        'details': "Adjustable angles for a better viewing experience. Sturdy and foldable design. Compatible with all phone sizes.",
        'colour': 'Silver',
        'category': 'Accessories'
    },
    {
        'name': 'Digital Alarm Clock',
        'price': 1499,
        'stock_quantity': 726,
        'brand': 'Casio',
        'size': 'One Size',
        'target_user': 'Unisex',
        'type': 'Clock',
        'image': 'defaults/alarm_clock.jpeg',
        'description': 'A modern digital alarm clock with LED display.',
        'details': "Bright LED display with adjustable brightness. Multiple alarm settings with snooze function. USB charging port for convenience.",
        'colour': 'Black',
        'category': 'Electronics'
    }
]