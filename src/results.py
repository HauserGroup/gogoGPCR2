from tqdm.notebook import tqdm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

def pval_stars(x: float) -> str:
    """[summary]

    Parameters
    ----------
    x : float
        [description]

    Returns
    -------
    str
        [description]
    """
    if x <= 0.0001:
        return "****"
    elif x <= 0.001:
        return "***"
    elif x <= 0.01:
        return "**"
    elif x <= 0.05:
        return "*"
    if x > 0.05:
        return ""


def pheno_search(
    x, ukb_coding: pd.DataFrame, custom_coding: pd.DataFrame
) -> dict:
    """[summary]

    Parameters
    ----------
    x : [type]
        [description]
    ukb_coding : pd.DataFrame
        [description]
    custom_coding : pd.DataFrame
        [description]

    Returns
    -------
    [type]
        [description]
    """
    ukb = dict(zip(ukb_coding.FieldID.astype(str), ukb_coding.Field))
    custom = dict(zip(custom_coding.FieldID.astype(str), custom_coding.Field))
    both = {**ukb, **custom}

    return both[str(x)]

def plot_BT(
    df,
    width=4,
    height=None,
    phenotypes=None,
    masks=None,
    lw=1.3,
    ms=5,
    fudge=0.6,
    xlim=[0, 12],
    title=None,
):
    df = df.loc[df.TRAIT == "BT", :]

    # Create confidence interval string
    df.loc[:, "CI"] = +(
        "("
        + df.loc[:, "OR_low"].round(2).astype(str)
        + ","
        + df.loc[:, "OR_up"].round(2).astype(str)
        + ")"
    )

    just = df.applymap(lambda x: len(str(x)) + 1).max()

    # Create the label column for annotations
    df.loc[:, "label"] = (
        df.loc[:, "N_pos"].astype(str).str.ljust(just["N_pos"])
        + df.loc[:, "OR"].round(2).astype(str).str.ljust(5)
        + df.loc[:, "CI"].str.ljust(just["CI"])
        + "p="
        + df.loc[:, "pval"].apply(lambda p: f"{p:.2e}").str.ljust(4)
        + " "
        + df.loc[:, "pval_stars"].str.ljust(4)
    )

    if phenotypes is None:
        phenotypes = df.Phenotype.unique()

    num_pheno = len(phenotypes)
    if not height:
        height = 2 * num_pheno

    masks = df.MASK.unique()
    colors = plt.cm.viridis(np.linspace(0, 1, len(masks)))

    fig, axes = plt.subplots(nrows=num_pheno, sharex=True, figsize=(width, height))
    
    for i, ax in tqdm(enumerate(axes)):
        temp = df.loc[df.Phenotype.eq(phenotypes[i]), :]
        temp = temp.loc[df.MASK.isin(masks)]

        for color, mask in zip(colors, masks):
            temp1 = temp.loc[temp.MASK == mask, :]
            xerr = [temp1["OR_low_lim"].values, temp1["OR_up_lim"].values]

            if temp1.empty:
                continue  # Skip if temp1 is empty

            # Plot the data points with error bars
            ax.errorbar(
                temp1["OR"],
                temp1.index,
                alpha=0.99,
                xerr=xerr,
                fmt="o",
                c=color,
                ecolor="black",
                ms=ms,
                mew=0.0,
                mec="black",
                elinewidth=lw,
            )

            # Annotate the values to the right of the plot
            value_label = temp1.label.iloc[0]  # Use the first label for the annotation

            ax.text(
                xlim[1] + fudge,  # Position on the x-axis (right of the plot)
                temp1.index[0],  # Y-coordinate (use first index)
                value_label,  # The value label
                va='center',  # Vertically align to the center of the point
                ha='left',  # Horizontally align to the left
                fontsize=9,
                fontdict={"family": "monospace"},
            )

        ax.set_ylim(temp.index[0] - fudge, temp.index[-1] + fudge)
        ax.set_xlim(xlim[0] - fudge, xlim[1] + fudge)
        ax.set_xticks(np.arange(xlim[0], xlim[1] + 1, 1))

        # Set y-ticks to show masks dynamically
        ax.set_yticks(temp.index)
        mask_labels = [mask for mask in masks if mask in temp.MASK.values]
        ax.set_yticklabels(mask_labels[:len(temp.index)], fontsize=9, fontdict={"family": "monospace"})  # Y-tick labels

        ax.axvline(x=1, linestyle="--", color="#4f4f4f")

        # Set the title for each subplot to display the phenotype name
        ax.set_title(phenotypes[i], fontsize=10, fontweight='bold')

        # Aesthetics: Hide extra spines and ticks
        ax.tick_params(right=False)
        ax.spines["top"].set_alpha(0)
        ax.spines["left"].set_alpha(0)
        ax.spines["right"].set_alpha(0)
        ax.spines["bottom"].set_alpha(0)

        if i != len(phenotypes) - 1:
            ax.tick_params(bottom=False)

        if i == len(phenotypes) - 1:
            ax.set_xlabel("OR")
            ax.tick_params(bottom=True)

    # Set an overall title for the first subplot
    if title:
        plt.suptitle(title, fontsize=12, fontweight='bold', y=0.9)  # Adjust y position to move closer

    # Adjust spacing between plots
    plt.subplots_adjust(hspace=0.25, right=1)  # Adjust vertical spacing (hspace)

    return fig


def plot_BT_grouped_by_mask(
    df,
    width=4,
    height=None,
    phenotypes=None,
    masks=None,
    lw=1.3,
    ms=5,  # Reduced marker size
    fudge=0.6,
    xlim=[0, 12],
    title=None,
):

    df = df.loc[df.TRAIT == "BT", :]

    # Create confidence interval string
    df.loc[:, "CI"] = +(
        "("
        + df.loc[:, "OR_low"].round(2).astype(str)
        + ","
        + df.loc[:, "OR_up"].round(2).astype(str)
        + ")"
    )

    just = df.applymap(lambda x: len(str(x)) + 1).max()

    # Create the label column for annotations
    df.loc[:, "label"] = (
        df.loc[:, "N_pos"].astype(str).str.ljust(just["N_pos"])
        + df.loc[:, "OR"].round(2).astype(str).str.ljust(5)
        + df.loc[:, "CI"].str.ljust(just["CI"])
        + "p="
        + df.loc[:, "pval"].apply(lambda p: f"{p:.2e}").str.ljust(5)
        + " "
        + df.loc[:, "pval_stars"].str.ljust(4)
    )

    if masks is None:
        masks = df.MASK.unique()
    
    if phenotypes is None:
        phenotypes = df.Phenotype.unique()

    num_masks = len(masks)
    if not height:
        height = 2 * num_masks  # Set height based on number of masks

    colors = plt.cm.viridis(np.linspace(0, 1, len(phenotypes)))

    fig, axes = plt.subplots(nrows=num_masks, sharex=True, figsize=(width, height))

    for i, ax in tqdm(enumerate(axes)):
        temp = df.loc[df.MASK.eq(masks[i]), :]

        for j, phenotype in enumerate(phenotypes):
            temp1 = temp.loc[temp.Phenotype == phenotype]

            if temp1.empty:
                continue  # Skip if temp1 is empty

            # Plot the data points with smaller markers
            ax.errorbar(
                temp1["OR"],
                [j] * len(temp1),  # Y position corresponds to the phenotype index
                alpha=0.99,
                xerr=[temp1["OR_low_lim"].values, temp1["OR_up_lim"].values],
                fmt="o",
                c=colors[j],
                ecolor="black",
                ms=ms,  # Smaller marker size
                mew=0.0,
                mec="black",
                elinewidth=lw,
            )

            # Create the label string for the right annotation
            value_label = temp1.label.iloc[0]  # Use the first label for the annotation

            # Annotate the values to the right of the plot
            ax.text(
                xlim[1] + fudge,  # Position on the x-axis (right of the plot)
                j,  # Y-coordinate (use phenotype index)
                value_label,  # The value label
                va='center',  # Vertically align to the center of the point
                ha='left',  # Horizontally align to the left
                fontsize=9,
                fontdict={"family": "monospace"},
            )
        
        ax.set_ylim(-0.5, len(phenotypes) - 0.5)  # Set the limits for y-axis
        ax.set_xlim(xlim[0] - fudge, xlim[1] + fudge)
        ax.set_xticks(np.arange(xlim[0], xlim[1] + 1, 1))

        # Set y-ticks to show phenotype labels dynamically
        ax.set_yticks(range(len(phenotypes)))  # Set y-ticks to the number of unique phenotypes
        ax.set_yticklabels(phenotypes, fontsize=9, fontdict={"family": "monospace"})  # Set y-tick labels

        ax.axvline(x=1, linestyle="--", color="#4f4f4f")  # Reference line at OR=1

        # Set the title for each subplot to display the mask name
        ax.set_title(masks[i], fontsize=10, fontweight='bold')

        # Aesthetics: Hide extra spines and ticks
        ax.tick_params(right=False)
        ax.spines["top"].set_alpha(0)
        ax.spines["left"].set_alpha(0)
        ax.spines["right"].set_alpha(0)
        ax.spines["bottom"].set_alpha(0)

        if i != len(masks) - 1:
            ax.tick_params(bottom=False)

        if i == len(masks) - 1:
            ax.set_xlabel("OR")
            ax.tick_params(bottom=True)

    # Set an overall title for the first subplot
    if title:
        plt.suptitle(title, fontsize=12, fontweight='bold', y=0.9)  # Adjust y position to move closer

    # Adjust spacing between plots
    plt.subplots_adjust(hspace=0.25, right=1)  # Adjust vertical spacing (hspace)

    return fig


def plot_QT(
    df,
    width=4,
    height=None,
    phenotypes=None,
    masks=None,
    lw=1.3,
    ms=5,  # Reduced marker size
    fudge=0.6,
    xlim=[-1, 1],
    title=None,
):

    df = df.loc[df.TRAIT == "QT", :]

    just = df.applymap(lambda x: len(str(x)) + 1).max()

    # Create the label column
    df.loc[:, "label"] = (
        df.loc[:, "N_pos"].astype(str).str.ljust(just["N_pos"])
        + df.loc[:, "BETA"].round(2).astype(str).str.ljust(5)
        + "± "
        + df.loc[:, "SE"].round(2).astype(str).str.ljust(5)
        + "p="
        + df.loc[:, "pval"].apply(lambda p: f"{p:.2e}").str.ljust(5)
        + " "
        + df.loc[:, "pval_stars"].str.ljust(4)
    )

    if phenotypes is None:
        phenotypes = df.Phenotype.unique()

    num_pheno = len(phenotypes)
    if not height:
        height = 2 * num_pheno

    masks = df.MASK.unique()
    colors = plt.cm.viridis(np.linspace(0, 1, len(masks)))

    fig, axes = plt.subplots(nrows=num_pheno, sharex=True, figsize=(width, height))

    for i, ax in tqdm(enumerate(axes)):

        temp = df.loc[df.Phenotype.eq(phenotypes[i]), :]
        temp = temp.loc[df.MASK.isin(masks)]

        for color, mask in zip(colors, masks):
            temp1 = temp.loc[temp.MASK == mask, :]

            if temp1.empty:
                continue  # Skip if temp1 is empty

            # Plot the data points with smaller markers
            ax.errorbar(
                temp1["BETA"],
                temp1.index,
                alpha=0.99,
                xerr=temp1["SE"],
                fmt="o",
                c=color,
                ecolor="black",
                ms=ms,  # Smaller marker size
                mew=0.0,
                mec="black",
                elinewidth=lw,
            )

            # Create the label string using the specified format for the right annotation
            value_label = (
                temp1["N_pos"].astype(str).str.ljust(just["N_pos"]).iloc[0] +
                temp1["BETA"].round(2).astype(str).str.ljust(5).iloc[0] +
                "± " + temp1["SE"].round(2).astype(str).str.ljust(5).iloc[0] +
                "p=" + temp1["pval"].apply(lambda p: f"{p:.2e}").str.ljust(5).iloc[0] +
                " " + temp1["pval_stars"].str.ljust(4).iloc[0]
            )

            # Annotate the values to the right of the plot
            ax.text(
                xlim[1] + fudge,  # Position on the x-axis (right of the plot)
                temp1.index[0],  # Y-coordinate (for each point, use first)
                value_label,  # The value label
                va='center',  # Vertically align to the center of the point
                ha='left',  # Horizontally align to the left
                fontsize=9,
                fontdict={"family": "monospace"},
            )

        ax0 = ax.twinx()
        ax0.set_ylim(temp.index[0] - fudge, temp.index[-1] + fudge)
        ax0.set_yticks([])  # Hide right y-ticks since we're annotating on the left

        ax.set_xlim(xlim[0] - fudge, xlim[1] + fudge)
        ax.set_xticks(np.arange(xlim[0], xlim[1] + 1, 1))

        # Set y-ticks to show mask labels dynamically
        y_ticks = temp.index  # Y-tick locations based on the index of temp
        ax.set_yticks(y_ticks)  # Set y-ticks to the indices

        # Dynamically create y-tick labels based on the current subset
        mask_labels = [mask for mask in masks if mask in temp.MASK.values]
        ax.set_yticklabels(mask_labels[:len(y_ticks)], fontsize=9, fontdict={"family": "monospace"})  # Match lengths

        ax.axvline(x=0, linestyle="--", color="#4f4f4f")

        # Set the title for each subplot to display the phenotype name
        ax.set_title(phenotypes[i], fontsize=10, fontweight='bold')

        # Aesthetics: Hide extra spines and ticks
        ax.tick_params(right=False)
        ax.tick_params(left=False)
        ax.spines["top"].set_alpha(0)
        ax.spines["left"].set_alpha(0)
        ax.spines["right"].set_alpha(0)
        ax.spines["bottom"].set_alpha(0)

        ax0.spines["top"].set_alpha(0)
        ax0.spines["left"].set_alpha(0)
        ax0.spines["right"].set_alpha(0)

        if i != len(phenotypes) - 1:
            ax0.spines["bottom"].set_alpha(0)
            ax.tick_params(bottom=False)

        if i == len(phenotypes) - 1:
            ax.set_xlabel("β")
            ax.tick_params(bottom=True)

    # Set an overall title for the first subplot
    if title:
        plt.suptitle(title, fontsize=12, fontweight='bold', y=0.9)  # Adjust y position to move closer

    # Adjust spacing between plots
    plt.subplots_adjust(hspace=0.25, right=1)  # Adjust vertical spacing (hspace)

    return fig


def plot_QT_grouped_by_mask(
    df,
    width=4,
    height=None,
    phenotypes=None,
    masks=None,
    lw=1.3,
    ms=5,  # Reduced marker size
    fudge=0.6,
    xlim=[-1, 1],
    title=None,
):

    df = df.loc[df.TRAIT == "QT", :]

    just = df.applymap(lambda x: len(str(x)) + 1).max()

    # Create the label column
    df.loc[:, "label"] = (
        df.loc[:, "N_pos"].astype(str).str.ljust(just["N_pos"])
        + df.loc[:, "BETA"].round(2).astype(str).str.ljust(5)
        + "± "
        + df.loc[:, "SE"].round(2).astype(str).str.ljust(5)
        + "p="
        + df.loc[:, "pval"].apply(lambda p: f"{p:.2e}").str.ljust(5)
        + " "
        + df.loc[:, "pval_stars"].str.ljust(4)
    )

    if masks is None:
        masks = df.MASK.unique()
    
    if phenotypes is None:
        phenotypes = df.Phenotype.unique()

    num_masks = len(masks)
    if not height:
        height = 2 * num_masks  # Set height based on number of masks

    colors = plt.cm.viridis(np.linspace(0, 1, len(phenotypes)))

    fig, axes = plt.subplots(nrows=num_masks, sharex=True, figsize=(width, height))

    for i, ax in tqdm(enumerate(axes)):
        temp = df.loc[df.MASK.eq(masks[i]), :]

        for j, phenotype in enumerate(phenotypes):
            temp1 = temp.loc[temp.Phenotype == phenotype]

            if temp1.empty:
                continue  # Skip if temp1 is empty

            # Plot the data points with smaller markers
            ax.errorbar(
                temp1["BETA"],
                [j] * len(temp1),  # Y position corresponds to the phenotype index
                alpha=0.99,
                xerr=temp1["SE"],
                fmt="o",
                c=colors[j],
                ecolor="black",
                ms=ms,  # Smaller marker size
                mew=0.0,
                mec="black",
                elinewidth=lw,
            )

            # Create the label string using the specified format for the right annotation
            value_label = (
                temp1["N_pos"].astype(str).str.ljust(just["N_pos"]).iloc[0] +
                temp1["BETA"].round(2).astype(str).str.ljust(5).iloc[0] +
                "± " + temp1["SE"].round(2).astype(str).str.ljust(5).iloc[0] +
                "p=" + temp1["pval"].apply(lambda p: f"{p:.2e}").str.ljust(5).iloc[0] +
                " " + temp1["pval_stars"].str.ljust(4).iloc[0]
            )

            # Annotate the values to the right of the plot
            ax.text(
                xlim[1] + fudge,  # Position on the x-axis (right of the plot)
                j,  # Y-coordinate (use phenotype index)
                value_label,  # The value label
                va='center',  # Vertically align to the center of the point
                ha='left',  # Horizontally align to the left
                fontsize=9,
                fontdict={"family": "monospace"},
            )
            
        ax0 = ax.twinx()
        ax0.set_ylim(temp.index[0] - fudge, temp.index[-1] + fudge)
        ax0.set_yticks([])  # Hide right y-ticks since we're annotating on the left
            
        ax.set_ylim(-0.5, len(phenotypes) - 0.5)  # Set the limits for y-axis

        ax.set_xlim(xlim[0] - fudge, xlim[1] + fudge)
        ax.set_xticks(np.arange(xlim[0], xlim[1] + 1, 1))

        # Set y-ticks to show phenotype labels dynamically
        ax.set_yticks(range(len(phenotypes)))  # Set y-ticks to the number of unique phenotypes
        ax.set_yticklabels(phenotypes, fontsize=9, fontdict={"family": "monospace"})  # Set y-tick labels

        ax.axvline(x=0, linestyle="--", color="#4f4f4f")

        # Set the title for each subplot to display the mask name
        ax.set_title(masks[i], fontsize=10, fontweight='bold')

        # Aesthetics: Hide extra spines and ticks
        ax.tick_params(right=False)
        ax.tick_params(left=False)
        ax.spines["top"].set_alpha(0)
        ax.spines["left"].set_alpha(0)
        ax.spines["right"].set_alpha(0)
        ax.spines["bottom"].set_alpha(0)
        
        ax0.spines["top"].set_alpha(0)
        ax0.spines["left"].set_alpha(0)
        ax0.spines["right"].set_alpha(0)

        if i != len(masks) - 1:
            ax0.spines["bottom"].set_alpha(0)
            ax.tick_params(bottom=False)

        if i == len(masks) - 1:
            ax.set_xlabel("β")
            ax.tick_params(bottom=True)

    # Set an overall title for the first subplot
    if title:
        plt.suptitle(title, fontsize=12, fontweight='bold', y=0.9)  # Adjust y position to move closer

    # Adjust spacing between plots
    plt.subplots_adjust(hspace=0.25, right=1)  # Adjust vertical spacing (hspace)

    return fig
