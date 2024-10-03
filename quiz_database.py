import database, sqlite3

def get_question_labels():
    query = "select label from questions"
    data = database.execute_query("quiz.db", query, "all")

    labels = []

    for item in data:
        labels.append(item[0])

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


def get_question_qai(question_number: int):
    query = """
    select question, answer, info
    from questions
    where number = {}
    """.format(question_number)

    data = database.execute_query("quiz.db", query, "one")

    return data


def get_question_info_photo(question_number: int):
    con = sqlite3.connect("data/quiz.db")
    con.text_factory = bytes
    cur = con.cursor()

    query = """
    select info_photo
    from questions
    where rowid = {}
    """.format(question_number)

    cur.execute(query)
    data = cur.fetchone()

    con.close()
    return data[0]


def get_hints_amount(question_number: int):
    query = """
    select count(*)
    from hints
    where question_number = {}
    """.format(question_number)

    data = database.execute_query("quiz.db", query, "one")

    return data[0]


def get_hint_photo(question_number: int, hint_number: int):
    con = sqlite3.connect("data/quiz.db")
    con.text_factory = bytes
    cur = con.cursor()

    query = """
    select photo
    from hints
    where question_number = {} and hint_number = {}
    """.format(question_number, hint_number)

    cur.execute(query)
    data = cur.fetchone()

    con.close()
    return data[0]


def get_hint_text(question_number: int, hint_number: int):
    query = """
    select hint
    from hints
    where question_number = {} and hint_number = {}
    """.format(question_number, hint_number)

    data = database.execute_query("quiz.db", query, "one")

    return data[0]
