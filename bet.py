from uuid import uuid4
from flask import Flask, jsonify, request


class Bettor:
    def __init__(self, name):
        self.uuid = uuid4()
        self.name = name
        self.bets = []


class Spread:
    def __init__(self, point_differential, team):
        self.point_differential = point_differential
        self.team = team


class Bet:
    def __init__(self, bettor, bettee, amount, game, spread):
        self.bettor = bettor
        self.bettee = bettee
        self.amount = amount
        self.game = game
        self.spread = spread

class Game:
    def __init__(self, home_team, away_team, end_time, home_team_score, away_team_score):
        self.end_time = end_time
        self.home_team = home_team
        self.away_team = away_team
        self.end_time = end_time
        self.home_team_score = home_team_score
        self.away_team_score = away_team_score

class BettingSystem:
    def __init__(self):
        self.games = []
        self.users = []
        self.bets = []
        self.openbets = []

    def place_bet(self, bet):
        self.bets.append(bet)

    @property
    def open_bets(self):
        return [bet for bet in self.bets if bet.bettee is None]




# print(test_betting.open_bets)



app = Flask(__name__)

game = BettingSystem()
cavs = uuid4()
celtics = uuid4()
test_betting = BettingSystem()
james = Bettor("James")
jonny = Bettor("Jonny")
test_spread = Spread(6, celtics)
test_game = Game(cavs, celtics, 0, 0, 0)
test_spread = Spread(6, celtics)
test_open_bet = Bet(james, None, 10, test_game, test_spread)

game.place_bet(test_open_bet)

@app.route("/open_bets", methods=['GET'])
def open_bets():
    open_bets_info = [
                    {
                    "bettor_name": bet.bettor.name,
                    "amount": bet.amount,
                    "home_team": bet.game.home_team,
                    "away_team": bet.game.away_team,
                    "spread_point_differential": bet.spread.point_differential,
                    "spread_team": bet.spread.team
                    }
                    for bet in game.open_bets]

    return jsonify(open_bets_info), 200

@app.route("/place_bet", methods=['POST'])
def place_bet():
    required = ['bettor', 'bettee', 'amount', 'game']
    if not all(k in values for k in required):
        return 'Missing values', 400
    return 'Not done yet', 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
