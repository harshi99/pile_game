from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'POST':
        player1 = request.form['player1']
        player2 = request.form['player2']
        pile1 = int(request.form['pile1'])
        pile2 = int(request.form['pile2'])
        pile3 = int(request.form['pile3'])
        min_pick = 1
        max_pick = min(pile1, pile2, pile3)

        if 'current_player' not in request.form:
            current_player = player1
            piles = [pile1, pile2, pile3]
        else:
            current_player = request.form['current_player']
            piles = [
                int(request.form['pile1']),
                int(request.form['pile2']),
                int(request.form['pile3'])
            ]

            pile_index = int(request.form['pile_index'])
            stones = int(request.form['stones'])
            piles[pile_index] -= stones
            current_player = player2 if current_player == player1 else player1

        if all(pile == 0 for pile in piles):
            winner = player1 if piles[0] == 0 else player2
            return render_template('result.html', player1=player1, player2=player2, winner=winner)

        return render_template('game.html', player1=player1, player2=player2, current_player=current_player,
                               piles=piles, min_pick=min_pick, max_pick=max_pick)

    return render_template('game.html')

@app.route('/result')
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run()
