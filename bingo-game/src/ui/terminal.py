# src/ui/terminal.py

def ask_card_numbers(rows=3, cols=5, min_n=1, max_n=75):
    print(f"Enter your {rows*cols} numbers (between {min_n} and {max_n}), no duplicates.")
    numbers = []
    while len(numbers) < rows * cols:
        try:
            value = int(input(f"Number {len(numbers)+1}: "))
        except ValueError:
            print("Not a number, try again.")
            continue

        if value < min_n or value > max_n:
            print("Out of range, try again.")
            continue
        if value in numbers:
            print("Duplicate, try again.")
            continue

        numbers.append(value)
    return numbers

