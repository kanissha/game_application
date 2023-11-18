from flask import Flask, jsonify, request,render_template
import psycopg2
import os

app = Flask(__name__)

conn = psycopg2.connect(
        host="localhost",
        database="game_db",
        user="k.palanisamy",
        password="password")
cur = conn.cursor()

#cur.execute('CREATE TABLE reserve1(id serial PRIMARY KEY,roomno varchar (10) ,guestname varchar (40) ,checkin varchar (40),checkout varchar (40))')
# cur.execute('INSERT INTO reserve1 (roomno,guestname,checkin,checkout)'
#             'VALUES (%s, %s, %s, %s)',
#             ('room 101',
#              'kani',
#              '12th march',
#              '14th march')
#             )
# cur.execute('CREATE TABLE games ('
#                'id serial PRIMARY KEY,'
#                'title VARCHAR(255) NOT NULL,'
#                'genre VARCHAR(255) NOT NULL,'
#                'year INT NOT NULL,'
#                'is_favorite BOOLEAN NOT NULL)'
#                )
cur.execute('INSERT INTO games (title,genre,year,is_favorite)'
            'VALUES (%s, %s, %s, %s)',
            (
             'title1',
             'genre1',
             '2002',
             'true',
             )
            )

@app.route('/')
def landing_page():
    cur.execute('SELECT COUNT(*) FROM games')
    count = cur.fetchone()[0]
    if count == 0:
        return render_template('landing_page.html', message='No games saved', show_button=True)
    else:
        return render_template('landing_page.html', message='', show_button=False)

@app.route('/games', methods=['GET'])
def get_games():
    cur.execute('SELECT * FROM games')
    result = cur.fetchall()
    games = [{'id': row[0], 'title': row[1], 'genre': row[2], 'year': row[3], 'is_favorite': row[4]} for row in result]
    return jsonify(games)

@app.route('/games/search', methods=['GET'])
def search_games():
    # Sample search query: /games/search?genre=Action&year=2020
    genre = request.args.get('genre')
    year = request.args.get('year')

    query = 'SELECT * FROM games WHERE'
    conditions = []

    if genre:
        conditions.append(f"genre = '{genre}'")
    if year:
        conditions.append(f"year = {year}")

    if conditions:
        query += ' AND '.join(conditions)

    cur.execute(query)
    result = cur.fetchall()
    games = [{'id': row[0], 'title': row[1], 'genre': row[2], 'year': row[3], 'is_favorite': row[4]} for row in result]
    return jsonify(games)

@app.route('/games/favorite/<int:game_id>', methods=['PUT'])
def mark_as_favorite(game_id):
    cur.execute('UPDATE games SET is_favorite = NOT is_favorite WHERE id = %s', (game_id,))
    conn.commit()
    return jsonify({'message': 'Game marked as favorite successfully'})



# conn.commit()
# cur.close()
# conn.close()

if __name__ == '_main_':
    app.run(debug=True)