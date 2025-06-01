# kobo_split_automation

## Project Description
The `kobo-finance-figures-monthly` project is designed to automate the processing of Kobo data files, specifically focusing on generating billing details from input datasets. The project takes input data in the form of Excel or CSV files, processes it according to specified criteria, and outputs the results in a structured format. This automation eliminates the need for manual intervention, making data handling more efficient and reliable.

## Prerequisites
To run this project, you will need:
- Python 3.x installed on your machine.
- The following Python packages:
  - pandas
  - numpy
  - matplotlib
  - openpyxl (for Excel file handling)

You can install the required packages using the following command:
```
pip install -r requirements.txt
```

## Launch Instructions
1. Place your input data files (e.g., `kobo_asset_details_Apr25.xlsx`) in the `data/dataset` directory.
2. Open a terminal and navigate to the project root directory.
3. Run the main script using the following command:
```
python scripts/kobo_split.py
```
4. The processed output files will be saved in the `plots/` directory within the project structure.

## Project Structure
```
kobo_split_automation
├── data
│   └── dataset          # Directory for input data files
├── scripts
│   ├── kobo_split.py    # Main automation script
│   └── utils.py         # Utility functions for data processing
├── tests
│   └── test_kobo_split.py # Unit tests for the project
├── .gitignore            # Files and directories to ignore by Git
├── requirements.txt      # List of dependencies
├── README.md             # Project documentation
└── LICENSE               # Licensing information
```

## Limitations
- The current implementation assumes that the input data files are correctly formatted and contain the necessary columns as expected by the script.
- The script is designed to handle specific country codes and account names; modifications may be required for different datasets.

## Contribution
Contributions to the project are welcome. Please fork the repository and submit a pull request with your changes. Ensure that you include tests for any new functionality added.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.