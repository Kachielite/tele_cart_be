CREATE TABLE customers (
  id SERIAL PRIMARY KEY,
  telegram_id INTEGER,
  name VARCHAR(255),
  phone_number VARCHAR(255) UNIQUE,
  address VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_customers_id ON customers(id);
CREATE INDEX idx_customers_telegram_id ON customers(telegram_id);
CREATE INDEX idx_customers_phone_number ON customers(phone_number);