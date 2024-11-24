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
            title_element = record.find(".//titles/title/style")
            title = title_element.text if title_element is not None else "No Title"

            # Extract abstract
            abstract_element = record.find(".//abstract/style")
            abstract = abstract_element.text if abstract_element is not None else "No Abstract"

            # Extract metadata (optional, like keywords or database info)
            metadata = []
            keyword_elements = record.findall(".//keywords/keyword/style")
            for keyword in keyword_elements:
                if keyword is not None and keyword.text:
                    metadata.append(keyword.text)
            metadata = ", ".join(metadata) if metadata else "No Metadata"
            
            records.append({
                "Title": title,
                "Abstract": abstract,
                "Metadata": metadata
            })
        
        return pd.DataFrame(records)
    
    except FileNotFoundError:
        print(f"Error: File {xml_file} not found")
        raise
    except ET.ParseError:
        print(f"Error: Unable to parse XML file {xml_file}")
        raise

if __name__ == "__main__":
    # pd.set_option("display.max_colwidth", None)  
    # pd.set_option("display.max_columns", None)  
    # pd.set_option("display.width", 1000)     

    df = parse_xml_to_dataframe(RAW_DATA_PATH)
    print(df.head(1))