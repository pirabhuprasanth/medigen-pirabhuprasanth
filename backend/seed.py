# backend/seed.py
from app import create_app
from app.models import (
    db, User, Product, Salt, FAQ, Review, Manufacturer, 
    Category, ProductSalt, Substitute
)
from datetime import datetime, date
import random

app = create_app()

with app.app_context():
    print("Dropping all tables...")
    db.drop_all()
    print("Creating all tables...")
    db.create_all()

    # --- Create Dummy Users ---
    print("Creating dummy users...")
    users = [
        User(
            username='admin',
            email='admin@medigen.com',
            first_name='Admin',
            last_name='User'
        ),
        User(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        ),
        User(
            username='john_doe',
            email='john@example.com',
            first_name='John',
            last_name='Doe'
        )
    ]
    
    for user in users:
        user.set_password('password123')
        db.session.add(user)
    
    db.session.commit()

    # --- Create Manufacturers ---
    print("Creating manufacturers...")
    manufacturers = [
        Manufacturer(
            name='Abbott Healthcare',
            country='India',
            established_year=1944,
            website='https://www.abbott.co.in',
            description='Leading healthcare company specializing in pharmaceuticals'
        ),
        Manufacturer(
            name='Sun Pharmaceutical',
            country='India',
            established_year=1983,
            website='https://www.sunpharma.com',
            description='Largest pharmaceutical company in India'
        ),
        Manufacturer(
            name='Dr. Reddy\'s Laboratories',
            country='India',
            established_year=1984,
            website='https://www.drreddys.com',
            description='Global pharmaceutical company'
        ),
        Manufacturer(
            name='Cipla Limited',
            country='India',
            established_year=1935,
            website='https://www.cipla.com',
            description='Global pharmaceutical and biotechnology company'
        ),
        Manufacturer(
            name='Lupin Limited',
            country='India',
            established_year=1968,
            website='https://www.lupin.com',
            description='Innovation led transnational pharmaceutical company'
        )
    ]
    
    for manufacturer in manufacturers:
        db.session.add(manufacturer)
    
    db.session.commit()

    # --- Create Categories ---
    print("Creating categories...")
    categories = [
        Category(name='Pain Relief', description='Medicines for pain management'),
        Category(name='Digestive Health', description='Medicines for digestive disorders'),
        Category(name='Cardiovascular', description='Heart and blood vessel medications'),
        Category(name='Respiratory', description='Lung and breathing medications'),
        Category(name='Antibiotics', description='Anti-bacterial medications'),
        Category(name='Vitamins & Supplements', description='Nutritional supplements')
    ]
    
    for category in categories:
        db.session.add(category)
    
    db.session.commit()

    # --- Create Salts ---
    print("Creating salts...")
    salts = [
        Salt(
            name='Paracetamol',
            chemical_formula='C8H9NO2',
            molecular_weight=151.163,
            description='Analgesic and antipyretic drug',
            therapeutic_class='Non-narcotic analgesic'
        ),
        Salt(
            name='Ursodeoxycholic Acid',
            chemical_formula='C24H40O4',
            molecular_weight=392.57,
            description='Naturally occurring bile acid used to dissolve gallstones',
            therapeutic_class='Choleretic agent'
        ),
        Salt(
            name='Ibuprofen',
            chemical_formula='C13H18O2',
            molecular_weight=206.29,
            description='Non-steroidal anti-inflammatory drug',
            therapeutic_class='NSAID'
        ),
        Salt(
            name='Aspirin',
            chemical_formula='C9H8O4',
            molecular_weight=180.16,
            description='Salicylate drug used for pain relief',
            therapeutic_class='NSAID'
        ),
        Salt(
            name='Omeprazole',
            chemical_formula='C17H19N3O3S',
            molecular_weight=345.42,
            description='Proton pump inhibitor',
            therapeutic_class='Antacid'
        )
    ]
    
    for salt in salts:
        db.session.add(salt)
    
    db.session.commit()

    # --- Create Products ---
    print("Creating products...")
    products = [
        Product(
            name='UDILIV 300MG TABLET 15\'S',
            sku='UDLV300T15',
            manufacturer_id=manufacturers[0].id,  # Abbott Healthcare
            category_id=categories[1].id,  # Digestive Health
            price=34.00,
            mrp=40.00,
            discount_percentage=15.0,
            description_general='UDILIV 300MG TABLET is a medicine that is used to dissolve gallstones and prevent them from forming.',
            uses='Gallstones;Primary Biliary Cirrhosis;Cystic fibrosis-related liver disease',
            how_it_works='UDILIV 300MG TABLET works by reducing the amount of cholesterol produced by the liver and dissolving the cholesterol that has formed into gallstones.',
            how_to_use='Take this medicine in the dose and duration as advised by your doctor. Swallow it as a whole. Do not chew, crush or break it.',
            side_effects='Diarrhea;Nausea;Stomach pain;Rash',
            precautions='Inform your doctor if you have liver disease;Avoid alcohol consumption',
            interactions='May interact with antacids;Consult doctor before taking with other medications',
            dosage_form='Tablet',
            strength='300mg',
            pack_size='15 tablets',
            prescription_required=True,
            stock_quantity=100,
            expiry_date=date(2026, 12, 31),
            manufacturing_date=date(2024, 6, 15),
            batch_number='UDLV2024-06',
            storage_conditions='Store in a cool, dry place away from light'
        ),
        Product(
            name='Dolo 650mg Tablet',
            sku='DLO650T10',
            manufacturer_id=manufacturers[1].id,  # Sun Pharmaceutical
            category_id=categories[0].id,  # Pain Relief
            price=34.00,
            mrp=40.00,
            discount_percentage=15.0,
            description_general='Dolo 650 Tablet is a medicine used to relieve pain and reduce fever.',
            uses='Fever;Headache;Toothache;Body ache;Common cold symptoms',
            how_it_works='It blocks the production of certain chemical messengers in the brain that cause pain and fever.',
            how_to_use='Take this medicine as per the dose and duration prescribed by your doctor.',
            side_effects='Nausea;Vomiting;Stomach pain;Loss of appetite',
            precautions='Do not exceed recommended dose;Avoid alcohol consumption',
            interactions='May interact with blood thinners;Inform doctor about all medications',
            dosage_form='Tablet',
            strength='650mg',
            pack_size='10 tablets',
            prescription_required=False,
            stock_quantity=150,
            expiry_date=date(2026, 8, 20),
            manufacturing_date=date(2024, 2, 10),
            batch_number='DLO2024-02',
            storage_conditions='Store below 30°C in a dry place'
        ),
        Product(
            name='Crocin Advance 500mg',
            sku='CRC500T20',
            manufacturer_id=manufacturers[2].id,  # Dr. Reddy's
            category_id=categories[0].id,  # Pain Relief
            price=28.00,
            mrp=32.00,
            discount_percentage=12.5,
            description_general='Crocin Advance provides fast and effective relief from pain and fever.',
            uses='Fever;Headache;Body pain;Dental pain;Cold and flu symptoms',
            how_it_works='Contains paracetamol which reduces pain and fever by blocking pain signals to the brain.',
            how_to_use='Take 1-2 tablets every 4-6 hours as needed. Do not exceed 8 tablets in 24 hours.',
            side_effects='Rare allergic reactions;Skin rash;Liver problems with overdose',
            precautions='Not recommended for children under 12;Avoid with liver disease',
            interactions='May enhance effect of blood thinners;Avoid with other paracetamol containing medicines',
            dosage_form='Tablet',
            strength='500mg',
            pack_size='20 tablets',
            prescription_required=False,
            stock_quantity=200,
            expiry_date=date(2026, 10, 15),
            manufacturing_date=date(2024, 4, 20),
            batch_number='CRC2024-04',
            storage_conditions='Store in a cool, dry place'
        ),
        Product(
            name='Brufen 400mg Tablet',
            sku='BRF400T15',
            manufacturer_id=manufacturers[3].id,  # Cipla
            category_id=categories[0].id,  # Pain Relief
            price=42.00,
            mrp=50.00,
            discount_percentage=16.0,
            description_general='Brufen 400mg Tablet is a pain-relieving medicine used to treat pain and inflammation.',
            uses='Pain relief;Inflammation;Fever;Arthritis;Muscle pain',
            how_it_works='It works by blocking certain chemical messengers that cause pain and inflammation.',
            how_to_use='Take with food to avoid stomach upset. Follow prescribed dosage.',
            side_effects='Stomach pain;Nausea;Indigestion;Dizziness;Drowsiness',
            precautions='Take with food;Avoid in stomach ulcers;Monitor blood pressure',
            interactions='May interact with blood thinners;Avoid with ACE inhibitors',
            dosage_form='Tablet',
            strength='400mg',
            pack_size='15 tablets',
            prescription_required=True,
            stock_quantity=80,
            expiry_date=date(2025, 12, 30),
            manufacturing_date=date(2024, 1, 15),
            batch_number='BRF2024-01',
            storage_conditions='Store below 25°C'
        ),
        Product(
            name='Omez 20mg Capsule',
            sku='OMZ20C10',
            manufacturer_id=manufacturers[4].id,  # Lupin
            category_id=categories[1].id,  # Digestive Health
            price=56.00,
            mrp=65.00,
            discount_percentage=13.8,
            description_general='Omez 20mg Capsule is used to treat stomach acid-related conditions.',
            uses='Acidity;Heartburn;Stomach ulcers;GERD;Acid reflux',
            how_it_works='It reduces the amount of acid produced in the stomach.',
            how_to_use='Take on empty stomach, preferably in the morning. Swallow whole.',
            side_effects='Headache;Nausea;Stomach pain;Constipation;Flatulence',
            precautions='Complete full course even if symptoms improve;Inform doctor about bone problems',
            interactions='May affect absorption of some medicines;Take iron supplements separately',
            dosage_form='Capsule',
            strength='20mg',
            pack_size='10 capsules',
            prescription_required=True,
            stock_quantity=120,
            expiry_date=date(2026, 6, 25),
            manufacturing_date=date(2024, 3, 10),
            batch_number='OMZ2024-03',
            storage_conditions='Store in a cool, dry place'
        )
    ]
    
    for product in products:
        db.session.add(product)
    
    db.session.commit()

    # --- Create Product-Salt Associations ---
    print("Creating product-salt associations...")
    product_salt_associations = [
        ProductSalt(product_id=products[0].id, salt_id=salts[1].id, strength='300mg', percentage=100.0),  # UDILIV - Ursodeoxycholic Acid
        ProductSalt(product_id=products[1].id, salt_id=salts[0].id, strength='650mg', percentage=100.0),  # Dolo - Paracetamol
        ProductSalt(product_id=products[2].id, salt_id=salts[0].id, strength='500mg', percentage=100.0),  # Crocin - Paracetamol
        ProductSalt(product_id=products[3].id, salt_id=salts[2].id, strength='400mg', percentage=100.0),  # Brufen - Ibuprofen
        ProductSalt(product_id=products[4].id, salt_id=salts[4].id, strength='20mg', percentage=100.0),   # Omez - Omeprazole
    ]
    
    for assoc in product_salt_associations:
        db.session.add(assoc)
    
    db.session.commit()

    # --- Create Substitutes ---
    print("Creating substitute relationships...")
    substitutes = [
        Substitute(product_id=products[1].id, substitute_product_id=products[2].id, similarity_score=0.95),  # Dolo -> Crocin
        Substitute(product_id=products[2].id, substitute_product_id=products[1].id, similarity_score=0.95),  # Crocin -> Dolo
    ]
    
    for substitute in substitutes:
        db.session.add(substitute)
    
    db.session.commit()

    # --- Create FAQs ---
    print("Creating FAQs...")
    faqs = [
        FAQ(
            salt_id=salts[0].id,  # Paracetamol
            question='What should I do if I miss a dose of Paracetamol?',
            answer='Take the missed dose as soon as you remember. If it is almost time for your next dose, skip the missed dose. Do not take a double dose.',
            category='Usage'
        ),
        FAQ(
            salt_id=salts[0].id,  # Paracetamol
            question='Can I take Paracetamol with alcohol?',
            answer='It is not recommended to consume alcohol while taking paracetamol as it may increase the risk of liver damage.',
            category='Interactions'
        ),
        FAQ(
            salt_id=salts[1].id,  # Ursodeoxycholic Acid
            question='How long does it take for Ursodeoxycholic Acid to work?',
            answer='It may take several months to dissolve gallstones completely. Continue taking as prescribed by your doctor.',
            category='Usage'
        ),
        FAQ(
            product_id=products[0].id,  # UDILIV
            question='Should UDILIV be taken with food?',
            answer='UDILIV can be taken with or without food. However, taking it with food may help reduce stomach upset.',
            category='Usage'
        ),
        FAQ(
            product_id=products[1].id,  # Dolo
            question='Is Dolo 650 safe for children?',
            answer='Dolo 650 should only be given to children under medical supervision. The dosage depends on the child\'s weight and age.',
            category='Safety'
        )
    ]
    
    for faq in faqs:
        db.session.add(faq)
    
    db.session.commit()

    # --- Create Reviews ---
    print("Creating reviews...")
    reviews = [
        Review(
            product_id=products[0].id,  # UDILIV
            user_id=users[1].id,
            rating=5,
            title='Effective for gallstones',
            comment='The medicine is good but it is costly when compared with the exact generic medicine. However, it works well.',
            reviewer_name='Test User',
            verified_purchase=True,
            helpful_count=5
        ),
        Review(
            product_id=products[0].id,  # UDILIV
            user_id=users[2].id,
            rating=4,
            title='Good results',
            comment='Very effective and worked as expected. Highly recommend for gallstone problems.',
            reviewer_name='John Doe',
            verified_purchase=True,
            helpful_count=3
        ),
        Review(
            product_id=products[1].id,  # Dolo
            user_id=users[1].id,
            rating=5,
            title='Quick relief',
            comment='Fast acting and effective for fever and pain relief. Good value for money.',
            reviewer_name='Test User',
            verified_purchase=True,
            helpful_count=8
        ),
        Review(
            product_id=products[2].id,  # Crocin
            user_id=users[2].id,
            rating=4,
            title='Reliable medicine',
            comment='Trusted brand for headaches and fever. Works quickly and is gentle on stomach.',
            reviewer_name='John Doe',
            verified_purchase=False,
            helpful_count=2
        ),
        Review(
            product_id=products[3].id,  # Brufen
            user_id=users[1].id,
            rating=3,
            title='Good for inflammation',
            comment='Effective for joint pain but can cause stomach irritation. Take with food.',
            reviewer_name='Test User',
            verified_purchase=True,
            helpful_count=4
        )
    ]
    
    for review in reviews:
        db.session.add(review)

    db.session.commit()
    
    print("✅ Database has been seeded successfully!")
    print(f"✅ Created {len(users)} users")
    print(f"✅ Created {len(manufacturers)} manufacturers")
    print(f"✅ Created {len(categories)} categories")
    print(f"✅ Created {len(salts)} salts")
    print(f"✅ Created {len(products)} products")
    print(f"✅ Created {len(product_salt_associations)} product-salt associations")
    print(f"✅ Created {len(substitutes)} substitute relationships")
    print(f"✅ Created {len(faqs)} FAQs")
    print(f"✅ Created {len(reviews)} reviews")
    print("\n🔐 Test Login Credentials:")
    print("Username: admin, Password: password123")
    print("Username: testuser, Password: password123")
    print("Username: john_doe, Password: password123")