from faker import Faker

fake = Faker()

def generate_shipment_data():

    origin_country = fake.country()
    destination_country = fake.country()
    
    customer_first_name = fake.first_name()
    customer_last_name = fake.last_name()
    
    shipment_id = f"SHIP{fake.random_number(digits=14)}"
    order_id = f"ORD{fake.random_number(digits=14)}"
    data = {
        "shipment_id": shipment_id,
        "order_id": order_id,
        "shipment_type": fake.random_element(elements=("Standard", "Express", "Overnight")),
        "shipment_weight": round(fake.pyfloat(min_value=0.5, max_value=50.0), 2),
        "shipment_dimensions": {
            "length": round(fake.pyfloat(min_value=10.0, max_value=100.0), 2),
            "width": round(fake.pyfloat(min_value=10.0, max_value=100.0), 2),
            "height": round(fake.pyfloat(min_value=10.0, max_value=100.0), 2)
        },
        "priority_level": fake.random_element(elements=("Low", "Medium", "High")),
        "insurance_coverage": round(fake.pyfloat(min_value=0.0, max_value=10000.0), 2),
        "customer_id": f"CUST{fake.random_number(digits=6)}",
        "customer_first_name": customer_first_name,
        "customer_last_name": customer_last_name,
        "customer_type": fake.random_element(elements=("Business", "Individual")),
        "customer_region": origin_country,
        "current_status": fake.random_element(elements=("Pending", "In Transit", "Delivered", "Delayed")),
        "last_updated": fake.iso8601(),
        "estimated_delivery_date": fake.date_between(start_date="today", end_date="+7d"),
        "actual_delivery_date": None if fake.boolean(chance_of_getting_true=20) else fake.date_between(start_date="today", end_date="+7d"),
        "current_location": {
            "address": fake.street_address(),
            "postal_code": fake.postcode(),
            "country": fake.country()
        },
        "delivery_attempts": fake.random_int(min=0, max=3),
        "origin_address": {
            "address": fake.street_address(),
            "postal_code": fake.postcode(),
            "country": origin_country
        },
        "destination_address": {
            "address": fake.street_address(),
            "postal_code": fake.postcode(),
            "country": destination_country
        },
        "distance_traveled": round(fake.pyfloat(min_value=0.0, max_value=5000.0), 2),
        "transport_mode": fake.random_element(elements=("Truck", "Air", "Ship")),
        "shipment_cost": round(fake.pyfloat(min_value=10.0, max_value=500.0), 2),
        "revenue_generated": round(fake.pyfloat(min_value=50.0, max_value=1000.0), 2),
        "delivery_penalty": round(fake.pyfloat(min_value=0.0, max_value=100.0), 2) if fake.boolean(chance_of_getting_true=10) else 0.0,
        "order_date": fake.date_between(start_date="-30d", end_date="today"),
        "shipment_created_date": fake.date_between(start_date="-30d", end_date="today"),
        "transit_time": round(fake.pyfloat(min_value=1.0, max_value=10.0), 1),
        "delay_reason": None if fake.boolean(chance_of_getting_true=90) else fake.random_element(elements=("Weather", "Customs", "Traffic")),
        "warehouse_id": f"WH{fake.random_number(digits=3)}",
        "delivery_agent_id": f"AGENT{fake.random_number(digits=4)}",
        "vehicle_id": f"VEH{fake.random_number(digits=4)}",
        "temperature_sensitivity": fake.boolean()
    }
    return data
    
    
