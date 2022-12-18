import json

bonus_points = {
    "Argentina" : 35,
    "France": 25,
    "Messi": 20,
    "Mbappe": 20
}

possible_outcomes = {
    0: "Tie",
    1: "Argentina win",
    2: "France win"
}

Winning_team = {
    0: "France",
    1: "Argentina"
}

Scorer = {
    0: "Messi",
    1: "Mbappe"
}

class Game_Simulation():
    def __init__(self, kivun:int, scorer:int, winning_team:int, gamblers_file:str) -> None:
        self.kivun = kivun
        self.scorer = scorer
        self.winning_team = winning_team
        self.Gamblers = []

        self.init_Gamblers(gamblers_file)
        self.run()

    def init_Gamblers(self, file_path:str):
        with open(file_path, "r") as file:
            data = json.load(file)
            for gambler_data in data:
                gambler = Gambler(gambler_data['name'], gambler_data['current_score'], gambler_data['bonus_bets'])
                self.Gamblers.append(gambler)

    def run(self):
        print(f"For the match ending with {possible_outcomes[self.kivun]}, the winning team is {Winning_team[self.winning_team]} and scorer is {Scorer[self.scorer]}:\n")
        for i in range(3):
            for gambler in self.Gamblers:
                gambler.update_bet(i)
                points = gambler.calc_points(self.kivun, self.winning_team, self.scorer)
                print(f"{gambler.name} bet {possible_outcomes[i]} and scored: {points}, ({points+6})")
            print("\n")


class Gambler():
    def __init__(self, name:str, current_score:float, bonus_bets:{str,str}) -> None:
        self.name = name
        self.current_score = current_score
        self.bonus_bets = bonus_bets
        self.bet = 0


    def calc_bonus(self, winning_team:int, highest_goalscorer:int):
        bonus = 0
        if self.bonus_bets["team"] == Winning_team[winning_team]:
            bonus += bonus_points[self.bonus_bets["team"]]
        if self.bonus_bets["scorer"] == Scorer[highest_goalscorer]:
            bonus += bonus_points[self.bonus_bets["scorer"]]
        return bonus

    def calc_match_points(self, kivun:int):
        points = 0
        if kivun == self.bet:
            if kivun == 0 or kivun == 1:
                points += 6
            else:
                points += 5
        return points

    def calc_points(self, kivun:int,
                    winning_team:int, highest_goalscorer:int):
        points = self.current_score
        points += self.calc_bonus(winning_team, highest_goalscorer)
        points += self.calc_match_points(kivun)
        return points


    def update_bet(self, bet:int):
        self.bet = bet


def main():

    for i in range(3):
        for j in range(2):
            Game_Simulation(i, j, i%2, "gamblers.json")
            if i == 0:
                Game_Simulation(i, j, i + 1, "gamblers.json")

if __name__ == '__main__':
    main()