CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  email VARCHAR(120) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE accounts (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(id),
  balance NUMERIC(14,2) DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
  id SERIAL PRIMARY KEY,
  account_id INT NOT NULL REFERENCES accounts(id),
  amount NUMERIC(14,2) NOT NULL,
  type VARCHAR(20) NOT NULL,
  category VARCHAR(80) NOT NULL,
  description TEXT NOT NULL,
  date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  sender VARCHAR(120) NOT NULL,
  receiver VARCHAR(120) NOT NULL
);

CREATE TABLE employees (
  id SERIAL PRIMARY KEY,
  business_id INT NOT NULL REFERENCES accounts(id),
  name VARCHAR(120) NOT NULL,
  salary NUMERIC(12,2) NOT NULL,
  pension NUMERIC(12,2) NOT NULL,
  nhis NUMERIC(12,2) NOT NULL
);

CREATE TABLE payroll_records (
  id SERIAL PRIMARY KEY,
  employee_id INT NOT NULL REFERENCES employees(id),
  gross_salary NUMERIC(12,2) NOT NULL,
  taxable_income NUMERIC(12,2) NOT NULL,
  paye_deduction NUMERIC(12,2) NOT NULL,
  date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE vat_wallet (
  id SERIAL PRIMARY KEY,
  account_id INT NOT NULL REFERENCES accounts(id),
  balance NUMERIC(14,2) DEFAULT 0
);

CREATE TABLE cit_wallet (
  id SERIAL PRIMARY KEY,
  account_id INT NOT NULL REFERENCES accounts(id),
  balance NUMERIC(14,2) DEFAULT 0
);

CREATE TABLE tax_estimations (
  id SERIAL PRIMARY KEY,
  account_id INT NOT NULL REFERENCES accounts(id),
  estimated_annual_income NUMERIC(14,2) DEFAULT 0,
  estimated_profit NUMERIC(14,2) DEFAULT 0,
  estimated_tax NUMERIC(14,2) DEFAULT 0,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
