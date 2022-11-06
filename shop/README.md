# Shop App

## Database Entites in Shop App
1. Product
2. Collection
3. Customer
4. Cart
5. CartItem
6. Order
7. OrderItem

### Product Attributes
1. title 
2. Slug
3. description
4. price
5. inventory
6. created_at
7. last_updated

### Customer Attributes
1. first_name
2. last_name
3. email --> (unique field)
4. phone
5. birth_date (can be null)
6. membership --> (enum choices)

### Order Attributes
1. placed_at
2. payment_status --> (enum choices)
3. customer --> (Order entity is many to one relationship with customer. i.e. customer has many orders)