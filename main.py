import requests
import pandas as pd
import base64


# GitHub repository search API
url = "https://api.github.com/search/repositories"


# Search parameters
params = {
    "q": "machine learning",
    "sort": "stars",
    "order": "desc",
    "per_page": 10
}


# Send request to GitHub
response = requests.get(url, params=params)

print("Status:", response.status_code)

data = response.json()


repositories = []


# Loop through repositories
for repo in data["items"]:

    # Get repository name
    repo_name = repo["full_name"]

    # GitHub README API
    readme_url = f"https://api.github.com/repos/{repo_name}/readme"

    readme_response = requests.get(readme_url)

    readme_text = ""

    if readme_response.status_code == 200:

        readme_data = readme_response.json()

        # GitHub returns README content encoded in Base64
        encoded_content = readme_data["content"]

        readme_text = base64.b64decode(
            encoded_content
        ).decode("utf-8", errors="ignore")

    else:
        print(f"README not found: {repo_name}")


    # Create repository record
    repository = {
        "name": repo["full_name"],
        "description": repo["description"],
        "readme": readme_text,
        "stars": repo["stargazers_count"],
        "forks": repo["forks_count"],
        "language": repo["language"],
        "topics": repo["topics"],
        "updated_at": repo["updated_at"],
        "license": repo["license"]["name"] if repo["license"] else None,
        "url": repo["html_url"]
    }

    repositories.append(repository)


# Convert to DataFrame
df = pd.DataFrame(repositories)


print("\nDataset:")
print(df)


# Save dataset
df.to_csv("data/repositories.csv", index=False)


print("\nDataset saved successfully!")