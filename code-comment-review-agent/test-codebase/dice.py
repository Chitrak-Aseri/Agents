import random
import math

def roll_dice(sides=6):
    """Roll a dice with specified number of sides.
    
    Args:
        sides (int): Number of sides on the dice (default 6)
    
    Returns:
        int: Random integer between 1 and sides (inclusive)
    """
    return random.randint(1, sides)

def factorial(n):
    """Calculate the factorial of a non-negative integer.
    
    Args:
        n (int): Number to calculate factorial for
    
    Returns:
        int: Factorial of n
    
    Raises:
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("Factorial is undefined for negative numbers.")
    if n == 0:
        return 1
    return n * factorial(n - 1)

def draw_card():
    """Draw a random playing card from a standard 52-card deck.
    
    Returns:
        str: String representation of the drawn card (e.g. 'Queen of Hearts')
    """
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    
    rank = random.choice(ranks)
    suit = random.choice(suits)
    
    return f"{rank} of {suit}"

def calculate_pi(terms=1000):
    """Estimate the value of π using the Leibniz formula.
    
    Args:
        terms (int): Number of terms to use in the approximation (default 1000)
    
    Returns:
        float: Approximation of π
    """
    pi_estimate = 0
    for i in range(terms):
        # Leibniz formula for π: alternating series of odd denominators
        pi_estimate += ((-1) ** i) / (2 * i + 1)
    return 4 * pi_estimate

def simulate_game():
    """Simulate a game that rolls dice, calculates factorial, draws card, and estimates π.
    
    Prints results of all operations to console.
    """
    dice_roll = roll_dice()
    fact_result = factorial(dice_roll)
    card = draw_card()
    pi_value = calculate_pi()
    
    print(f"Dice Roll: {dice_roll}")
    print(f"Factorial of {dice_roll}: {fact_result}")
    print(f"Drawn Card: {card}")
    print(f"Estimated Pi Value: {pi_value}")

if __name__ == "__main__":
    simulate_game()