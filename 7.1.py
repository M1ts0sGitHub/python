import os, random, time

cards = [1,1,2,2,3,3,4,4]
random.shuffle(cards)
cards_shown = [False,False,False,False,False,False,False,False]
prospatheies = 0

def print_cards():
    for position in range(len(cards)):
         print(cards[position], end=" ") if cards_shown[position] else print("#",end=" ")
    print()

def give_ans():
    global cards_shown
    try:
        ans = int(input("Επέλεξε μια κλειστή κάρτα από το 1 έως το 8: "))
        if ans > 0 and ans < 9 and not(cards_shown[ans-1]):
            return ans-1
        else:
            print("Λανθασμένη επιλογή. Προσπάθησε ξανά.")
            return give_ans()    
    except:
        print("Λανθασμένη επιλογή. Προσπάθησε ξανά.")
        return give_ans()

#main game loop
while True:
    os.system('cls')
    prospatheies +=1
    print("Οι κάρτες του παιχνιδιού")
    print_cards()
    ans1 = give_ans()
    print(f"\nΜετά το άνοιγμα της πρώτης κάρτας:")
    cards_shown[ans1] = True
    print_cards()
    ans2 = give_ans()
    print(f"\nΜετά το άνοιγμα της δεύτερης κάρτας:")
    cards_shown[ans2] = True
    print_cards()
    if cards[ans1] != cards[ans2]:
        cards_shown[ans1] = False
        cards_shown[ans2] = False
        print("Δεν βρήκες δύο ίδιες, προσπάθησε ξανά!")
    elif all(cards_shown):
        print(f"Μπράβο, νίκησες το παιχνίδι με {prospatheies} προσπάθειες!")
        break
    else:
        print("Μπράβο, βρήκες δύο ίδιες! Συνέχισε την καλή προσπάθεια!")
    time.sleep(5)