import random
import csv
import time

initTime = int(time.time() * 1000000)
class Card:
    values = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
    colors = ["♣️","♦️","♠️","♥️"]
    def __init__(self, value, color) -> None:
        assert value in self.values
        assert color in self.colors
        self.value = value
        self.color = color
    def __repr__(self) -> str:
        return f"{self.value}{self.color}"

class CardDeck:
    def __init__(self) -> None:
        self.deck = [Card(val,col) for val in Card.values for col in Card.colors]
    def __repr__(self) -> str:
        return str(self.deck)
    def shuffle(self):
        random.shuffle(self.deck)
    def distribute(self, list_of_players, table):
        for _ in range(2):
            for player in list_of_players:
                table.add_cards([self.deck[0]])
                player.hand.append(self.deck.pop(0))
    def deal(self, nb_of_cards, table):
        self.deck.pop(0) # Burn card
        tab = [self.deck.pop(0) for _ in range(nb_of_cards)]
        table.add_cards(tab)
        return tab

class Player:
    def __init__(self) -> None:
        self.hand = []
        self.id = int(time.time()*1000000) - initTime
    def __repr__(self) -> str:
        return f"{self.id} : {self.hand}"

class Table:
    combinaisons = {
        0:"Nothing",
        1:"High Card",
        2:"One Pair",
        3:"Two Pairs",
        4:"Three of a kind",
        5:"Straight",
        6:"Flush",
        7:"Full House",
        8:"Four of a kind",
        9:"Straight Flush",
        10:"Royal Flush"
    }
    def __init__(self) -> None:
        self.all_cards = []
        self.high_card = ""
    def add_cards(self, list_of_cards):
        self.all_cards += list_of_cards
    def getHighCard(self):
        all_values = [i.value for i in self.all_cards]
        all_values.sort(key=lambda x: Card.values.index(x))
        self.high_card = all_values[-1]
    def detect_combinaison(self, hand):
        if self.is_royal(hand):
            return 10 # Royal Flush
        elif self.is_flush(hand) and self.is_straight(hand):
            return 9 # Straight Flush
        elif self.is_four_of_a_kind(hand):
            return 8 # Four of a kind
        elif self.is_full_house(hand):
            return 7 # Full House
        elif self.is_flush(hand):
            return 6 # Flush
        elif self.is_straight(hand):
            return 5 # Straight
        elif self.is_three_of_a_kind(hand):
            return 4 # Three of a kind
        elif self.is_two_pairs(hand):
            return 3 # Two pairs
        elif self.is_one_pair(hand):
            return 2 # One pair
        elif self.is_a(hand,self.high_card):
            return 1 # High card
        else:
            return 0 # Nothing
    def is_a(self,hand,car):
        for card in hand:
            if car in str(card):
                return True
        return False
    def is_one_pair(self,hand):
        k = 0
        for card in hand:
            if self.is_a(hand,card.value):
                k += 1
        return k == 2
    def is_two_pairs(self,hand):
        pairs = {i:0 for i in Card.values}
        for card in hand:
            pairs[card.value] += 1
        k = 0
        for i in pairs.values():
            if i == 2:
                k += 1
        return k>=2
    def is_three_of_a_kind(self,hand):
        k = 0
        for card in hand:
            if self.is_a(hand,card.value):
                k += 1
        return k == 3
    def is_straight(self,hand):
        all_values = [i.value for i in hand]
        all_values.sort(key=lambda x: Card.values.index(x))
        if ["2","3","4","5","A"] in all_values:
            return True
        if ["2","3","4","5","6"] in all_values:
            return True
        if ["3","4","5","6","7"] in all_values:
            return True
        if ["4","5","6","7","8"] in all_values:
            return True
        if ["5","6","7","8","9"] in all_values:
            return True
        if ["6","7","8","9","10"] in all_values:
            return True
        if ["7","8","9","10","J"] in all_values:
            return True
        if ["8","9","10","J","Q"] in all_values:
            return True
        if ["9","10","J","Q","K"] in all_values:
            return True
        if ["10","J","Q","K","A"] in all_values:
            return True
        return False
    def is_flush(self,hand):
        k = {
            "♣️":0,
            "♦️":0,
            "♠️":0,
            "♥️":0
        }
        for card in hand:
            k[card.color] += 1
        return max(k.values()) >= 5
    def is_full_house(self,hand):
        pairs = {i:0 for i in Card.values}
        for card in hand:
            pairs[card.value] += 1
        j = 0
        k = 0
        for i in pairs.values():
            if i == 3:
                k += 1
            if i == 2:
                j += 1
        return k>=1 and j>=1
    def is_four_of_a_kind(self,hand):
        k = 0
        for card in hand:
            if self.is_a(hand,card.value):
                k += 1
        return k == 4
    def is_royal(self,hand):
        all_cards = [str(i) for i in hand]
        if "A♣️" in all_cards and "K♣️" in all_cards and "Q♣️" in all_cards and "J♣️" in all_cards and "10♣️" in all_cards:
            return True
        if "A♦️" in all_cards and "K♦️" in all_cards and "Q♦️" in all_cards and "J♦️" in all_cards and "10♦️" in all_cards:
            return True
        if "A♠️" in all_cards and "K♠️" in all_cards and "Q♠️" in all_cards and "J♠️" in all_cards and "10♠️" in all_cards:
            return True
        if "A♥️" in all_cards and "K♥️" in all_cards and "Q♥️" in all_cards and "J♥️" in all_cards and "10♥️" in all_cards:
            return True
        return False

if __name__ == "__main__":
    nb_of_players = int(input("Number of players: "))
    assert type(nb_of_players) == int
    assert nb_of_players > 0
    nb_of_rounds = int(input("Number of rounds: "))
    assert type(nb_of_rounds) == int
    assert nb_of_rounds > 0
    save = input("Save the game? (y/n): ")
    assert save in ["y","n","Y","N",""]
    if save == "y" or save == "Y":
        save = True
    else:
        print("The game won't be saved !")
        save = False
    print(f"Generating {nb_of_rounds} game{'s' if nb_of_rounds > 1 else ''} with {nb_of_players} player{'s' if nb_of_players > 1 else ''}...")
    
    game = []
    
    for round_nb in range(nb_of_rounds):
        print(f"\r[{'#'*int(round_nb/nb_of_rounds*100)}{'_'*(99-int(round_nb/nb_of_rounds*100))}] {round_nb+1}/{nb_of_rounds} ({round(((round_nb+1)/(nb_of_rounds))*100,2)}%)", end="")
        table = Table()
        players = [Player() for _ in range(nb_of_players)]
        deck = CardDeck()
        deck.shuffle()
        deck.distribute(players,table)
        game.append({f"player{i+1}":players[i].hand for i in range(nb_of_players)})
        game[-1]["FlopTurnRiver"] = list(deck.deal(3,table) + deck.deal(1,table) + deck.deal(1,table))
        table.getHighCard()
        plrys = {f"player{i+1}":0 for i in range(nb_of_players)}
        for plyr in plrys.keys():
            plrys[plyr] = table.detect_combinaison(game[-1][plyr]+game[-1]["FlopTurnRiver"])
            game[-1][f"{plyr}_result"] = table.combinaisons[plrys[plyr]]
        # Detect the winner
        winners  = []
        max_combinaison = 0
        for plyr in plrys.keys():
            if plrys[plyr] > max_combinaison:
                max_combinaison = plrys[plyr]
        for plyr in plrys.keys():
            if plrys[plyr] == max_combinaison:
                winners.append(plyr)
        game[-1]["winner"] = winners
    print()
    
    if save:
        # Save the game into a csv file
        print("Saving the game into a csv file...")
        with open(f"{nb_of_players}p-{nb_of_rounds}r_game_{initTime}.csv", "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["FlopTurnRiver"] + [f"player{i+1}" for i in range(nb_of_players)] + [f"player{i+1}_result" for i in range(nb_of_players)] + ["winner"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            for round in game:
                writer.writerow(round)
    print("### Done! ###")
