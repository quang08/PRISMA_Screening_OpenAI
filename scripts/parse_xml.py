import xml.etree.ElementTree as ET
import pandas as pd
from config.settings import RAW_DATA_PATH

def parse_xml_to_df(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    records = []

    for record in root.findall("record"): 
        title = record.find('title') if record.title is not None else "No Title"
        abstract = record.find('abstract') if record.abstract is not None else "No Abstract"
        metadata = record.find('metadata') if record.metadata is not None else "No Metadata"

        records.append({
            "Title": title,
            "Abstract": abstract,
            "Metadata": metadata
        })

if __name__ == "__main__":
    df = parse_xml_to_df(RAW_DATA_PATH)
    print(df.head())