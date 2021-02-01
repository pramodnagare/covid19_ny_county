CREATE TABLE IF NOT EXISTS {} (
    test_date TIMESTAMP NOT NULL,
    county VARCHAR (50) NOT NULL,
    new_positives INTEGER NOT NULL,
    cumulative_number_of_positives INTEGER NOT NULL,
    total_number_of_tests INTEGER NOT NULL,
    cumulative_number_of_tests INTEGER NOT NULL,
    load_date TIMESTAMP NOT NULL DEFAULT NOW()
);