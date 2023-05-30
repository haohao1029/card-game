from flask import Flask, jsonify, render_template, request
import random

app = Flask(__name__)

memory = {}

@app.route("/")
def hello_world():
    return render_template('home.html')

@app.route('/assign_cards', methods=['POST'])
def assign_cards():
    id = request.get_json().get('id')
    print(memory[str(id)])
    cards = memory[str(id)]["cards"]
    banker_cards = random.sample(cards, 2)
    for i in banker_cards:
        memory[str(id)]["cards"].remove(i)
        
    # random pick 2 cards from deck for player then remove from deck
    player_cards = random.sample(cards, 2)
    for i in player_cards:
        memory[str(id)]["cards"].remove(i)
    print(memory[str(id)])
        

    banker_value = calculate_total_value(banker_cards)
    player_value = calculate_total_value(player_cards)
    
    winner = determine_winner(str(id),banker_value, player_value)
    
    return jsonify({'banker_cards': banker_cards, 'player_cards': player_cards, 'banker_value': banker_value, 'player_value': player_value, 'winner': winner, 'stats': memory[str(id)]["stats"]})

def calculate_total_value(cards):
    total_value = sum(get_card_value(card) for card in cards)
    return total_value % 10


def determine_winner(id, banker_value, player_value):
    if banker_value > player_value:
        memory[id]["stats"]["banker_win"] += 1
        return 'Banker Wins'
    elif banker_value < player_value:
        memory[id]["stats"]["player_win"] += 1

        return 'Player Wins'
    else:
        memory[id]["stats"]["draw"] += 1
        return 'Draw'

def get_card_value(card):
    value = int(card[:2])
    if value == 1:
        return 1
    elif value >= 10:
        return 10
    else:
        return value

@app.route('/shuffle', methods=['POST'])
def shuffle_api():
    cards = initialize_cards()
    id = request.get_json().get('id')
    memory[str(id)] = {}
    memory[str(id)]["cards"] = cards
    memory[str(id)]["stats"] = {"banker_win": 0, "player_win": 0, "draw": 0}
    return jsonify({'message': 'Shuffle Success', 'stats': memory[str(id)]["stats"]})


# Initialize the deck of cards
def initialize_cards():
    deck = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13']
    shape = ['c', 'd', 'h', 's']
    cards = [str(i) + j for i in deck for j in shape]
    return cards
