CREATE TABLE IF NOT EXISTS game_results (
    id VARCHAR(14) PRIMARY KEY,
    visitor TEXT NOT NULL,
    home TEXT NOT NULL,
    dates INT NOT NULL,
    visitor_score INT NOT NULL,
    home_score INT NOT NULL
);