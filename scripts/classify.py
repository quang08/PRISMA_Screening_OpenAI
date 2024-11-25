from openai import OpenAI
from tqdm import tqdm
import time
import logging
import os
import pandas as pd

api_key = os.getenv("OPENAI_API_KEY", "").strip()

client = OpenAI(api_key=api_key)

VALID_CATEGORIES = [
    "Challenges and Proposed Solutions",
    "Factors Influencing Prediction Accuracy",
    "Impact on Teaching",
    "Performance of Prediction Methods",
    "Student's Score Prediction Methods",
    "Excluded Studies for Screening Phase"
]

def normalize_and_validate_group(group_name):
    group_name = group_name.strip()
    if group_name.startswith("-"):
        group_name = group_name[1:].strip()

    for valid_category in VALID_CATEGORIES:
        if group_name.lower() == valid_category.lower():
            return valid_category 

    return "Excluded Studies for Screening Phase"

def classify_batch(batch, max_retries=5):
    abstracts = batch["Abstract"].tolist()
    prompt = f"""
    Classify the following {len(batch)} abstracts into one of these **exact** categories:
    - Challenges and Proposed Solutions
    - Factors Influencing Prediction Accuracy
    - Impact on Teaching
    - Performance of Prediction Methods
    - Student's Score Prediction Methods
    - Excluded Studies for Screening Phase

    If none of these categories fit, classify as "Excluded Studies for Screening Phase".

    Provide exactly one classification per abstract, in the same order as the abstracts, separated by newlines.
    Do not create new categories or modify the given ones.

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
                model="gpt-4o-mini",
            )

            logging.info(f"Full response: {response}")

            # Extract and clean results
            results = response.choices[0].message.content.strip().split("\n")
            results = [normalize_and_validate_group(result) for result in results if result.strip()]

            # Handle mismatched results
            if len(results) != len(batch):
                logging.warning(f"Mismatch: Expected {len(batch)} results, got {len(results)}. Adjusting.")
                while len(results) < len(batch):
                    results.append("Excluded Studies for Screening Phase")
                results = results[:len(batch)]

            return results
        except Exception as e:
            logging.error(f"Error during batch classification: {e}. Retrying in {backoff} seconds...")
            retries += 1
            time.sleep(backoff)
            backoff *= 2 

    return ["Excluded Studies for Screening Phase"] * len(batch)


def classify_in_batches(df, batch_size=20, output_file="data/processed/output.csv"):
    if "ID" not in df.columns:
        df["ID"] = range(1, len(df) + 1)

    output_dir = os.path.dirname(output_file)
    os.makedirs(output_dir, exist_ok=True)

    if os.path.exists(output_file):
        logging.info(f"Loading existing output file: {output_file}")
        processed_df = pd.read_csv(output_file)
        processed_ids = set(processed_df["ID"])
    else:
        logging.info("No output file found. Starting fresh.")
        processed_df = pd.DataFrame(columns=df.columns.tolist() + ["Group"])
        processed_ids = set()

    logging.info(f"Starting classification of {len(df)} records in batches of {batch_size}")

    for i in tqdm(range(0, len(df), batch_size)):
        batch = df.iloc[i : i + batch_size]

        batch = batch[~batch["ID"].isin(processed_ids)]
        if batch.empty:
            continue

        logging.info(f"Processing batch starting at index {i}")

        # Classify the batch
        batch_results = classify_batch(batch)
        batch.loc[:, "Group"] = batch_results

        logging.info(f"Batch {i // batch_size + 1} DataFrame after classification:")
        logging.info("\n" + batch.to_string())

        processed_df = pd.concat([processed_df, batch], ignore_index=True)

        processed_df.to_csv(output_file, index=False)
        logging.info(f"Batch {i // batch_size + 1} results successfully exported to {output_file}")
        logging.info(f"Batch {i // batch_size + 1} completed successfully.")

    return processed_df