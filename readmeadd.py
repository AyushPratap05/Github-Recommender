import requests
import pandas as pd
import base64
import time
import os
from dotenv import load_dotenv


load_dotenv()

token = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}

# Load our existing dataset
df = pd.read_csv("Data/repositories.csv")

# Store README text here
readmes = []


for index, row in df.iterrows():

    repo_name = row["name"]

    # README already exists
    if pd.notna(row["readme"]) and row["readme"] != "":
        print(f"{index + 1}/{len(df)} - Already have README: {repo_name}")
        continue

    print(f"{index + 1}/{len(df)} - {repo_name}")

    readme_url = f"https://api.github.com/repos/{repo_name}/readme"

    try:
        response = requests.get(readme_url, headers=headers)

        if response.status_code == 200:

            data = response.json()

            encoded_content = data["content"]

            readme_text = base64.b64decode(
                encoded_content
            ).decode("utf-8", errors="ignore")

        else:
             print(
              f"Failed: {repo_name} | "
             f"Status: {response.status_code}")
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