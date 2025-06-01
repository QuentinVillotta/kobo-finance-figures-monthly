import os
import yaml
import json

def load_api_config(config_path="config/config.yaml"):
    """
    Load API configuration from a YAML file.

    Parameters:
        config_path (str): Path to the YAML configuration file.

    Returns:
        dict: Configuration data.
    """
    with open(config_path, "r") as file:
        return yaml.safe_load(file)

def load_api_token(credentials_path="credentials/api_token.json"):
    """
    Load API token from a JSON file.

    Parameters:
        credentials_path (str): Path to the JSON credentials file.

    Returns:
        str: API token.
    """
    with open(credentials_path, "r") as file:
        return json.load(file)["token"]

def create_billing_month_folder(base_output_path, billing_month):
    """
    Create a subfolder for the billing month inside the base output directory.

    Parameters:
        base_output_path (str): The base output directory.
        billing_month (str): The billing month (e.g., '04_2025').

    Returns:
        str: The full path to the created subfolder.
    """
    folder_path = os.path.join(base_output_path, billing_month)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

