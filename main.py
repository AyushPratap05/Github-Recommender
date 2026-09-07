import requests
import pandas as pd


# GitHub API
url = "https://api.github.com/search/repositories"


# Topics we want to collect
search_queries = [
    "machine learning",
    "deep learning",
    "computer vision",
    "natural language processing",
    "generative AI",
    "data science",
    "web development",
    "data analysis",
    "reinforcement learning",
    "MLOps"
]


repositories = []


# Search each category
for query in search_queries:

    print(f"\nSearching: {query}")

    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": 50
    }

    response = requests.get(url, params=params)

    print("Status:", response.status_code)

    data = response.json()

    for repo in data["items"]:

        repository = {
            "name": repo["full_name"],
            "description": repo["description"],
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


# Remove duplicate repositories
df = df.drop_duplicates(subset="name")


print("\nFinal dataset:")
print(df.shape)

print("\nRepositories by language:")
print(df["language"].value_counts())


# Save dataset
df.to_csv("Data/repositories.csv", index=False)

print("\nDataset saved successfully!")