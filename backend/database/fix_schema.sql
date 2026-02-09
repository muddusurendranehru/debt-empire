-- Fix phone column to be nullable
ALTER TABLE users ALTER COLUMN phone DROP NOT NULL;
