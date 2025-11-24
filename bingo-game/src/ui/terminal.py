# src/ui/terminal.py

def ask_card_numbers(rows=3, cols=5, min_n=1, max_n=75):
    """
    Prompt user to enter numbers for their Bingo card.
    
    Args:
        rows: Number of rows in the card (default: 3)
        cols: Number of columns in the card (default: 5)
        min_n: Minimum number allowed (default: 1)
        max_n: Maximum number allowed (default: 75)
    
    Returns:
        list: List of numbers entered by the user
    
    Raises:
        KeyboardInterrupt: If user interrupts input
    """
    total_numbers = rows * cols
    print(f"\nEnter your {total_numbers} numbers (between {min_n} and {max_n}), no duplicates.")
    print("You can type 'quit' at any time to cancel.\n")
    
    numbers = []
    while len(numbers) < total_numbers:
        try:
            user_input = input(f"Number {len(numbers)+1}/{total_numbers}: ").strip()
            
            # Allow user to quit
            if user_input.lower() in ['quit', 'q', 'exit']:
                raise KeyboardInterrupt("Card creation cancelled by user.")
            
            value = int(user_input)
            
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
            continue
        except KeyboardInterrupt:
            raise

        if value < min_n or value > max_n:
            print(f"❌ Number must be between {min_n} and {max_n}. Try again.")
            continue
            
        if value in numbers:
            print(f"❌ You already entered {value}. No duplicates allowed. Try again.")
            continue

        numbers.append(value)
        print(f"✓ Added {value}")
    
    print(f"\n✓ Card created successfully with {total_numbers} numbers!")
    return numbers

