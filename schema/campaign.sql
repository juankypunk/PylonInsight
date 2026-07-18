CREATE TABLE campaign (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    capture_date TIMESTAMP NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT now(),
);