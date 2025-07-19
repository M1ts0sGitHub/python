import os
import random
import time

def print_cards(cards, cards_shown):
    for position in range(len(cards)):
        print(cards[position], end=" ") if cards_shown[position] else print("#", end=" ")
    print()

def give_ans(cards_shown):
    while True:
        try:
            ans = int(input(f"Επέλεξε μια κλειστή κάρτα από το 1 έως το {len(cards_shown)}: ")) - 1
            if 0 <= ans < len(cards_shown) and not cards_shown[ans]:
                return ans
        except:
            pass
        print("Λανθασμένη επιλογή. Προσπάθησε ξανά.")

def main():
    difficulty = 4
    cards = [*range(1, difficulty+1)] * 2
    random.shuffle(cards)
    cards_shown = [False] * len(cards)
    attempts = 0

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        attempts += 1
        print("Οι κάρτες του παιχνιδιού")
        print_cards(cards, cards_shown)
        
        ans1 = give_ans(cards_shown)
        cards_shown[ans1] = True
        print("\nΜετά το άνοιγμα της πρώτης κάρτας:")
        print_cards(cards, cards_shown)
        
        ans2 = give_ans(cards_shown)
        cards_shown[ans2] = True
        print("\nΜετά το άνοιγμα της δεύτερης κάρτας:")
        print_cards(cards, cards_shown)
        
        if cards[ans1] != cards[ans2]:
            cards_shown[ans1] = cards_shown[ans2] = False
            print("Δεν βρήκες δύο ίδιες, προσπάθησε ξανά!")
        elif all(cards_shown):
            print(f"Μπράβο, νίκησες το παιχνίδι με {attempts} προσπάθειες!")
            break
        else:
            print("Μπράβο, βρήκες δύο ίδιες! Συνέχισε την καλή προσπάθεια!")
        
        time.sleep(5)

if __name__ == "__main__":
    main()
