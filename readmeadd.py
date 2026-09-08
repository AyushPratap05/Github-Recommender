import requests
import pandas as pd
import base64
import time


# Load our existing dataset
df = pd.read_csv("Data/repositories.csv")

# Store README text here
readmes = []


for index, repo_name in enumerate(df["name"]):

    print(f"{index + 1}/{len(df)} - {repo_name}")

    readme_url = f"https://api.github.com/repos/{repo_name}/readme"

    try:
        response = requests.get(readme_url)

        if response.status_code == 200:

            data = response.json()

            encoded_content = data["content"]

            readme_text = base64.b64decode(
                encoded_content
            ).decode("utf-8", errors="ignore")

        else:
            print(f"README not found: {repo_name}")
            readme_text = ""

    except Exception as e:

        print(f"Error: {repo_name} -> {e}")
        readme_text = ""

    readmes.append(readme_text)

    # Small pause between requests
    time.sleep(0.1)


# Add README as a new column
df["readme"] = readmes


# Save the enriched dataset
df.to_csv("Data/repositories.csv", index=False)


print("\nREADME collection completed!")
print("Dataset shape:", df.shape)