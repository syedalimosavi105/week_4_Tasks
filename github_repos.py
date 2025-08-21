import requests

def fetch_repos(username, token=None):
    repos = []
    page = 1
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'

    while True:
        params = {'per_page': 100, 'page': page}
        url = f"https://api.github.com/users/{username}/repos"
        try:
            r = requests.get(url, headers=headers, params=params, timeout=10)
        except requests.RequestException as e:
            print("Network error:", e)
            return repos

        if not r.ok:
            print(f"Error fetching repos: status {r.status_code}")
            try:
                print("Message:", r.json().get("message"))
            except Exception:
                pass
            return repos

        data = r.json()
        if not data:
            break
        repos.extend(data)
        page += 1

    return repos

def print_repos(repos):
    if not repos:
        print("No repositories found.")
        return
    print(f"Found {len(repos)} repos:\n")
    for repo in repos:
        name = repo.get("name")
        desc = repo.get("description") or ""
        stars = repo.get("stargazers_count", 0)
        forks = repo.get("forks_count", 0)
        url = repo.get("html_url")
        print(f"- {name} | ⭐ {stars} | Forks: {forks}")
        if desc:
            print(f"    {desc}")
        print(f"    {url}\n")

if __name__ == "__main__":
    username = input("Enter GitHub username (press Enter for syedalimosavi105): ").strip() or "syedalimosavi105"
    use_token = input("Do you want to use a GitHub token? (y/N): ").strip().lower()
    token = None
    if use_token == 'y':
        token = input("Paste your GitHub Personal Access Token (will not be stored): ").strip() or None

    repos = fetch_repos(username, token=token)
    print_repos(repos)
