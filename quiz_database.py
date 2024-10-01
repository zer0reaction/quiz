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


def get_question_qha(question_number: int):
    query = """
    select question, hint, answer
    from questions
    where rowid = {}
    """.format(question_number)

    data = database.execute_query("quiz.db", query, "one")

    return data
