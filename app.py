from flask import Flask, render_template, request
from azure.cosmos import CosmosClient

app = Flask(__name__)
cosmosdb_endpoint = 'https://game1.documents.azure.com:443/'
cosmosdb_key = '<ufNro7u1nUuEePVKsGluq6k8ZvuHrYctHd00XRDf3mB90bLS9eaHBB8nQlWB17wxAospNf0XfmsgACDbVRjQlg==>'
database_name = '<game>'
container_name = '<game>'

# Initialize the Cosmos DB client
client = CosmosClient(cosmosdb_endpoint, cosmosdb_key)
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

player1 = ""
player2 = ""
judge = ""
piles = [0, 0, 0]
min_pick = 0
max_pick = 0
current_player = ""
scores = {
    "player1": 0,
    "player2": 0
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    global player1, player2, judge, piles, min_pick, max_pick, current_player, scores

    if request.method == 'POST':
        if 'player1' in request.form:
            player1 = request.form['player1']
            player2 = request.form['player2']
            judge = request.form['judge']
            piles = [
                int(request.form['pile1']),
                int(request.form['pile2']),
                int(request.form['pile3'])
            ]
            min_pick = int(request.form['min_pick'])
            max_pick = int(request.form['max_pick'])
            current_player = player1
            scores = {
                "player1": 0,
                "player2": 0
            }

            return render_template('game.html', player1=player1, player2=player2, judge=judge, piles=piles,
                                   min_pick=min_pick, max_pick=max_pick, current_player=current_player,scores=scores)

        pile_index = int(request.form['pile_index'])
        stones = int(request.form['stones'])
        piles[pile_index] -= stones

        scores = {
            'player1': 0,
            'player2': 0
        }

        if 'scores' in request.form:
            scores = {
                'player1': int(request.form['scores[\'player1\']']),
                'player2': int(request.form['scores[\'player2\']'])
            }

        if current_player == player1:
            scores["player1"] += stones
            current_player = player2
        else:
            scores["player2"] += stones
            current_player = player1

        if all(pile == 0 for pile in piles):
            if scores["player1"] > scores["player2"]:
                winner = player1
            elif scores["player1"] < scores["player2"]:
                winner = player2
            else:
                winner = "It's a tie"

            return render_template('result.html', player1=player1, player2=player2, judge=judge, winner=winner,
                                   scores=scores)

        return render_template('game.html', player1=player1, player2=player2, judge=judge, piles=piles,
                               min_pick=min_pick, max_pick=max_pick, current_player=current_player,scores=scores)

    return render_template('game.html', player1=player1, player2=player2, judge=judge, piles=piles,
                           min_pick=min_pick, max_pick=max_pick, current_player=current_player,scores=scores)

@app.route('/result')
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run()
