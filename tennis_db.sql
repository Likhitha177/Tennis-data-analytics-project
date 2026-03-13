------Create First Table (Categories)-----------
CREATE TABLE Categories (
    category_id VARCHAR(50) PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);
------Create Competitions Table-----------------
CREATE TABLE Competitions (
    competition_id VARCHAR(50) PRIMARY KEY,
    competition_name VARCHAR(100) NOT NULL,
    type VARCHAR(20) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    parent_id VARCHAR(50),
    category_id VARCHAR(50),
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);
------Create Complexes Table----------
CREATE TABLE Complexes (
    complex_id VARCHAR(50) PRIMARY KEY,
    complex_name VARCHAR(100) NOT NULL
);
------Create Venues Table-------------
CREATE TABLE Venues (
    venue_id VARCHAR(50) PRIMARY KEY,
    venue_name VARCHAR(100) NOT NULL,
    city_name VARCHAR(100) NOT NULL,
    country_name VARCHAR(100) NOT NULL,
    country_code CHAR(3) NOT NULL,
    timezone VARCHAR(100) NOT NULL,
    complex_id VARCHAR(50),
    FOREIGN KEY (complex_id) REFERENCES Complexes(complex_id)
);
--------Create Competitors Table------------
CREATE TABLE Competitors (
    competitor_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    country_code CHAR(3) NOT NULL,
    abbreviation VARCHAR(10) NOT NULL
);
---------Create Competitor_Rankings Table--------------
CREATE TABLE Competitor_Rankings (
    rank_id SERIAL PRIMARY KEY,
    rank INT NOT NULL,
    movement INT NOT NULL,
    points INT NOT NULL,
    competitions_played INT NOT NULL,
    competitor_id VARCHAR(50),
    FOREIGN KEY (competitor_id) REFERENCES Competitors(competitor_id)
); 

SELECT * FROM categories;
SELECT * FROM competitions;

SELECT * FROM complexes;
SELECT * FROM venues;

SELECT * FROM competitors;
SELECT * FROM competitor_rankings;

-----Relationship (JOIN)------
---Since we created foreign keys, we must show relationships work.
---      Competitions + Categories ------
SELECT 
    c.competition_name,
    cat.category_name
FROM competitions c
JOIN categories cat
ON c.category_id = cat.category_id;

------  Venues + Complexes ----- 
SELECT 
    v.venue_name,
    v.city_name,
    c.complex_name
FROM venues v
JOIN complexes c
ON v.complex_id = c.complex_id;

--------- Rankings + Competitors -------
SELECT 
    comp.name,
    r.rank,
    r.points
FROM competitor_rankings r
JOIN competitors comp
ON r.competitor_id = comp.competitor_id; 

-----Top Ranked Player-----
SELECT name, points
FROM competitors c
JOIN competitor_rankings r
ON c.competitor_id = r.competitor_id
ORDER BY points DESC
LIMIT 1;

-----Count Competitions per Category -------
SELECT 
    cat.category_name,
    COUNT(c.competition_id) AS total_competitions
FROM competitions c
JOIN categories cat
ON c.category_id = cat.category_id
GROUP BY cat.category_name;

------Count Venues per Complex----- 
SELECT 
    c.complex_name,
    COUNT(v.venue_id) AS total_venues
FROM complexes c
JOIN venues v
ON c.complex_id = v.complex_id
GROUP BY c.complex_name;

CREATE INDEX idx_competition_category
ON competitions(category_id); 

