CREATE TABLE order_items (
  id SERIAL PRIMARY KEY,
  orders_id INTEGER REFERENCES orders(id) NOT NULL,
  products_id INTEGER REFERENCES products(id) NOT NULL,
  quantity INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_order_items_id ON order_items(id);
CREATE INDEX idx_order_items_orders_id ON order_items(orders_id);
CREATE INDEX idx_order_items_products_id ON order_items(products_id);
