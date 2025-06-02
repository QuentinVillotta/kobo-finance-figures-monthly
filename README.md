# kobo-finance-figures-monthly

## Project Description
The `kobo-finance-figures-monthly` project automates the processing of Kobo data files to generate billing details. It fetches data from the Kobo API, applies filters, generates visualizations, and outputs structured results in Excel and ZIP formats. This automation streamlines data handling, making it efficient and reliable.

## Prerequisites
To run this project, you will need:
- Python 3.x installed on your machine.
- Quarto installed on your system. You can download it from [Quarto's official website](https://quarto.org/). To verify your installation, run:
  ```
  quarto check
  ```
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
1. Ensure your configuration files are correctly set up:
   - **`config/config.yaml`**: This file should contain the following structure:
     ```yaml
     kobo:
       project_view_id: <your_project_view_id>
       server: <your_kobo_server_url>
     output_path: <path_to_output_directory>
     country_mask: [<list_of_countries_to_exclude>]
     account_mask: [<list_of_accounts_to_exclude>]
     ncount_mask: <minimum_submission_count>
     ```
     Replace placeholders with your actual configuration values.

   - **`credentials/api_token.json`**: This file must be located in the `credentials/` directory and should contain your API token in the following format:
     ```json
     {
       "token": "<your_api_token>"
     }
     ```
     Replace `<your_api_token>` with your actual Kobo API token. Ensure the file is named `api_token.json` and is in the correct directory, as the script depends on this for successful execution.

2. Run the script using the following command:
```
python main.py --month <MM> --year <YYYY>
```
Replace `<MM>` with the billing month (e.g., 04 for April) and `<YYYY>` with the billing year (e.g., 2025).


## Output
The script generates:
- Visualizations (e.g., total submissions, percentage usage, number of projects).
- An Excel file with billing details.
- A Quarto HTML report summarizing the results.
- A ZIP archive containing all outputs, including the Quarto report.



## Contribution
Contributions to the project are welcome. Please fork the repository and submit a pull request with your changes. Ensure that you include tests for any new functionality added.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
