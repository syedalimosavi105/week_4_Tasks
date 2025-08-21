import requests

def fetch_jokes(amount=5):
    """
    Fetch `amount` jokes from JokeAPI (https://v2.jokeapi.dev).
    Returns a list of joke objects (may be empty on error).
    """
    url = f"https://v2.jokeapi.dev/joke/Any?amount={amount}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        # API returns either {"jokes":[...]} or a single joke object
        jokes = data.get("jokes") if isinstance(data, dict) and "jokes" in data else [data]
        return jokes
    except requests.RequestException as e:
        print("Network or request error:", e)
        return []

def print_jokes(jokes):
    if not jokes:
        print("No jokes to show.")
        return
    for i, j in enumerate(jokes, start=1):
        print(f"\nJoke #{i}:")
        # two types: "single" or "twopart"
        if j.get("type") == "single":
            print(j.get("joke"))
        else:
            print(j.get("setup"))
            print(j.get("delivery"))

if __name__ == "__main__":
    try:
        n = int(input("How many jokes do you want (1-10)? ").strip() or "5")
        if n < 1: n = 1
        if n > 10: n = 10
    except ValueError:
        n = 5

    jokes = fetch_jokes(amount=n)
    print_jokes(jokes)