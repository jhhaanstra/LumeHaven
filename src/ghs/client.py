import sqlite3

if __name__ == '__main__':
    connection = sqlite3.connect("../../ghs/ghs.sqlite")
    cursor = connection.cursor()
    result = cursor.execute('SELECT * FROM "main"."games" WHERE id = 1;')
    print(result.fetchone())