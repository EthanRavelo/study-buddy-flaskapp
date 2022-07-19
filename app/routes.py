# Authors: CS For Insight (Summer19 - JG)

try:
    from flask import Flask, session, jsonify, render_template, redirect, url_for, request, send_from_directory, flash, Blueprint, url
except:
    print("Not able to import all of the calls needed from the Flask library.")

from pyparsing import match_only_at_col
from app import app
import os

import sqlalchemy
import requests
import json

from flask_socketio import SocketIO, send
from datetime import timedelta
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask_sqlalchemy import SQLAlchemy
from .models import User, Coin, Item, All_Items, currentData, Message, Chat_Room, New_Message
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user, UserMixin
from sqlalchemy import text, update, or_
from config import Config
from flask_socketio import SocketIO, send
import random
import pusher
from sqlalchemy import create_engine, MetaData, Table, Column, Numeric, Integer, VARCHAR
from sqlalchemy.engine import result
import copy

try:
    from PIL import Image
    import PIL.ImageOps
except:
    print("Make sure to pip install Pillow")

app.secret_key = "hello"

usersToMessage = []

adjectives = ["Adorable", "Adventurous", "Alert",
              "Attractive", "Average", "Beautiful", "Blue-Eyed",
              "Blushing", "Bright", "Clean", "Clear", 
              "Cloudy", "Colorful", "Cute", "Dark", 
              "Distinct", "Dull", "Elegant", "Excited", 
              "Fancy", "Glamorous", "Gleaming", "Gorgeous", 
              "Graceful", "Handsome", "Homely", "Light",
              "Long", "Magnificent", "Misty", "Muddy", 
              "Old-fashioned", "Plain", "Poised", "Precious", "Quaint", 
              "Shiny", "Smoggy", "Sparkling", "Spotless","Stormy",
              "Wide-eyed","Beautiful","Brainy","Busy","Careful","Cautious","Clever","Clumsy",
              "Concerned","Crazy","Curious",
              "Famous","Gifted","Helpful","Important","Inquisitive","Outstanding","Powerful","Prickly",
              "Puzzled","Rich","Shy","Sleepy","Super",
              "Talented","Tame","Tough","Uninterested",
              "Wandering","Wild","Amused","Brave",
              "Calm","Charming","Cheerful","Comfortable","Cooperative",
              "Courageous","Delightful","Determined","Eager","Elated",
              "Enchanting","Encouraging","Energetic","Enthusiastic","Excited",
              "Exuberant","Fantastic","Friendly","Funny",
              "Gentle","Glorious","Good","Happy","Healthy","Helpful","Hilarious",
              "Jolly","Joyous","Kind","Lively","Lovely","Lucky","Nice",
              "Perfect","Pleasant","Proud","Relieved","Silly","Smiling",
              "Splendid","Successful","Thankful","Thoughtful","Victorious",
              "Vivacious","Witty","Wonderful","Zealous","Zany", "3-Eyed", "3-Eyed", "3-Eyed", "3-Eyed", "3-Eyed", "3-Eyed"]

animals = ["Aardvark","Albatross","Alligator","Alpaca","Ant","Anteater","Antelope",
           "Ape","Armadillo","Baboon","Badger","Barracuda","Bat","Bear","Beaver",
           "Bee","Bison","Boar","Butterfly","Camel","Caribou","Cat","Caterpillar",
           "Chamois","Cheetah","Chicken","Chimpanzee","Chinchilla",
           "Clam","Cobra","Cod", "Coyote","Crab","Crocodile",
           "Crow","Deer","Dinosaur","Dog","Dolphin","Donkey","Dove",
           "Dragonfly","Duck", "Eagle","Eel","Elephant","Elk",
           "Emu","Falcon","Ferret","Finch","Fish","Flamingo","Fly","Fox","Frog",
           "Fazelle","Gerbil","Giraffe","Gnat","Goat","Goose","Goldfish","Gorilla",
           "Grasshopper","Gull","Hamster","Hare","Hawk",
           "Hedgehog","Heron","Herring","Hippopotamus","Hornet","Horse","Hummingbird",
           "Hyena","Jackal","Jaguar","Jay","Jellyfish","Kangaroo","Koala","kouprey",
           "Lark","Lemur","Leopard","Lion","Llama","Lobster",
           "Lyrebird","Magpie","Manatee","Marten","Meerkat","Mink","Monkey","Moose",
           "Mouse","Mosquito","Mule","Narwhal","Newt","Nightingale","Octopus","Opossum",
           "Ostrich","Otter","Owl","Ox","Oyster","Parrot","Partridge","Pelican",
           "Penguin","Pheasant","Pig","Pigeon","Pony","Porcupine",
           "Rabbit","Raccoon","Rat","Raven","Reindeer","Rhinoceros","Salamander",
           "Salmon","Sardine","Scorpion","Seahorse","Shark","Sheep","Shrew",
           "Shrimp","Skunk","Snail","Snake","Spider","Squid","Squirrel","Stingray",
           "Stinkbug","Stork","Swan","Termite","Tiger","Toad","Trout",
           "Turtle","Vulture","Wallaby","Walrus","Wasp","Weasel","Whale","Wolf",
           "Wolverine","Wombat","Woodpecker","Worm","Wren","Yak","Zebra", "Alien", "Alien", "Alien", "Alien", "Alien", "Alien"]


def username():
    """randomly generate a list of 3 usernames (random adjective + random animal)
       Results: list of 3 usernames (all strings)
    """
    adjective_lst = adjectives
    animal_lst = animals

    choices = []

    adjective_choices = random.sample(adjective_lst, 3)
    animal_choices = random.sample(animal_lst, 3)

    for x in range(3):
        choices.append(str(adjective_choices[x]) + " " + str(animal_choices[x]))
        
    return choices


@app.route('/usernameChoice', methods=['POST', 'GET'])
def usernameChoice():
    lst = username()

    if request.method == "POST":
        return render_template("homescreen.html")

    return render_template('usernameChoice.html', lst=lst)


@app.route('/users')
def users():
    users = User.query.all()
    my_school = current_user.school
    all_users = []
    logged_in_users = []
    school = []

    for user in users:
        all_users.append([user.email, user.school, user.logged_in])

    for user in all_users:
        if user[2] == "True":
            logged_in_users.append(user)
            
    for user in logged_in_users:
        if user[1] == my_school:
            school.append(user)

    return render_template('users.html', user_lst=logged_in_users, persons=User.query.all(), school=school)


@app.route('/usersToFetch')
def usersToFetch():
    currentdata = currentData.query.all()
    datadisplay = []
    users = User.query.all()
    my_school = current_user.school
    all_users = []
    logged_in_users = []
    school = []
    display = []
    dict = {}

    data = currentData.query.filter_by(user_id=current_user.id)
    current_items = []

    # create LoL of the currently active accessories in each spot [avatar, spot1, spot2, etc]
    for item in data:
        current_items.append([item.avatar, item.spot1, item.spot2, item.spot3, item.spot4])

    for user in currentdata:
        datadisplay.append([user.user_id, user.year, user.subject, user.username, user.time, user.messaging, user.avatar, user.spot1, user.spot2, user.spot3, user.spot4])

    for user in users:
        all_users.append([user.email, user.school, user.logged_in, user.id])

    for user in all_users:
        if user[2] == "True":
            logged_in_users.append(user)
            
    for user in logged_in_users:
        if user[1] == my_school:
            school.append(user)

    for user in datadisplay:
        for loggedinuser in school:
            if loggedinuser[3] == user[0]:
                display.append(user)

    for user in display:
        print("user:", user)
        for x in range(6, 11):
            if user[x] == "None" or user[x] == "none" or user[x] == "":
                user[x] = 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/HD_transparent_picture.png/800px-HD_transparent_picture.png'


    print(display)

    display.sort(key = lambda x: x[0])
    
    dict["Users"] = display

    return jsonify(dict)


@app.route('/food')
def food():
    return render_template('food.html')


@app.route('/populate')
def populate():
    """populates database with all the shop items on load
    """
    db.session.query(All_Items).delete()
    db.session.commit()

    # avatars LoL [name, url, price]
    avatars = [
        ['ghost', 'https://uxwing.com/wp-content/themes/uxwing/download/10-brands-and-social-media/snapchat-color.svg', 1500], #new
        ['smiley', 'https://uxwing.com/wp-content/themes/uxwing/download/41-emoji-emoticon/smiley.svg', 300], #new
        ['sadface', 'https://uxwing.com/wp-content/themes/uxwing/download/41-emoji-emoticon/strange.svg', 300], #new
        ['sheep', 'https://uxwing.com/wp-content/themes/uxwing/download/29-animals-and-birds/sheep.svg', 450], #new
        ['panda', 'https://uxwing.com/wp-content/themes/uxwing/download/29-animals-and-birds/panda.svg', 450], #new
        ['shiba', 'https://uxwing.com/wp-content/themes/uxwing/download/10-brands-and-social-media/shiba-inu-shib.svg', 450], #new
        ['dog1', 'https://uxwing.com/wp-content/themes/uxwing/download/29-animals-and-birds/dog-face-color.svg', 450], #new
        ['pig', 'https://uxwing.com/wp-content/themes/uxwing/download/20-food-and-drinks/pork.svg', 450], #new
        ['alienhead', 'https://uxwing.com/wp-content/themes/uxwing/download/10-brands-and-social-media/alienware-laptop-logo.svg', 480], #new
        ['dave', 'https://uxwing.com/wp-content/themes/uxwing/download/40-beauty-fashion/bearded-man.svg', 6000], #new
        ['devil', 'https://uxwing.com/wp-content/themes/uxwing/download/41-emoji-emoticon/evil.svg', 1000], #new
        ['alien', 'https://i.ibb.co/gtzq6Q9/alien-removebg-preview-3.png', 9999], #new
        ['santa', 'https://uxwing.com/wp-content/themes/uxwing/download/22-festival-culture-religion/santa.svg', 5000], #new
        ['elephant', 'https://uxwing.com/wp-content/themes/uxwing/download/10-brands-and-social-media/postgresql.svg', 450], #new
        ['spiderMan', 'https://uxwing.com/wp-content/themes/uxwing/download/28-toys-and-childhood/spiderman.svg', 1500], #new
        ['pacman', 'https://uxwing.com/wp-content/themes/uxwing/download/10-brands-and-social-media/pacman.svg', 1500], #new
        ['birdInCircle', 'https://uxwing.com/wp-content/themes/uxwing/download/10-brands-and-social-media/prestashop.svg', 450], #new
        ['mickey', 'https://uxwing.com/wp-content/themes/uxwing/download/28-toys-and-childhood/mickey-mouse-emoji.svg', 1500], #new
        ['cool', 'https://uxwing.com/wp-content/themes/uxwing/download/41-emoji-emoticon/bright.svg', 300], #new
        ['smiley2', 'https://uxwing.com/wp-content/themes/uxwing/download/10-brands-and-social-media/waze.svg', 150], #new
        ['worried', 'https://uxwing.com/wp-content/themes/uxwing/download/41-emoji-emoticon/confused.svg', 300],
        ['toungeOut', 'https://uxwing.com/wp-content/themes/uxwing/download/41-emoji-emoticon/emoji-tongue.svg', 300],
        ['angry', 'https://uxwing.com/wp-content/themes/uxwing/download/41-emoji-emoticon/angry.svg', 300],
        ['kingEmblem', 'https://pixelartmaker-data-78746291193.nyc3.digitaloceanspaces.com/image/0dc6b0270ea5513.png', 3000],
        ['shark', 'https://creazilla-store.fra1.digitaloceanspaces.com/cliparts/7822338/shark-jaws-clipart-md.png', 500],
        ['party', 'https://creazilla-store.fra1.digitaloceanspaces.com/emojis/55757/partying-face-emoji-clipart-sm.png', 325],
        ['heart', 'https://creazilla-store.fra1.digitaloceanspaces.com/cliparts/7764918/kawaii-st-valentine-s-heart-clipart-md.png', 600],
        ['cupcake', 'https://creazilla-store.fra1.digitaloceanspaces.com/cliparts/7764909/kawaii-st-valentine-s-cupcake-clipart-md.png', 650],
        ['terrier', 'https://creazilla-store.fra1.digitaloceanspaces.com/cliparts/7764032/yorkshire-terrier-clipart-md.png', 450]
    ]
    avatars.sort(key=lambda y: y[2])    # sorts by price least --> greatest

    # desk LoL [name, url, price]
    backgrounds = [
        ['beach', 'https://images.unsplash.com/photo-1481988535861-271139e06469?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1190&q=80',100],
        ['spaceboat', 'https://cdn.pixabay.com/photo/2018/08/14/13/23/ocean-3605547_1280.jpg', 100], #new
        ['earth', 'https://cdn.pixabay.com/photo/2016/10/20/18/35/earth-1756274_1280.jpg',100],#new
        ['emptyLake', 'https://cdn.pixabay.com/photo/2016/05/05/02/37/sunset-1373171_1280.jpg', 200], #new
        ['northernLights', 'https://cdn.pixabay.com/photo/2016/02/13/12/26/aurora-1197753_1280.jpg', 3000], #new
        ['space', "https://images.unsplash.com/photo-1548222606-6c4f581fd09d?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1197&q=80", 600], #new
        ['citylights', 'https://images.unsplash.com/photo-1548602088-9d12a4f9c10f?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2052&q=80', 450], #new
        ['forest', 'https://cdn.pixabay.com/photo/2018/08/21/23/29/forest-3622519_1280.jpg', 100], #new
        ['desert', 'https://cdn.pixabay.com/photo/2017/06/23/17/46/desert-2435404_1280.jpg', 100], #new
        ['clouds', 'https://cdn.pixabay.com/photo/2019/05/19/23/47/clouds-4215608_1280.jpg', 100], #new
        ['moonKite', 'https://cdn.pixabay.com/photo/2020/02/24/06/33/crescent-4875339_1280.jpg', 100], #new
        ['blueorange', 'https://images.unsplash.com/photo-1620503374956-c942862f0372?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80', 400], #new
        ['pinkBlueSky', 'https://cdn.pixabay.com/photo/2019/03/12/17/18/trees-4051288_1280.jpg', 100], #new
        ['cubes?', 'https://images.unsplash.com/photo-1622737133809-d95047b9e673?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1332&q=80', 150], #new
        ['whiteBrick', 'https://cdn.pixabay.com/photo/2017/02/15/11/05/texture-2068283__480.jpg', 100], #new
        ['snow', 'https://cdn.pixabay.com/photo/2015/11/04/11/46/winter-1022401_1280.jpg', 100], #new
        ['wall', 'https://cdn.pixabay.com/photo/2016/11/22/20/01/abstract-1850416_1280.jpg', 100],
        ['waterColor', 'https://cdn.pixabay.com/photo/2017/06/15/23/47/painting-2407262_1280.jpg', 100],
        ['blue', 'https://cdn.pixabay.com/photo/2016/12/01/20/17/texture-1876097_1280.jpg', 100],
        ['blueGreen', 'https://cdn.pixabay.com/photo/2017/06/15/17/31/background-2406119_1280.jpg', 100],
        ['sky', 'https://cdn.pixabay.com/photo/2017/06/27/08/08/cloud-2446630_1280.jpg', 100],
        ['neonrainbow', 'https://images.unsplash.com/photo-1566055909643-a51b4271aa47?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80', 100],
        ['wallPlant', 'https://cdn.pixabay.com/photo/2021/02/21/03/36/empty-room-6035190_1280.jpg', 100]
    ]
    backgrounds.sort(key=lambda y: y[2])    # sorts by price least --> greatest

    # desk LoL [name, url, price]
    desk = [
        ['rubber_duck', 'https://uxwing.com/wp-content/themes/uxwing/download/29-animals-and-birds/duck-color.svg', 4000], #new
        ['plant', 'https://uxwing.com/wp-content/themes/uxwing/download/23-nature-and-environment/potted-plant.svg', 850], #new
        ['soda', 'https://uxwing.com/wp-content/themes/uxwing/download/10-brands-and-social-media/gulp-js.svg', 1100], #new
        ['coconut', 'https://uxwing.com/wp-content/themes/uxwing/download/05-fruits-vegetables/coconut-with-straw.svg', 800], #new
        ['flask', 'https://uxwing.com/wp-content/themes/uxwing/download/21-medical-science-lab/flask-lab-laboratory-research.svg', 750], #new
        ['teddy', 'https://uxwing.com/wp-content/themes/uxwing/download/28-toys-and-childhood/teddy-bear-brown.svg', 1500], #new
        ['trophy', 'https://uxwing.com/wp-content/themes/uxwing/download/24-sport-and-awards/prize.svg', 5000], #new
        ['microscope', 'https://uxwing.com/wp-content/themes/uxwing/download/21-medical-science-lab/laboratory-microscope-test.svg', 750], #new
        ['xmastree', 'https://uxwing.com/wp-content/themes/uxwing/download/22-festival-culture-religion/christmas-tree-xmas.svg', 5000], #new
        ['chessPiece', 'https://uxwing.com/wp-content/themes/uxwing/download/24-sport-and-awards/chess-game-knight.svg', 1200],
        ['rocket', 'https://uxwing.com/wp-content/themes/uxwing/download/42-business-professional-services/startup.svg', 4200], #new
        ['fireExtinguisher', 'https://uxwing.com/wp-content/themes/uxwing/download/33-tools-equipment-construction/fire-extinguisher.svg', 3000], #new
        ['paint', 'https://uxwing.com/wp-content/themes/uxwing/download/36-arts-graphic-shapes/painting.svg', 700], #new
        ['gamingConsole', 'https://uxwing.com/wp-content/themes/uxwing/download/24-sport-and-awards/video-game-gamepad.svg', 6000], #new
        ['book', 'https://uxwing.com/wp-content/themes/uxwing/download/18-education-school/study.svg', 350], #new
        ['piggyBank', 'https://uxwing.com/wp-content/themes/uxwing/download/16-banking-finance/money-saving-dollar.svg', 3000], #new
        ['apple', 'https://uxwing.com/wp-content/themes/uxwing/download/05-fruits-vegetables/fresh-apple.svg', 100], #new
        ['pineapple', 'https://uxwing.com/wp-content/themes/uxwing/download/05-fruits-vegetables/pineapple-fruit.svg', 200], #new
        ['salad', 'https://uxwing.com/wp-content/themes/uxwing/download/05-fruits-vegetables/vegetarian-food.svg', 500], #new
        ['pokemonBall', 'https://uxwing.com/wp-content/themes/uxwing/download/10-brands-and-social-media/pokemon.svg', 7000],
        ['kiwi', 'https://uxwing.com/wp-content/themes/uxwing/download/05-fruits-vegetables/kiwi-food.svg', 150],
        ['globe', 'https://uxwing.com/wp-content/themes/uxwing/download/18-education-school/geography.svg', 750],
        ['bat', 'https://creazilla-store.fra1.digitaloceanspaces.com/cliparts/3342637/halloween-h-9-clipart-md.png', 1100],
        ['pepper', 'https://creazilla-store.fra1.digitaloceanspaces.com/cliparts/7873743/jalapeno-clipart-md.png', 650],
        ['balloons', 'https://creazilla-store.fra1.digitaloceanspaces.com/cliparts/3152885/birthday-party-clipart-sm.png', 950],
        ['plant2', 'https://creazilla-store.fra1.digitaloceanspaces.com/cliparts/69466/potted-plant-clipart-sm.png', 850],
        ['plant3', 'https://creazilla-store.fra1.digitaloceanspaces.com/cliparts/7816007/sprout-plant-clipart-sm.png', 420],
        ['banjo', 'https://creazilla-store.fra1.digitaloceanspaces.com/cliparts/7764875/banjo-clipart-md.png', 1125],
        ['soysauce', 'https://creazilla-store.fra1.digitaloceanspaces.com/cliparts/7525887/soy-souse-clipart-sm.png', 900],
        ['notepad', 'https://creazilla-store.fra1.digitaloceanspaces.com/cliparts/3152562/school-clipart-sm.png', 350],
        ['soloCup', 'https://creazilla-store.fra1.digitaloceanspaces.com/cliparts/3167038/drink-clipart-sm.png', 3500],
        ['sushi', 'https://creazilla-store.fra1.digitaloceanspaces.com/emojis/47968/sushi-emoji-clipart-md.png', 2000]
        
    ]
    desk.sort(key=lambda y: y[2])   # sorts by price least --> greatest
    
    # adds avatars to db
    for item in avatars:
        new_item = All_Items(item=item[0], category="avatar", url=item[1], price = item[2])
        db.session.add(new_item)
        db.session.commit()

    # adds backgrounds to db
    for item in backgrounds:
        new_item = All_Items(item=item[0], category="background", url=item[1], price = item[2])
        db.session.add(new_item)
        db.session.commit()

    # adds desk items to db
    for item in desk:
        new_item = All_Items(item=item[0], category="desk", url=item[1], price = item[2])
        db.session.add(new_item)
        db.session.commit()

    return("Items have been added!")


@app.route('/reset')
def reset():
    """gives the current users 0 coins and clears their inventory
       ** USED FOR DEV TESTING **
    """
    db.session.query(Item).filter(Item.user_id==current_user.id).delete()   # query.delete inventory
    db.session.commit()

    user = Coin.query.get(current_user.id)  # query user's coins
    user.coins = 0  # set coins to 10000
    db.session.commit()

    # user = currentData.query.get(current_user.id)
    # user.time = 0
    # db.session.commit()

    return ("Reset complete! (10,000 coins, 0 items, 0:00 session timer)")


@app.route('/correctHorseBatteryAlien231812')
def admin():
    """gives the current users 100,000,000 coins and clears their inventory
       ** USED FOR DEV TESTING **
    """
    db.session.query(Item).filter(Item.user_id==current_user.id).delete()   # query.delete inventory
    db.session.commit()

    user = Coin.query.get(current_user.id)  # query user's coins
    user.coins = 100000000  # set coins to 10000
    db.session.commit()

    # user = currentData.query.get(current_user.id)
    # user.time = 0
    # db.session.commit()

    return ("Reset complete! (100,000,000 coins, 0 items, 0:00 session timer)")

@app.route('/testing')
def testing():
    """gives the current users 100,000,000 coins and clears their inventory
       ** USED FOR DEV TESTING **
    """

    user = Coin.query.get(current_user.id)  # query user's coins
    user.coins = 4350  # set coins to 10000
    db.session.commit()

    # user = currentData.query.get(current_user.id)
    # user.time = 0
    # db.session.commit()

    return ("Reset complete! (some coins coins)")
    

# @app.route('/ajax_test', methods=['POST', 'GET'])
# def ajax_test():
#   if request.method == "POST":
#     data = request.get_json()
#     selectedFlavor = data[0]['selectedFlavor']
#   print(data)
#   return jsonify(selectedFlavor)


@app.route('/setUsername', methods=['POST', 'GET'])
def setUsername():
    if request.method == 'POST':
        data = request.get_json()
        choice = data[0]['username']

        urls = currentData.query.filter_by(user_id=current_user.id)

        avatar = ""
        spot1 = ""
        spot2 = ""
        spot3 = ""
        spot4 = ""

        print("urls:", urls)
        
        for item in urls:
            print("data.avatar:", item.avatar)
            avatar = item.avatar
            spot1 = item.spot1
            spot2 = item.spot2
            spot3 = item.spot3
            spot4 = item.spot4

        db.session.query(currentData).filter(currentData.user_id==current_user.id).delete()
        db.session.commit()

        new_item = currentData(subject="None", year="None", messaging = False, time=0, username=choice, user_id=current_user.id, avatar = avatar, spot1 = spot1, spot2 = spot2, spot3 = spot3, spot4 = spot4)
        db.session.add(new_item)
        db.session.commit()

    return ("Success")


@app.route('/getImage', methods=['POST', 'GET'])
def getImage():
    if request.method == 'POST':
        data = request.get_json()
        url = data[0]['url']
        item = data[1]['name']
        category = data[2]['category']
    
    new_item = Item(item=item, url=url, category=category, active="false", user_id=current_user.id)
    db.session.add(new_item)
    db.session.commit()
    
    return("Success")


@app.route('/show_all')
def show_all():
   return render_template('show_all.html', users = Coin.query.all(), persons = User.query.all(), items = Item.query.all(), current_user = current_user)

@app.route('/show_messages')
def show_messages():
    messages = Message.query.all()
    return render_template('show_messages.html', messages=messages)


# Home page, renders the index.html template
@app.route('/index')
@app.route('/')
def index():
    return render_template('homescreen.html', title='Home')


@app.route('/login',methods=['GET','POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                # session["user"] = user
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)

                user = User.query.get(current_user.id)
                user.logged_in = "True"
                db.session.commit()
                
                return redirect(url_for("usernameChoice"))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user, title ='Login', first_time = False)
    # return render_template("login.html", title ='Login')

# @app.route("/user")
# def user():
#     if "user" in session:
#         user = session["user"]
#         return f"<h1>{user}</h1>"
#     else:
#         return redirect(url_for("login"))

@app.route('/logout')
@login_required
def logout():
    user = User.query.get(current_user.id)
    user.logged_in = "False"
    db.session.commit()
    
    db.session.query(Chat_Room).filter(Chat_Room.user_id==current_user.id).delete()
    db.session.query(Message).filter(Message.sender_id==current_user.id).delete()
    db.session.query(Message).filter(Message.receiver_id==current_user.id).delete()
    db.session.commit()

    logout_user()
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        student_id = request.form.get('student_id')
        school = request.form.get('school').upper()

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, 
                            password=generate_password_hash(password1, method='sha256'),
                            student_id = student_id, 
                            school = school,
                            logged_in = "True")
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            current_coins = Coin(coins=1, user_id=current_user.id)
            db.session.add(current_coins)
            db.session.commit()
            print("ACCOUNT CREATED!")
            flash('Account created!', category='success')
            # return "Success!!"  + str(email) + " !!  " + str(current_user.id) + "   !!!!!!"
            return redirect(url_for('usernameChoice'))

    return render_template("signup.html", user=current_user, first_time = True)


@app.route('/homescreen',methods=['GET','POST'])
@login_required
def homescreen():
    currentdata = currentData.query.all()
    datadisplay = []
    users = User.query.all()
    my_school = current_user.school
    all_users = []
    logged_in_users = []
    school = []
    display = []


    for user in currentdata:
        datadisplay.append([user.user_id, user.year, user.subject, user.username, user.time, user.messaging])

    for user in users:
        all_users.append([user.email, user.school, user.logged_in, user.id])

    for user in all_users:
        if user[2] == "True":
            logged_in_users.append(user)
            
    for user in logged_in_users:
        if user[1] == my_school:
            school.append(user)

    for user in datadisplay:
        for loggedinuser in school:
            if loggedinuser[3] == user[0]:
                display.append(user)


    user = Coin.query.get(current_user.id)
    return render_template('homescreen.html', title='STUDY BUDDY', current_user = current_user.id ,coins=user.coins, display=display, total=len(school))


@app.route('/setCoins', methods=['GET','POST'])
def setCoins():
    user = Coin.query.get(current_user.id)  # access the 'Coin' db table through the current user's id
    if request.method == 'POST':
        data = request.get_json()   # data sent from ajax request (in base?)
        coins = data[0]['coins']    # get coins form ajax request
        user.coins = coins          # set current user's coins to new coin value
        db.session.commit()         # commit to db
    return("success")


@app.route('/setTime', methods=['GET','POST'])
def setTime():

    if request.method == 'POST':
        # print("POSTING TIME")
        timeData = request.get_json()
        # print(timeData)
        time = int(timeData[0]['time'])
        # print(time)

        # print(user.time)
        # user.time = time
        # db.session.commit()
        a = []
        name = currentData.query.filter_by(user_id=current_user.id)

        for data in name:
            a.append(data.id)
            a.append(data.subject) 
            a.append(data.year)
            a.append(data.messaging)
            a.append(data.username) 
            a.append(data.time)
            a.append(data.avatar)
            a.append(data.spot1)
            a.append(data.spot2)
            a.append(data.spot3)
            a.append(data.spot4)

        # print("User data (from setTime): " + str(a))

        db.session.query(currentData).filter(currentData.user_id==current_user.id).delete()

        current_data = currentData(username=a[4], subject=a[1], year=a[2], messaging=a[3], time= time, user_id=current_user.id, avatar = a[6], spot1 = a[7], spot2 = a[8], spot3 = a[9], spot4 = a[10])
        db.session.add(current_data)
        db.session.commit()

    return("success")


@app.route('/shopTest')
def shopTest():
    user = Coin.query.get(current_user.id)
    user_items = Item.query.filter_by(user_id=current_user.id)   # query user's inventory (already bought/owned)
    all_items = All_Items.query.all()   # query all availabe shop items
    owned = []
    everything = []
    unowned = []

    # create LoL of the user's invenory --> [name, url, category]
    for item in user_items:
        owned.append([item.item, item.url, item.category])

    # create LoL of all the available shop items --> [name, url, category]
    for item in all_items:
        everything.append([item.item, item.url, item.category])

    # sort everything unowned by the user into 'unowned' list
    for item in everything:
        if item not in owned:
            unowned.append(item)

    # sort unowned/unowned lists into 3 seperate lists by category (avatar, background, desk)
    owned_avatar = []
    owned_background = []
    owned_desk = []
    for item in owned:
        if item[2] == 'avatar':
            owned_avatar.append(item)
        elif item[2] == 'background':
            owned_background.append(item)
        else:
            owned_desk.append(item)

    unowned_avatar = []
    unowned_background = []
    unowned_desk = []
    for item in unowned:
        if item[2] == 'avatar':
            unowned_avatar.append(item)
        elif item[2] == 'background':
            unowned_background.append(item)
        else:
            unowned_desk.append(item)

    return render_template('shopTest.html', 
                           owned_avatar=owned_avatar, 
                           owned_background=owned_background, 
                           owned_desk=owned_desk, 
                           unowned_avatar=unowned_avatar, 
                           unowned_background=unowned_background, 
                           unowned_desk=unowned_desk, 
                           owned=owned, unowned=unowned, 
                           title='Shop', items=Item.query.all(), 
                           current_user=current_user, 
                           allItems=All_Items.query.all(), coins = user.coins)


@app.route('/shop', methods=['GET','POST'])
@login_required
def shop():
    user = Coin.query.get(current_user.id)
    user_items = Item.query.filter_by(user_id=current_user.id)   # query user's inventory (already bought/owned)
    all_items = All_Items.query.all()   # query all availabe shop items
    owned = []
    everything = []
    unowned = []

    # create LoL of the user's invenory --> [name, url, category]
    for item in user_items:
        owned.append([item.item, item.url, item.category])

    # create LoL of all the available shop items --> [name, url, category]
    for item in all_items:
        everything.append([item.item, item.url, item.category, item.price])

    # sort everything unowned by the user into 'unowned' list
    for item in everything:
        if item[:3] not in owned:
            unowned.append(item)

    # sort unowned/unowned lists into 3 seperate lists by category (avatar, background, desk)
    owned_avatar = []
    owned_background = []
    owned_desk = []
    for item in owned:
        if item[2] == 'avatar':
            owned_avatar.append(item)
        elif item[2] == 'background':
            owned_background.append(item)
        else:
            owned_desk.append(item)

    unowned_avatar = []
    unowned_background = []
    unowned_desk = []
    for item in unowned:
        if item[2] == 'avatar':
            unowned_avatar.append(item)
        elif item[2] == 'background':
            unowned_background.append(item)
        else:
            unowned_desk.append(item)

    for list in unowned:
        list.append("buyable"+list[0])

    # print("unonwed", unowned)
    
    return render_template('shop.html', 
                            owned_avatar=owned_avatar, 
                           owned_background=owned_background, 
                           owned_desk=owned_desk, 
                           unowned_avatar=unowned_avatar, 
                           unowned_background=unowned_background, 
                           unowned_desk=unowned_desk, 
                           owned=owned, unowned=unowned, 
                           title='SHOP', items=Item.query.all(), 
                           current_user=current_user, 
                           allItems=All_Items.query.all(),
                           coins = user.coins)


@app.route('/inventory',methods=['GET','POST'])
@login_required
def inventory():
    user = Coin.query.get(current_user.id)
    user_items = Item.query.filter_by(user_id=current_user.id)   # query user's inventory (already bought/owned)
    data = currentData.query.filter_by(user_id=current_user.id)
    owned = []
    current_items = []
    display_items = []
    return_owned = []

    # create LoL of the user's invenory --> [name, url, category]
    for item in user_items:
        owned.append([item.item, item.url, item.category, item.id])

    # create LoL of the currently active accessories in each spot [avatar, spot1, spot2, etc]
    for item in data:
        current_items.append([item.avatar, item.spot1, item.spot2, item.spot3, item.spot4])
    
    # for every item in owned, add that item to display_items if the item's url is found in current_items

    for x in range(len(current_items[0])):
        new = 0
        for item in owned:
            if current_items[0][x] in item:
                display_items.append(item)
                new = 1
        
        if new == 0:
            display_items.append(["none"])
    
    print(display_items)

    return_owned = copy.deepcopy(owned)

    # for every item in owned, replace the url with "" if the url is found in current items
    for item in return_owned:
        if item[1] in current_items[0]:
            item[1] = ""

  
    # sort unowned/unowned lists into 3 seperate lists by category (avatar, background, desk)
    owned_avatar = []
    owned_background = []
    owned_desk = []
    for item in return_owned:
        if item[2] == 'avatar':
            owned_avatar.append(item)
        elif item[2] == 'background':
            owned_background.append(item)
        else:
            owned_desk.append(item)

    return render_template('inventory.html', 
                           owned_avatar=owned_avatar, 
                           owned_background=owned_background, 
                           owned_desk=owned_desk, title='INVENTORY', 
                           items=Item.query.all(), 
                           current_user=current_user,
                           coins = user.coins,
                           current_items = display_items)


@app.route('/dropAdd', methods=['GET', 'POST'])
def dropAdd():
    data = request.get_json()
    img_location = data[1]["id"]
    img_url = data[0]["url"]
    
    calledItem = Item.query.filter_by(url=img_url)
    id = 0

    for item in calledItem:
        id = item.id

    item = Item.query.get(id)
    item.active = "true"
    db.session.commit()   

    new_data = currentData.query.filter_by(user_id = current_user.id)
    
    current_id = 0

    urls = []
    for url in new_data:
        urls.append([url.avatar, url.spot1, url.spot2, url.spot3, url.spot4])

    for data in new_data:
        current_id = data.id

    called_data = currentData.query.get(current_id)


    indexToSpot = {0:"avatar", 1:"spot1", 2:"spot2", 3:"spot3", 4:"spot4"}
    if img_url in urls[0]:
        for x in range(len(urls[0])):
            if urls[0][x] == img_url:
                index = indexToSpot[x]
        if index == "avatar":
            called_data.avatar = "None"
        elif index == "spot1":
            called_data.spot1 = "None"
        elif index == "spot2":
            called_data.spot2 = "None"
        elif index == "spot3":
            called_data.spot3 = "None"
        elif index == "spot4":
            called_data.spot4 = "None"
        
    if img_location == "avatar":
        called_data.avatar = img_url
    elif img_location == "spot1":
        called_data.spot1 = img_url
    elif img_location == "spot2":
        called_data.spot2 = img_url
    elif img_location == "spot3":
        called_data.spot3 = img_url
    elif img_location == "spot4":
        called_data.spot4 = img_url
        
    db.session.commit()

    return ("Success")

@app.route('/dropRemove', methods=['GET', 'POST'])
def dropRemove():
    data = request.get_json()
    img_location = data[1]["id"]
    img_url = data[0]["url"]
    
    calledItem = Item.query.filter_by(url=img_url)
    id = 0

    for item in calledItem:
        id = item.id

    item = Item.query.get(id)
    item.active = "false"
    db.session.commit()   

    new_data = currentData.query.filter_by(user_id = current_user.id)
    
    current_id = 0

    for data in new_data:
        current_id = data.id

    called_data = currentData.query.get(current_id)

    if called_data.avatar == img_url:
        called_data.avatar = "None"
    elif called_data.spot1 == img_url:
        called_data.spot1 = "None"
    elif called_data.spot2 == img_url:
        called_data.spot2 = "None"
    elif called_data.spot3 == img_url:
        called_data.spot3 = "None"
    elif called_data.spot4 == img_url:
        called_data.spot4 = "None"
    
    db.session.commit()

    # print(called_data.avatar)

    return ("Success")

@app.route('/dropRemove', methods=['GET', 'POST'])
# def dropRemove():

@app.route('/settings',methods=['GET','POST'])
@login_required
def settings():
    settingInfo = currentData.query.filter_by(user_id=current_user.id)
    name = currentData.query.filter_by(user_id=current_user.id)
    
    user = Coin.query.get(current_user.id)
    lst = username()
    a = ""
    time = ""
    info = []
    avatar = ""
    spot1 = ""
    spot2 = ""
    spot3 = ""
    spot4 = ""

    for data in settingInfo:
        info.append([str(data.subject), str(data.year), str(data.messaging)])

    # print("INFO BELOW!! [subject, year, messaging preference]")
    # print(info)

    for data in name:
        a = str(data.username)
        time = int(data.time)
        avatar = data.avatar
        spot1 = data.spot1
        spot2 = data.spot2
        spot3 = data.spot3
        spot4 = data.spot4

    # print("#1", a, "session time:", time)

    if request.method == 'POST':
        user = User.query.get(current_user.id)

        subject = request.form['subject']
        year = request.form['year']
        # time = user.currentData.time
        convertedmessaging = True
        
        try:
            request.form['messaging']
        except:
            convertedmessaging = False
        else:
            convertedmessaging = True

        db.session.query(currentData).filter(currentData.user_id==current_user.id).delete()

        current_data = currentData(username=a, subject=subject, year=year, messaging=convertedmessaging, time=time, user_id=current_user.id, avatar = avatar, spot1 = spot1, spot2 = spot2, spot3 = spot3, spot4 = spot4)
        db.session.add(current_data)
        db.session.commit()

        
        userData = currentData.query.filter_by(user_id=current_user.id)
        chatRoomData = Chat_Room.query.all()
    
        messagingPreference = ""
        currentUsername = ""
        currentId = str(current_user.id)
        chatRoomUsers = []

        for user in chatRoomData:
            chatRoomUsers.append(user.username)

        for data in userData:
            messagingPreference = str(data.messaging)
            currentUsername = str(data.username)

        if messagingPreference == "True" and currentUsername not in chatRoomUsers:
            new_user = Chat_Room(username=currentUsername, user_id=currentId)
            db.session.add(new_user)
            db.session.commit()
            print("added to DB")
        else:
            db.session.query(Chat_Room).filter(Chat_Room.user_id==current_user.id).delete()
            db.session.commit()

        # print("#2", a, "session time:", time)
        
        return redirect(url_for('homescreen'))
        
    return render_template('settings.html', title='SETTINGS', coins=user.coins, lst=lst, name=a, info=info)

pusher_client = pusher.Pusher(
  app_id='1429475',
  key='2dd35a38909a3742c906',
  secret='31f2abcb2629c011c24d',
  cluster='us2',
  ssl=True
)

@app.route('/set_id', methods=['GET', 'POST'])
def set_id():
    if request.method == 'POST':
        data = request.get_json()
        receiver_id = data[0]

        print(receiver_id)

        new_message = Message(username="", message="", sender_id=current_user.id, receiver_id = receiver_id)
        db.session.add(new_message)
        db.session.commit()

        new_post = New_Message(sender_id = current_user.id, target_id = receiver_id)
        db.session.add(new_post)
        db.session.commit()

    return ("Success")

@app.route('/message', methods=['GET', 'POST'])
@login_required
def message():
    messageInfo = Message.query.filter_by(sender_id=current_user.id)
    
    receiver_id = ""


    for data in messageInfo:
        receiver_id = str(data.receiver_id)

    print(receiver_id)

    allMessages = Message.query.all()
    messages = []
    messageList = []

    for message in allMessages:
        messages.append([message.username, message.message, message.sender_id, message.receiver_id])

    for message in messages:
        if str(message[2]) == str(current_user.id) and str(message[3]) == receiver_id:
            messageList.append(message)
        if str(message[2]) == str(receiver_id) and str(message[3]) == str(current_user.id):
            messageList.append(message)
        
    print("MESSAGE LIST...")
    print(messageList)
    # messageInfo = Message.query.filter_by(receiver_id=current_user.id) | (sender_id = current_user.id)
    # messageInfo2 = db.session.query(Message).filter(or_((Message.sender_id == current_user.id, Message.receiver_id == receiver_id),(Message.sender_id == receiver_id, Message.receiver_id == current_user.id)))
    
    userdata = []

    currentdata = currentData.query.filter_by(user_id=current_user.id)

    for data in currentdata:
        userdata.append([str(data.username)])
    return render_template('message.html', messages=messageList, username=userdata[0])


@app.route('/newmessage', methods=['GET', 'POST'])
def newmessage():
    
    messageInfo = Message.query.filter_by(sender_id=current_user.id)
    
    receiver_id = ""


    for data in messageInfo:
        receiver_id = str(data.receiver_id)


    print("INFO BELOW!! [receiver_id]")
    print(receiver_id)

    try: 
        username = request.form.get('username')
        message = request.form.get('message')

        db.session.query(Message).filter(Message.username=='').delete()
        if message != '':
            new_message = Message(username=username, message=message, sender_id = current_user.id, receiver_id = receiver_id)
            db.session.add(new_message)
            db.session.commit()

            pusher_client.trigger('chat-channel', 'new-message', {'username' : username, 'message': message, 'sender_id': str(current_user.id), 'receiver_id': receiver_id})

        return jsonify({'result' : 'success'})

    except:
        return jsonify({'result' : 'failure'})


@app.route('/fetchMessages', methods=['GET', 'POST'])
def fetchMessages():
    myReceiver = ""
    data = New_Message.query.all()
    messageData = Message.query.all()
    target = ""
    returnDict = {}

    for message in messageData:
        myReceiver = str(message.receiver_id)
    
    for message in data:
        if message.sender_id == myReceiver:
            target = str(message.target_id)

    returnDict["target"] = target

    return jsonify(returnDict)

@app.route('/fetchLatestMessage', methods=['GET', 'POST'])
def fetchLatestMessage():
    sender = ""
    data = New_Message.query.all()
    messageData = Message.query.all()
    target = ""
    returnDict = {}

    for message in messageData:
        sender = str(message.sender_id)

    for message in data:
        if message.sender_id == sender:
            target = str(message.target_id)
        
    returnDict["sender"] = sender
    returnDict["target"] = target
    
    return jsonify(returnDict)

@app.route('/chatRoom', methods=['GET', 'POST'])
@login_required
def chatRoom():
    # print(usersToMessage)
    lst = []

    me = str(current_user.id)
    
    data = currentData.query.filter_by(user_id=current_user.id)
    username = ""

    for x in data:
        username = str(x.username)

    lst = Chat_Room.query.all()
    chatRoomData = []
    returnLst = []

    for user in lst:
        chatRoomData.append([user.username, user.user_id])

    for user in chatRoomData:
        if user[0] != username:
            returnLst.append(user)

    # if true...
    
    messageInfo = Message.query.filter_by(sender_id=current_user.id)
    
    receiver_id = ""

    for data2 in messageInfo:
        receiver_id = str(data2.receiver_id)

    allMessages = Message.query.all()
    messages = []
    messageList = []


    for message in allMessages:
        if message.username != '' or message.message != '':
            messages.append([message.username, message.message, message.sender_id, message.receiver_id, message.id])
    

    for message in messages:
        if str(message[2]) == str(current_user.id) and str(message[3]) == str(receiver_id):
            messageList.append(message)
        if str(message[2]) == str(receiver_id) and str(message[3]) == str(current_user.id):
            messageList.append(message)
        
    # print("MESSAGE LIST...")
    # print(messages)
    # messageInfo = Message.query.filter_by(receiver_id=current_user.id) | (sender_id = current_user.id)
    # messageInfo2 = db.session.query(Message).filter(or_((Message.sender_id == current_user.id, Message.receiver_id == receiver_id),(Message.sender_id == receiver_id, Message.receiver_id == current_user.id)))
    
    userdata = []

    currentdata = currentData.query.filter_by(user_id=current_user.id)

    for data3 in currentdata:
        userdata.append([str(data3.username)])

    return render_template('chatRoom.html', title='CHAT ROOM', usersToMessage = returnLst, messages=messageList, username=userdata[0], me=me)



