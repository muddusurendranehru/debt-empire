-- Debt Empire Database Schema
-- Neon PostgreSQL Database
-- UUID primary keys for all tables

-- Users table for authentication
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Loans table (migrated from masters.json)
CREATE TABLE IF NOT EXISTS loans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR(100) NOT NULL,
    account_ref VARCHAR(255),
    outstanding BIGINT NOT NULL DEFAULT 0,
    emi BIGINT NOT NULL DEFAULT 0,
    tenure_months INTEGER NOT NULL DEFAULT 0,
    ots_amount_70pct BIGINT DEFAULT 0,
    savings BIGINT DEFAULT 0,
    start_date DATE,
    loan_type VARCHAR(50) DEFAULT 'personal',
    status VARCHAR(50) DEFAULT 'RUNNING_PAID_EMI',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Monthly statements table (for CSV uploads)
CREATE TABLE IF NOT EXISTS monthly_statements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    month_name VARCHAR(50) NOT NULL,
    csv_path TEXT,
    parsed_data JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Projections table (for monthly projections)
CREATE TABLE IF NOT EXISTS projections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    loan_id UUID REFERENCES loans(id) ON DELETE CASCADE,
    month_name VARCHAR(50) NOT NULL,
    projection_data JSONB,
    excel_path TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_loans_user_id ON loans(user_id);
CREATE INDEX IF NOT EXISTS idx_loans_provider ON loans(provider);
CREATE INDEX IF NOT EXISTS idx_monthly_statements_user_id ON monthly_statements(user_id);
CREATE INDEX IF NOT EXISTS idx_projections_user_id ON projections(user_id);
CREATE INDEX IF NOT EXISTS idx_projections_loan_id ON projections(loan_id);
