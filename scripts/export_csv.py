import pandas as pd
from config.settings import PROCESSED_DATA_PATH

def export_to_csv(data, output_path):
    data.to_csv(output_path, index=False)
    print(f'Data successfully exported to {output_path}')

# if __name__ == "__main__":
#     classified_data = pd.read_csv('data/processed/classified_data.csv')
#     export_to_csv(classified_data, PROCESSED_DATA_PATH)