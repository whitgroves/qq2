import psycopg

with psycopg.connect('dbname=qq2 user=app password=qqueue') as conn:
    
    with conn.cursor() as cur:

        with open('schema_postgres.sql') as f:
            cur.execute(f.read())
        
        rows = [
            ('A Tale of Two Cities', 'Charles Dickens', 489, 'A classic.'),
            ('Anna Karenina', 'Leo Tolstoy', 864, 'Another classic.'),
        ]

        for row in rows:
            cur.execute('INSERT INTO books (title, author, pages_num, review) \
                         VALUES (%s, %s, %s, %s)', row)
    
        conn.commit()
