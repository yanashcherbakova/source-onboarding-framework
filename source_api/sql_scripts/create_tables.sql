CREATE TABLE IF NOT EXISTS plans (
    plan_id SERIAL PRIMARY KEY,
    plan_name TEXT NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted BOOLEAN NOT NULL DEFAULT FALSE
);

-- test data
INSERT INTO plans (plan_name, price)
VALUES
    ('basic', 9.99),
    ('pro', 19.99),
    ('family', 29.99);


CREATE TABLE subscriptions (
    subscription_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    plan_id INT NOT NULL,
    status TEXT NOT NULL, -- trialing / active / past_due / canceled
    started_at TIMESTAMP NOT NULL,
    current_period_start TIMESTAMP,
    current_period_end TIMESTAMP,
    discount_percent NUMERIC(5,2),
    discount_reason TEXT, -- trial (100), retention_offer (20), promo(5), NULL(0)
    canceled_at TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted BOOLEAN NOT NULL DEFAULT FALSE
);

--test data
INSERT INTO subscriptions (
    user_id,
    plan_id,
    status,
    started_at,
    current_period_start,
    current_period_end,
    discount_percent,
    discount_reason,
    canceled_at,
    updated_at,
    deleted
)
VALUES
    (101, 1, 'trialing', '2026-03-01 09:00:00', '2026-03-01 09:00:00', '2026-03-15 09:00:00', 100.00, 'trial', NULL, '2026-03-01 09:00:00', FALSE),
    (102, 2, 'active', '2026-02-10 10:00:00', '2026-03-10 10:00:00', '2026-04-10 10:00:00', NULL, NULL, NULL, '2026-03-10 10:00:00', FALSE),
    (103, 1, 'active', '2026-01-20 12:30:00', '2026-02-20 12:30:00', '2026-03-20 12:30:00', 5.00, 'promo', NULL, '2026-02-20 12:30:00', FALSE),
    (104, 3, 'past_due', '2026-02-01 08:15:00', '2026-03-01 08:15:00', '2026-04-01 08:15:00', NULL, NULL, NULL, '2026-03-08 14:20:00', FALSE),
    (105, 2, 'canceled', '2025-12-05 15:00:00', '2026-02-05 15:00:00', '2026-03-05 15:00:00', NULL, NULL, '2026-03-02 11:00:00', '2026-03-02 11:00:00', FALSE),

    (106, 1, 'active', '2026-01-11 11:10:00', '2026-03-11 11:10:00', '2026-04-11 11:10:00', 20.00, 'retention_offer', NULL, '2026-03-11 11:10:00', FALSE),
    (107, 3, 'trialing', '2026-03-09 07:40:00', '2026-03-09 07:40:00', '2026-03-23 07:40:00', 100.00, 'trial', NULL, '2026-03-09 07:40:00', FALSE),
    (108, 2, 'active', '2026-02-14 19:00:00', '2026-03-14 19:00:00', '2026-04-14 19:00:00', NULL, NULL, NULL, '2026-03-14 19:00:00', FALSE),
    (109, 1, 'canceled', '2025-11-01 13:00:00', '2026-02-01 13:00:00', '2026-03-01 13:00:00', 20.00, 'retention_offer', '2026-02-25 18:00:00', '2026-02-25 18:00:00', FALSE),
    (110, 3, 'active', '2026-01-05 06:30:00', '2026-03-05 06:30:00', '2026-04-05 06:30:00', 5.00, 'promo', NULL, '2026-03-05 06:30:00', FALSE),

    (111, 2, 'past_due', '2026-02-22 16:45:00', '2026-03-22 16:45:00', '2026-04-22 16:45:00', NULL, NULL, NULL, '2026-03-10 09:25:00', FALSE),
    (112, 1, 'active', '2026-01-17 21:00:00', '2026-03-17 21:00:00', '2026-04-17 21:00:00', NULL, NULL, NULL, '2026-03-17 21:00:00', FALSE),
    (113, 3, 'canceled', '2025-10-10 10:10:00', '2026-02-10 10:10:00', '2026-03-10 10:10:00', NULL, NULL, '2026-03-09 20:00:00', '2026-03-09 20:00:00', FALSE),
    (114, 2, 'trialing', '2026-03-10 14:00:00', '2026-03-10 14:00:00', '2026-03-24 14:00:00', 100.00, 'trial', NULL, '2026-03-10 14:00:00', FALSE),
    (115, 1, 'active', '2026-02-03 09:50:00', '2026-03-03 09:50:00', '2026-04-03 09:50:00', 20.00, 'retention_offer', NULL, '2026-03-03 09:50:00', FALSE),

    (116, 3, 'active', '2026-01-28 17:35:00', '2026-02-28 17:35:00', '2026-03-28 17:35:00', NULL, NULL, NULL, '2026-02-28 17:35:00', FALSE),
    (117, 2, 'past_due', '2026-02-18 12:00:00', '2026-03-18 12:00:00', '2026-04-18 12:00:00', 5.00, 'promo', NULL, '2026-03-19 08:10:00', FALSE),
    (118, 1, 'active', '2026-01-09 22:15:00', '2026-03-09 22:15:00', '2026-04-09 22:15:00', NULL, NULL, NULL, '2026-03-09 22:15:00', FALSE),
    (119, 3, 'canceled', '2025-09-15 05:20:00', '2026-02-15 05:20:00', '2026-03-15 05:20:00', 20.00, 'retention_offer', '2026-03-11 07:00:00', '2026-03-11 07:00:00', TRUE),
    (120, 2, 'active', '2026-02-27 18:25:00', '2026-03-27 18:25:00', '2026-04-27 18:25:00', 5.00, 'promo', NULL, '2026-03-27 18:25:00', FALSE);


subscription_events
-trial_started
-trial_converted
-renewed
-payment_failed
-cancel_requested
-canceled
-resumed
-retention_offer_shown
-retention_offer_accepted
-retention_offer_rejected