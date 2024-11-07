CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT NOT NULL,
  price FLOAT DEFAULT 0.0,
  in_stock BOOLEAN DEFAULT FALSE,
  image_url VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  businesses_id INTEGER REFERENCES businesses(id) NOT NULL,
  CONSTRAINT fk_product_businesses FOREIGN KEY (businesses_id) REFERENCES businesses(id)
);


CREATE INDEX idx_product_id ON products(id);