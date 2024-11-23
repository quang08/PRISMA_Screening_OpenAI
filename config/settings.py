import os 

# File paths
RAW_DATA_PATH = 'data/raw/ToBeScreened.xml' 
PROCESSED_DATA_PATH = 'data/processed/output.csv'

# Research Questions Groups
GROUPS = [
    "Challenges and Proposed Solutions",
    "Factors Influencing Prediction Accuracy",
    "Impact on Teaching",
    "Performance of Prediction Methods",
    "Student's Score Prediction Methods",
    "Excluded Studies for Screening Phase"
]

# OpenAI API Key
OPEN_API_KEY = os.getenv('OPENAI_API_KEY')