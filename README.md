# Abstract Classification Pipeline

This project provides a pipeline for parsing XML files containing academic abstracts, classifying them into predefined categories using OpenAI’s GPT-based model, and exporting the results to a CSV file. The project is modular, with distinct scripts handling parsing, classification, and data export.

## Problem Justification

Systematic review and classification of academic abstracts are critical yet time-consuming tasks in research. Researchers often spend a significant amount of time screening and categorizing abstracts, making the process tedious and prone to errors. Leveraging large language models (LLMs) such as OpenAI's GPT provides a promising solution to streamline this workflow, offering high accuracy and reliability.

### Supporting Research

1. **Accuracy and Efficiency of LLMs in Abstract Screening**  
   A study highlighted that large language models (LLMs), particularly GPT-4o, GPT-4T, and Claude3-Opus, achieved impressive accuracies of 97% to 98% in abstract screening tasks, closely matching human performance levels of 96% to 98%, while maintaining low error rates. This demonstrates the reliability of LLMs in automating classification processes with minimal compromise in quality.  
   **Source:** [MedRxiv Study](https://www.medrxiv.org/content/10.1101/2024.10.01.24314702v1.full)

2. **Enhanced Sensitivity and Precision**  
   Research has shown that LLMs can outperform humans in terms of sensitivity and precision in classification tasks. Specifically, LLMs achieved a maximum sensitivity of 1.000 compared to the maximum human sensitivity of 0.775. This underscores the potential of LLMs to reduce errors and capture nuanced classifications that humans might miss.  
   **Source:** [Arxiv Study](https://arxiv.org/abs/2411.02451)

3. **Screening Articles for Systematic Reviews with ChatGPT**  
   A practical study investigated ChatGPT's performance in screening articles for systematic reviews. The results demonstrated that ChatGPT could effectively reduce the time and cognitive load required for manual screening, providing a scalable and efficient solution for research teams.  
   **Source:** [ScienceDirect Study](https://www.sciencedirect.com/science/article/pii/S2590118424000303)

4. **Methodological Insights into ChatGPT's Screening Performance**  
   Additional methodological insights reveal that ChatGPT consistently delivers high-quality classifications for systematic reviews, often aligning with human judgments. This supports its use as an aid or even a replacement for certain aspects of human screening.  
   **Source:** [ResearchGate Study](https://www.researchgate.net/publication/379336186_Methodological_insights_into_ChatGPT's_screening_performance_in_systematic_reviews)

### Implications

These findings justify the adoption of LLM-based solutions in abstract classification pipelines. The significant overlap in performance between LLMs and humans, along with the efficiency gains, provides a strong rationale for integrating tools like GPT into academic workflows. This project aims to leverage these insights to deliver a robust, scalable, and efficient pipeline for abstract classification.

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
