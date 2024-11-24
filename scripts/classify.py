from openai import OpenAI
from tqdm import tqdm
import time
import logging
import os
import pandas as pd

api_key = os.getenv("OPENAI_API_KEY", "").strip()

client = OpenAI(api_key=api_key)

def classify_batch(batch, max_retries=5):
    abstracts = batch["Abstract"].tolist()
    prompt = f"""
    Classify the following abstracts into these categories:
    - Challenges and Proposed Solutions
    - Factors Influencing Prediction Accuracy
    - Impact on Teaching
    - Performance of Prediction Methods
    - Student's Score Prediction Methods
    If none of these categories fit, classify as "Excluded Studies for Screening Phase".

    Provide one classification per abstract, in the same order as the abstracts, separated by newlines.

    Abstracts:
    """
    for idx, abstract in enumerate(abstracts):
        prompt += f"\n{idx + 1}. {abstract if isinstance(abstract, str) else 'No Abstract'}"

    retries = 0
    backoff = 1
    while retries < max_retries:
        try:
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="gpt-3.5-turbo",
            )

            # Log token usage
            print(f"Tokens used: {response.usage.total_tokens}")

            # Extract and clean results
            results = response.choices[0].message.content.strip().split("\n")
            results = [result.split(": ", 1)[-1].strip() for result in results if ": " in result]

            # Ensure the number of results matches the batch size
            if len(results) != len(batch):
                raise ValueError(f"Mismatch: Expected {len(batch)} results, got {len(results)}")

            return results
        except Exception as e:
            print(f"Error during batch classification: {e}. Retrying in {backoff} seconds...")
            retries += 1
            time.sleep(backoff)
            backoff *= 2  # Exponential backoff

    # Return "Excluded" for all abstracts if retries fail
    return ["Excluded Studies for Screening Phase"] * len(batch)


def classify_in_batches(df, batch_size=50, intermediate_file="data/processed/intermediate.csv"):
    """Classify records in batches, saving progress after each batch."""
    if "ID" not in df.columns:
        df["ID"] = range(1, len(df) + 1)

    if os.path.exists(intermediate_file):
        logging.info(f"Loading intermediate file: {intermediate_file}")
        processed_df = pd.read_csv(intermediate_file)
        processed_ids = set(processed_df["ID"])
    else:
        logging.info("No intermediate file found. Starting fresh.")
        processed_df = pd.DataFrame(columns=df.columns.tolist() + ["Group"])
        processed_ids = set()

    logging.info(f"Starting classification of {len(df)} records in batches of {batch_size}")
    for i in tqdm(range(0, len(df), batch_size)):
        batch = df.iloc[i : i + batch_size]
        batch = batch[~batch["ID"].isin(processed_ids)]  # Skip already processed
        if batch.empty:
            continue

        logging.info(f"Processing batch starting at index {i}")
        batch_results = classify_batch(batch, client=client)
        batch["Group"] = batch_results

        # Save progress
        processed_df = pd.concat([processed_df, batch], ignore_index=True)
        processed_df.to_csv(intermediate_file, index=False)
        logging.info(f"Saved progress to {intermediate_file}")

        time.sleep(20)

    return processed_df