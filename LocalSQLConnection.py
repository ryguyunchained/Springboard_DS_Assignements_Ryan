import sqlite3
from sqlite3 import Error

 
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.sqlite_version)
    except Error as e:
        print(e)
 
    return conn

 
def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    
    query1 = """
        SELECT *
        FROM FACILITIES
        """
    cur.execute(query1)

    query2 = """
        SELECT name
        FROM facilities
        WHERE membercost = 0"""
    cur.execute(query2)

    query3 = """
        SELECT COUNT(*)
        FROM facilities
        WHERE membercost = 0"""
    cur.execute(query3)

    query4 = """
        SELECT facid, name, membercost, monthlymaintenance
        FROM facilities
        WHERE membercost > 0 AND membercost < 0.2 * monthlymaintenance"""
    cur.execute(query4)

    query5 = """
       SELECT name, monthlymaintenance,
        CASE
            WHEN monthlymaintenance > 100 THEN 'expensive'
            ELSE 'cheap'
        END AS cost_label
        FROM facilities """
    cur.execute(query5)

    query6 = """
        SELECT firstname, surname
        FROM members
        WHERE joindate = (SELECT MAX(joindate) FROM members)"""
    cur.execute(query6)    

    query7 = """
        SELECT DISTINCT (m.surname || ', ' || m.firstname) AS member_name, f.name
        FROM members AS m
        JOIN bookings AS b ON m.memid = b.memid
        JOIN facilities AS f ON b.facid = f.facid
        WHERE f.name LIKE '%Tennis Court%'
        ORDER BY member_name ASC"""
    cur.execute(query7)

    query8 = """
        SELECT f.name, (m.surname || ',' || m.firstname) AS member_name, 
            CASE
                WHEN b.memid = 0 THEN f.guestcost *b.slots
                ELSE f.membercost * b.slots
            END AS cost
        FROM bookings AS b
        JOIN facilities AS f ON b.facid = f.facid
        JOIN members AS m ON b.memid = m.memid
        WHERE b.starttime LIKE '2012-09-14%' AND 
            CASE
                WHEN b.memid = 0 THEN f.guestcost *b.slots
                ELSE f.membercost * b.slots
            END > 30
        ORDER BY cost DESC"""
    cur.execute(query8)

    query9 = """
        SELECT member_name, facility, cost
            FROM (
                SELECT (m.surname || ',' || m.firstname) AS member_name,
                f.name AS facility,
                    CASE
                        WHEN b.memid = 0 THEN f.guestcost * b.slots
                        ELSE f.membercost * b.slots
                    END AS cost
                FROM bookings AS b
                JOIN facilities AS f ON b.facid = f.facid
                JOIN members AS m ON b.memid = m.memid
                WHERE b.starttime LIKE '2012-09-14%'
            ) AS subquery
        WHERE cost > 30
        ORDER BY cost DESC"""
    cur.execute(query9)

    query10 = """
        SELECT f.name AS facility_name, 
            SUM(CASE
                WHEN b.memid = 0 THEN f.guestcost * b.slots
                ELSE f.membercost * b.slots
            END) AS total_revenue
        FROM facilities AS f 
        JOIN bookings AS b ON f.facid = b.facid
        GROUP BY f.name
        HAVING total_revenue < 1000
        ORDER BY total_revenue ASC
        """
    cur.execute(query10)

    query11 = """
        SELECT m.surname AS member_surname, m.firstname AS member_firstname,
            CASE
                WHEN m.recommendedby IS NOT NULL THEN (SELECT surname || ', ' || firstname 
                                                       FROM members WHERE memid = m.recommendedby)
                ELSE 'No recommender'
            END AS recommender_name
        FROM members AS m
        ORDER BY member_surname, member_firstname"""
    cur.execute(query11)

    query12 = """
        SELECT f.name AS facility_name, SUM(b.slots) AS total_slots, (m.surname || ', ' || m.firstname) AS member_name
        FROM bookings AS b
        JOIN facilities AS f ON b.facid = f.facid
        JOIN members AS m ON b.memid = m.memid
        WHERE b.memid != 0
        GROUP BY f.name, member_name
        ORDER BY f.name, total_slots DESC"""
    cur.execute(query12)

    query13 = """
        SELECT f.name AS facility_name, SUM(b.slots) AS total_slots, strftime('%Y-%m', b.starttime) AS month
        FROM bookings AS b
        JOIN facilities AS f ON b.facid = f.facid
        WHERE b.memid != 0
        GROUP BY f.name, month
        ORDER BY f.name, month"""
    cur.execute(query13)

    queries = [
    ("Q1", query1),
    ("Q2", query2),
    ("Q3", query3),
    ("Q4", query4),
    ("Q5", query5),
    ("Q6", query6),
    ("Q7", query7),
    ("Q8", query8),
    ("Q9", query9),
    ("Q10", query10),
    ("Q11", query11),
    ("Q12", query12),
    ("Q13", query13)
]

    for label, query in queries:
        print(f"\n{label}:")
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            print(row)


def main():
    database = "sqlite_db_pythonsqlite.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn: 
        print("2. Query all tasks")
        select_all_tasks(conn)
 
 
if __name__ == '__main__':
    main()