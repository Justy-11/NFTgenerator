import os
import json
import csv

# Path to the folder containing your JSON metadata files
METADATA_DIR = "output_nfts/metadata"  # Replace with the path to your metadata folder
CSV_FILE = "nft_metadata.csv"         # Output CSV file name

# Static description for all NFTs
STATIC_DESCRIPTION = (
    "Where apes meet haute couture. This uniquely dressed primate is part of the "
    "Ape Couture Society collection—ready to rock your digital world!"
)

# Main function to process JSON files and generate CSV
def generate_csv():
    # List to hold all rows of data
    rows = []
    trait_columns = set()  # To track all unique trait names

    # Loop through all files in the metadata directory
    for filename in os.listdir(METADATA_DIR):
        if filename.endswith(".json"):  # Process only JSON files
            file_path = os.path.join(METADATA_DIR, filename)
            
            # Open and load the JSON file
            with open(file_path, "r") as f:
                metadata = json.load(f)
            
            # Extract mandatory fields
            tokenID = int(filename.split(".")[0])  # Extract tokenID from file name (e.g., "1.json" -> 1)
            name = metadata.get("name", "")
            file_name = f"{tokenID}.png"  # Assuming all files are .png

            # Use the static description for all NFTs
            description = STATIC_DESCRIPTION

            # Extract attributes and build trait columns
            attributes = metadata.get("attributes", [])
            row = {
                "tokenID": tokenID,
                "name": name,
                "file_name": file_name,
                "description": description
            }
            for attr in attributes:
                trait_type = attr.get("trait_type")
                value = attr.get("value")
                row[f"attributes[{trait_type}]"] = value
                trait_columns.add(f"attributes[{trait_type}]")

            # Append the data as a row
            rows.append(row)

    # Write the rows to a CSV file
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
        # Define the header row
        header = ["tokenID", "name", "file_name", "description"] + sorted(trait_columns)
        
        writer = csv.DictWriter(csvfile, fieldnames=header)
        
        # Write the header and data rows
        writer.writeheader()
        writer.writerows(rows)

    print(f"CSV file '{CSV_FILE}' has been generated successfully!")

# Run the script
if __name__ == "__main__":
    generate_csv()