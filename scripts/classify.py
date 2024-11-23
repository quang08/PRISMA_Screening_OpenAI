from openai import OpenAI
from tqdm import tqdm
import time
import logging
import os

api_key = os.getenv("OPENAI_API_KEY", "").strip()

client = OpenAI(api_key=api_key)

def classify_row(row, max_retries=5):
    if not isinstance(row['Abstract'], str) or not row['Abstract'].strip():
        return "Excluded Studies for Screening Phase"

    prompt = f"""
    You are a research assistant. Classify the following study abstract into one of these categories:
    - Challenges and Proposed Solutions
    - Factors Influencing Prediction Accuracy
    - Impact on Teaching
    - Performance of Prediction Methods
    - Student's Score Prediction Methods
    If the abstract does not fit any of these categories, classify it as "Excluded Studies for Screening Phase".
    
    Abstract: {row['Abstract']}
    
    Your response should only be the category name.
    """

    retries = 0
    backoff = 1

    while retries < max_retries:
        try:
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="gpt-3.5-turbo",
            )
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"Error during classification: {e}. Retrying in {backoff} seconds...")

        retries += 1
        time.sleep(backoff)
        backoff *= 2  # Double the backoff time
    
    return "Excluded Studies for Screening Phase"

def classify_in_batches(df, batch_size=10):
    logging.info(f"Starting classification of {len(df)} records in batches of {batch_size}")
    results = []
    for i in tqdm(range(0, len(df), batch_size)):
        batch = df.iloc[i:i+batch_size]
        batch_results = batch.apply(classify_row, axis=1)
        results.extend(batch_results)
        time.sleep(1) # Delay
    df["Group"] = results
    return df