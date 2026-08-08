# Telco Customer Churn Analysis — ABC Communications Ltd

Business analytics case study completed for the **AnalystLab Africa Data Analytics Internship Programme** (Week 1: Business Analytics Case Study).

Acting as a Junior Data Analyst at AnalystLab Africa Consulting, this project investigates customer churn for ABC Communications Ltd and delivers data-driven retention recommendations for management.

## Business Questions

1. What does the customer base look like?
2. Which segments have the highest churn?
3. Does contract type influence retention?
4. Does tenure affect loyalty?
5. Which services influence churn?
6. Which payment methods have higher churn?
7. What actions should management take?

## Dataset

[Telco Customer Churn Dataset](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) — 7,043 customers, 21 attributes covering demographics, account/contract details, subscribed services, billing, and churn outcome.

## Repository Structure

```
.
├── churn_analysis.py                    # Full analysis script (cleaning, EDA, charts, insights)
├── requirements.txt                     # Python dependencies
├── data/
│   └── WA_Fn-UseC_-Telco-Customer-Churn.csv
├── outputs/
│   └── charts/                          # Generated PNG charts (created on run)
├── Telco_Churn_Analysis.ipynb           # Notebook version with narrative + embedded charts
├── Business_Understanding_Report.docx   # Part 1 — business research report
├── Dataset_Inspection_Report.docx       # Part 2 — data quality & inspection report
└── Churn_Business_Presentation.pptx     # Business presentation for stakeholders
```

## Key Findings

| Driver | Finding |
|---|---|
| **Contract type** | Month-to-month customers churn at **42.7%** vs **2.8%** for two-year contracts — the strongest churn signal in the data |
| **Tenure** | Churn is front-loaded: **47.4%** of customers under 12 months churn, vs **9.5%** past 49 months |
| **Internet service** | Fiber-optic subscribers churn at **41.9%**, more than double DSL (19.0%) |
| **Add-on services** | Customers without Online Security or Tech Support churn at **~2.5–3x** the rate of those with it |
| **Payment method** | Electronic check payers churn at **45.3%**, ~3x automatic-payment customers (15–17%) |

Overall churn rate: **26.5%** (1,869 of 7,043 customers).

## Recommendations

1. Launch a contract-conversion incentive to migrate month-to-month customers onto 1–2 year plans.
2. Build a first-90-days retention programme targeting the highest-risk early-tenure window.
3. Investigate the fiber-optic service experience (pricing and quality review).
4. Bundle protective add-ons (Security, Tech Support) into core packages for at-risk segments.
5. Nudge Electronic Check payers toward automatic payment methods.
6. Prioritise retention outreach by expected revenue at risk, not churn probability alone.

Full analysis, visualisations (3 bar charts, 2 pie charts, 2 histograms, 1 box plot, 1 correlation heatmap), and detailed interpretations are in [`Telco_Churn_Analysis.ipynb`](Telco_Churn_Analysis.ipynb) and [`churn_analysis.py`](churn_analysis.py).

## How to Run

```bash
# Clone the repository
git clone https://github.com/<your-username>/telco-churn-analysis.git
cd telco-churn-analysis

# Install dependencies
pip install -r requirements.txt

# Run the analysis script
python churn_analysis.py
```

Charts are saved to `outputs/charts/` and key statistics are printed to the console.

Alternatively, open `Telco_Churn_Analysis.ipynb` in Jupyter to explore the full narrative walkthrough.

## Tools & Libraries

- Python (pandas, numpy, matplotlib)
- Jupyter Notebook
- Microsoft Word / PowerPoint (business deliverables)

## Author

Benissan LENDIT Data analyst Intern, [AnalystLab Africa](https://analystlabafrica.com) Data Analytics Internship Programme.

#AnalystLabAfrica

