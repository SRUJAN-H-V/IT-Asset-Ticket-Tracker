-- IT Asset & Ticket Tracker
-- Database Schema

PRAGMA foreign_keys = ON;

-- =========================
-- USERS TABLE
-- =========================

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    department TEXT NOT NULL,
    role TEXT NOT NULL CHECK (
        role IN ('Employee', 'Technician', 'Admin')
    ),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


-- =========================
-- ASSETS TABLE
-- =========================

CREATE TABLE assets (
    asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_tag TEXT NOT NULL UNIQUE,
    asset_type TEXT NOT NULL,
    brand TEXT NOT NULL,
    model TEXT,
    serial_number TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'Available' CHECK (
        status IN ('Available', 'Assigned', 'Under Repair', 'Retired')
    ),
    purchase_date DATE,
    assigned_user_id INTEGER,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (assigned_user_id)
        REFERENCES users(user_id)
        ON DELETE SET NULL
);


-- =========================
-- TICKETS TABLE
-- =========================

CREATE TABLE tickets (
    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,

    priority TEXT NOT NULL DEFAULT 'Medium' CHECK (
        priority IN ('Low', 'Medium', 'High', 'Critical')
    ),

    status TEXT NOT NULL DEFAULT 'Open' CHECK (
        status IN (
            'Open',
            'Assigned',
            'In Progress',
            'Resolved',
            'Closed'
        )
    ),

    user_id INTEGER NOT NULL,
    asset_id INTEGER,
    technician_id INTEGER,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    FOREIGN KEY (asset_id)
        REFERENCES assets(asset_id)
        ON DELETE SET NULL,

    FOREIGN KEY (technician_id)
        REFERENCES users(user_id)
        ON DELETE SET NULL
);


-- =========================
-- MAINTENANCE TABLE
-- =========================

CREATE TABLE maintenance (
    maintenance_id INTEGER PRIMARY KEY AUTOINCREMENT,

    asset_id INTEGER NOT NULL,
    ticket_id INTEGER,

    description TEXT NOT NULL,
    cost REAL DEFAULT 0 CHECK (cost >= 0),

    maintenance_date DATE NOT NULL,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (asset_id)
        REFERENCES assets(asset_id)
        ON DELETE CASCADE,

    FOREIGN KEY (ticket_id)
        REFERENCES tickets(ticket_id)
        ON DELETE SET NULL
);