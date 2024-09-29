import sqlite3


# ----- USERS -----

def check_user_existence(user_id: int):
    con = sqlite3.connect("data/users.db")
    cur = con.cursor()

    query = """
    select exists(
        select 1 
        from state 
        where id = {}
    )""".format(user_id)

    cur.execute(query)
    data = cur.fetchone()

    con.close()
    return data[0] == 1


def init_user(user_id: int):
    if not check_user_existence(user_id):
        con = sqlite3.connect("data/users.db")
        cur = con.cursor()

        query_for_state = """
        insert into state values (
            {},
            'welcome'
        )
        """.format(user_id)

        query_for_questions = """
        insert into questions values (
            ?, ?, ?
        )
        """

        records = [
            (user_id, 1, 'not_answered'),
            (user_id, 2, 'not_answered'),
            (user_id, 3, 'not_answered'),
            (user_id, 4, 'not_answered'),
            (user_id, 5, 'not_answered')
        ]

        cur.execute(query_for_state)
        cur.executemany(query_for_questions, records)

        con.commit()
        con.close()


def get_user_state(user_id: int):
    if check_user_existence(user_id):
        con = sqlite3.connect("data/users.db")
        cur = con.cursor()

        query = """
        select state
        from state
        where id = {}
        """.format(user_id)

        cur.execute(query)
        data = cur.fetchone()

        con.close()
        return data[0]


def change_user_state(user_id: int, state: str):
    if check_user_existence(user_id):
        con = sqlite3.connect("data/users.db")
        cur = con.cursor()

        query = """
        update state
        set state = '{}'
        where id = {}
        """.format(state, user_id)

        cur.execute(query)
        con.commit()
        con.close()

# ----- USERS -----


# ----- QUESTIONS -----

def get_question_labels():
    con = sqlite3.connect("data/quiz.db")
    cur = con.cursor()

    query = "select label from questions"
    cur.execute(query)

    data = cur.fetchall()
    labels = []

    for item in data:
        labels.append(item[0])

    con.close()
    return labels


def get_question_photo(question_number: int):
    con = sqlite3.connect("data/quiz.db")
    con.text_factory = bytes
    cur = con.cursor()

    query = """
    select photo
    from questions
    where rowid = {}
    """.format(question_number)

    cur.execute(query)
    data = cur.fetchone()

    con.close()
    return data[0]


def get_question_qha(question_number: int):
    con = sqlite3.connect("data/quiz.db")
    cur = con.cursor()

    query = """
    select question, hint, answer
    from questions
    where rowid = {}
    """.format(question_number)

    cur.execute(query)
    data = cur.fetchall()

    con.close()
    return data[0]


def change_question_status(question_number: int, user_id: int, status: str):
    con = sqlite3.connect("data/users.db")
    cur = con.cursor()

    query = """
    update questions
    set status = '{}' 
    where id = {} and number = {}
    """.format(status, user_id, question_number)

    cur.execute(query)

    con.commit()
    con.close()

# ----- QUESTIONS -----
