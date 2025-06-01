import os
import zipfile
import logging

def create_zip_archive(save_path, billing_month):
    """
    Creates a ZIP archive containing the final dataset and generated plots.

    Args:
        save_path (str): The directory where the files are saved.
        billing_month (str): The billing month identifier (e.g., '04_2025').

    Returns:
        str: The path to the created ZIP archive.
    """
    logging.info("Creating a ZIP archive with the final dataset and plots...")

    zip_filename = os.path.join(save_path, f"billing_details_{billing_month}.zip")
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        # Add the final Excel file
        final_excel_path = os.path.join(save_path, f"billing_details_{billing_month}.xlsx")
        zipf.write(final_excel_path, os.path.basename(final_excel_path))

        # Add the plots
        plot_files = [
            os.path.join(save_path, f"total_usage_{billing_month}.png"),
            os.path.join(save_path, f"percentage_usage_{billing_month}.png"),
            os.path.join(save_path, f"number_projects_{billing_month}.png")
        ]
        for plot_file in plot_files:
            zipf.write(plot_file, os.path.basename(plot_file))

    logging.info(f"ZIP archive created successfully: {zip_filename}")
    return zip_filename
