import function
import json

def add_times(parent_dir, filename, times):
    try:
        query = "INSERT INTO Stats(DIR, FILENAME, TIMES) " \
                "VALUES (:dir, :filename, :times)"
        conn = function.get_connection()
        conn.cursor().execute(query, {'dir': parent_dir, 'filename': filename, 'times': times})
        conn.commit()
    except Exception as ex:
        print(ex)


def check_times(parent_dir):
    try:
        query = "SELECT TIMES, FILENAME FROM Stats WHERE DIR = :dir"
        conn = function.get_connection()
        c = conn.cursor().execute(query, {'dir': parent_dir})
        return c
    except Exception as ex:
        print(ex)


def check_times_a_file(parent_dir, filename):
    try:
        query = "SELECT TIMES FROM Stats WHERE DIR = :dir AND FILENAME = :filename"
        conn = function.get_connection()
        c = conn.cursor().execute(query, {'dir': parent_dir, 'filename': filename})
        for row in c:
            if row is not None:
                return row[0]
        return "Not existed"
    except Exception as ex:
        print(ex)


def update_times(parent_dir, filename, times):
    try:
        query = "UPDATE Stats SET TIMES = :times WHERE DIR = :dir AND FILENAME = :filename"
        conn = function.get_connection()
        conn.cursor().execute(query, {'dir': parent_dir, 'filename': filename, 'times': times})
        conn.commit()
    except Exception as ex:
        print(ex)


def delete_file(parent_dir, filename):
    try:
        query = "DELETE FROM Stats WHERE DIR = :dir AND FILENAME = :filename"
        conn = function.get_connection()
        conn.cursor().execute(query, {'filename': filename, 'dir': parent_dir})
        conn.commit()
    except Exception as ex:
        print(ex)


def edit_file_name(parent_dir, filename, new_name):
    try:
        query = "UPDATE Stats SET FILENAME = :new_name WHERE DIR = :dir AND FILENAME = :filename"
        conn = function.get_connection()
        conn.cursor().execute(query, {'new_name': new_name, 'filename': filename, 'dir': parent_dir})
        conn.commit()
    except Exception as ex:
        print(ex)

def get_stats(parent_dir):
    list_stats = check_times(parent_dir)
    stats = []
    for row in list_stats:
        s = {"file_name": row[1], "times": row[0]}
        stats.append(s)
    return json.dumps(stats)


def download(parent_dir, filename):
    times = str(int(check_times_a_file(parent_dir, filename)) + 1)
    update_times(parent_dir, filename, times)