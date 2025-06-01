import os
import logging
import datetime

def generate_quarto_report(log_file_path, output_dir, billing_month):
    """
    Generate a Quarto report for the Head of Finance, viewable in a web browser.

    Args:
        log_file_path (str): Path to the log file containing processing details.
        output_dir (str): Directory where the report will be saved.
        billing_month (str): The billing month (e.g., '05_2025').
    """
    logging.info("Generating Quarto report...")

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Read the log file
    with open(log_file_path, 'r') as log_file:
        log_content = log_file.read()

    # Get the current date
    current_date = datetime.date.today().strftime("%B %d, %Y")

    # Prepare the Quarto content
    quarto_content = f"""
---
title: "Finance Report for {billing_month}"
author: "Quentin Villotta"
date: "{current_date}"
format:
  html: default
---

# Visualizations

The following visualizations were generated for this billing month:

- **Total Submissions**:

<img src="total_usage_{billing_month}.png" style="width:70%;" alt="Total Submissions">

- **Percentage Usage**:

<img src="percentage_usage_{billing_month}.png" style="width:70%;" alt="Percentage Usage">

- **Number of Projects**:

<img src="number_projects_{billing_month}.png" style="width:70%;" alt="Number of Projects">

# Full Logs

<details>
<summary>Click to expand full logs</summary>

```
{log_content}
```

</details>

"""

    # Save the Quarto file
    quarto_file_path = os.path.join(output_dir, f"finance_report_{billing_month}.qmd")
    with open(quarto_file_path, 'w') as quarto_file:
        quarto_file.write(quarto_content)

    logging.info(f"Quarto report generated: {quarto_file_path}")

    # Render the Quarto file to HTML
    try:
        os.system(f"quarto render {quarto_file_path} --to html")
        logging.info("Quarto report rendered successfully.")
    except Exception as e:
        logging.error(f"Failed to render Quarto report: {e}")

    # Return the path to the HTML file for inclusion in the ZIP archive
    return os.path.join(output_dir, f"finance_report_{billing_month}.html")
