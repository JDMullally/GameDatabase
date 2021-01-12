# Authors: Joseph Mullally, Li Chong Glen Seow and Mark Shomakhov
# Project Code
#
# April 12, 2020

import pymysql
import time
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
'''
If this modules do not work, try to install them using "pip3 install module_name" in the bash or terminal or command prompt
'''

# Global variables
db = 'game_schema'

get_all_games = 'call select_all_games'
insert_game = 'call insert_game_with_publisher'
select_game_name_by_id = 'call select_game_name_by_id'
select_game_id_by_game = 'call select_game_id_by_name'
select_genres_by_game_id = 'call select_genres_by_game_id'
select_publisher_by_game_id = 'call select_publisher_by_game_id'
insert_game_with_publisher = 'select insert_game_with_publisher(%s,%s,%s,%s)'
remove_game_by_id = 'select remove_game_by_id(%s)'
update_game_by_id = 'select update_game_by_id(%s, %s)'
get_all_publishers = 'call get_all_publishers'
get_all_platforms = 'call get_all_platforms'
get_all_genres = 'call get_all_genres'
get_all_platforms_by_game_id = 'call get_all_platforms_by_game_id'
insert_platform = 'select insert_platform(%s)'
add_platform_to_game = 'select add_platform_to_game(%s,%s)'
add_genre_to_game = 'select add_genre_to_game(%s,%s)'
insert_genre = 'select insert_genre(%s)'


def pair_does_not_exist(cur, id, game_id, indicator):
    if indicator == 'genre_game':
        cur.execute(select_genres_by_game_id + '(%s)', game_id)
        for result in cur.fetchall():
            if str(result['genre_id']) == id:
                return False
        return True
    if indicator == 'platform_game':
        cur.execute(get_all_platforms_by_game_id + '(%s)', game_id)
        for result in cur.fetchall():
            if str(result['platform_id']) == id:
                return False
        print('succeed?')
        return True
    else:
        print('wrong input')
        return False


def game_exists(cur, game_id):
    exists = False
    cur.execute(get_all_games)
    for result in cur.fetchall():
        if str(result['game_id']) == game_id:
            exists = True
    return exists


def check_id(cur, id, id_type):
    if id_type == 'game':
        cur.execute(get_all_games)
        for result in cur.fetchall():
            if str(result['game_id']) == id:
                return True
    elif id_type == 'genre':
        cur.execute(get_all_genres)
        for result in cur.fetchall():
            if str(result['genre_id']) == id:
                return True
    elif id_type == 'platform':
        cur.execute(get_all_platforms)
        for result in cur.fetchall():
            if str(result['platform_id']) == id:
                return True
    else:
        print(id_type + ' id does not exist')
        return False


def verify(cur, name, publisher_id):
    cur.execute(get_all_games)
    publisher_exists = False
    for result in cur.fetchall():
        if result['game_name'].lower() == name.lower():
            return False

    if publisher_id == 'None':
        return True

    cur.execute(get_all_publishers)
    for result in cur.fetchall():
        if str(result['publisher_id']) == publisher_id:
            publisher_exists = True

    return publisher_exists


def generalSelect(cur, statement, param, desired):
    if statement == get_all_games:
        cur.execute(statement)
        for result in cur.fetchall():
            print('id: ' + str(result['game_id']) + ' name: ' + result['game_name'])
        time.sleep(1)
        cur.close()
        c = input('Continue? (y/n) ')
        return c
    else:
        cur.execute(statement + '(%s)', param)
        zoot = cur.fetchall()
        if len(zoot) == 0:
            print('Looks like nothing is here!')
            cur.close()
            c = input('Continue? (y/n) ')
            return c
        else:
            for result in zoot:
                print(result[desired])
            time.sleep(1)
            cur.close()
            c = input('Continue? (y/n) ')
            return c


def connect(username, password):
    try:
        cnx = pymysql.connect(host='localhost', user=username, password=password,
                              db=db, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    except:
        print("Incorrect Login Info.  Shutting down.")
        return 0

    loop = True
    while loop:
        cur = cnx.cursor()
        # cur.execute(getAll)
        print("Welcome to our game list!")
        print("1. Show all id and names of games")
        print("2. Find game name by ID")
        print("3. Find game ID by name")
        print("4. Find publisher by game ID")
        print("5. Find genres by game ID")
        print("6. Insert game into database")
        print("7. Update a game's name by ID")
        print("8. Remove a game by game ID")
        print("9. Show all genres")
        print("10. Show all platforms")
        print("11. Show a game's platforms by ID")
        print("12. Add a genre to a game")
        print("13. Add a platform to a game")
        print("14. Statistics (Sales per Year)")
        print("0. Exit")
        menu_item = int(input("Type menu item and then 'enter': "))
        if menu_item == 0:
            return 0
        elif menu_item == 1:
            c = generalSelect(cur, get_all_games, None, None)
            if c != 'y':
                break
        elif menu_item == 2:
            game_id = int(input("Type in the id of your desired game's id: "))
            c = generalSelect(cur, select_game_name_by_id, game_id, 'game_name')
            if c != 'y':
                break
        elif menu_item == 3:
            game_name = input("Type in the name of your desired game': ")
            c = generalSelect(cur, select_game_id_by_game, game_name, 'game_id')
            if c != 'y':
                break
        elif menu_item == 4:
            game_id = input("Type in your desired game's id': ")
            c = generalSelect(cur, select_publisher_by_game_id, game_id, 'publisher_name')
            if c != 'y':
                break
        elif menu_item == 5:
            game_id = input("Type in your desired game's id': ")
            c = generalSelect(cur, select_genres_by_game_id, game_id, 'genre_name')
            if c != 'y':
                break
        elif menu_item == 6:
            game_name = input("Enter the name of game you would like to enter: ")
            game_year = input("Enter the year the game was made: ")
            game_sales = input('Enter the game\'s total sales: ')
            game_publisher = input('Enter the game\'s publisher: ')
            v = verify(cur, game_name, game_publisher)
            args = [game_name, game_year, game_sales, game_publisher]
            if v:
                cur.execute(insert_game_with_publisher, args)
                for result in cur.fetchall():
                    print(result)
                cnx.commit()
            else:
                print('Your string was not verified')
            time.sleep(1)
            cur.close()
            c = input('Continue? (y/n) ')
            if c != 'y':
                break
        elif menu_item == 7:
            game_id = input("Enter the id of the game you would like to rename: ")
            game_name = input("Enter the new name: ")
            v = verify(cur, game_name, 'None')
            ge = game_exists(cur, game_id)
            args = [game_id, game_name]
            if v and ge:
                cur.execute(update_game_by_id, args)
                for result in cur.fetchall():
                    print(result)
                cnx.commit()
            else:
                print('Your string was not verified')
            time.sleep(1)
            cur.close()
            c = input('Continue? (y/n) ')
            if c != 'y':
                break
        elif menu_item == 8:
            game_id = input("Enter the id of the game you would like to remove: ")
            ge = game_exists(cur, game_id)
            if ge:
                cur.execute(remove_game_by_id, game_id)
                for result in cur.fetchall():
                    print(result)
                cnx.commit()
            else:
                print('Your id doesn\'t seem to exist')
            time.sleep(1)
            cur.close()
            c = input('Continue? (y/n) ')
            if c != 'y':
                break
        elif menu_item == 9:
            cur.execute(get_all_genres)
            for result in cur.fetchall():
                print('id: ' + str(result['genre_id']) + ' name: ' + result['genre_name'])
            time.sleep(1)
            cur.close()
            c = input('Continue? (y/n) ')
            if c != 'y':
                break
        elif menu_item == 10:
            cur.execute(get_all_platforms)
            for result in cur.fetchall():
                print('id: ' + str(result['platform_id']) + ' name: ' + result['platform_name'])
            time.sleep(1)
            cur.close()
            c = input('Continue? (y/n) ')
            if c != 'y':
                break
        elif menu_item == 11:
            game_id = input("Enter the id of the game you would like to know the platform of: ")
            c = generalSelect(cur, get_all_platforms_by_game_id, game_id, 'platform_name')
            if c != 'y':
                break
        elif menu_item == 12:
            genre_id = input('Enter the genre id you would like to connect a game to: ')
            game_id = input('Enter the id of the game you would like to connect')
            genre_valid = check_id(cur, genre_id, 'genre')
            game_valid = check_id(cur, game_id, 'game')
            if game_valid and genre_valid:
                args = [genre_id, game_id]
                if pair_does_not_exist(cur, genre_id, game_id, 'genre_game'):
                    cur.execute(add_genre_to_game, args)
                    for result in cur.fetchall():
                        print(result)
                    cnx.commit()
                    time.sleep(1)
                else:
                    print('Game already has that genre')
            else:
                print('Input invalid')
            cur.close()
            c = input('Continue? (y/n) ')
            if c != 'y':
                break
        elif menu_item == 13:
            platform_id = input('Enter the platform id you would like to connect a game to: ')
            game_id = input('Enter the id of the game you would like to connect')
            platform_valid = check_id(cur, platform_id, 'platform')
            game_valid = check_id(cur, game_id, 'game')
            if game_valid and platform_valid:
                args = [platform_id, game_id]
                if pair_does_not_exist(cur, platform_id, game_id, 'platform_game'):
                    cur.execute(add_platform_to_game, args)
                    for result in cur.fetchall():
                        print(result)
                    cnx.commit()
                    time.sleep(1)
                else:
                    print('Game already has that platform')
            else:
                print('Input invalid')
            cur.close()
            c = input('Continue? (y/n) ')
            if c != 'y':
                break
        elif menu_item == 14:
            stmt_select = "SELECT year, SUM(global_sales) AS sales FROM game GROUP BY year ORDER BY year"
            cur.execute(stmt_select)
            df0 = cur.fetchall()
            df = pd.DataFrame(df0)
            cur.close()
            df['sales'] = df['sales'].astype(float)
            plt.bar(df['year'], df['sales'], align='center', alpha=0.5)
            #plt.xticks(df['year'], objects)
            plt.ylabel('Total Sales (millions of dollars)')
            plt.title('Total Sales for All Games for each Year of Production')
            plt.show()
            c = input('Continue? (y/n) ')
            if c != 'y':
                break
        else:
            print('Aw shucks! That wasn\'t and option!')
            time.sleep(.600)
            print('Try again!')
            time.sleep(.300)

    print("Connection closed.  See ya later alligator!")


def main():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        connect(username, password)


main()
