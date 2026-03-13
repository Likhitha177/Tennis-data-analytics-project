import json
import psycopg2

try:
    # Connect
    conn = psycopg2.connect(
        database="tennis_db",
        user="postgres",
        password="raksha",
        host="localhost",
        port="5432"
    )

    cursor = conn.cursor()

    # -------------------------
    # Insert Competitions
    # -------------------------

    with open("competitions.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for comp in data.get("competitions", []):
        category = comp.get("category", {})

        cursor.execute("""
            INSERT INTO Categories (category_id, category_name)
            VALUES (%s, %s)
            ON CONFLICT (category_id) DO NOTHING;
        """, (category.get("id"), category.get("name")))

        cursor.execute("""
            INSERT INTO Competitions
            (competition_id, competition_name, type, gender, parent_id, category_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (competition_id) DO NOTHING;
        """, (
            comp.get("id"),
            comp.get("name"),
            comp.get("type"),
            comp.get("gender"),
            comp.get("parent_id"),
            category.get("id")
        ))

    # -------------------------
    # Insert Complexes
    # -------------------------

    with open("complexes.json", "r", encoding="utf-8") as f:
        complexes_data = json.load(f)

    for compx in complexes_data.get("complexes", []):

        cursor.execute("""
            INSERT INTO Complexes (complex_id, complex_name)
            VALUES (%s, %s)
            ON CONFLICT (complex_id) DO NOTHING;
        """, (compx.get("id"), compx.get("name")))

        for venue in compx.get("venues", []):
            cursor.execute("""
                INSERT INTO Venues
                (venue_id, venue_name, city_name, country_name, country_code, timezone, complex_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (venue_id) DO NOTHING;
            """, (
                venue.get("id"),
                venue.get("name"),
                venue.get("city_name"),
                venue.get("country_name"),
                venue.get("country_code"),
                venue.get("timezone"),
                compx.get("id")
            ))

    # -------------------------
    # Insert Rankings
    # -------------------------

    with open("rankings.json", "r", encoding="utf-8") as f:
        rankings_data = json.load(f)

    for ranking in rankings_data.get("rankings", []):
        for comp_rank in ranking.get("competitor_rankings", []):

            competitor = comp_rank.get("competitor", {})

            cursor.execute("""
                INSERT INTO Competitors
                (competitor_id, name, country, country_code, abbreviation)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (competitor_id) DO NOTHING;
            """, (
                competitor.get("id"),
                competitor.get("name"),
                competitor.get("country"),
                competitor.get("country_code"),
                competitor.get("abbreviation")
            ))

            cursor.execute("""
                INSERT INTO Competitor_Rankings
                (rank, movement, points, competitions_played, competitor_id)
                VALUES (%s, %s, %s, %s, %s);
            """, (
                comp_rank.get("rank"),
                comp_rank.get("movement"),
                comp_rank.get("points"),
                comp_rank.get("competitions_played"),
                competitor.get("id")
            ))

    # Commit ONCE
    conn.commit()

    # Close ONCE
    cursor.close()
    conn.close()

    print("All data inserted successfully ")

except Exception as e:
    print("Error:", e)
