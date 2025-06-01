import os
import numpy as np
import matplotlib.pyplot as plt

# Apply consistent plot styling
plt.style.use('bmh')  # ggplot

params = {
    'legend.fontsize': 'xx-large',
    'figure.figsize': (15, 10),
    'figure.dpi': 300,
    'axes.labelsize': 'xx-large',
    'axes.titlesize': 'xx-large',
    'xtick.labelsize': 'xx-large',
    'ytick.labelsize': 'xx-large'
}

plt.rcParams.update(params)

def plot_total_submissions(df, save_path, billing_month):
    """
    Generate and save a bar plot for total submissions by country.

    Parameters:
        df (pd.DataFrame): The filtered DataFrame.
        save_path (str): The directory to save the plot.
        billing_month (str): The billing month (e.g., '04_2025').
    """
    palette_mask = plt.cm.tab20b(np.arange(len(df["country"].unique())))
    submission_ = df.groupby("country")["submission_count"].sum().sort_index()
    submission_.plot(kind="bar", ylabel="#Submission (log scale)", title=billing_month,
                     ylim=[1, max(submission_) * 10], log=True, color=palette_mask)
    plt.savefig(os.path.join(save_path, f"total_usage_{billing_month}.png"))
    plt.clf()


def plot_percentage_usage(df, save_path, billing_month):
    """
    Generate and save a bar plot for percentage usage by country.

    Parameters:
        df (pd.DataFrame): The filtered DataFrame.
        save_path (str): The directory to save the plot.
        billing_month (str): The billing month (e.g., '04_2025').
    """
    palette_mask = plt.cm.tab20b(np.arange(len(df["country"].unique())))
    submission_ = df.groupby("country")["submission_count"].sum().sort_index()
    submission_n = submission_ / submission_.sum() * 100
    ax = submission_n.plot(kind="bar", ylabel="Usage [%]", title=billing_month,
                            ylim=[0, max(submission_n) + 5], color=palette_mask)
    for p in ax.patches:
        ax.annotate(str(round(p.get_height(), 2)), (p.get_x(), p.get_height() * 1.03), fontsize="xx-large")
    plt.savefig(os.path.join(save_path, f"percentage_usage_{billing_month}.png"))
    plt.clf()


def plot_number_of_projects(df, save_path, billing_month):
    """
    Generate and save a bar plot for the number of projects by country.

    Parameters:
        df (pd.DataFrame): The filtered DataFrame.
        save_path (str): The directory to save the plot.
        billing_month (str): The billing month (e.g., '04_2025').
    """
    palette_mask = plt.cm.tab20b(np.arange(len(df["country"].unique())))
    n_projects = df["country"].value_counts()
    n_projects.sort_index().plot(kind="bar", ylabel="#Projects", title=billing_month, ylim=[0, max(n_projects) + 2], color=palette_mask)
    plt.savefig(os.path.join(save_path, f"number_projects_{billing_month}.png"))
    plt.clf()
