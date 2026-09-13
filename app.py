from recommend import search_repositories


print("=" * 50)
print("       GitHub Repository Recommender")
print("=" * 50)

query = input("\nWhat kind of repository are you looking for?\n> ")

results = search_repositories(query)

print("\nTop Recommendations:\n")

for i, repo in enumerate(results, start=1):

    print(f"{i}. {repo['name']}")
    print(f"   Description: {repo['description']}")
    print(f"   Language: {repo['language']}")
    print(f"   Stars: {repo['stars']}")
    print(f"   Similarity: {repo['similarity']}%")
    print(f"   URL: {repo['url']}")
    print()