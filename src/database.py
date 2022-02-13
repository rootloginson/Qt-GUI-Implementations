import sqlite3
from datetime import datetime, timezone


def update_db(track_details: dict) -> None:
    """datetime is the time of adding track to database"""

    # connects to the database. If the database does not exist, create one.
    conn = sqlite3.connect('track_request_history.sql')
    cur = conn.cursor()

    sql_db_create = """
    CREATE TABLE IF NOT EXISTS Random_Tracks(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            date_time TEXT,
            artist_name TEXT,
            album_name TEXT,
            track_name TEXT,
            track_external_url TEXT
    )
    """
    # create the table if it doesn't exist
    cur.execute(sql_db_create)

    if track_details:
        # timezone is GMT/UTC+0
        date_time = datetime.now(timezone.utc)

        # Create the row to insert into the database
        sql_update_db = """
        INSERT INTO Random_Tracks
        (date_time, artist_name, album_name, track_name, track_external_url)
        VALUES (?, ?, ?, ?, ?)
        """
        values = (
            date_time,
            track_details['artist_name'],
            track_details['album_name'],
            track_details['track_name'],
            track_details['track_external_urls'],
            )
        # insert a row of track data
        cur.execute(sql_update_db, values)

    # commit the changes
    conn.commit()

    # close the database
    conn.close()
