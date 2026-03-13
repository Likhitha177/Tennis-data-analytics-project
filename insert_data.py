import sqlite3
import json

# connect to database
conn = sqlite3.connect("tennis_db.db")
cursor = conn.cursor()

# ---------- Insert Categories and Competitions ----------

with open("competitions.json") as f:
    data = json.load(f)

for comp in data["competitions"]:

    category_id = comp["category"]["id"]
    category_name = comp["category"]["name"]

    cursor.execute(
        "INSERT OR IGNORE INTO categories VALUES (?, ?)",
        (category_id, category_name)
    )

    cursor.execute(
        "INSERT OR IGNORE INTO competitions VALUES (?, ?, ?, ?, ?, ?)",
        (
            comp["id"],
            comp["name"],
            comp["type"],
            comp["gender"],
            comp["parent_id"],
            category_id
        )
    )


# ---------- Insert Complexes and Venues ----------

with open("complexes.json") as f:
    data = json.load(f)

for complex in data["complexes"]:

    cursor.execute(
        "INSERT OR IGNORE INTO complexes VALUES (?, ?)",
        (complex["id"], complex["name"])
    )

    for venue in complex["venues"]:

        cursor.execute(
            "INSERT OR IGNORE INTO venues VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                venue["id"],
                venue["name"],
                venue["city_name"],
                venue["country_name"],
                venue["country_code"],
                venue["timezone"],
                complex["id"]
            )
        )


# ---------- Insert Competitors and Rankings ----------

with open("rankings.json") as f:
    data = json.load(f)

for ranking in data["rankings"]:

    for player in ranking["competitor_rankings"]:

        comp = player["competitor"]

        cursor.execute(
            "INSERT OR IGNORE INTO competitors VALUES (?, ?, ?, ?, ?)",
            (
                comp["id"],
                comp["name"],
                comp["country"],
                comp["country_code"],
                comp["abbreviation"]
            )
        )

        cursor.execute(
            """INSERT INTO competitor_rankings
            (rank, movement, points, competitions_played, competitor_id)
            VALUES (?, ?, ?, ?, ?)""",
            (
                player["rank"],
                player["movement"],
                player["points"],
                player["competitions_played"],
                comp["id"]
            )
        )


conn.commit()
conn.close()

print("Data inserted successfully!")