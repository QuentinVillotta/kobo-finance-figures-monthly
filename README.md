# kobo_split_automation

## Project Description
The `kobo-finance-figures-monthly` project automates the processing of Kobo data files to generate billing details. It fetches data from the Kobo API, applies filters, generates visualizations, and outputs structured results in Excel and ZIP formats. This automation streamlines data handling, making it efficient and reliable.

## Prerequisites
To run this project, you will need:
- Python 3.x installed on your machine.
- The following Python packages:
  - pandas
  - numpy
  - matplotlib
  - openpyxl
  - pytest
  - pyyaml

You can install the required packages using the following command:
```
pip install -r requirements.txt
```

## Launch Instructions
1. Ensure your configuration files (`config/config.yaml` and `credentials/api_token.json`) are correctly set up.
2. Run the script using the following command:
```
python main.py --month <MM> --year <YYYY>
```
Replace `<MM>` with the billing month (e.g., 04 for April) and `<YYYY>` with the billing year (e.g., 2025).

## Output
The script generates:
- Visualizations (e.g., total submissions, percentage usage, number of projects).
- An Excel file with billing details.
- A ZIP archive containing all outputs.

## Contribution
Contributions to the project are welcome. Please fork the repository and submit a pull request with your changes. Ensure that you include tests for any new functionality added.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.