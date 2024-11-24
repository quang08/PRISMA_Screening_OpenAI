# Abstract Classification Pipeline

This project provides a pipeline for parsing XML files containing academic abstracts, classifying them into predefined categories using OpenAI’s GPT-based model, and exporting the results to a CSV file. The project is modular, with distinct scripts handling parsing, classification, and data export.

## Features

- XML Parsing: Extracts relevant data (e.g., title, abstract, metadata) from structured XML files.
- Classification: Uses OpenAI’s GPT model to classify abstracts into predefined categories.
- Batch Processing: Handles large datasets in batches to optimize API usage and processing time.
- Export Functionality: Saves the processed data into a structured CSV format for further analysis.

## Project Structure

```
├── config/
│   ├── settings.py   # Configuration for input/output paths
├── data/
│   ├── raw/          # Directory for raw XML input files
│   ├── processed/    # Directory for processed CSV output files
├── scripts/
│   ├── parse_xml.py  # Script for parsing XML into a DataFrame
│   ├── classify.py   # Script for classifying abstracts
│   ├── export_csv.py # Script for exporting data to CSV
├── main.py           # Main pipeline script orchestrating all steps
├── README.md         # Documentation (this file)
```

## Setup Instructions

**1. Prerequisites**

- Python 3.8+
- API key from OpenAI (stored as an environment variable OPENAI_API_KEY)

**2. Install Dependencies**

Install the required Python libraries:
```
pip install -r requirements.txt
```

**3. Directory Setup**

Ensure the following directories exist:
- data/raw/: Place your input XML files here.
- data/processed/: Output CSV files will be saved here.

**4. Environment Variables**

Set the OPENAI_API_KEY environment variable with your OpenAI API key:

export OPENAI_API_KEY='your_openai_api_key'

**Usage**

**1. Run the Pipeline**

Execute the main.py script to run the entire pipeline:

```
python main.py
```

**2. Output**

- The processed data will be saved in data/processed/output.csv.

## Files Description

### main.py

The orchestrator script for the pipeline:
1. Parses XML files into a Pandas DataFrame.
2. Classifies abstracts into categories using OpenAI API.
3. Exports the results to a CSV file.

### scripts/parse_xml.py

- Parses structured XML files and extracts:
- Title
- Abstract
- Metadata (e.g., keywords)
- Outputs a Pandas DataFrame.

### scripts/classify.py

- Processes abstracts in batches using OpenAI API.
- Includes:
  - Normalization: Cleans category names to avoid duplicates.
  - Retry Logic: Handles API rate limits and other errors.
  - Categories:
    - Challenges and Proposed Solutions
    - Factors Influencing Prediction Accuracy
    - Impact on Teaching
    - Performance of Prediction Methods
    - Student's Score Prediction Methods
    - Excluded Studies for Screening Phase

### scripts/export_csv.py

- Exports the processed DataFrame to a CSV file.

### config/settings.py

- Specifies paths for raw input (RAW_DATA_PATH) and processed output (PROCESSED_DATA_PATH).

## Example Workflow

1. Input: Place your XML file (e.g., data/raw/abstracts.xml) in the data/raw/ directory.
2.	Run the Pipeline:

```
python main.py
```


3. Output: Check the data/processed/output.csv file for results.
