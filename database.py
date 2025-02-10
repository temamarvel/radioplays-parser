import psycopg2

try:
    # пытаемся подключиться к базе данных
    conn = psycopg2.connect(dbname='artemdenisov', user='artemdenisov', password='', host='localhost')
    print("ok")

    cursor = conn.cursor()

    with cursor as curs:
        print(1)
        tests = 'tewfffs'
        curs.execute(f"INSERT INTO plays (name) VALUES ('{tests}')")
        print(2)

        conn.commit()

        curs.execute("SELECT * FROM plays")
        all = curs.fetchall()
        print(all)

    conn.close()
except:
    # в случае сбоя подключения будет выведено сообщение в STDOUT
    print('Can`t establish connection to database')