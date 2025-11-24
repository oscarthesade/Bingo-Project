from src.game.card import BingoCard
from src.game.draw import NumberDrawer
from src.game.score import ScoreTracker
from src.ui.terminal import ask_card_numbers


def main():
    """Main game loop for the Bingo game."""
    try:
        # Get user preference for card creation
        while True:
            choice = input("Do you want to enter your own numbers? (y/n): ").lower().strip()
            if choice in ['y', 'yes']:
                try:
                    nums = ask_card_numbers()
                    card = BingoCard(numbers=nums)
                    break
                except (ValueError, KeyboardInterrupt) as e:
                    print(f"\nError creating card: {e}")
                    retry = input("Would you like to try again? (y/n): ").lower().strip()
                    if retry not in ['y', 'yes']:
                        card = BingoCard()
                        print("Using a random card instead.")
                        break
            elif choice in ['n', 'no']:
                card = BingoCard()
                break
            else:
                print("Please enter 'y' for yes or 'n' for no.")

        # Initialize game components
        drawer = NumberDrawer()
        score = ScoreTracker()
        
        # Display high score if available
        high_score = score.get_high_score()
        if high_score > 0:
            print(f"\n🏆 High Score: {high_score}")

        print("\nYour card:")
        print(card)
        print("\n" + "="*50)

        # Main game loop
        while True:
            try:
                input("\nPress Enter to draw a number...")
                n = drawer.draw_number()
                
                if n is None:
                    print("\n🎲 No more numbers available. Game over!")
                    print(f"Final Score: {score.get_score()}")
                    break

                print(f"\n🎲 Number drawn: {n}")
                card.mark_number(n)

                # Update score
                score.update_score(card.marked)

                print("\nCurrent card:")
                print(card)
                print(f"📊 Score: {score.get_score()}")

                # Check for bingo
                if score.has_bingo:
                    print("\n" + "="*50)
                    print("🎉🎉🎉 BINGO!! 🎉🎉🎉")
                    print(f"🏆 Final Score: {score.get_score()}")
                    print("="*50)
                    break
                    
            except KeyboardInterrupt:
                print("\n\nGame interrupted by user.")
                print(f"Final Score: {score.get_score()}")
                break
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                print("Continuing game...")
                
    except KeyboardInterrupt:
        print("\n\nGame exited.")
    except Exception as e:
        print(f"\nFatal error: {e}")
        raise


if __name__ == "__main__":
    main()
