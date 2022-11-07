# Shop App

## Database Entites in Shop App
1. Product
2. Collection
3. Customer
4. Cart
5. CartItem
6. Order
7. OrderItem

### Promotion Attributes
1. description
2. discount

### Collection Attributes
1. title
2. featured_product ---> (one to many relation with product)

### Product Attributes
1. title 
2. Slug
3. description
4. price
5. inventory
6. collection --> (one to many relation ship)
7. promotion --> (many to many realtionship)
8. created_at
9. last_updated

### Customer Attributes
1. first_name
2. last_name
3. email --> (unique field)
4. phone
5. birth_date (can be null)
6. gender --> (choice field)
7. membership --> (enum choices)

### Order Attributes
1. placed_at
2. payment_status --> (enum choices)
3. customer --> (Order entity is many to one relationship with customer. i.e. customer has many orders)

### OrderItem attributes
1. order --> (many to one relation with Order)
2. product  --> (many to one relationwith product)
3. quantity 
4. unit_price

### Address Model
1. street
2. city
3. state
4. postal_code
5. customer --> (many to one with customer, i.e. a customer may have many address)

### Cart Model
1. created_at

### Cart Item Model
1. cart
2. product
3. quantity