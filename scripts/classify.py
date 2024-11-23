from config.settings import GROUPS, OPEN_API_KEY
import pandas as pd
import openai
from tqdm import tqdm
import time
import logging

openai.api_key = OPEN_API_KEY

def classify_row(row):
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
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are a research assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error during classification: {e}")
        return "Excluded Studies for Screening Phase"

def classify_in_batches(df, batch_size=5):
    logging.info(f"Starting classification of {len(df)} records in batches of {batch_size}")
    results = []
    for i in tqdm(range(0, len(df), batch_size)):
        batch = df.iloc[i:i+batch_size]
        batch_results = batch.apply(classify_row, axis=1)
        results.extend(batch_results)
        time.sleep(1) # Delay
    df["Group"] = results
    return df