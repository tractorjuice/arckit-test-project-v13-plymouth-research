-- Migration: Create data_quality_metrics table (E-006 from data model ARC-001-DATA-v1.0)
-- Tracks data quality metrics over time for continuous monitoring

CREATE TABLE IF NOT EXISTS data_quality_metrics (
    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
    metric_date TEXT NOT NULL,           -- ISO 8601 date
    metric_type TEXT NOT NULL CHECK(metric_type IN ('completeness', 'accuracy', 'timeliness', 'duplication', 'freshness')),
    metric_value REAL NOT NULL CHECK(metric_value >= 0.0 AND metric_value <= 1.0),
    entity_name TEXT,                    -- restaurants, menu_items, trustpilot_reviews, google_reviews
    attribute_name TEXT,                 -- Specific attribute measured
    details TEXT,                        -- JSON drill-down information
    measured_at TEXT NOT NULL             -- ISO 8601 timestamp
);

CREATE INDEX IF NOT EXISTS idx_dqm_date ON data_quality_metrics(metric_date);
CREATE INDEX IF NOT EXISTS idx_dqm_type ON data_quality_metrics(metric_type);
CREATE INDEX IF NOT EXISTS idx_dqm_entity ON data_quality_metrics(entity_name);
