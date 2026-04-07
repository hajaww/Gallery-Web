-- Migration: Add profile_photo column to users table
-- Run this SQL to update your existing database

ALTER TABLE users ADD COLUMN profile_photo VARCHAR(255) DEFAULT NULL AFTER password;
