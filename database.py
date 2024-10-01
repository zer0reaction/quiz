import sqlite3


def execute_query(database :str, query: str, return_option: str | None = "none"):
    con = sqlite3.connect("data/" + database)
    cur = con.cursor()

    cur.execute(query)
    data = []

    if return_option == "one":
        data = cur.fetchone()

    elif return_option == "all":
        data = cur.fetchall()

    else:
        data = []

    con.commit()
    con.close()
    return data


def executemany_query(database: str, query: str, input: list):
    con = sqlite3.connect("data/" + database)
    cur = con.cursor()

    cur.executemany(query, input)

    con.commit()
    con.close()
