"""
Telco Customer Churn Analysis — ABC Communications Ltd
AnalystLab Africa | Data Analytics Internship Programme | Week 1

Loads, cleans, and analyses the Telco Customer Churn dataset, answers the
assignment's business questions, generates the required visualisations,
and prints the resulting business insights and recommendations.

Usage:
    python churn_analysis.py
"""

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATA_PATH = os.path.join("data", "WA_Fn-UseC_-Telco-Customer-Churn.csv")
OUTPUT_DIR = os.path.join("outputs", "charts")

NAVY = "#1F3B57"
TEAL = "#2E8B8B"
CORAL = "#E15759"
GOLD = "#E8A33D"
GREY = "#8C9196"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.titleweight": "bold",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})


# --------------------------------------------------------------------------
# Part 2 — Data Loading & Inspection
# --------------------------------------------------------------------------

def load_and_inspect(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    print("=" * 70)
    print("DATASET INSPECTION")
    print("=" * 70)
    print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"\nData types:\n{df.dtypes}")
    print(f"\nDuplicate customerIDs: {df['customerID'].duplicated().sum()}")
    print(f"Fully duplicated rows: {df.duplicated().sum()}")
    print(f"\nMissing values (raw):\n{df.isnull().sum().sum()} total")

    # TotalCharges is stored as text; convert and expose hidden missing values
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    n_missing = df["TotalCharges"].isna().sum()
    print(f"\nMissing TotalCharges after numeric conversion: {n_missing}")
    print("All correspond to tenure == 0 (brand-new, not yet billed):")
    print(df.loc[df["TotalCharges"].isna(), ["customerID", "tenure", "MonthlyCharges"]])

    # New customers have not accrued charges yet -> fill with 0 rather than drop
    df["TotalCharges"] = df["TotalCharges"].fillna(0)

    print("\nSummary statistics (numeric fields):")
    print(df[["tenure", "MonthlyCharges", "TotalCharges"]].describe().round(2))

    print("\nChurn distribution:")
    print(df["Churn"].value_counts())
    print((df["Churn"].value_counts(normalize=True) * 100).round(1))

    return df


# --------------------------------------------------------------------------
# Part 3 — Business Data Analysis (churn-rate tables + required charts)
# --------------------------------------------------------------------------

def churn_rate_by(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Return churn rate (%) and customer count for each category of `column`."""
    table = pd.crosstab(df[column], df["Churn"], normalize="index") * 100
    table["count"] = df[column].value_counts()
    return table.sort_values("Yes", ascending=False).round(1)


def add_tenure_group(df: pd.DataFrame) -> pd.DataFrame:
    df["tenure_group"] = pd.cut(
        df["tenure"],
        bins=[-1, 12, 24, 48, 72],
        labels=["0-12 mo", "13-24 mo", "25-48 mo", "49-72 mo"],
    )
    return df


def style_ax(ax, title):
    ax.set_title(title, fontsize=14, pad=14, color=NAVY)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", color="#E5E5E5", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)


def save(fig, name):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, name)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Saved: {path}")


def make_bar_charts(df: pd.DataFrame):
    # Bar 1 — Churn rate by Contract
    fig, ax = plt.subplots(figsize=(7, 5))
    ct = pd.crosstab(df["Contract"], df["Churn"], normalize="index")["Yes"] * 100
    ct = ct.reindex(["Month-to-month", "One year", "Two year"])
    bars = ax.bar(ct.index, ct.values, color=[CORAL, GOLD, TEAL], zorder=3, width=0.55)
    for b, v in zip(bars, ct.values):
        ax.text(b.get_x() + b.get_width() / 2, v + 1, f"{v:.1f}%", ha="center",
                 fontsize=11, fontweight="bold", color=NAVY)
    style_ax(ax, "Churn Rate by Contract Type")
    ax.set_ylabel("Churn Rate (%)")
    ax.set_ylim(0, 50)
    save(fig, "bar1_contract.png")

    # Bar 2 — Churn rate by Internet Service
    fig, ax = plt.subplots(figsize=(7, 5))
    ct = pd.crosstab(df["InternetService"], df["Churn"], normalize="index")["Yes"] * 100
    ct = ct.reindex(["Fiber optic", "DSL", "No"])
    bars = ax.bar(ct.index, ct.values, color=[CORAL, GOLD, TEAL], zorder=3, width=0.55)
    for b, v in zip(bars, ct.values):
        ax.text(b.get_x() + b.get_width() / 2, v + 1, f"{v:.1f}%", ha="center",
                 fontsize=11, fontweight="bold", color=NAVY)
    style_ax(ax, "Churn Rate by Internet Service Type")
    ax.set_ylabel("Churn Rate (%)")
    ax.set_ylim(0, 50)
    save(fig, "bar2_internet.png")

    # Bar 3 — Churn rate by Payment Method
    fig, ax = plt.subplots(figsize=(8, 5.5))
    ct = pd.crosstab(df["PaymentMethod"], df["Churn"], normalize="index")["Yes"] * 100
    ct = ct.sort_values(ascending=True)
    bars = ax.barh(ct.index, ct.values, color=TEAL, zorder=3, height=0.55)
    bars[-1].set_color(CORAL)
    for b, v in zip(bars, ct.values):
        ax.text(v + 0.8, b.get_y() + b.get_height() / 2, f"{v:.1f}%", va="center",
                 fontsize=11, fontweight="bold", color=NAVY)
    ax.set_title("Churn Rate by Payment Method", fontsize=14, color=NAVY, pad=14)
    ax.set_xlabel("Churn Rate (%)")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", color="#E5E5E5", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlim(0, 52)
    save(fig, "bar3_payment.png")

    # Bar 4 — Churn rate by tenure group
    df = add_tenure_group(df)
    fig, ax = plt.subplots(figsize=(7, 5))
    ct = pd.crosstab(df["tenure_group"], df["Churn"], normalize="index")["Yes"] * 100
    bars = ax.bar(ct.index.astype(str), ct.values, color=[CORAL, GOLD, "#7CA982", TEAL],
                   zorder=3, width=0.55)
    for b, v in zip(bars, ct.values):
        ax.text(b.get_x() + b.get_width() / 2, v + 1, f"{v:.1f}%", ha="center",
                 fontsize=11, fontweight="bold", color=NAVY)
    style_ax(ax, "Churn Rate by Tenure Group")
    ax.set_ylabel("Churn Rate (%)")
    ax.set_ylim(0, 55)
    save(fig, "bar4_tenure_group.png")


def make_pie_charts(df: pd.DataFrame):
    # Pie 1 — Overall churn split
    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    vals = df["Churn"].value_counts()
    wedges, texts, autotexts = ax.pie(
        vals, labels=["Retained (No)", "Churned (Yes)"], autopct="%1.1f%%",
        colors=[TEAL, CORAL], startangle=90, explode=(0, 0.06),
        wedgeprops={"edgecolor": "white", "linewidth": 2},
    )
    for at in autotexts:
        at.set_color("white")
        at.set_fontweight("bold")
    ax.set_title("Overall Customer Churn Distribution", fontsize=14, color=NAVY, pad=16)
    save(fig, "pie1_churn_distribution.png")

    # Pie 2 — Contract type mix
    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    vals = df["Contract"].value_counts().reindex(["Month-to-month", "One year", "Two year"])
    wedges, texts, autotexts = ax.pie(
        vals, labels=vals.index, autopct="%1.1f%%", colors=[CORAL, GOLD, TEAL],
        startangle=90, wedgeprops={"edgecolor": "white", "linewidth": 2},
    )
    for at in autotexts:
        at.set_color("white")
        at.set_fontweight("bold")
    ax.set_title("Customer Base by Contract Type", fontsize=14, color=NAVY, pad=16)
    save(fig, "pie2_contract_mix.png")


def make_histograms(df: pd.DataFrame):
    # Histogram 1 — Tenure
    fig, ax = plt.subplots(figsize=(7.5, 5))
    ax.hist(df[df["Churn"] == "No"]["tenure"], bins=24, alpha=0.75, label="Retained", color=TEAL, zorder=3)
    ax.hist(df[df["Churn"] == "Yes"]["tenure"], bins=24, alpha=0.75, label="Churned", color=CORAL, zorder=3)
    style_ax(ax, "Distribution of Customer Tenure (months)")
    ax.set_xlabel("Tenure (months)")
    ax.set_ylabel("Number of Customers")
    ax.legend(frameon=False)
    save(fig, "hist1_tenure.png")

    # Histogram 2 — Monthly charges
    fig, ax = plt.subplots(figsize=(7.5, 5))
    ax.hist(df[df["Churn"] == "No"]["MonthlyCharges"], bins=24, alpha=0.75, label="Retained", color=TEAL, zorder=3)
    ax.hist(df[df["Churn"] == "Yes"]["MonthlyCharges"], bins=24, alpha=0.75, label="Churned", color=CORAL, zorder=3)
    style_ax(ax, "Distribution of Monthly Charges")
    ax.set_xlabel("Monthly Charges ($)")
    ax.set_ylabel("Number of Customers")
    ax.legend(frameon=False)
    save(fig, "hist2_monthly_charges.png")


def make_box_plot(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    data = [df[df["Churn"] == "No"]["MonthlyCharges"], df[df["Churn"] == "Yes"]["MonthlyCharges"]]
    bp = ax.boxplot(data, tick_labels=["Retained", "Churned"], patch_artist=True, widths=0.5,
                     medianprops={"color": "white", "linewidth": 2})
    for patch, color in zip(bp["boxes"], [TEAL, CORAL]):
        patch.set_facecolor(color)
        patch.set_alpha(0.85)
    style_ax(ax, "Monthly Charges by Churn Status")
    ax.set_ylabel("Monthly Charges ($)")
    save(fig, "box1_monthly_charges.png")


def make_correlation_heatmap(df: pd.DataFrame):
    dfc = df.copy()
    dfc["Churn_num"] = (dfc["Churn"] == "Yes").astype(int)
    dfc["SeniorCitizen"] = dfc["SeniorCitizen"].astype(int)
    dfc["Partner_num"] = (dfc["Partner"] == "Yes").astype(int)
    dfc["Dependents_num"] = (dfc["Dependents"] == "Yes").astype(int)
    dfc["PaperlessBilling_num"] = (dfc["PaperlessBilling"] == "Yes").astype(int)

    cols = ["tenure", "MonthlyCharges", "TotalCharges", "SeniorCitizen",
            "Partner_num", "Dependents_num", "PaperlessBilling_num", "Churn_num"]
    labels = ["Tenure", "Monthly\nCharges", "Total\nCharges", "Senior\nCitizen",
              "Partner", "Dependents", "Paperless\nBilling", "Churn"]
    corr = dfc[cols].corr()

    print("\nCorrelation matrix:")
    print(corr.round(2))

    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(corr.values, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=10)
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=10)
    for i in range(len(labels)):
        for j in range(len(labels)):
            v = corr.values[i, j]
            color = "white" if abs(v) > 0.55 else "#222222"
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=9, color=color)
    ax.set_title("Correlation Heatmap of Key Numeric & Encoded Features", fontsize=13, color=NAVY, pad=14)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    save(fig, "heatmap_correlation.png")


# --------------------------------------------------------------------------
# Part 4 — Business Insights
# --------------------------------------------------------------------------

def print_insights():
    print("\n" + "=" * 70)
    print("BUSINESS INSIGHTS")
    print("=" * 70)

    insights = [
        "Contract type is the dominant churn lever: month-to-month churns ~15x "
        "more than two-year contracts (42.7% vs 2.8%).",
        "Churn is front-loaded in the customer lifecycle: 47.4% of customers "
        "under 12 months tenure churn, vs 9.5% past 49 months.",
        "Fiber-optic subscribers are the highest-risk product segment (41.9% "
        "churn) despite being ABC's premium, most-subscribed internet product.",
        "Lack of protective add-ons (security, tech support, backup, device "
        "protection) roughly doubles-to-triples churn risk.",
        "Electronic check payers churn 3x more than automatic-payment "
        "customers (45.3% vs 15-17%).",
    ]
    for i, text in enumerate(insights, 1):
        print(f"{i}. {text}")

    risks = [
        "Revenue concentration risk: churned customers have higher average "
        "monthly bills ($74.44) than retained ones ($61.27).",
        "Early-tenure attrition erodes acquisition ROI: ~47% of first-year "
        "customers leave before recouping acquisition cost.",
        "Fiber-optic dissatisfaction could damage brand reputation in the "
        "premium segment if left unaddressed.",
    ]
    print("\nBusiness Risks:")
    for i, text in enumerate(risks, 1):
        print(f"{i}. {text}")

    opportunities = [
        "Contract migration campaigns could cut churn dramatically given the "
        "~15x gap already observed.",
        "A first-90-days retention programme targets the highest-churn window "
        "directly.",
        "Bundling add-on services can raise stickiness while growing average "
        "revenue per user.",
    ]
    print("\nBusiness Opportunities:")
    for i, text in enumerate(opportunities, 1):
        print(f"{i}. {text}")


# --------------------------------------------------------------------------
# Part 5 — Business Recommendations
# --------------------------------------------------------------------------

def print_recommendations():
    print("\n" + "=" * 70)
    print("BUSINESS RECOMMENDATIONS")
    print("=" * 70)

    recommendations = [
        "Launch a contract-conversion incentive for month-to-month customers "
        "moving to 1- or 2-year contracts.",
        "Build a first-90-days retention programme for new sign-ups "
        "(proactive check-ins, month-12 loyalty milestone).",
        "Investigate the fiber-optic service experience (pricing and quality "
        "review vs. DSL).",
        "Bundle protective services (Online Security, Tech Support) into core "
        "packages for at-risk segments.",
        "Nudge Electronic Check payers toward automatic payment methods with "
        "a small incentive.",
        "Prioritise retention outreach by expected revenue at risk, not churn "
        "probability alone.",
    ]
    for i, text in enumerate(recommendations, 1):
        print(f"{i}. {text}")


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main():
    df = load_and_inspect(DATA_PATH)

    print("\n" + "=" * 70)
    print("CHURN RATE BY SEGMENT")
    print("=" * 70)
    for col in ["Contract", "InternetService", "PaymentMethod", "SeniorCitizen",
                "Partner", "Dependents", "PaperlessBilling", "OnlineSecurity",
                "TechSupport"]:
        print(f"\n--- {col} ---")
        print(churn_rate_by(df, col))

    print("\nGenerating charts...")
    make_bar_charts(df)
    make_pie_charts(df)
    make_histograms(df)
    make_box_plot(df)
    make_correlation_heatmap(df)

    print_insights()
    print_recommendations()

    print(f"\nAll charts saved to: {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
