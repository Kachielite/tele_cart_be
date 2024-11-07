CREATE TYPE order_status AS ENUM ('pending', 'accepted', 'rejected', 'cancelled', 'completed', 'refunded', 'returned', 'exchanged', 'shipped', 'delivered', 'failed', 'unknown');

CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  customers_id INTEGER REFERENCES customers(id) NOT NULL,
  businesses_id INTEGER REFERENCES businesses(id) NOT NULL,
  status order_status NOT NULL,
  total FLOAT DEFAULT 0.0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_order_id ON orders(id);
CREATE INDEX idx_order_customers_id ON orders(customers_id);
CREATE INDEX idx_order_businesses_id ON orders(businesses_id);