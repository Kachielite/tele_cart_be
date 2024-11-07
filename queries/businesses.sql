CREATE TABLE businesses (
    id SERIAL PRIMARY KEY,
    identifier VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    description TEXT,
    address TEXT,
    phone_number VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    image_url VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX idx_business_id ON businesses(id);
CREATE INDEX idx_business_identifier ON businesses(identifier);
CREATE INDEX idx_business_email ON businesses(email);
CREATE INDEX idx_business_phone_number ON businesses(phone_number);