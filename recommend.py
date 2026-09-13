import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer, util


# -----------------------------
# Load repository data
# -----------------------------

df = pd.read_csv(
    r"C:\Users\ayush\PROJECTS\Github-Recommender\Data\repositories.csv"
)


# -----------------------------
# Load saved embeddings
# -----------------------------

embeddings = np.load(
    r"C:\Users\ayush\PROJECTS\Github-Recommender\Data\embeddings.npy"
)


# -----------------------------
# Load embedding model
# -----------------------------

model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


# -----------------------------
# Detect programming language
# -----------------------------

def detect_language(query):

    query = query.lower()

    languages = [
        "python",
        "javascript",
        "typescript",
        "java",
        "c++",
        "c#",
        "go",
        "rust",
        "kotlin",
        "swift",
        "php"
    ]

    for language in languages:

        if language in query:
            return language

    return None


# -----------------------------
# Calculate keyword bonus
# -----------------------------

def calculate_keyword_bonus(query, repo_text):

    query = query.lower()
    repo_text = repo_text.lower()

    stop_words = {
        "i", "want", "a", "an", "the",
        "for", "me", "find", "project",
        "using", "with", "please"
    }

    words = [
        word.strip(".,!?;:()[]{}\"'")
        for word in query.split()
    ]

    words = [
        word
        for word in words
        if word not in stop_words and len(word) > 2
    ]

    bonus = 0

    # Check important 2-word concepts
    for i in range(len(words) - 1):

        phrase = " ".join(words[i:i + 2])

        if phrase in repo_text:
            bonus += 0.10

    # Check individual meaningful words
    for word in words:

        if word in repo_text:
            bonus += 0.01

    return bonus
# -----------------------------
# Search repositories
# -----------------------------

def search_repositories(query, top_k=5):

    query_embedding = model.encode(query)

    similarities = util.cos_sim(
        query_embedding,
        embeddings
    )[0]

    requested_language = detect_language(query)

    scored_results = []

    for idx in range(len(df)):

        semantic_score = similarities[idx].item()

        language_bonus = 0

        repo_text = (
            str(df.iloc[idx]["name"]) + " " +
            str(df.iloc[idx]["description"]) + " " +
            str(df.iloc[idx]["topics"]) + " " +
            str(df.iloc[idx]["readme"])
        )

        keyword_bonus = calculate_keyword_bonus(
            query,
            repo_text
        )

        repo_language = df.iloc[idx]["language"]

        if (
            requested_language is not None
            and pd.notna(repo_language)
            and repo_language.lower() == requested_language
        ):
            language_bonus = 0.10

        final_score = (
            semantic_score
            + language_bonus
            + keyword_bonus
        )

        scored_results.append(
            (
                idx,
                final_score,
                semantic_score,
                keyword_bonus
            )
        )

    scored_results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    results = []

    for (
        idx,
        final_score,
        semantic_score,
        keyword_bonus
    ) in scored_results[:top_k]:

        results.append({

            "name": df.iloc[idx]["name"],

            "description": df.iloc[idx]["description"],

            "language": (
                df.iloc[idx]["language"]
                if pd.notna(df.iloc[idx]["language"])
                else "Not specified"
            ),

            "stars": int(df.iloc[idx]["stars"]),

            "url": df.iloc[idx]["url"],

            "similarity": round(
                semantic_score * 100,
                2
            ),

            "keyword_bonus": round(
                keyword_bonus * 100,
                2
            ),

            "score": round(
                final_score * 100,
                2
            )
        })

    return results