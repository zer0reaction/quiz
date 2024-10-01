import database


def check_user_existence(user_id: int):
    query = """
    select exists(
        select 1 
        from state 
        where id = {}
    )""".format(user_id)

    data = database.execute_query("users.db", query, "one")
    return data[0] == 1


def init_user(user_id: int):
    if not check_user_existence(user_id):
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

        database.execute_query("users.db", query_for_state)
        database.executemany_query("users.db", query_for_questions, records)


def reset_user(user_id: int):
    if check_user_existence(user_id):
        query = "delete from state where id = {}".format(user_id)
        database.execute_query("users.db", query)

        query = "delete from questions where id = {}".format(user_id)
        database.execute_query("users.db", query)

        init_user(user_id)

    else:
        print("Error resetting user! User " + str(user_id) + " does not exits")
        print("Initializing user " + str(user_id))
        init_user(user_id)


def get_user_state(user_id: int):
    if check_user_existence(user_id):
        query = """
        select state
        from state
        where id = {}
        """.format(user_id)

        data = database.execute_query("users.db", query, "one")

        return data[0]

    else:
        print("Error getting user state! User " + str(user_id) + " does not exits")
        print("Initializing user " + str(user_id))
        init_user(user_id)


def change_user_state(user_id: int, state: str):
    if check_user_existence(user_id):
        query = """
        update state
        set state = '{}'
        where id = {}
        """.format(state, user_id)

        database.execute_query("users.db", query)

    else:
        print("Error changing user state! User " + str(user_id) + " does not exits")
        print("Initializing user " + str(user_id))
        init_user(user_id)


def get_question_statuses(user_id: int):
    if check_user_existence(user_id):
        query = """
        select status
        from questions
        where id = {}
        """.format(user_id)

        data = database.execute_query("users.db", query, "all")

        statuses = []

        for item in data:
            statuses.append(item[0])

        return statuses

    else:
        print("Error getting question statuses! User " + str(user_id) + " does not exits")
        print("Initializing user " + str(user_id))
        init_user(user_id)
        return []


def change_question_status(question_number: int, user_id: int, status: str):
    if check_user_existence(user_id):
        query = """
        update questions
        set status = '{}' 
        where id = {} and number = {}
        """.format(status, user_id, question_number)

        database.execute_query("users.db", query)

    else:

        print("Error changing question status! User " + str(user_id) + " does not exits")
        print("Initializing user " + str(user_id))
        init_user(user_id)
        return []
