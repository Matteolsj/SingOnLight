import sqlite3
from .settings import DATABASE_PATH

def initialize_database():
    """Create database tables and seed them when they do not exist."""
    connect = sqlite3.connect(DATABASE_PATH)
    connect.execute('CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY,value INTEGER);')
    connect.execute('CREATE TABLE IF NOT EXISTS story (key INTEGER PRIMARY KEY,rhythm TEXT,interval DOUBLE);')
    connect.execute('CREATE TABLE IF NOT EXISTS scores (score_range TEXT PRIMARY KEY, count INTEGER);')
    connect.execute('CREATE TABLE IF NOT EXISTS rhythm (id INTEGER PRIMARY KEY AUTOINCREMENT, rhythm CHAR(120));')
    data = connect.execute('SELECT * FROM settings;').fetchall()
    if len(data) == 0:
        connect.execute('INSERT INTO settings (key,value) VALUES (?,?);', ("threshold",50))
        connect.execute('INSERT INTO settings (key,value) VALUES (?,?);', ("interval_duration", 1))
        connect.execute('INSERT INTO settings (key,value) VALUES (?,?);', ("game_length", 25))
        connect.execute('INSERT INTO settings (key,value) VALUES (?,?);', ("win_streak", 0))
    if len(connect.execute("SELECT * FROM rhythm;").fetchall()) == 0:
        connect.execute('INSERT INTO rhythm (rhythm) VALUES (?);', ("",))

    if len(connect.execute("SELECT * FROM story;").fetchall()) == 0:
        # Easy levels: learn the game basics. Win condition: 50%.
        connect.execute('INSERT INTO story (key,rhythm,interval) VALUES (?,?,?);', (1, "11010",1.0)) # rhythm story 1
        connect.execute('INSERT INTO story (key,rhythm,interval) VALUES (?,?,?);', (2, "11101",0.6)) # rhythm story 2
        connect.execute('INSERT INTO story (key,rhythm,interval) VALUES (?,?,?);', (3, "0110010101",0.8)) # rhythm story 3
        connect.execute('INSERT INTO story (key,rhythm,interval) VALUES (?,?,?);', (4, "11101011",0.8)) # rhythm story 4
        connect.execute('INSERT INTO story (key,rhythm,interval) VALUES (?,?,?);', (5, "101001011",0.7)) # rhythm story 5

        # Intermediate levels: handle rhythm changes. Win condition: 60%.
        connect.execute('INSERT INTO story (key,rhythm,interval) VALUES (?,?,?);', (6, "011110001011011111",0.6))
        # rhythm story 6 [0.6s,2.4b,1.8s,0.6b,0.6s,1.2b,0.6s,3.0b]
        connect.execute('INSERT INTO story (key,rhythm,interval) VALUES (?,?,?);', (7, "101010101111011101001",0.5))
        # rhythm story 7 [0.5b,0.5s,0.5b,0.5s,0.5b,0.5s,0.5b,0.5s,2.0b,0.5s,1.5b,0.5s,0.5b,1.0s,0.5b]
        connect.execute('INSERT INTO story (key,rhythm,interval) VALUES (?,?,?);', (8, "10111101010101001010100011111101",0.4))
        # rhythm story 8 [0.4b,0.4s,1.6b,0.4s,0.4b,0.4s,0.4b,0.4s,0.4b,0.4s,0.4b,0.8s,0.4b,0.4s,0.4b,0.4s,0.4b,1.2s,2.4b,0.4s,0.4b]
        connect.execute('INSERT INTO story (key,rhythm,interval) VALUES (?,?,?);', (9, "11010110110101101110101101101100100011111",0.3))
        # rhythm story 9 [0.6b,0.3s,0.3b,0.3s,0.6b,0.3s,0.6b,0.3s,0.3b,0.3s,0.6b,0.3s,0.9b,0.3s,0.3b,0.3s,0.6b,0.3s,0.6b,0.3s,0.6b,0.6s,0.3b,0.9s,1.5b]
        connect.execute('INSERT INTO story (key,rhythm,interval) VALUES (?,?,?);', (10, "1011011011110010010011000000101111111110110101",0.3))
        # rhythm story 10 [0.3b,0.3s,0.6b,0.3s,0.6b,0.3s,1.2b,0.6s,0.3b,0.6s,0.3b,0.6s,0.6b,1.8s,0.3b,0.3s,2.7b,0.3s,0.6b,0.3s,0.3b,0.3s,0.3b]

        # Hard levels: handle changes in interval duration. Win condition: 60%.
        connect.execute('INSERT INTO story (key,rhythm,interval) VALUES (?,?,?);', (11, "1111100001111111000000000011110000111111111111111111111111111111000111001100111001111001100011",0.1))
        # rhythm story 11 [0.5b,0.4s,0.7b,1.0s,0.4b,0.4s,3.0b,0.3s,0.3b,0.2s,0.2b,0.2s,0.3b,0.2s,0.4b,0.2s,0.2b,0.3s,0.2b]
        connect.execute('INSERT INTO story (key,rhythm,interval) VALUES (?,?,?);', (12, "111000011111000000111111100000000000000000000111111100011100111100000111000011000001111100111000110011100111",0.1))
        # rhythm story 12 [0.3b,0.4s,0.5b,0.6s,0.7b,2.0s,0.7b,0.3s,0.3b,0.2s,0.4b,0.5s,0.3b,0.4s,0.2b,0.5s,0.5b,0.2s,0.3b,0.3s,0.2b,0.2s,0.3b,0.2s,0.3b]
        connect.execute('INSERT INTO story (key,rhythm,interval) VALUES (?,?,?);', (13, "11111111110000111000001111001110011110011100000111100011100110000011100000110011001100011100001100111100000000001111110011100000111001110001111111100001110011000111111001110001111110",0.1))
        # rhythm story 13 [1.0b,0.4s,0.3b,0.5s,0.4b,0.2s,0.3b,0.2s,0.4b,0.2s,0.3b,0.5s,0.4b,0.3s,0.3b,0.2s,0.2b,0.5s,0.3b,0.5s,0.2b,0.2s,0.2b,0.2s,0.2b,0.3s,0.3b,0.4s,0.2b,0.2s,0.4b,1.0s,0.6b,0.2s,0.3b,0.5s,0.3b,0.2s,0.3b,0.3s,0.8b,0.4s,0.2b,0.2s,0.2b,0.3s,0.2b,0.2s,0.2b,0.3s,0.5b,0.1s]
        connect.execute('INSERT INTO story (key,rhythm,interval) VALUES (?,?,?);', (14, "11100110011000110011111111110011110001110011111000001110011100111001110000000000000001111100011001110000000110111100111000000000011110000",0.1))
        # rhythm story 14 [0.3b,0.2s,0.2b,0.2s,0.2b,0.3s,0.2b,0.2s,1.0b,0.2s,0.4b,0.3s,0.3b,0.2s,0.5b,0.5s,0.3b,0.2s,0.3b,0.2s,0.3b,0.2s,0.3b,1.5s,0.5b,0.3s,0.2b,0.2s,0.3b,0.7s,0.2b,0.1s,0.4b,0.2s,0.3b,1.0s,0.4b,0.4s]
        connect.execute('INSERT INTO story (key,rhythm,interval) VALUES (?,?,?);', (15, "1111111111110000000000000001100110111110110110000111111100111000111101110000001101101100011111000000110011100000011011111001110011001111000110011100111",0.1))
        # rhythm story 15 [1.2b,1.5s,0.2b,0.2s,0.2b,0.1s,0.5b,0.1s,0.2b,0.1s,0.2b,0.4s,0.7b,0.2s,0.3b,0.3s,0.4b,0.1s,0.3b,0.6s,0.2b,0.1s,0.2b,0.1s,0.2b,0.3s,0.5b,0.6s,0.2b,0.2s,0.3b,0.6s,0.2b,0.1s,0.5b,0.2s,0.3b,0.2s,0.2b,0.2s,0.4b,0.3s,0.2b,0.2s,0.3b,0.2s,0.3b]

        # Impossible mode: good luck. Win condition: 70%.
        connect.execute('INSERT INTO story (key,rhythm,interval) VALUES (?,?,?);', (16, "11111110111011000011110111000010000010000001000010011010101100101010110001101000101011011001001010111101011000110111",0.1))
        # rhythm story 16 [0.7b,0.1s,0.3b,0.1s,0.2b,0.4s,0.4b,0.1s,0.3b,0.4s,0.1b,0.5s,0.1b,0.6s,0.1b,0.4s,0.1b,0.2s,0.2b,0.1s,0.1b,0.1s,0.1b,0.1s,0.2b,0.2s,0.1b,0.1s,0.1b,0.1s,0.1b,0.1s,0.2b,0.3s,0.2b,0.1s,0.1b,0.3s,0.1b,0.1s,0.1b,0.1s,0.2b,0.1s,0.2b,0.2s,0.1b,0.2s,0.1b,0.1s,0.1b,0.1s,0.4b,0.1s,0.1b,0.1s,0.2b,0.3s,0.2b,0.1s,0.3b]
        connect.execute('INSERT INTO story (key,rhythm,interval) VALUES (?,?,?);', (17, "1010100101000100100001110010010111110011111110011111110011111110010101001100010011100010011000111110100011111000111111011111001111110111110011111011111111000",0.1))
        # rhythm story 17 [1.2b,0.2s,0.1b,0.2s,0.1b,0.1s,0.5b,0.2s,0.7b,0.2s,0.7b,0.2s,0.7b,0.2s,0.1b,0.1s,0.1b,0.1s,0.1b,0.2s,0.2b,0.3s,0.1b,0.2s,0.3b,0.3s,0.1b,0.2s,0.2b,0.3s,0.5b,0.1s,0.1b,0.3s,0.5b,0.3s,0.6b,0.1s,0.5b,0.2s,0.6b,0.1s,0.5b,0.2s,0.5b,0.1s,0.8b,0.3s]
        connect.execute('INSERT INTO story (key,rhythm,interval) VALUES (?,?,?);', (18, "110100010101000100110001110010011001000111000111010111000100111001011111000111100011111000111000100100001000100010101010101010101010101010001100100110000",0.1))
        # rhythm story 18 [0.2b,0.1s,0.1b,0.3s,0.1b,0.1s,0.1b,0.1s,0.1b,0.3s,0.1b,0.2s,0.2b,0.3s,0.3b,0.2s,0.1b,0.2s,0.2b,0.2s,0.1b,0.3s,0.3b,0.3s,0.3b,0.1s,0.1b,0.1s,0.3b,0.3s,0.1b,0.2s,0.3b,0.2s,0.1b,0.1s,0.5b,0.3s,0.4b,0.3s,0.5b,0.3s,0.3b,0.3s,0.1b,0.2s,0.1b,0.4s,0.1b,0.3s,0.1b,0.3s,0.1b,0.1s,0.1b,0.1s,0.1b,0.1s,0.1b,0.1s,0.1b,0.1s,0.1b,0.1s,0.1b,0.1s,0.1b,0.1s,0.1b,0.1s,0.1b,0.1s,0.1b,0.1s,0.1b,0.1s,0.1b,0.3s,0.2b,0.2s,0.1b,0.2s,0.2b,0.4s]
        connect.execute('INSERT INTO story (key,rhythm,interval) VALUES (?,?,?);', (19, "01101101101111100111001100111000110000011001010101010101010110110111001001111100111100000001110011000110011000011001110011000011111101101110000010101001111010011000000011100110100110010000",0.1))
        # rhythm story 19 [0.1s,0.2b,0.1s,0.2b,0.1s,0.2b,0.1s,0.5b,0.2s,0.3b,0.2s,0.2b,0.2s,0.3b,0.3s,0.2b,0.5s,0.2b,0.2s,0.1b,0.1s,0.1b,0.1s,0.1b,0.1s,0.1b,0.1s,0.1b,0.1s,0.1b,0.1s,0.1b,0.1s,0.1b,0.1s,0.2b,0.1s,0.2b,0.1s,0.3b,0.2s,0.1b,0.2s,0.5b,0.2s,0.4b,0.7s,0.3b,0.2s,0.2b,0.3s,0.2b,0.2s,0.2b,0.4s,0.2b,0.2s,0.3b,0.2s,0.2b,0.4s,0.6b,0.1s,0.2b,0.1s,0.3b,0.5s,0.1b,0.1s,0.1b,0.1s,0.1b,0.2s,0.4b,0.1s,0.1b,0.2s,0.2b,0.7s,0.3b,0.2s,0.2b,0.1s,0.1b,0.2s,0.2b,0.2s,0.1b,0.4s]
        connect.execute('INSERT INTO story (key,rhythm,interval) VALUES (?,?,?);', (20, "011010111011101011110011111101101110110101010101010101000001100111110110011101101111100111111111111111111111111111100000000000000000011111000011111110000000111110000000000000000110011001110110011110011011100000110011101100111011011011011000010101100111100101011100111001010100101100101010010100101101100101101",0.1))
        # rhythm story 20 [0.1s,0.2b,0.1s,0.1b,0.1s,0.3b,0.1s,0.3b,0.1s,0.1b,0.1s,0.4b,0.2s,0.6b,0.1s,0.2b,0.1s,0.3b,0.1s,0.2b,0.1s,0.1b,0.1s,0.1b,0.1s,0.1b,0.1s,0.1b,0.1s,0.1b,0.1s,0.1b,0.1s,0.1b,0.1s,0.1b,0.5s,0.2b,0.2s,0.5b,0.1s,0.2b,0.2s,0.3b,0.1s,0.2b,0.1s,0.5b,0.2s,2.8b,1.8s,0.5b,0.4s,0.7b,0.7s,0.5b,1.6s,0.2b,0.2s,0.2b,0.2s,0.3b,0.1s,0.2b,0.2s,0.4b,0.2s,0.2b,0.1s,0.3b,0.5s,0.2b,0.2s,0.3b,0.1s,0.2b,0.2s,0.3b,0.1s,0.2b,0.1s,0.2b,0.1s,0.2b,0.1s,0.2b,0.4s,0.1b,0.1s,0.1b,0.1s,0.2b,0.2s,0.4b,0.2s,0.1b,0.1s,0.1b,0.1s,0.3b,0.2s,0.3b,0.2s,0.1b,0.1s,0.1b,0.1s,0.1b,0.2s,0.1b,0.1s,0.2b,0.2s,0.1b,0.1s,0.1b,0.1s,0.1b,0.2s,0.1b,0.1s,0.1b,0.2s,0.1b,0.1s,0.2b,0.1s,0.2b,0.2s,0.1b,0.1s,0.2b,0.1s,0.1b]
        
    stats = connect.execute('SELECT * FROM scores;')
    data_scores = stats.fetchall()
    if len(data_scores) == 0:
        for i in range(0,101,10):
            connect.execute('INSERT INTO scores (score_range, count) VALUES (?,?);', (str(i),0)) # Default score count.

    connect.commit()
    connect.close()