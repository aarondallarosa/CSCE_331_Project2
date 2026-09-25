DROP TABLE IF EXISTS order_toppings;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS menu_inventory;
DROP TABLE IF EXISTS menu_items;
DROP TABLE IF EXISTS toppings;
DROP TABLE IF EXISTS ingredients;
DROP TABLE IF EXISTS supplies;
DROP TABLE IF EXISTS employees;

-- EMPLOYEES TABLE
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    position VARCHAR(50) NOT NULL,
    hourly_rate DECIMAL(6,2) NOT NULL,
    hire_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- MENU ITEMS TABLE
CREATE TABLE menu_items (
    menu_item_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    base_price DECIMAL(6,2) NOT NULL,
    description VARCHAR(255),
    category VARCHAR(50),
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- TOPPINGS TABLE
CREATE TABLE toppings (
    topping_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    cost DECIMAL(6,2) NOT NULL
);

-- INGREDIENTS TABLE
CREATE TABLE ingredients (
    ingredient_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    cost DECIMAL(6,2) NOT NULL,
    unit_of_measure VARCHAR(20) DEFAULT 'oz'
);

-- SUPPLIES TABLE
CREATE TABLE supplies (
    supply_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    cost DECIMAL(6,2) NOT NULL,
    category VARCHAR(50) NOT NULL
);


-- MENU INVENTORY TABLE
CREATE TABLE menu_inventory (
    inventory_id INT PRIMARY KEY,
    menu_item_id INT NOT NULL,
    ingredient_id INT NOT NULL,
    quantity_per_serving DECIMAL(8,2) NOT NULL,
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(menu_item_id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id),
    UNIQUE KEY unique_menu_ingredient (menu_item_id, ingredient_id)
);


-- ORDERS TABLE
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    order_date DATETIME NOT NULL,
    menu_item_id INT NOT NULL,
    order_total DECIMAL(8,2) NOT NULL,
    employee_id INT NOT NULL,
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(menu_item_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    INDEX idx_order_date (order_date),
    INDEX idx_menu_item (menu_item_id),
    INDEX idx_employee (employee_id)
);


-- ORDER TOPPINGS TABLE
CREATE TABLE order_toppings (
    order_topping_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    topping_id INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (topping_id) REFERENCES toppings(topping_id),
    UNIQUE KEY unique_order_topping (order_id, topping_id)
);
