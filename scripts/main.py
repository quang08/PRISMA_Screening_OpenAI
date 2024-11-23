import sys
import os
# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.parse_xml import parse_xml_to_dataframe
from scripts.classify import classify_in_batches
from scripts.export_csv import export_to_csv
from config.settings import RAW_DATA_PATH, PROCESSED_DATA_PATH
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_pipeline():
    logging.info("Starting pipeline...")
    
    try:
        logging.info("Parsing XML...")
        df = parse_xml_to_dataframe(RAW_DATA_PATH)
        
        logging.info("Classifying data...")
        classified_data = classify_in_batches(df)
        
        logging.info("Exporting to CSV...")
        export_to_csv(classified_data, PROCESSED_DATA_PATH)
        
        logging.info("Pipeline finished successfully!")
    except Exception as e:
        logging.error(f"Pipeline failed: {str(e)}")
        raise

if __name__ == "__main__":
    run_pipeline()
