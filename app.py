from flask import Flask, render_template
from utils import get_all_players, get_graph_pts, chunks, get_graph_last_games, capitalize_names

app = Flask(__name__)


@app.route('/')
def index(): # put application's code here
    return render_template('index.html')

@app.route('/players/')
def players():  # put application's code here
    players = get_all_players()
    players = list(chunks(players, 100))
    return render_template('players.html', players=players)

@app.route('/players/<player_id>/<player_name>/<stat>/<graph>/')
def player_details(player_id, player_name, stat, graph):
    img_base64= get_graph_pts(player_id, player_name, stat, graph)
    return render_template('player_details.html', img_base64=img_base64, player_id=player_id, player_name=player_name, stat=stat, graph=graph)

@app.route('/players/last_games/<player_id>/<player_name>/')
def last_five_games_stats(player_id, player_name):
    table_html,img_base64 = get_graph_last_games(player_id)
    player_name = capitalize_names(player_name)
    return render_template('player_last5.html',table_html=table_html, img_base64=img_base64, player_id=player_id, player_name=player_name)


if __name__ == '__main__':
    app.run()
