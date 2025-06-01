import os
import pandas as pd
import logging
from utils.kobo_api import fetch_kobo_data
from utils.config_utils import load_api_config, load_api_token, save_to_excel, create_billing_month_folder
from utils.plot_utils import plot_total_submissions, plot_percentage_usage, plot_number_of_projects
from utils.zip_utils import create_zip_archive

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

    # Fetch data from Kobo API
    logging.info("Fetching data from Kobo API...")
    df = fetch_kobo_data(api_token, project_view_id, kobo_server)
    logging.info(f"Data fetched successfully with {len(df)} records.")

    # Create billing date
    logging.info("Filtering data for the specified billing month...")
    df["billing_date"] = pd.to_datetime(df["date_deployed"]).dt.strftime('%m_%Y')
    df_filtered = df[df["billing_date"] == billing_month]

    # Apply filters
    logging.info("Applying filters...")
    df_filtered = df_filtered[~df_filtered["owner__username"].isin(account_mask)]
    df_filtered = df_filtered[df_filtered["submission_count"] > ncount_mask]
    country_condition = ~df_filtered["country"].isin(country_mask)
    not_na_condition = df_filtered["country"].notna()
    not_empty_condition = df_filtered["country"] != ''
    df_filtered = df_filtered[country_condition & not_na_condition & not_empty_condition]
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

    # Create a ZIP archive with the final dataset and plots
    zip_filename = create_zip_archive(save_path, billing_month)
    logging.info(f"ZIP archive created successfully: {zip_filename}")

if __name__ == "__main__":
    # Example usage
    process_kobo_data("04", "2025")