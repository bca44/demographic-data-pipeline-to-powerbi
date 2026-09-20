# Demographic Data Pipeline & Power BI Dashboard

Hello! My name is Benjamin Andreasen. This repo is based on some consulting work I did. Obviously the data was sensitive, so I took great care to generate synthetic data that could be used as well as change the column names to hopefully obscure the original industry as well. 

## Dashboard Preview

<img width="1920" height="1080" alt="Screenshot 2026-09-20 031414" src="https://github.com/user-attachments/assets/c7b0c95d-2ba4-481d-8692-5049bcf5337f" />
<img width="1920" height="1080" alt="Screenshot 2026-09-20 031442" src="https://github.com/user-attachments/assets/1bf9cc47-0812-4c56-9a01-8dd58949d663" />

## Project Overview

I was given a data file with customer demographic information and asked to help my client understand their customer pool more in-depth.

I used the pandas library in Python to extract and clean the data. In an effort to pass this off completely to my non-technical clients, I researched and used PyInstaller to make a stand-alone executable that would run the extraction and cleaning script.

I was very proud of this step, until I learned that my clients run exclusively on Apple products, and due to some limitations I have not yet finished researching, my setup with PyInstaller did not allow me to create a Mac executable file. I am still working on that in the back of my brain somewhere.

After the data is processed, it is passed to Power BI, where it powers a simple, yet elegant demographic dashboard. Ideally this would be migrated to an account run by the client, but I don't think that will happen anytime soon. When and if it does happen though, I can automate a refresh cycle of both the underlying data through the processing application as well as the data powering the dashboard, keeping the views fresh and current.

To sum up my ramblings, here is a simple architecture diagram:

**Raw TXT → Python ETL → CSV/JSON → Power BI → Dashboard**

## Features

* Automated ingestion of raw TXT exports
* Data cleaning and standardization
* Parsing of coded categorical fields
* Derived demographic fields such as age ranges
* Generation of clean CSV output
* Generation of code/description JSON lookup
* Input validation and user-friendly error handling
* Power BI demographic reporting
* PyInstaller support for standalone Windows distribution

## Repository Structure

```
demographic-data-pipeline-powerbi/
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   └── import.py
├── sample_data/
│   └── synthetic_input.txt
├── sample_output/
│   ├── synthetic_input_cleaned.csv
│   └── synthetic_input_category_dict.json
└── powerbi/
    └── DemographicDashboard.pbix
```

## Data Processing Pipeline - src/import.py

### 1. Input

The script reads the tab-delimited source export from the `sample_data` directory. It also checks that exactly one input file is present before attempting to process anything. If no file is found, or if multiple files are present, the script stops and gives the user an appropriate error rather than guessing which file to use.

### 2. Transformation

Most of the actual transformation logic for the project lives in Python rather than Power Query. Some examples include:

* Parsing combined name fields into separate fields
* Converting coded category descriptions into structured values
* Generating a code-description dictionary
* Creating age ranges from numeric ages
* Removing fields that are not needed for analysis
* Reordering and standardizing the final analytical schema

Keeping this logic in Python gives me one central place to handle the data cleaning before the data ever reaches Power BI.

### 3. Output

The script produces two files:

* A cleaned CSV containing the data used by Power BI
* A JSON category/code lookup

The JSON lookup is not currently used by the dashboard, but I kept it because I expect to have a use for it as I continue developing the project.

Example versions of both outputs are included in the `sample_output` directory.

## Power BI Dashboard

Once the Python processing is complete, the cleaned CSV is loaded into Power BI.

I intentionally kept Power Query pretty boring. It handles the basics such as sourcing the CSV, promoting headers, and assigning appropriate data types. The actual cleaning and transformation logic lives primarily in Python.

The dashboard focuses on several demographic dimensions, including:

* Age
* Race
* Ethnicity
* Location

The landing page is intended to provide a quick overview of the population, while additional pages provide more detailed views of individual demographic categories. Navigation from the summary page allows a user to move into these more detailed views without overcrowding the main dashboard.

The included `.pbix` file is a scrubbed portfolio version of the original report and is populated entirely with synthetic data.
Note: If you want to open the pbix file, you will need to update the source file path with the full file path to your copy of 'synthetic_demographic_input_cleaned.csv'

## Running the Project

### Requirements

* Python 3.10
* pandas
* PyInstaller *(optional — only needed to build the standalone executable)*

Install the dependencies with:

```
pip install -r requirements.txt
```

Then run:

```
python src/import.py
```

The input file included in this repository is completely synthetic and exists only to demonstrate the pipeline. Running the script against it will generate the corresponding cleaned output files.

## Building the Standalone Application

One of my goals for this project was to make the data-processing portion usable by someone who does not have Python installed or know how to use a terminal.

The processor can be packaged using PyInstaller:

```
pyinstaller --onefile --name DemographicDataProcessor src/import.py
```

This bundles the Python application and its required dependencies into a standalone executable. The end user can then run the processor without setting up their own Python environment.

The executable itself is not included in this repository. The source code and build instructions are included instead so the application can be built locally.

One important limitation is that PyInstaller builds are OS-specific. An executable built on Windows is a Windows application; producing a native macOS version requires building the application in a macOS environment. Cross-platform packaging is one of the areas I would like to continue developing.

## Power BI Setup

The public Power BI file intentionally uses a sanitized placeholder for its local data-source path so that no personal or client file paths are included in the repository.

To connect the included report locally:

1. Run `src/import.py` or  launch the `DemographicDataProcessor` executable to generate the cleaned synthetic dataset. (see the comments on lines 101-103)
3. Open `powerbi/DemographicDashboard.pbix` in Power BI Desktop.
4. Open Power Query and update the **Source** step to point to the generated cleaned CSV.
5. Apply the change and refresh the report.

Once the source has been updated, the included synthetic dataset can be used to explore the dashboard without access to any of the original project data.

## Technologies

* **Python** — primary data-processing language
* **pandas** — data ingestion, cleaning, and transformation
* **pathlib** — file and directory handling
* **JSON** — generation of the category/code lookup
* **PyInstaller** — packaging the Python processor as a standalone application
* **Power BI** — data modeling and dashboard development
* **Power Query** — data ingestion, header promotion, and type assignment

## Data Privacy

**IMPORTANT:** All data included in this repository is synthetic and was generated specifically for demonstration purposes.

This repository contains no production data, personally identifiable information (PII), or client-identifying information. If you have any questions or concerns about this, please contact me directly.

The public implementation has been generalized from the original project for portfolio use. Column names, source paths, branding, and other potentially identifying details have been changed or removed.

## Future Improvements

There are several directions I would like to take this project if I continue developing it:

* **Cloud-hosted data source** — move the cleaned dataset to a location such as SharePoint or OneDrive that Power BI Service can access directly.
* **Automated Power BI Service refresh** — allow the dashboard to update after new data is processed without requiring a manual Power BI Desktop refresh and republish.
* **Cross-platform application packaging** — produce a native macOS version of the processing application in addition to the Windows build.
* **Additional input validation** — provide clearer validation of expected columns and source-file structure before processing begins.
* **Configuration-driven field mappings** — move mappings and other configurable behavior outside the Python source so future changes do not require editing the application itself.

The eventual goal would be a workflow where a non-technical user can provide a new source export, run the processor, and have the updated data flow through to the published dashboard with as little manual intervention as possible.
