from config.settings import GROUPS
import pandas as pd
from tqdm import tqdm

def classify(data):
    def classify_row(row):
        if not isinstance(row['Abstract'], str):
            return "Excluded Studies for Screening Phase"
        
        abstract = row['Abstract'].lower()
        
        # Create a scoring system for better classification
        scores = {group: 0 for group in GROUPS}
        
        # Challenges and Solutions
        if any(word in abstract for word in ["challenge", "solution", "problem", "resolve"]):
            scores["Challenges and Proposed Solutions"] += 1
        
        # Accuracy
        if any(word in abstract for word in ["accuracy", "precision", "performance", "error rate"]):
            scores["Factors Influencing Prediction Accuracy"] += 1
        
        # Get the group with highest score
        max_score = max(scores.values())
        if max_score == 0:
            return "Excluded Studies for Screening Phase"
        
        return max(scores.items(), key=lambda x: x[1])[0]
    
    tqdm.pandas()
    data["Group"] = data.progress_apply(classify_row, axis=1)

    return data

# if __name__ == '__main__':
#     df = pd.read_csv('data/processed/intermediate_data.csv') #?
#     classified_data = classify(df)
#     print(classified_data['Group'].value_counts())