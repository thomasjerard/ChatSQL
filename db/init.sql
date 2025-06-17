CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    name TEXT,
    salary NUMERIC,
    phone_no TEXT,
    address TEXT,
    department TEXT
);

INSERT INTO employees (name, salary, phone_no, address, department)
VALUES
('Alice', 60000, '9876543210', 'Bangalore', 'HR'),
('Bob', 70000, '9876543211', 'Chennai', 'Engineering'),
('Charlie', 55000, '9876543212', 'Delhi', 'Finance')
ON CONFLICT DO NOTHING;
