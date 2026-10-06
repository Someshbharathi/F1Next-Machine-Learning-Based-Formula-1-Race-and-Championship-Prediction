# ============================================================
# F1Next - VISUAL PROJECT REPORT GENERATOR
# Creates a Word document with tables, graphs, and results
# ============================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION

# ------------------------------------------------------------
# 1. CONFIGURATION
# ------------------------------------------------------------

DATA_PATH = "data/processed/f1_master_dataset_final.csv"
OUTPUT_DIR = "F1Next_Report_Assets"
REPORT_PATH = "F1Next_Project_Report.docx"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# If your dataset is in another location, change DATA_PATH.
df = pd.read_csv(DATA_PATH)

# ------------------------------------------------------------
# 2. REGRESSION RESULTS (2024 VALIDATION COMPARISON)
# ------------------------------------------------------------

regression_results = [
    ["Lasso Regression", 0.5670, 3.7874, 2.9472],
    ["ElasticNet Regression", 0.5668, 3.7886, 2.9439],
    ["Ridge Regression", 0.5658, 3.7928, 2.9368],
    ["Linear Regression", 0.5657, 3.7931, 2.9368],
    ["Polynomial Regression", 0.5538, 3.8449, 3.0167],
    ["Gradient Boosting", 0.5317, 3.9389, 3.0900],
    ["Random Forest", 0.5095, 4.0311, 3.1600],
    ["KNN Regressor", 0.4362, 4.3218, 3.3712],
    ["SVR", 0.4312, 4.3410, 3.1816],
    ["Decision Tree", -0.2615, 6.6494, 4.8343],
]

regression_df = pd.DataFrame(
    regression_results,
    columns=["Model", "R2", "RMSE", "MAE"]
)

# ------------------------------------------------------------
# 3. CLASSIFICATION RESULTS
# ------------------------------------------------------------

classification_results = [
    ["Logistic Regression", 0.8310, 0.8760, 0.9210],
    ["SVC", 0.8310, 0.8810, 0.9280],
    ["KNN", 0.8430, 0.8620, 0.8690],
    ["Gaussian Naive Bayes", 0.8058, 0.8260, 0.8260],
    ["Decision Tree", 0.8539, 0.8577, 0.7425],
]

classification_df = pd.DataFrame(
    classification_results,
    columns=["Model", "Accuracy", "Weighted F1", "ROC-AUC"]
)

# ------------------------------------------------------------
# 4. HYPERPARAMETER TUNING AND CROSS-VALIDATION RESULTS
# ------------------------------------------------------------

cv_results = [
    ["Lasso", 0.4122],
    ["ElasticNet", 0.4133],
]

tuning_results = [
    ["Lasso", "alpha = 0.05", 0.415],
    ["ElasticNet", "alpha = 0.05, l1_ratio = 0.9", 0.415],
]

tuned_results = [
    ["Tuned Lasso", 0.5676, 3.7849, 2.9587],
    ["Tuned ElasticNet", 0.5675, 3.7856, 2.9582],
]

final_test_results = [
    ["Tuned Lasso", 0.4518, 4.2618, 3.1280],
]

# ------------------------------------------------------------
# 5. RANDOM FOREST FEATURE IMPORTANCE
# ------------------------------------------------------------

feature_importance = [
    ["qualifying_position", 0.3567],
    ["avg_qualifying_last_5", 0.1248],
    ["avg_finish_all_previous", 0.0775],
    ["avg_finish_last_5", 0.0708],
    ["avg_qualifying_all_previous", 0.0693],
    ["career_races_before", 0.0641],
    ["constructor_points_so_far", 0.0608],
    ["previous_finish", 0.0469],
    ["season_points_so_far", 0.0418],
    ["grid", 0.0396],
    ["constructor_podiums_so_far", 0.0180],
    ["season_podiums_so_far", 0.0130],
    ["constructor_wins_so_far", 0.0092],
    ["season_wins_so_far", 0.0073],
]

importance_df = pd.DataFrame(
    feature_importance,
    columns=["Feature", "Importance"]
)

# ------------------------------------------------------------
# 6. CREATE GRAPHS
# ------------------------------------------------------------

sns.set_theme(style="whitegrid")

feature_columns = [
    "qualifying_position", "grid", "previous_finish",
    "avg_finish_all_previous", "avg_qualifying_all_previous",
    "avg_finish_last_5", "avg_qualifying_last_5",
    "season_points_so_far", "season_wins_so_far",
    "season_podiums_so_far", "constructor_points_so_far",
    "constructor_wins_so_far", "constructor_podiums_so_far",
    "career_races_before"
]

# A. Finishing position distribution
plt.figure(figsize=(9, 5))
sns.histplot(df["position"], bins=20, kde=False)
plt.title("Distribution of F1 Finishing Positions")
plt.xlabel("Finishing Position")
plt.ylabel("Number of Records")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/finishing_position.png", dpi=200)
plt.close()

# B. Podium distribution
plt.figure(figsize=(7, 5))
podium_counts = df["podium"].map({0: "No Podium", 1: "Podium"}).value_counts()
podium_counts = podium_counts.reindex(["No Podium", "Podium"])
podium_counts.plot(kind="bar")
plt.title("Podium vs No Podium Distribution")
plt.xlabel("Class")
plt.ylabel("Number of Records")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/podium_distribution.png", dpi=200)
plt.close()

# C. Feature distributions
available_features = [c for c in feature_columns if c in df.columns]

df[available_features].hist(
    figsize=(16, 13),
    bins=25,
    edgecolor="black"
)
plt.suptitle("Distribution of Model Features", fontsize=18)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/feature_distributions.png", dpi=200)
plt.close()

# D. Correlation heatmap
corr_columns = available_features + ["position"]
corr_columns = [c for c in corr_columns if c in df.columns]

plt.figure(figsize=(15, 11))
sns.heatmap(
    df[corr_columns].corr(numeric_only=True),
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    annot_kws={"size": 7}
)
plt.title("Correlation Heatmap of Features and Finishing Position")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/correlation_heatmap.png", dpi=200)
plt.close()

# E. Qualifying position vs finishing position
plt.figure(figsize=(8, 5))
plt.scatter(
    df["qualifying_position"],
    df["position"],
    alpha=0.4
)
plt.title("Qualifying Position vs Finishing Position")
plt.xlabel("Qualifying Position")
plt.ylabel("Finishing Position")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/qualifying_vs_finish.png", dpi=200)
plt.close()

# F. Recent qualifying performance vs finishing position
plt.figure(figsize=(8, 5))
plt.scatter(
    df["avg_qualifying_last_5"],
    df["position"],
    alpha=0.4
)
plt.title("Recent Qualifying Performance vs Finishing Position")
plt.xlabel("Average Qualifying Position - Last 5 Races")
plt.ylabel("Finishing Position")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/recent_qualifying_vs_finish.png", dpi=200)
plt.close()

# G. Regression model R² comparison
plot_df = regression_df.sort_values("R2", ascending=True)

plt.figure(figsize=(10, 6))
plt.barh(plot_df["Model"], plot_df["R2"])
plt.title("Regression Model Comparison - R²")
plt.xlabel("R² Score")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/regression_r2.png", dpi=200)
plt.close()

# H. Regression RMSE comparison
plot_df = regression_df.sort_values("RMSE", ascending=True)

plt.figure(figsize=(10, 6))
plt.barh(plot_df["Model"], plot_df["RMSE"])
plt.title("Regression Model Comparison - RMSE")
plt.xlabel("RMSE")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/regression_rmse.png", dpi=200)
plt.close()

# I. Classification accuracy comparison
plot_df = classification_df.sort_values("Accuracy", ascending=True)

plt.figure(figsize=(9, 5))
plt.barh(plot_df["Model"], plot_df["Accuracy"])
plt.title("Classification Model Comparison - Accuracy")
plt.xlabel("Accuracy")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/classification_accuracy.png", dpi=200)
plt.close()

# J. Random Forest feature importance
plot_df = importance_df.sort_values("Importance", ascending=True)

plt.figure(figsize=(10, 7))
plt.barh(plot_df["Feature"], plot_df["Importance"])
plt.title("Random Forest Feature Importance")
plt.xlabel("Importance")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/feature_importance.png", dpi=200)
plt.close()

# ------------------------------------------------------------
# 7. CREATE WORD DOCUMENT
# ------------------------------------------------------------

doc = Document()

# Page margins
section = doc.sections[0]
section.top_margin = Inches(0.65)
section.bottom_margin = Inches(0.65)
section.left_margin = Inches(0.75)
section.right_margin = Inches(0.75)

# Default font
style = doc.styles["Normal"]
style.font.name = "Arial"
style.font.size = Pt(10)

# Title page
title = doc.add_heading("F1Next", 0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

subtitle = doc.add_paragraph(
    "Machine Learning-Based Formula 1 Race and Championship Prediction"
)
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_paragraph()
p = doc.add_paragraph("Machine Learning Project Report")
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph("Review 1 - Regression and Classification Part A")
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_paragraph()
p = doc.add_paragraph("Prepared by: Somesh Bharathi")
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_page_break()

# Helper functions
def add_heading(text, level=1):
    doc.add_heading(text, level=level)

def add_table(dataframe, number_format=None):
    table = doc.add_table(rows=1, cols=len(dataframe.columns))
    table.style = "Light Shading Accent 1"

    for i, column in enumerate(dataframe.columns):
        table.rows[0].cells[i].text = str(column)

    for _, row in dataframe.iterrows():
        cells = table.add_row().cells
        for i, value in enumerate(row):
            if isinstance(value, (float, np.floating)):
                cells[i].text = f"{value:.4f}"
            else:
                cells[i].text = str(value)

    doc.add_paragraph()

def add_image(path, caption, width=6.2):
    doc.add_picture(path, width=Inches(width))
    p = doc.add_paragraph(caption)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

# ------------------------------------------------------------
# 8. REPORT CONTENT
# ------------------------------------------------------------

add_heading("1. Project Overview")

doc.add_paragraph(
    "F1Next is a machine learning project designed to predict Formula 1 "
    "race performance using historical race results, qualifying performance, "
    "driver statistics, and constructor statistics. The project explores "
    "regression models for predicting finishing position and classification "
    "models for predicting whether a driver finishes on the podium."
)

add_heading("2. Project Objectives")

for item in [
    "Predict a driver's finishing position using historical F1 data.",
    "Classify whether a driver achieves a podium finish.",
    "Compare multiple regression and classification algorithms.",
    "Evaluate models using appropriate performance metrics.",
    "Identify features that contribute to predicted race performance.",
]:
    doc.add_paragraph(item, style="List Bullet")

add_heading("3. Dataset Description")

doc.add_paragraph(
    "The dataset contains Formula 1 race and qualifying records from "
    "2010 to 2025. Race results and qualifying data were merged using "
    "season, round, and driver ID."
)

doc.add_paragraph(f"Total records: {len(df):,}")
doc.add_paragraph(f"Total columns in the final dataset: {len(df.columns)}")

add_heading("4. Data Preprocessing")

preprocessing_steps = [
    "Combined race results and qualifying datasets.",
    "Checked dataset shape, column types, missing values, and duplicate records.",
    "Handled missing qualifying positions using the starting grid position.",
    "Sorted records chronologically by season, round, and date.",
    "Created historical driver performance features using previous race data.",
    "Created season-to-date driver and constructor statistics.",
    "Created career experience features.",
    "Created the binary podium target: 1 for a top-three finish, otherwise 0.",
    "Checked feature outliers using the IQR method and retained valid F1 extremes.",
    "Applied StandardScaler, fitting it only on the training data.",
]

for item in preprocessing_steps:
    doc.add_paragraph(item, style="List Number")

add_heading("5. Feature Engineering")

doc.add_paragraph(
    "The project uses qualifying position, grid position, previous finishing "
    "results, historical averages, recent five-race performance, season-to-date "
    "statistics, constructor performance, and driver career experience."
)

doc.add_paragraph(
    "Historical features were shifted to use information from previous races "
    "rather than the current race outcome. This helps prevent target leakage."
)

add_heading("6. Dataset Split")

split_df = pd.DataFrame(
    [
        ["Training", "2010–2023", 5953],
        ["Validation", "2024", 479],
        ["Testing", "2025", 479],
        ["Future prediction", "2026", "Not included in training/testing"],
    ],
    columns=["Dataset", "Seasons", "Records"]
)

add_table(split_df)

doc.add_paragraph(
    "A chronological split was used to reflect the forecasting task: "
    "older seasons are used for training, followed by validation on 2024 "
    "and testing on 2025."
)

add_heading("7. Exploratory Data Analysis (EDA)")

doc.add_paragraph(
    "EDA was performed to understand the distribution of race results, "
    "feature values, class balance, and relationships between variables."
)

add_image(
    f"{OUTPUT_DIR}/finishing_position.png",
    "Figure 1. Distribution of finishing positions."
)

add_image(
    f"{OUTPUT_DIR}/podium_distribution.png",
    "Figure 2. Distribution of podium and non-podium outcomes."
)

add_image(
    f"{OUTPUT_DIR}/feature_distributions.png",
    "Figure 3. Distributions of the numerical model features.",
    width=6.5
)

add_image(
    f"{OUTPUT_DIR}/correlation_heatmap.png",
    "Figure 4. Correlation heatmap of model features and finishing position.",
    width=6.5
)

add_image(
    f"{OUTPUT_DIR}/qualifying_vs_finish.png",
    "Figure 5. Relationship between qualifying position and finishing position."
)

add_image(
    f"{OUTPUT_DIR}/recent_qualifying_vs_finish.png",
    "Figure 6. Relationship between recent qualifying performance and finishing position."
)

add_heading("8. Regression Models")

doc.add_paragraph(
    "Ten regression algorithms were trained using the 2010–2023 training "
    "data. Their initial comparison was performed using the 2024 validation "
    "dataset. The evaluation metrics were R², RMSE, and MAE."
)

add_table(regression_df)

add_image(
    f"{OUTPUT_DIR}/regression_r2.png",
    "Figure 7. R² comparison across regression models."
)

add_image(
    f"{OUTPUT_DIR}/regression_rmse.png",
    "Figure 8. RMSE comparison across regression models."
)

add_heading("9. Cross-Validation and Hyperparameter Tuning")

doc.add_paragraph(
    "Five-fold cross-validation was conducted for Lasso and ElasticNet. "
    "Hyperparameter tuning was performed using GridSearchCV."
)

add_heading("Cross-validation results", 2)
add_table(pd.DataFrame(cv_results, columns=["Model", "Mean CV R²"]))

add_heading("Best hyperparameters", 2)
add_table(pd.DataFrame(
    tuning_results,
    columns=["Model", "Best Parameters", "Best CV R²"]
))

add_heading("Tuned model validation results", 2)
add_table(pd.DataFrame(
    tuned_results,
    columns=["Model", "R²", "RMSE", "MAE"]
))

add_heading("10. Regression Final Test Result")

add_table(pd.DataFrame(
    final_test_results,
    columns=["Model", "R²", "RMSE", "MAE"]
))

doc.add_paragraph(
    "The final test result shown above is from the 2025 test dataset. "
    "The tuned Lasso model achieved an R² of 0.4518, RMSE of 4.2618, "
    "and MAE of 3.1280."
)

add_heading("11. Feature Importance")

doc.add_paragraph(
    "Random Forest feature importance was used to examine which input "
    "features contributed most to the model's predictions. Qualifying "
    "position had the largest reported importance."
)

add_table(importance_df)

add_image(
    f"{OUTPUT_DIR}/feature_importance.png",
    "Figure 9. Random Forest feature importance."
)

add_heading("12. Classification Models")

doc.add_paragraph(
    "The classification task predicts whether a driver finishes in the "
    "top three. The target is 1 for a podium finish and 0 otherwise."
)

doc.add_paragraph(
    "Five algorithms were evaluated: Logistic Regression, K-Nearest "
    "Neighbors, Gaussian Naive Bayes, Decision Tree, and Support Vector "
    "Classifier. Metrics include Accuracy, Weighted F1, and ROC-AUC."
)

add_table(classification_df)

add_image(
    f"{OUTPUT_DIR}/classification_accuracy.png",
    "Figure 10. Classification model accuracy comparison."
)

add_heading("13. Model Selection Summary")

doc.add_paragraph(
    "For regression, Lasso and ElasticNet were among the strongest models "
    "in the initial 2024 validation comparison and were selected for "
    "cross-validation and hyperparameter tuning. Tuned Lasso was evaluated "
    "on the 2025 test dataset."
)

doc.add_paragraph(
    "For classification, all five required algorithms were compared using "
    "Accuracy, Weighted F1, and ROC-AUC. The model selection should consider "
    "the podium class imbalance and the project's evaluation requirements."
)

add_heading("14. Conclusion")

doc.add_paragraph(
    "F1Next combines historical race results, qualifying information, and "
    "driver and constructor performance statistics to predict Formula 1 "
    "finishing positions and podium outcomes. The project completed data "
    "preprocessing, feature engineering, exploratory data analysis, "
    "regression model comparison, classification model comparison, and "
    "initial model tuning. Further work can include the remaining "
    "classification algorithms and clustering tasks required for the next review."
)

add_heading("15. Tools and Technologies")

for item in [
    "Python",
    "Pandas and NumPy",
    "Matplotlib and Seaborn",
    "Scikit-learn",
    "Jupyter Notebook",
    "Microsoft Word document generation using python-docx",
]:
    doc.add_paragraph(item, style="List Bullet")

# ------------------------------------------------------------
# 9. SAVE REPORT
# ------------------------------------------------------------

doc.save(REPORT_PATH)

print("========================================")
print("F1Next report generated successfully!")
print("Report:", os.path.abspath(REPORT_PATH))
print("Graphs folder:", os.path.abspath(OUTPUT_DIR))
print("========================================")