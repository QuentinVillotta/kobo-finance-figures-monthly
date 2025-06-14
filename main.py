import os
import pandas as pd
import logging
from utils.kobo_api import fetch_kobo_data
from utils.config_utils import load_api_config, load_api_token, create_billing_month_folder
from utils.plot_utils import plot_total_submissions, plot_percentage_usage, plot_number_of_projects
from utils.zip_utils import create_zip_archive
from utils.quarto_report_generator import generate_quarto_report
import argparse

# Reset the log file at the start of execution
with open("process_kobo_data.log", "w") as log_file:
    log_file.truncate()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("process_kobo_data.log"),
        logging.StreamHandler()
    ]
)

# Main processing function
def process_kobo_data(month, year, config_path="config/config.yaml", credentials_path="credentials/api_token.json"):
    logging.info("Starting Kobo data processing...")

    # Configure paths and load configurations
    logging.info("Loading configuration and credentials...")
    config = load_api_config(config_path)
    api_token = load_api_token(credentials_path)
    project_view_id = config["kobo"]["project_view_id"]
    kobo_server = config["kobo"]["server"]
    base_output_path = config["output_path"]

    # Output folder for the billing month
    billing_month = f"{month.zfill(2)}_{year}"
    save_path = create_billing_month_folder(base_output_path, billing_month)
    logging.info(f"Output folder created: {save_path}")

    # Load masks from configuration
    logging.info("Loading masks from configuration...")
    country_mask = config.get("country_mask")
    account_mask = config.get("account_mask")
    ncount_mask = config.get("ncount_mask")

    logging.info(f"Country mask applied: {country_mask}")
    logging.info(f"Account mask applied: {account_mask}")
    logging.info(f"Minimum submission count mask applied: {ncount_mask}")

    # Fetch data from Kobo API
    logging.info("Fetching data from Kobo API...")
    df = fetch_kobo_data(api_token, project_view_id, kobo_server)
    logging.info(f"Data fetched successfully with {len(df)} records.")

    # Create billing date
    logging.info("Filtering data for the specified billing month...")
    df["billing_date"] = pd.to_datetime(df["date_deployed"]).dt.strftime('%m_%Y')
    df_filtered = df[df["billing_date"] == billing_month]

    logging.info(f"Number of forms for the billing month {billing_month}: {len(df_filtered)}")

    # Apply filters
    logging.info("Applying filters...")

    # Filter by account mask
    initial_count = len(df_filtered)
    df_filtered = df_filtered[~df_filtered["owner__username"].isin(account_mask)]
    logging.info(f"Removed {initial_count - len(df_filtered)} forms due to account mask.")

    # Filter by minimum submission count
    initial_count = len(df_filtered)
    df_filtered = df_filtered[df_filtered["submission_count"] > ncount_mask]
    logging.info(f"Removed {initial_count - len(df_filtered)} forms due to submission count below {ncount_mask}.")

    # Filter by country mask and conditions
    initial_count = len(df_filtered)
    country_condition = ~df_filtered["country"].isin(country_mask)
    not_na_condition = df_filtered["country"].notna()
    not_empty_condition = df_filtered["country"] != ''
    df_filtered = df_filtered[country_condition & not_na_condition & not_empty_condition]
    logging.info(f"Removed {initial_count - len(df_filtered)} forms due to country mask or invalid country fields.")

    # Check for NA or empty countries
    na_countries = df_filtered["country"].isna().sum()
    empty_countries = (df_filtered["country"] == '').sum()
    logging.info(f"Number of forms with NA countries: {na_countries}")
    logging.info(f"Number of forms with empty country fields: {empty_countries}")

    logging.info(f"Data filtered successfully with {len(df_filtered)} records remaining.")

    # Save filtered data to CSV
    # logging.info("Saving filtered data to CSV...")
    # df_filtered.to_csv(os.path.join(save_path, "kobo_metadata.csv"), index=False)

    # Generate and save plots
    logging.info("Generating and saving plots...")
    plot_total_submissions(df_filtered, save_path, billing_month)
    plot_percentage_usage(df_filtered, save_path, billing_month)
    plot_number_of_projects(df_filtered, save_path, billing_month)
    logging.info("Plots generated successfully.")

    # Calculate additional metrics for the final output
    logging.info("Calculating additional metrics...")
    n_projects = df_filtered["country"].value_counts()
    submission_ = df_filtered.groupby("country")["submission_count"].sum().sort_index()
    submission_n = submission_ / submission_.sum() * 100

    # Combine metrics into a single DataFrame with explicit column names
    df_final = pd.concat(
        [
            n_projects.rename("country_count"),
            submission_.rename("submission_count"),
            round(submission_n, 2).rename("submission_count_perc")
        ],
        axis=1
    )
    # Ensure column names are unique and meaningful
    df_final.reset_index(inplace=True)
    df_final.rename(columns={"index": "country"}, inplace=True)

    # Save the final DataFrame to an Excel file
    logging.info("Saving the final DataFrame to an Excel file...")
    df_final.to_excel(os.path.join(save_path, f"billing_details_{billing_month}.xlsx"))
    logging.info("Kobo data processing completed successfully.")

    logging.info(f"Final dataset statistics:")
    logging.info(f"Number of countries: {df_final['country'].nunique()}")
    logging.info(f"Total number of submissions: {df_final['submission_count'].sum()}")

    # Generate Quarto report and get the HTML file path
    html_report_path = generate_quarto_report(
        log_file_path="process_kobo_data.log",
        output_dir=save_path,
        billing_month=billing_month
    )

    # Create a ZIP archive with the final dataset, plots, and Quarto report
    zip_filename = create_zip_archive(save_path, billing_month, additional_files=[html_report_path])
    logging.info(f"ZIP archive created successfully: {zip_filename}")


if __name__ == "__main__":
    # Parse command-line arguments for month and year
    parser = argparse.ArgumentParser(description="Run Kobo data processing pipeline.")
    parser.add_argument("--month", type=str, required=True, help="The billing month (e.g., 04 for April). This argument is required.")
    parser.add_argument("--year", type=str, required=True, help="The billing year (e.g., 2025). This argument is required.")
    args = parser.parse_args()

    month = args.month
    year = args.year

    # Validate month and year inputs
    if not (month.isdigit() and 1 <= int(month) <= 12):
        parser.error(f"Invalid month '{month}'. Please provide a valid month (01-12).")

    if not (year.isdigit() and len(year) == 4):
        parser.error(f"Invalid year '{year}'. Please provide a valid year (e.g., 2025).")

    # Run the processing function
    process_kobo_data(month, year)