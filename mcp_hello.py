from fastmcp import FastMCP
import random
import sys

print(sys.executable, file=sys.stderr)

mcp = FastMCP("hello_server")


@mcp.tool()
async def get_greetings(name: str) -> str:
    """Greet the user.
    Args:
        name: The name of the user
    """
    return f"Hi Mr.{name}. I'm your first MCP server!!"


@mcp.tool()
async def get_random_joke() -> str:
    """Return a random joke."""
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "Why don't eggs tell jokes? They'd crack each other up!",
        "What do you call a fake noodle? An impasta!",
        "Why did the bicycle fall over? Because it was two-tired!",
        "What do you call cheese that isn't yours? Nacho cheese!",
        "Why can't you give Elsa a balloon? Because she'll let it go!",
        "I'm reading a book about anti-gravity. It's impossible to put down!",
        "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!",
    ]
    return random.choice(jokes)


@mcp.tool()
async def get_random_quote() -> str:
    """Return a random inspirational quote."""
    quotes = [
        "The only way to do great work is to love what you do. – Steve Jobs",
        "In the middle of every difficulty lies opportunity. – Albert Einstein",
        "It does not matter how slowly you go as long as you do not stop. – Confucius",
        "Life is what happens when you're busy making other plans. – John Lennon",
        "The future belongs to those who believe in the beauty of their dreams. – Eleanor Roosevelt",
        "Success is not final, failure is not fatal: it is the courage to continue that counts. – Winston Churchill",
        "You miss 100% of the shots you don't take. – Wayne Gretzky",
        "Whether you think you can or you think you can't, you're right. – Henry Ford",
        "The best time to plant a tree was 20 years ago. The second best time is now. – Chinese Proverb",
        "Believe you can and you're halfway there. – Theodore Roosevelt",
    ]
    return random.choice(quotes)


@mcp.tool()
async def get_random_number(min_value: int = 1, max_value: int = 100) -> str:
    """Return a random number between min_value and max_value.
    Args:
        min_value: The minimum value (default: 1)
        max_value: The maximum value (default: 100)
    """
    if min_value > max_value:
        return f"Error: min_value ({min_value}) cannot be greater than max_value ({max_value})."
    number = random.randint(min_value, max_value)
    return f"Your random number between {min_value} and {max_value} is: {number}"


@mcp.tool()
async def get_random_fact() -> str:
    """Return a random interesting fact."""
    facts = [
        "Honey never spoils. Archaeologists have found 3,000-year-old honey in Egyptian tombs that was still edible.",
        "A group of flamingos is called a 'flamboyance'.",
        "Octopuses have three hearts, blue blood, and can taste with their suckers.",
        "The Eiffel Tower can be 15 cm taller during the summer due to thermal expansion.",
        "Bananas are berries, but strawberries are not — botanically speaking.",
        "A day on Venus is longer than a year on Venus.",
        "The shortest war in history lasted only 38–45 minutes — between Britain and Zanzibar in 1896.",
        "Cleopatra lived closer in time to the Moon landing than to the construction of the Great Pyramid.",
        "There are more possible iterations of a game of chess than there are atoms in the observable universe.",
        "Sharks are older than trees — they've existed for over 450 million years.",
    ]
    return random.choice(facts)


if __name__ == "__main__":
    mcp.run()