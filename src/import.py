import pandas as pd
import json
from pathlib import Path
import sys

def read_input(input_path):
    ### IMPORT DATA
    return pd.read_table(
        input_path,
        sep = '\t',
        header = 1,
        skipfooter = 1,
        engine = 'python',
        na_values = ["-", "Not Yet Answered", "Declined to Specify"],
        date_format = "%d/%m/%Y")

def parse_data(df):
    # SPLIT NAME COLUMN
    df[["Last Name", "First Name"]] = df["Last, First"].str.split(", ", n=1, expand=True)

    # REWORK Category List COLUMN

    # first - make dictionary of category codes and descriptions
    all_categories = ";".join(df["Category List"].fillna("").astype(str))
    all_categories = all_categories.split(";")
    category_dict = {}
    for category in all_categories:
        if category:
            code, description = category.split(") ", 1)
            code = code.strip(" (")
            category_dict[code] = description

    # next - remove descriptions from the Category List column, leaving only codes
        # split Category List by semicolon, then split each category by ") "
        # and keep only the first part (the code)
    def extract_codes(category_list):
        if pd.isna(category_list):
            return ""
        categories = category_list.split(";")
        codes = []
        for category in categories:
            if ") " in category:
                code = category.split(") ")[0].strip(" (")
                codes.append(code)
        return codes
    # now apply the function to the Category List column
    df["Category List"] = df["Category List"].apply(extract_codes)

    # then - add a new column containing the number of categories for each record
    # why abstract? let's keep # of probs and the list, no need to remove
    df["# of categories"] = df["Category List"].apply(len)

    df["Race"] = df["Races"]

    # Add column for age ranges
    def age_range(age):
        if pd.isna(age):
            return ""
        elif age < 18:
            return "0-17"
        elif age < 30:
            return "18-29"
        elif age < 40:
            return "30-39"
        elif age < 50:
            return "40-49"
        elif age < 60:
            return "50-59"
        elif age < 70:
            return "60-69"
        elif age < 80:
            return "70-79"
        else:
            return "80+"
    df["Age Range"] = df["Age"].apply(age_range)

    # DROP UNNECESSARY COLUMNS
    df.drop(columns=[
        "Last, First", "Unnamed: 17",
        "Attr A", "Attr B", "Follow-Up Date",
        "Office", "Races"], inplace=True)

    # REORDER COLUMNS
    df = df[[
        'Record ID', 'First Name', 'Last Name', 'Date of Birth', 'Age', 'Age Range', 'Sex',
        'Location', '# of categories', 'Category List', 'Attribute List', 'Follow-Up Type', 'Ethnicity',
        'Race', 'Language', 'Contact Method']]

    return category_dict, df

def write_json(dict, output_path):
    ### FINI
    with open(output_path, "w") as f:
        json.dump(dict, f, indent=4)

def write_csv(df, output_path):
    ### FINI
    df.to_csv(output_path, index=False)

def main():
    base_dir = Path(sys.executable).resolve().parent.parent # this line works when running the pyinstaller executable, but not in dev mode
    # if you want to run in dev mode, comment out the line above and uncomment the line below
    # base_dir = Path(__file__).resolve().parent.parent

    input_dir = base_dir / "sample_data"
    output_dir = base_dir / "output"

    files = list(input_dir.glob("*.txt"))

    if not files:
        raise FileNotFoundError("No .txt files were found in the input directory.")

    elif len(files) > 1:
        raise RuntimeError("Multiple .txt files were found in the input directory." \
        "Please ensure only one file is present.")

    input_path = files[0]
    output_path_json = output_dir / (input_path.stem + "_category_dict.json")
    output_path_csv = output_dir / (input_path.stem + "_cleaned.csv")

    output_dir.mkdir(exist_ok=True)

    print(f"Processing file: {input_path.name}")

    raw_data = read_input(input_path)
    category_dict, clean_data = parse_data(raw_data)
    write_json(category_dict, output_path_json)
    write_csv(clean_data, output_path_csv)

    print(f"Cleaned data has been saved in the 'output' directory.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error has occurred: {e}")

    input("\nPress Enter to exit...")
