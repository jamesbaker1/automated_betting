from uuid import uuid4
from flask import Flask, jsonify, request
import time


class Bettor:
    def __init__(self, bettor_uuid, name):
        self.uuid = bettor_uuid
        self.name = name
        self.bets = []
    def __eq__(self, other):
        return self.uuid == other.uuid


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
    def __init__(self, home_team, away_team, end_time):
        self.end_time = end_time
        self.home_team = home_team
        self.away_team = away_team
        self.end_time = end_time
        self.home_team_score = 0
        self.away_team_score = 0
    def result(self):
        if self.end_time > time.now():
            raise ValueError('Game not finished')
        return Spread(self.home_team_score - self.away_team_score, self.home_team)
    def __eq__(self, other):
        return self.home_team == other.home_team and \
               self.away_team == other.away_team and \
               self.end_time == other.end_time


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

    def get_game(self, home_team, away_team, end_time):
        potential_new_game = Game(home_team, away_team, end_time)
        for game in self.games:
            if potential_new_game == game:
                return game
        self.games.append(potential_new_game)
        return potential_new_game

    def get_bettor(self, bettor_uuid, bettor_name):
        potential_user = Bettor(bettor_uuid, bettor_name)

        if bettor_uuid is None:
            return None

        if potential_user not in self.users:
            self.users.append(potential_user)

        return potential_user


app = Flask(__name__)

game = BettingSystem()

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
    values = request.get_json()

    required = [
                'bettor_uuid',
                'bettor_name',
                'amount',
                'point_differential',
                'spread_team',
                'home_team',
                'away_team',
                'end_time'
               ]
    if not all(k in values for k in required):
        return 'Missing values', 400

    bettee_uuid = values['bettee_uuid'] if 'bettee_uuid' in values else None
    bettee_name = values['bettee_name'] if 'bettee_name' in values else None

    potential_game = game.get_game(values['home_team'], values['away_team'], values['end_time'])
    bettor = game.get_bettor(values['bettor_uuid'], values['bettor_name'])
    bettee = game.get_bettor(bettee_uuid, bettee_name)
    spread = Spread(values['point_differential'], values['spread_team'])

    new_bet = Bet(bettor, bettee, values['amount'], potential_game, spread)

    game.place_bet(new_bet)

    return 'Bet placed', 200

@app.route("/all_bets", methods=['GET'])
def all_bets():
    open_bets_info = [
                    {
                    "bettor_name": bet.bettor.name,
                    "bettee_name": "Open bet" if bet.bettee is None else bet.bettee.name,
                    "amount": bet.amount,
                    "home_team": bet.game.home_team,
                    "away_team": bet.game.away_team,
                    "spread_point_differential": bet.spread.point_differential,
                    "spread_team": bet.spread.team
                    }
                    for bet in game.bets]

    return jsonify(open_bets_info), 200

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
