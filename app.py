from flask import Flask, render_template
from utils import get_all_players, get_graph_pts, chunks

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    players = get_all_players()
    players = list(chunks(players, 100))
    return render_template('index.html', players=players)

@app.route('/players/<player_id>/<player_name>/<stat>/<graph>/')
def player_details(player_id, player_name, stat, graph):
    img_base64= get_graph_pts(player_id, player_name, stat, graph)
    return render_template('player_details.html', img_base64=img_base64, player_id=player_id, player_name=player_name, stat=stat, graph=graph)


if __name__ == '__main__':
    app.run()
