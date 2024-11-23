from scripts.parse_xml import parse_xml_to_df
from scripts.classify import classify
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
        df = parse_xml_to_df(RAW_DATA_PATH)
        
        logging.info("Classifying data...")
        classified_data = classify(df)
        
        logging.info("Exporting to CSV...")
        export_to_csv(classified_data, PROCESSED_DATA_PATH)
        
        logging.info("Pipeline finished successfully!")
    except Exception as e:
        logging.error(f"Pipeline failed: {str(e)}")
        raise

if __name__ == "__main__":
    run_pipeline()
