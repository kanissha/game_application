Problem Statement #6:Game List application using Flask and Postgrtesql[Backend] 

Initial installation steps:

1)Initially a flask application is created using the following commands:
python3 -m venv env
source env/bin/activate
2)pip install flask
3)Add the required packages in requirements.txt 
 pip install -r requirements.txt
 to update to latest version-pip freeze>requirements.txt
4)Give necessary functions in app.py along with debug =True for the app to run in deplyment server
5)flask run
The application will now be running in localhost: http://127.0.0.1:5000/


Now we have create the database and connect it to the application via psycopg2.connect using the foloowing credentials
1)host
2)databse
3)user 
4)password
These details can be collected from the postgres connection that we have created
![image](https://github.com/kanissha/game_application/assets/79655057/f79c6155-a428-4282-94e2-25d93f95b06b)

Once database is connected have to create table and give the necessary insert queries

Following are the databases created
1)users:


cur.execute('CREATE TABLE users ('
              'uid serial PRIMARY KEY,'
              'username VARCHAR(100) UNIQUE  NOT NULL,'
              'email VARCHAR(100)  UNIQUE NOT NULL, '
              'password VARCHAR(100)  UNIQUE NOT NULL)
              )

2)games:

cur.execute('CREATE TABLE games ('
              'id serial PRIMARY KEY,'
              'title VARCHAR(255) NOT NULL,'
              'genre VARCHAR(255) NOT NULL,'
              'year INT NOT NULL,'
              'is_favourite BOOLEAN NOT NULL,'
              'description VARCHAR(255) NOT NULL,'
              'language VARCHAR(255) NOT NULL,'
              'platform VARCHAR(255) NOT NULL,'
              'playtime INT NOT NULL,'
              'virtual_currency_balance INT NOT NULL,'
              'virtual_currency_earned INT NOT NULL)'
              )


3)feedback

cur.execute('CREATE TABLE feedback ('
              'rid serial PRIMARY KEY,'
              'id INT REFERENCES games(id),'
              'uid INT REFERENCES users(uid),'
              'username VARCHAR(100) NOT NULL,'
              'rating INT NOT NULL,'
              'comment TEXT,'
              'created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'
              )

Users table is to handle the details of the users who login to add/see the games listed in the game list application
Games table is to handle the information of the games where there is an interesting column named virtual_currency_balance which tracks the virtual currency  of game 
Feedback table is to handle all the comments given by the user to the games


Features implemented:

1)Initially users have to register to use the application
They can register to the application by giving their username,email and password
To implement this functionality a post api is written
![image](https://github.com/kanissha/game_application/assets/79655057/84e8617e-e718-44ef-87b2-f45998ed0b45)

2)Login
The registered users are only allowed to login
To implement this functionality a post api is written
username and password are validated and are allowed to login
![image](https://github.com/kanissha/game_application/assets/79655057/d363ad0d-25a0-42ae-a1f3-fc15b785019f)
Validations:
password validation
![image](https://github.com/kanissha/game_application/assets/79655057/9091a30e-bab2-4703-9f9a-d37d9bffe3a6)
username validation
![image](https://github.com/kanissha/game_application/assets/79655057/ec5e5b66-b129-4d78-99fb-d3be67621114)



3)Landing page where when there is no games Using the add button games can be added
when games are there it lists the Games 
Add game button:Post api
![image](https://github.com/kanissha/game_application/assets/79655057/d9b75283-d423-4712-b02a-99e263319b49)

4)Listing the Games 
Get api:
![image](https://github.com/kanissha/game_application/assets/79655057/6f21afc5-65ea-4199-8085-d429d680f12b)
Display games api:
Display the games in the application on the main page
![image](https://github.com/kanissha/game_application/assets/79655057/3cb180d8-7351-45e5-980f-cf07be9a7a96)

5)Search  game feature
Implemented a search feature for games based on different criteria such as
genre, year, title, etc...

Title search:
![image](https://github.com/kanissha/game_application/assets/79655057/551cd12c-4a87-4f91-9444-bb4570917958)

Year search:
![image](https://github.com/kanissha/game_application/assets/79655057/0eb9ee43-c0cc-4db2-872e-ec9bf98e960f)

genre search:
![image](https://github.com/kanissha/game_application/assets/79655057/fbe875d1-b17a-426b-9e1e-32ac35d731e4)

Platform search:
![image](https://github.com/kanissha/game_application/assets/79655057/39a001c9-6505-4adb-ad7a-f28927202a98)

Playtime search:
![image](https://github.com/kanissha/game_application/assets/79655057/7331d8aa-4e99-4d82-b81a-45cb6fd78b71)

Language search:
![image](https://github.com/kanissha/game_application/assets/79655057/c6ba0375-83f6-4c75-84fe-804f81ab9e93)

Description Search:
![image](https://github.com/kanissha/game_application/assets/79655057/59722203-1e57-48a2-a2c1-6ed3644396d8)

6)Favourite the game:
Intially is_favorite flag is assigned as false-unfavourite
is_favourite is a boolean flag
When PUT api is called is changed to true indicating that it is favourting

![image](https://github.com/kanissha/game_application/assets/79655057/117ab193-1759-4b71-a11a-b3708e1a1739)

7)Add Feedback to the game which gets tracked in feedback table
This is achieved via a POST api

![image](https://github.com/kanissha/game_application/assets/79655057/035a23a3-fe57-4f45-9010-19954c4cc544)
Users by entering their name relevant rating and comment to the game can be added

8)Tracking virtual currency balance and virtual currency earned by cumulating it along with the earned points[determined via playtime]

Playtime is the value which is entered in hours
For 1 hour the value is increased 5 times and by this earned points are calculated
finally this earned points are updated to that game's balance and  currency earned via a update sql command
SQL command used in the update api:
UPDATE games SET virtual_currency_balance = virtual_currency_balance + %s, virtual_currency_earned = virtual_currency_earned + %s WHERE id = %s RETURNING virtual_currency_balance, virtual_currency_earned

![image](https://github.com/kanissha/game_application/assets/79655057/f13a65e7-44e0-4779-8750-c30b74b49956)


9)Delete game functionality implemented via delete api
When the users find that the game is not necessary they can delete

![image](https://github.com/kanissha/game_application/assets/79655057/3605731d-c089-42b9-84c9-e7c6420d8224)
