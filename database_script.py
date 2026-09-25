import csv
import random
from datetime import datetime, timedelta
from collections import defaultdict

# ============================================================================
# HARDCODED NON-NUMERICAL DATA
# ============================================================================

MENU_ITEMS = [
    {"id": 1, "name": "Classic Milk Tea", "base_price": 4.99},
    {"id": 2, "name": "Jasmine Green Tea", "base_price": 4.49},
    {"id": 3, "name": "Oolong Tea", "base_price": 4.99},
    {"id": 4, "name": "Brown Sugar Milk Tea", "base_price": 5.49},
    {"id": 5, "name": "Taro Milk Tea", "base_price": 5.49},
    {"id": 6, "name": "Matcha Latte", "base_price": 5.99},
    {"id": 7, "name": "Strawberry Tea", "base_price": 5.49},
    {"id": 8, "name": "Mango Tea", "base_price": 5.49},
    {"id": 9, "name": "Lychee Green Tea", "base_price": 5.49},
    {"id": 10, "name": "Thai Tea", "base_price": 5.49},
    {"id": 11, "name": "Honey Lemon Tea", "base_price": 5.49},
    {"id": 12, "name": "Peach Oolong", "base_price": 5.49},
    {"id": 13, "name": "Winter Melon Tea", "base_price": 4.99},
    {"id": 14, "name": "Brown Sugar Boba Latte", "base_price": 6.49},
    {"id": 15, "name": "Toffee Almond Latte", "base_price": 6.49},
    {"id": 16, "name": "Hokkaido Milk Tea", "base_price": 6.49},
    {"id": 17, "name": "Fermented Black Tea", "base_price": 5.49},
    {"id": 18, "name": "Ginger Milk Tea", "base_price": 5.49},
    {"id": 19, "name": "Rose Milk Tea", "base_price": 5.49},
    {"id": 20, "name": "Sesame Milk Tea", "base_price": 5.49},
]

TOPPINGS = [
    {"id": 1, "name": "Boba Pearls", "cost": 0.50},
    {"id": 2, "name": "Popping Boba", "cost": 0.75},
    {"id": 3, "name": "Jelly Cubes", "cost": 0.40},
    {"id": 4, "name": "Pudding", "cost": 0.60},
    {"id": 5, "name": "Red Bean", "cost": 0.45},
    {"id": 6, "name": "Grass Jelly", "cost": 0.40},
    {"id": 7, "name": "Lychee Jelly", "cost": 0.50},
    {"id": 8, "name": "Aloe Vera", "cost": 0.45},
    {"id": 9, "name": "Whipped Cream", "cost": 0.75},
]

SUPPLIES = [
    {"id": 1, "name": "16oz Cup", "cost": 0.15, "category": "cups"},
    {"id": 2, "name": "24oz Cup", "cost": 0.20, "category": "cups"},
    {"id": 3, "name": "Plastic Straw", "cost": 0.05, "category": "straw"},
    {"id": 4, "name": "Stainless Steel Straw", "cost": 0.25, "category": "straw"},
    {"id": 5, "name": "Napkin Pack", "cost": 0.10, "category": "napkin"},
    {"id": 6, "name": "Paper Bag (Large)", "cost": 0.20, "category": "bag"},
    {"id": 7, "name": "Paper Bag (Small)", "cost": 0.10, "category": "bag"},
    {"id": 8, "name": "Cup Holder", "cost": 0.05, "category": "holder"},
]

INGREDIENTS = [
    {"id": 1, "name": "Black Tea Leaves", "cost": 0.30},
    {"id": 2, "name": "Green Tea Leaves", "cost": 0.35},
    {"id": 3, "name": "Milk", "cost": 0.50},
    {"id": 4, "name": "Brown Sugar Syrup", "cost": 0.40},
    {"id": 5, "name": "Honey", "cost": 0.60},
    {"id": 6, "name": "Taro Powder", "cost": 0.80},
    {"id": 7, "name": "Matcha Powder", "cost": 1.20},
    {"id": 8, "name": "Strawberry Syrup", "cost": 0.50},
    {"id": 9, "name": "Mango Puree", "cost": 0.70},
    {"id": 10, "name": "Lychee Syrup", "cost": 0.50},
    {"id": 11, "name": "Oolong Tea Leaves", "cost": 0.40},
    {"id": 12, "name": "Jasmine Tea Leaves", "cost": 0.45},
]

EMPLOYEES = [
    {"id": 1, "name": "Alice Chen", "position": "Manager", "hourly_rate": 18.50},
    {"id": 2, "name": "Bob Johnson", "position": "Barista", "hourly_rate": 15.00},
    {"id": 3, "name": "Carol Martinez", "position": "Barista", "hourly_rate": 15.00},
    {"id": 4, "name": "Diana Patel", "position": "Barista", "hourly_rate": 15.00},
    {"id": 5, "name": "Evan Smith", "position": "Cashier", "hourly_rate": 14.50},
]

# ============================================================================
# DATA GENERATION CONFIGURATION
# ============================================================================

WEEKS = 52
TOTAL_SALES_TARGET = 1_000_000  # $1M
PEAK_DAYS = 3  # Number of peak sales days
PEAK_MULTIPLIER = 3.5  # Peak days have 3.5x normal sales

# Peak day dates (e.g., start of semesters, holidays)
PEAK_DAY_OFFSETS = [
    (7, "Fall Semester Start"),      # Week 7
    (27, "Spring Semester Start"),   # Week 27
    (50, "Final Exams Period"),      # Week 50
]

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def generate_date_range(weeks=52):
    """Generate date range for 52 weeks starting ~1 year ago"""
    end_date = datetime.now()
    start_date = end_date - timedelta(weeks=weeks)
    return start_date, end_date

def is_peak_day(date, start_date, peak_weeks):
    """Check if date is a peak sales day"""
    for week_num, _ in peak_weeks:
        # Peak days are on specific weeks (Mondays)
        peak_date = start_date + timedelta(weeks=week_num - 1)
        # Make it a Monday
        peak_date = peak_date - timedelta(days=peak_date.weekday())
        
        if date.date() == peak_date.date():
            return True
    return False

def get_hourly_pattern():
    """Return hourly sales multiplier (simulates realistic sales patterns)"""
    # Higher sales during morning/afternoon, lower at night
    patterns = {
        8: 0.5,   # Early morning
        9: 0.8,   # Morning rush start
        10: 1.2,  # Morning peak
        11: 1.5,  # Late morning
        12: 1.8,  # Lunch rush
        13: 1.6,  # Post-lunch
        14: 1.3,  # Afternoon
        15: 1.4,  # Afternoon peak
        16: 1.5,  # Late afternoon
        17: 1.3,  # Evening start
        18: 1.0,  # Evening
        19: 0.7,  # Late evening
        20: 0.4,  # Night
    }
    return patterns

def get_day_multiplier(day_of_week):
    """Return day-of-week sales multiplier"""
    # Higher sales on weekdays, lower on weekends
    patterns = {
        0: 1.2,  # Monday
        1: 1.3,  # Tuesday
        2: 1.3,  # Wednesday
        3: 1.2,  # Thursday
        4: 1.1,  # Friday
        5: 0.9,  # Saturday
        6: 0.8,  # Sunday
    }
    return patterns.get(day_of_week, 1.0)

def generate_orders(start_date, end_date, total_sales_target, peak_weeks):
    """Generate realistic sales orders"""
    orders = []
    order_id = 1
    current_sales = 0
    hourly_pattern = get_hourly_pattern()
    
    current_date = start_date
    
    while current_date <= end_date:
        day_of_week = current_date.weekday()
        day_mult = get_day_multiplier(day_of_week)
        
        # Check if peak day
        is_peak = is_peak_day(current_date, start_date, peak_weeks)
        peak_mult = PEAK_MULTIPLIER if is_peak else 1.0
        
        # Generate orders for each hour
        for hour in range(8, 21):  # 8 AM to 8 PM
            hour_mult = hourly_pattern.get(hour, 0.5)
            
            # Baseline orders per hour: ~30-50 orders
            base_orders = random.randint(30, 50)
            num_orders = int(base_orders * day_mult * peak_mult * hour_mult)
            
            for _ in range(num_orders):
                # Randomly select menu items and toppings
                menu_item = random.choice(MENU_ITEMS)
                toppings = random.choices(TOPPINGS, k=random.randint(0, 3))
                
                # Calculate price
                order_total = menu_item["base_price"]
                for topping in toppings:
                    order_total += topping["cost"]
                
                # Add small random variation
                order_total *= random.uniform(0.95, 1.05)
                order_total = round(order_total, 2)
                
                # Create order
                order = {
                    "order_id": order_id,
                    "order_date": current_date.replace(hour=hour, minute=random.randint(0, 59)),
                    "menu_item_id": menu_item["id"],
                    "menu_item_name": menu_item["name"],
                    "toppings": [t["name"] for t in toppings],
                    "order_total": order_total,
                    "employee_id": random.choice(EMPLOYEES)["id"],
                }
                
                orders.append(order)
                current_sales += order_total
                order_id += 1
                
                # Check if we've reached our sales target
                if current_sales >= total_sales_target:
                    return orders
        
        current_date += timedelta(days=1)
    
    return orders

def generate_menu_inventory():
    """Generate inventory assignments for menu items"""
    menu_inventory = []
    inventory_id = 1
    
    # Base ingredients that go in most drinks
    base_ingredients = [1, 2, 3]  # Tea, Milk, Sweetener
    
    for menu_item in MENU_ITEMS:
        # Every menu uses a base
        for ingredient_id in base_ingredients:
            menu_inventory.append({
                "inventory_id": inventory_id,
                "menu_item_id": menu_item["id"],
                "ingredient_id": ingredient_id,
                "quantity_per_serving": round(random.uniform(1, 3), 2),
            })
            inventory_id += 1
        
        # Add 2-4 specialty ingredients based on menu name
        name_lower = menu_item["name"].lower()
        special_ingredients = []
        
        if "brown sugar" in name_lower:
            special_ingredients.append(4)
        if "matcha" in name_lower:
            special_ingredients.append(7)
        if "taro" in name_lower:
            special_ingredients.append(6)
        if "strawberry" in name_lower:
            special_ingredients.append(8)
        if "mango" in name_lower:
            special_ingredients.append(9)
        if "lychee" in name_lower:
            special_ingredients.append(10)
        if "oolong" in name_lower:
            special_ingredients.append(11)
        if "jasmine" in name_lower:
            special_ingredients.append(12)
        if "honey" in name_lower:
            special_ingredients.append(5)
        
        # If no special ingredients, add random ones
        if not special_ingredients:
            special_ingredients = random.sample(range(4, 13), k=random.randint(1, 3))
        
        for ingredient_id in special_ingredients:
            menu_inventory.append({
                "inventory_id": inventory_id,
                "menu_item_id": menu_item["id"],
                "ingredient_id": ingredient_id,
                "quantity_per_serving": round(random.uniform(0.5, 2), 2),
            })
            inventory_id += 1
    
    return menu_inventory

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("🧋 Generating Bubble Tea Sales Data for CSCE 331 Project 2...")
    print(f"   Team Size: 5 members")
    print(f"   Weeks: {WEEKS}")
    print(f"   Target Sales: ${TOTAL_SALES_TARGET:,}")
    print(f"   Peak Days: {PEAK_DAYS}")
    print()
    
    # Generate date range
    start_date, end_date = generate_date_range(WEEKS)
    print(f"📅 Date Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    # Generate orders
    print(f"📊 Generating orders...")
    orders = generate_orders(start_date, end_date, TOTAL_SALES_TARGET, PEAK_DAY_OFFSETS)
    total_revenue = sum(o["order_total"] for o in orders)
    print(f"   ✓ Generated {len(orders):,} orders")
    print(f"   ✓ Total Revenue: ${total_revenue:,.2f}")
    print(f"   ✓ Average Order: ${total_revenue / len(orders):.2f}")
    
    # Generate menu inventory
    print(f"📋 Generating menu inventory...")
    menu_inventory = generate_menu_inventory()
    print(f"   ✓ Generated {len(menu_inventory)} menu-ingredient mappings")
    
    # Write CSV files
    print(f"\n💾 Writing CSV files...")
    
    # Orders
    with open("orders.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["order_id", "order_date", "menu_item_id", "menu_item_name", "toppings", "order_total", "employee_id"])
        writer.writeheader()
        for order in orders:
            row = order.copy()
            row["toppings"] = ";".join(row["toppings"]) if row["toppings"] else ""
            writer.writerow(row)
    print(f"   ✓ orders.csv ({len(orders)} rows)")
    
    # Menu Items
    with open("menu_items.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "base_price"])
        writer.writeheader()
        writer.writerows(MENU_ITEMS)
    print(f"   ✓ menu_items.csv ({len(MENU_ITEMS)} rows)")
    
    # Toppings
    with open("toppings.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "cost"])
        writer.writeheader()
        writer.writerows(TOPPINGS)
    print(f"   ✓ toppings.csv ({len(TOPPINGS)} rows)")
    
    # Supplies
    with open("supplies.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "cost", "category"])
        writer.writeheader()
        writer.writerows(SUPPLIES)
    print(f"   ✓ supplies.csv ({len(SUPPLIES)} rows)")
    
    # Ingredients
    with open("ingredients.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "cost"])
        writer.writeheader()
        writer.writerows(INGREDIENTS)
    print(f"   ✓ ingredients.csv ({len(INGREDIENTS)} rows)")
    
    # Menu Inventory
    with open("menu_inventory.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["inventory_id", "menu_item_id", "ingredient_id", "quantity_per_serving"])
        writer.writeheader()
        writer.writerows(menu_inventory)
    print(f"   ✓ menu_inventory.csv ({len(menu_inventory)} rows)")
    
    # Employees
    with open("employees.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "position", "hourly_rate"])
        writer.writeheader()
        writer.writerows(EMPLOYEES)
    print(f"   ✓ employees.csv ({len(EMPLOYEES)} rows)")
    
    print(f"\n✨ Data generation complete!")
    print(f"\nFiles created:")
    print(f"  • orders.csv")
    print(f"  • menu_items.csv")
    print(f"  • toppings.csv")
    print(f"  • supplies.csv")
    print(f"  • ingredients.csv")
    print(f"  • menu_inventory.csv")
    print(f"  • employees.csv")