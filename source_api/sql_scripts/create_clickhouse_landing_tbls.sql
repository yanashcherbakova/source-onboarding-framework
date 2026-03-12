CREATE DATABASE IF NOT EXISTS landing;

CREATE TABLE landing.landing_plans
(
    source_id String,
    pk String,
    payload_json String,
    source_updated_at DateTime,
    ingested_at DateTime DEFAULT now(),
    run_id String
)
ENGINE = MergeTree
ORDER BY (pk, source_updated_at);

CREATE TABLE landing.landing_subscriptions
(
    source_id String,
    pk String,
    payload_json String,
    source_updated_at DateTime,
    ingested_at DateTime DEFAULT now(),
    run_id String
)
ENGINE = MergeTree
ORDER BY (pk, source_updated_at);

CREATE TABLE landing.landing_subscription_events
(
    source_id String,
    pk String,
    payload_json String,
    source_updated_at DateTime,
    ingested_at DateTime DEFAULT now(),
    run_id String
)
ENGINE = MergeTree
ORDER BY (pk, source_updated_at);