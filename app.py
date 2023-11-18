from flask import Flask, jsonify, request,render_template,session
import psycopg2
from psycopg2 import sql
app = Flask(__name__)
app.secret_key = 'kanisshhhhhhhhhhh'

conn = psycopg2.connect(
        host="localhost",
        database="game_db",
        user="k.palanisamy",
        password="password")
cur = conn.cursor()

# SQL commands for creating table and inserting queries 
# cur.execute('CREATE TABLE users ('
#                'uid serial PRIMARY KEY,'
#                'username VARCHAR(100) UNIQUE  NOT NULL,'
#                'email VARCHAR(100)  UNIQUE NOT NULL)'
#                )
# cur.execute('CREATE TABLE games ('
#                'id serial PRIMARY KEY,'
#                'title VARCHAR(255) NOT NULL,'
#                'genre VARCHAR(255) NOT NULL,'
#                'year INT NOT NULL,'
#                'is_favourite BOOLEAN NOT NULL,'
#                'description VARCHAR(255) NOT NULL,'
#                'language VARCHAR(255) NOT NULL,'
#                'platform VARCHAR(255) NOT NULL,'
#                'playtime INT NOT NULL,'
#                'virtual_currency_balance INT NOT NULL,'
#                'virtual_currency_earned INT NOT NULL)' 
#                )

# cur.execute('CREATE TABLE feedback ('
#                'rid serial PRIMARY KEY,'
#                'id INT REFERENCES games(id),'
#                'uid INT REFERENCES users(uid),'
#                'username VARCHAR(100) NOT NULL,'
#                'rating INT NOT NULL,'
#                'comment TEXT,'
#                'created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'
#                )
# cur.execute('INSERT INTO games (title,genre,year,is_favourite,description,language,platform,playtime,virtual_currency_balance,virtual_currency_earned)'
#             'VALUES (%s, %s, %s, %s,%s ,%s,%s,%s,%s,%s)',
#             (
#              'witcher3',
#              'Stimulation',
#              '2009',
#              'false',
#              'farm game',
#              'English',
#              'Playstation',
#              '8',
#              '150',
#              '50'
#              )
#             )
# cur.execute('INSERT INTO users (username,email)'
#             'VALUES (%s, %s)',
#             (
#              'Kanissha',
#              'kani@gmail.com',
#              )
#             )

# cur.execute('INSERT INTO feedback (id,uid,username,rating,comment,created_at)'
#             'VALUES (%s, %s,%s,%s,%s,%s)',
#             (
#              '25',
#              '3',
#              'Kanissha',
#              '7',
#              'Good',
#              '2023-11-18 03:22:49.968'
#              )
#             )

@app.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        cur.execute('SELECT uid FROM users WHERE username = %s OR email = %s', (username, email))
        existing_user = cur.fetchone()

        if existing_user:
            return jsonify({'error': 'Username or email already exists'})

        cur.execute('INSERT INTO users (username, email) VALUES (%s, %s) RETURNING uid', (username, email))
        uid = cur.fetchone()[0]
        conn.commit()

        return jsonify({'message': 'User registered successfully', 'user_id': uid})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')

        cur.execute('SELECT uid FROM users WHERE username = %s', (username,))
        uid = cur.fetchone()

        if not uid:
            return jsonify({'error': 'Invalid username'})

        session['uid'] = uid
        return jsonify({'message': 'Login successful', 'user_id': uid})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/')
def landing_page():
    cur.execute('SELECT * FROM games')
    results=cur.fetchall()
    games = []
    print(results)
    for result in results:
        game_b = {
           
            "title": result[0],
            "genre": result[1],
            "year": result[2],
            "is_favourite": result[3], 
            "description":result[4],
            "language":result[5],
            "platform":result[6],
            "playtime":result[7],
            "virtual_currency_balance":result[8],
            "virtual_currency_earned":result[9]
        }
        games.append(game_b)
    if not games:
        return render_template('landing_page.html', message='No games saved', show_button=True)
    else:
        return render_template('landing_page.html', games=games, show_button=False)


@app.route('/games', methods=['GET'])
def get_games():
    cur.execute('SELECT * FROM games')
    result = cur.fetchall()
    games = [{'id': row[0], 'title': row[1], 'genre': row[2], 'year': row[3], 'is_favourite': row[4],'decription': row[5],'language': row[6],'platform': row[7],'playtime': row[8],'virtual_currency_balance':row[9],'virtual_currency_earned':row[10]} for row in result]
    return jsonify(games)



@app.route('/games/search', methods=['GET'])
def search_games():
    genre = request.args.get('genre')
    year = request.args.get('year')
    title = request.args.get('title')
    description = request.args.get('description')
    language = request.args.get('language')
    platform = request.args.get('platform')
    playtime = request.args.get('playtime')
    virtual_currency_balance= request.args.get('virtual_currency_balance')
    virtual_currency_earned=request.args.get('virtual_currency_earned')

    # cur.execute('SELECT * FROM games WHERE genre = %s AND year = %s', (genre, year))
    cur.execute('SELECT * FROM games WHERE genre = %s OR year = %s OR title ILIKE%s  OR description = %s  OR language = %s  OR platform = %s  OR playtime = %s  OR virtual_currency_balance = %s  OR virtual_currency_earned = %s', (genre, year,f"%{title}%",description,language,platform,playtime,virtual_currency_balance,virtual_currency_earned))
    result = cur.fetchall()
    games = []
    for row in result:
        game = {
            'id': row[0],
            'title': row[1],
            'genre': row[2],
            'year': row[3],
            'is_favourite': row[4],
            'description': row[5],
            'language': row[6],
            'platform': row[7],
            'playtime': row[8],
            'virtual_currency_balance':row[9],
            'virtual_currency_earned':row[10]
        }
        games.append(game)

    return jsonify(games)
  
    

@app.route('/add_game', methods=['POST'])
def add_game():

    data = request.get_json()   
    cur.execute("INSERT INTO games (title,genre,year,is_favourite,description,language,platform,playtime,virtual_currency_balance,virtual_currency_earned) VALUES (%s, %s, %s, %s, %s,%s ,%s,%s,%s,%s)",
                   (data['title'], data['genre'], data['year'],data['is_favourite'],data['description'],data['language'],data['platform'],data['playtime'],data['virtual_currency_balance'],data['virtual_currency_earned']))

    conn.commit()
    return jsonify({'message': 'Game added  successfully'})
    
    

@app.route('/games/favourite/<int:id>', methods=['PUT'])
def mark_as_favorite(id):
    try:
        # Check if the game_id exists
        cur.execute('SELECT id, is_favourite FROM games WHERE id = %s', (id,))
        result = cur.fetchone()

        if not result:
            return jsonify({'message': 'Game not found'}), 404

        game_id, is_favourite = result

        is_favourite = not is_favourite

        cur.execute('UPDATE games SET is_favourite = %s WHERE id = %s', (is_favourite, id))
        conn.commit()

        message = 'Game marked as favorite' if is_favourite else 'Game marked as un favorite'
        result = {'game_id': game_id, 'is_favourite': is_favourite, 'message': message}
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/games/addfeedback/<int:id>', methods=['POST'])
def add_review_to_game(id):
    try:
        data = request.get_json()
        username = data.get('username')
        rating = data.get('rating')
        comment = data.get('comment')

        uid = session.get('uid')

        if not uid:
            return jsonify({'error': 'User not logged in'})

        cur.execute('INSERT INTO feedback (id, uid, username, rating, comment) VALUES (%s, %s, %s, %s, %s)',
                    (id, uid, username, rating, comment))
        conn.commit()

        return jsonify({'message': 'Comment added to the game successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/games/earn_virtual_currency/<int:id>', methods=['PUT'])
def earn_virtual_currency(id):
  
        data = request.get_json()
        virtual_currency_balance = data.get('virtual_currency_balance')
        virtual_currency_earned = data.get('virtual_currency_earned')
        playtime = data.get('playtime')
        playtime=int(playtime)
        earned_amount = playtime * 5
        virtual_currency_balance=int(virtual_currency_balance)
        virtual_currency_earned=int(virtual_currency_earned)
        
        cur.execute('UPDATE games SET virtual_currency_balance = virtual_currency_balance + %s, virtual_currency_earned = virtual_currency_earned + %s WHERE id = %s RETURNING virtual_currency_balance, virtual_currency_earned',
         (earned_amount, earned_amount, id))

       
        updated_values = cur.fetchone()
        updated_virtual_currency_balance, updated_virtual_currency_earned = updated_values[0], updated_values[1]

        conn.commit()
        return jsonify({'virtual_currency_balance': updated_virtual_currency_balance, 'virtual_currency_earned': updated_virtual_currency_earned})
       

@app.route('/deletegame/<int:id>', methods=['DELETE'])
def delete_game(id):
   
    cur.execute("DELETE FROM games WHERE id = %s", (id,))
    conn.commit()
    return jsonify({'message': 'Game deleted successfully'})

# conn.commit()
# cur.close()
# conn.close()

# if __name__ == '_main_':
#     app.run(debug=True)