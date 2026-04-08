CREATE DATABASE IF NOT EXISTS galeri_db CHARACTER
SET
    utf8mb4 COLLATE utf8mb4_unicode_ci;

USE galeri_db;

-- =====================================================
-- TABEL USERS
-- =====================================================
CREATE TABLE
    IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(120) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_email (email),
        INDEX idx_created_at (created_at)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- =====================================================
-- TABEL PHOTOS
-- =====================================================
CREATE TABLE
    IF NOT EXISTS photos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        title VARCHAR(200) NOT NULL,
        description TEXT,
        image_file VARCHAR(255) NOT NULL,
        likes_count INT DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
        INDEX idx_user_id (user_id),
        INDEX idx_created_at (created_at),
        INDEX idx_likes (likes_count)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- =====================================================
-- TABEL LIKES
-- =====================================================
CREATE TABLE
    IF NOT EXISTS likes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        photo_id INT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
        FOREIGN KEY (photo_id) REFERENCES photos (id) ON DELETE CASCADE,
        UNIQUE KEY unique_user_photo_like (user_id, photo_id),
        INDEX idx_user_id (user_id),
        INDEX idx_photo_id (photo_id)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Password hash untuk 'password123': scrypt:32768:8:1$...
-- INSERT INTO users (name, email, password) VALUES
-- ('Test User', 'test@example.com', 'scrypt:32768:8:1$...');
-- =====================================================
-- QUERY BERGUNA 
-- =====================================================
-- Lihat semua user
-- SELECT * FROM users;
-- Lihat semua foto dengan nama uploader
-- SELECT p.*, u.name as uploader_name
-- FROM photos p
-- JOIN users u ON p.user_id = u.id;
-- Lihat total like per foto
-- SELECT p.title, COUNT(l.id) as total_likes
-- FROM photos p
-- LEFT JOIN likes l ON p.id = l.photo_id
-- GROUP BY p.id;
-- Lihat user dengan foto terbanyak
-- SELECT u.name, COUNT(p.id) as total_photos
-- FROM users u
-- LEFT JOIN photos p ON u.id = p.user_id
-- GROUP BY u.id
-- ORDER BY total_photos DESC;