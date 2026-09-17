# F1Next — Machine Learning-Based Formula 1 Race and Championship Prediction

## 📌 Project Overview

F1Next is a machine learning project designed to analyze historical Formula 1 race data and predict driver performance.

The project uses historical Formula 1 race and qualifying information to predict:

1. **Race Finishing Position** — Regression
2. **Podium Finish (Yes/No)** — Classification

The project follows a chronological machine learning approach so that future seasons are not used to train models for earlier seasons.

---

## 🎯 Objectives

The main objectives of F1Next are:

- Analyze historical Formula 1 race and qualifying data.
- Perform Exploratory Data Analysis (EDA).
- Preprocess and clean the dataset.
- Engineer historical driver and constructor performance features.
- Predict race finishing positions using regression algorithms.
- Predict whether a driver will finish on the podium using classification algorithms.
- Compare multiple machine learning algorithms.
- Evaluate models using appropriate performance metrics.
- Use the trained system for future Formula 1 prediction.

---

## 📊 Dataset

The project uses Formula 1 race and qualifying data covering:

**2010–2025**

The dataset contains information related to:

- Race seasons
- Race rounds
- Drivers
- Constructors
- Grid positions
- Qualifying positions
- Race finishing positions
- Race points
- Previous race performance
- Driver historical performance
- Constructor performance

The combined dataset contains approximately **6,911 race-driver records**.

---

## 🔍 Exploratory Data Analysis

EDA was performed to understand the structure and characteristics of the dataset.

The following analyses were performed:

- Dataset shape and structure
- Data types
- Missing-value analysis
- Duplicate analysis
- Statistical summary
- Finishing-position distribution
- Podium vs non-podium distribution
- Feature distributions
- Correlation heatmap
- Feature-target scatter plots

Important observations included relationships between qualifying performance, historical finishing performance, accumulated points, and race finishing position.

---

## 🧹 Data Preprocessing

The following preprocessing steps were performed:

- Missing-value analysis
- Duplicate checking
- Data type conversion
- Invalid-value checking
- Chronological sorting
- Feature engineering
- Outlier analysis
- Missing historical-feature handling
- Classification target creation
- Feature selection
- Feature scaling

### Missing Values

Missing values were identified in several raw qualifying and fastest-lap attributes.

These attributes were not included in the final 14-feature modeling set.

The final modeling features were checked to ensure that no missing values remained.

### Outliers

The IQR method was used to identify potential outliers.

Extreme values were examined in the context of Formula 1 data rather than being automatically removed, since some extreme values represent legitimate race or driver-performance conditions.

---

## 🧠 Feature Engineering

Historical and performance-based features were created to improve prediction.

The final 14 features are:

1. `qualifying_position`
2. `grid`
3. `previous_finish`
4. `avg_finish_all_previous`
5. `avg_qualifying_all_previous`
6. `avg_finish_last_5`
7. `avg_qualifying_last_5`
8. `season_points_so_far`
9. `season_wins_so_far`
10. `season_podiums_so_far`
11. `constructor_points_so_far`
12. `constructor_wins_so_far`
13. `constructor_podiums_so_far`
14. `career_races_before`

Historical features were generated using previous race information to reduce target leakage.

---

# 📈 Regression

## Regression Target

The regression target is:

```text
finish_position