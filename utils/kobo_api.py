import requests
import pandas as pd

def fetch_kobo_data(api_token, project_view_id, kobo_server):
    """
    Fetch data from Kobo API.

    Parameters:
        api_token (str): The API token for authentication.
        project_view_id (str): The project view ID.
        kobo_server (str): The Kobo server URL.

    Returns:
        pd.DataFrame: A DataFrame containing the fetched data.
    """
    url = f"{kobo_server}/api/v2/project-views/{project_view_id}/assets/"
    headers = {"Authorization": f"Token {api_token}"}

    assets_metadata = []
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        for asset in data.get("results", []):
            if asset.get("asset_type") == "survey":
                metadata = extract_form_metadata(asset)
                assets_metadata.append(metadata)

        url = data.get("next")

    return pd.DataFrame(assets_metadata)

def extract_form_metadata(asset):
    """
    Extract metadata from a Kobo API response asset.

    Parameters:
        asset (dict): The asset dictionary from the API response.

    Returns:
        dict: A dictionary containing extracted metadata.
    """
    settings = asset.get("settings", {})
    countries = settings.get("country", [])
    country_code = ", ".join(c.get("value") for c in countries if "value" in c)

    return {
        "uid": asset.get("uid"),
        "name": asset.get("name"),
        "asset_type": asset.get("asset_type"),
        "date_modified": asset.get("date_modified"),
        "date_created": asset.get("date_created"),
        "date_deployed": asset.get("date_deployed"),
        "owner__username": asset.get("owner__username"),
        "owner__email": asset.get("owner__email"),
        "owner__name": asset.get("owner__name"),
        "owner__organization": asset.get("owner__organization"),
        "deployment_status": asset.get("deployment_status"),
        "submission_count": asset.get("deployment__submission_count"),
        "country": country_code,
        "sector": settings.get("sector", {}).get("label", ""),
        "description": settings.get("description", "")
    }
