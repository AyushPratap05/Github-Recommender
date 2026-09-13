import requests
import pandas as pd
import base64
import time
import os
from dotenv import load_dotenv


# Load .env file
load_dotenv()

# Get GitHub token
token = os.getenv("GITHUB_TOKEN")

if not token:
    raise ValueError("GITHUB_TOKEN not found in .env file")


# Headers for authenticated GitHub API requests
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}


# Load our EXISTING dataset
df = pd.read_csv("Data/repositories.csv")


# Make sure README column exists
if "readme" not in df.columns:
    df["readme"] = ""


# Process each existing repository
for index, row in df.iterrows():

    repo_name = row["name"]

    # ------------------------------------------------
    # 1. If README already exists, keep it
    # ------------------------------------------------
    if pd.notna(row["readme"]) and str(row["readme"]).strip() != "":
        print(
            f"{index + 1}/{len(df)} - "
            f"Already have README: {repo_name}"
        )
        continue


    # ------------------------------------------------
    # 2. Fetch README only if it is missing
    # ------------------------------------------------
    print(
        f"{index + 1}/{len(df)} - "
        f"Fetching README: {repo_name}"
    )

    readme_url = f"https://api.github.com/repos/{repo_name}/readme"

    try:

        response = requests.get(
            readme_url,
            headers=headers,
            timeout=15
        )


        # README successfully found
        if response.status_code == 200:

            readme_data = response.json()

            encoded_content = readme_data["content"]

            readme_text = base64.b64decode(
                encoded_content
            ).decode("utf-8", errors="ignore")

            df.at[index, "readme"] = readme_text

            print("   ✓ README added")


        # README does not exist
        elif response.status_code == 404:

            print("   - README not found")


        # Rate limit / forbidden
        elif response.status_code == 403:

            print("   ⚠️ 403 Forbidden / rate limit")
            print("   Stopping to avoid more failed requests.")
            break


        # Other errors
        else:

            print(
                f"   ⚠️ Failed with status "
                f"{response.status_code}"
            )


    except requests.RequestException as e:

        print(f"   ⚠️ Request error: {e}")


    # Small delay
    time.sleep(0.2)


    # Save progress after every repository
    df.to_csv(
        "Data/repositories.csv",
        index=False
    )


print("\nProcess completed.")

print(
    "README available:",
    (df["readme"].fillna("").str.strip() != "").sum()
)

print(
    "README missing:",
    (df["readme"].fillna("").str.strip() == "").sum()
)

print("Dataset shape:", df.shape)