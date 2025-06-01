import os
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yaml
import json
from datetime import datetime
from utils.kobo_api import fetch_kobo_data

# Load API configuration from a YAML file
def load_api_config(config_path="config/config.yaml"):
    with open(config_path, "r") as file:
        return yaml.safe_load(file)

# Load API token from a JSON file
def load_api_token(credentials_path="credentials/api_token.json"):
    with open(credentials_path, "r") as file:
        return json.load(file)["token"]

# Create output folder
def create_folder(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

# Main processing function
def process_kobo_data(month, year, config_path="config/config.yaml", credentials_path="credentials/api_token.json"):
    config = load_api_config(config_path)
    api_token = load_api_token(credentials_path)
    project_view_id = config["kobo"]["project_view_id"]
    kobo_server = config["kobo"]["server"]

    # Fetch data from Kobo API
    df = fetch_kobo_data(api_token, project_view_id, kobo_server)

    # Filter and process data
    billing_month = f"{month[:3]}_{year}"
    df["billing_date"] = pd.to_datetime(df["deployed_date"]).dt.strftime('%b_%Y')
    df_filtered = df[df["billing_date"] == billing_month]

    # Create output folder
    save_path = os.path.join("output", billing_month)
    create_folder(save_path)

    # Generate and save plots
    generate_plots(df_filtered, save_path, billing_month)

    # Save final data to Excel
    save_to_excel(df_filtered, save_path, billing_month)

# Generate plots
def generate_plots(df, save_path, billing_month):
    palette_mask = plt.cm.tab20b(np.arange(len(df["country"].unique())))

    # Total submissions
    submission_ = df.groupby("country")["submission_count"].sum().sort_index()
    submission_.plot(kind="bar", ylabel="#Submission (log scale)", title=billing_month,
                     ylim=[1, max(submission_) * 10], log=True, color=palette_mask)
    plt.savefig(os.path.join(save_path, f"total_usage_{billing_month}.png"))
    plt.clf()

    # Percentage usage
    submission_n = submission_ / submission_.sum() * 100
    ax = submission_n.plot(kind="bar", ylabel="Usage [%]", title=billing_month,
                            ylim=[0, max(submission_n) + 5], color=palette_mask)
    for p in ax.patches:
        ax.annotate(str(round(p.get_height(), 2)), (p.get_x(), p.get_height() * 1.03), fontsize="xx-large")
    plt.savefig(os.path.join(save_path, f"percentage_usage_{billing_month}.png"))
    plt.clf()

# Save data to Excel
def save_to_excel(df, save_path, billing_month):
    df.to_excel(os.path.join(save_path, f"billing_details_{billing_month}.xlsx"), index=False)

if __name__ == "__main__":
    # Example usage
    process_kobo_data("Apr", "2025")
