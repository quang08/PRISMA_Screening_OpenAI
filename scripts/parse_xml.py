import xml.etree.ElementTree as ET
import pandas as pd
from config.settings import RAW_DATA_PATH

def parse_xml_to_dataframe(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        records = []
        for record in root.findall(".//record"):
            # Extract title
            title_element = record.find(".//titles/title")
            if title_element is not None:
                title = title_element.text

            # Extract abstract
            abstract_element = record.find(".//abstract")
            if abstract_element is not None:
                abstract = abstract_element.text

            # Extract metadata (optional, like keywords or database info)
            metadata = []
            keyword_elements = record.findall(".//keywords/keyword")
            for keyword in keyword_elements:
                if keyword is not None and keyword.text:
                    metadata.append(keyword.text)
            metadata = ", ".join(metadata) if metadata else None
            
            records.append({
                "Title": title.text if title is not None else "No Title",
                "Abstract": abstract.text if abstract is not None else "No Abstract",
                "Metadata": metadata.text if metadata is not None else "No Metadata"
            })
        
        return pd.DataFrame(records)
    
    except FileNotFoundError:
        print(f"Error: File {xml_file} not found")
        raise
    except ET.ParseError:
        print(f"Error: Unable to parse XML file {xml_file}")
        raise

if __name__ == "__main__":
    df = parse_xml_to_dataframe(RAW_DATA_PATH)
    print(df.head())