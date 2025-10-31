from src.game.card import BingoCard
from src.game.draw import NumberDrawer
from src.game.score import ScoreTracker
from src.ui.terminal import ask_card_numbers

def main():
    choice = input("Do you want to enter your own numbers? (y/n): ").lower()
    if choice == "y":
        nums = ask_card_numbers()
        card = BingoCard(numbers=nums)
    else:
        card = BingoCard()

    drawer = NumberDrawer()
    score = ScoreTracker()

    print("\nYour card:")
    print(card)

    while True:
        input("Press Enter to draw a number...")
        n = drawer.draw_number()
        if n is None:
            print("No more numbers. Game over.")
            break

        print(f"\nNumber drawn: {n}")
        card.mark_number(n)

        # update score
        score.update_score(card.marked)

        print("\nCurrent card:")
        print(card)
        print(f"Score: {score.get_score()}")

        if score.has_bingo:
            print("BINGO!! 🎉")
            break

if __name__ == "__main__":
    main()
