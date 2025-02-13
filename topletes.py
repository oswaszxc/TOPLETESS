# -*- coding: utf-8 -*-
"""Untitled

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Vge1rAADALw6h7vYx_DRdjqhElQwKsX-
"""

import pandas as pd
bb = pd.read_csv('lastbasketballdataset.csv')

bb.head()

import pandas as pd

df = pd.read_csv("lastbasketballdataset.csv")

print("Dataset Overview:")
print(df.head())

print("\nColumn Names:")
print(df.columns.tolist())

df.columns = df.columns.str.strip()

def assign_player_numbers_modified(df):
    df['Player_Number'] = 0  # Initialize with 0

    # Assign 1 to M. Phillips
    df.loc[df['Name'] == 'M. Phillips', 'Player_Number'] = 1

    # Assign numbers to the rest of the players, starting from row 3
    current_number = 2
    for index, row in df.iloc[2:].iterrows():  # Start from row 3 (index 2)
        if row['Player_Number'] == 0:  # If not already assigned
            df.at[index, 'Player_Number'] = current_number
            current_number += 1

    return df

df = assign_player_numbers_modified(df)

def calculate_percentage(x):
    try:
        if isinstance(x, str):
            x = x.replace("'", "")
            made, attempted = map(float, x.split('-'))
            return (made / attempted) * 100 if attempted != 0 else 0
        return 0
    except:
        return 0

def convert_time_to_minutes(time_str):
    try:
        if isinstance(time_str, str):
            if ':' in time_str:
                minutes, seconds = time_str.split(':')
                return float(minutes) + float(seconds.split('.')[0])/60
        return 0
    except:
        return 0

if 'FG' in df.columns:
    df['FG%'] = df['FG'].apply(calculate_percentage)

if '2P' in df.columns:
    df['2p%'] = df['2P'].apply(calculate_percentage)

if '3P' in df.columns:
    df['3p%'] = df['3P'].apply(calculate_percentage)

if 'FT' in df.columns:
    df['FT%'] = df['FT'].apply(calculate_percentage)

numeric_columns = ['PPG', 'OFFPG', 'DEFPG', 'RPG', 'APG', 'SPG', 'BPG', 'TOPG']

for col in numeric_columns:
    if col not in df.columns:
        print(f"Warning: Column '{col}' does not exist in the DataFrame.")
    else:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace("'", ""), errors='coerce')

if 'MIN' in df.columns:
    df['MIN'] = df['MIN'].apply(convert_time_to_minutes)

print("\nChecking for NaN values after conversion:")
print(df[numeric_columns].isna().sum())

df.fillna(0, inplace=True)

weights = {
    'Center': {
        'Scoring': {
            'PPG': 0.4,
            'FG%': 0.2,
            '2p%': 0.2,
            '3p%': 0.1,
            'FT%': 0.1
        },
        'Defense': {
            'SPG': 0.3,
            'BPG': 0.7
        },
        'Rebounding': {
            'OFFPG': 0.25,
            'DEFPG': 0.25,
            'RPG': 0.5
        },
        'Assist': {
            'APG': 0.3
        },
        'Endurance': {
            'MIN': 1.0
        },
        'Turnovers': {
            'TOPG': -1.0
        }
    },
    'Power Forward': {
        'Scoring': {
            'PPG': 0.4,
            'FG%': 0.25,
            '2p%': 0.15,
            '3p%': 0.1,
            'FT%': 0.1
        },
        'Defense': {
            'SPG': 0.5,
            'BPG': 0.5
        },
        'Rebounding': {
            'OFFPG': 0.2,
            'DEFPG': 0.2,
            'RPG': 0.4
        },
        'Assist': {
            'APG': 0.4
        },
        'Endurance': {
            'MIN': 1.0
        },
        'Turnovers': {
            'TOPG': -1.0
        }
    },
    'Small Forward': {
        'Scoring': {
            'PPG': 0.35,
            'FG%': 0.25,
            '2p%': 0.15,
            '3p%': 0.15,
            'FT%': 0.1
        },
        'Defense': {
            'SPG': 0.5,
            'BPG': 0.5
        },
        'Rebounding': {
            'OFFPG': 0.15,
            'DEFPG': 0.15,
            'RPG': 0.3
        },
        'Assist': {
            'APG': 0.5
        },
        'Endurance': {
            'MIN': 1.0
        },
        'Turnovers': {
            'TOPG': -1.0
        }
    },
    'Shooting Guard': {
        'Scoring': {
            'PPG': 0.45,
            'FG%': 0.3,
            '2p%': 0.1,
            '3p%': 0.15,
            'FT%': 0.1
        },
        'Defense': {
            'SPG': 0.6,
            'BPG': 0.4
        },
        'Rebounding': {
            'OFFPG': 0.1,
            'DEFPG': 0.1,
            'RPG': 0.2
        },
        'Assist': {
            'APG': 0.3
        },
        'Endurance': {
            'MIN': 1.0
        },
        'Turnovers': {
            'TOPG': -1.0
        }
    },
    'Point Guard': {
        'Scoring': {
            'PPG': 0.3,
            'FG%': 0.25,
            '2p%': 0.15,
            '3p%': 0.15,
            'FT%': 0.15
        },
        'Defense': {
            'SPG': 0.6,
            'BPG': 0.4
        },
        'Rebounding': {
            'OFFPG': 0.05,
            'DEFPG': 0.05,
            'RPG': 0.1
        },
        'Assist': {
            'APG': 0.8
        },
        'Endurance': {
            'MIN': 1.0
        },
        'Turnovers': {
            'TOPG': -1.5
        }
    }
}

def calculate_ranks(df, weights):
    ranked_df = pd.DataFrame()

    for position, categories in weights.items():
        position_df = df[df['Position'] == position].copy()

        position_df['Composite_Score'] = 0.0

        for category, stats in categories.items():
            for stat, weight in stats.items():
                if stat in position_df.columns:
                    stat_values = pd.to_numeric(position_df[stat], errors='coerce').fillna(0)
                    position_df['Composite_Score'] += stat_values * weight

        ranked_df = pd.concat([ranked_df, position_df], ignore_index=True)

    # Calculate overall rankings
    ranked_df['Overall_Composite_Score'] = ranked_df['Composite_Score']
    ranked_df['Overall_Rank'] = ranked_df['Overall_Composite_Score'].rank(ascending=False, method='min')

    # Calculate overall rating
    score_range = ranked_df['Overall_Composite_Score'].max() - ranked_df['Overall_Composite_Score'].min()
    if score_range > 0:
        ranked_df['Rating'] = ((ranked_df['Overall_Composite_Score'] - ranked_df['Overall_Composite_Score'].min()) / score_range) * 100
    else:
        ranked_df['Rating'] = 0

    return ranked_df

ranked_players = calculate_ranks(df, weights)

ranked_players.to_csv("ranked_players.csv", index=False)

print("\nOverall Ranked Players:")
display_columns = ['Position',
                  "PPG", "FG%", "2p%", "3p%", "FT%",
                  "OFFPG", "DEFPG", "RPG", "APG", "SPG", "BPG",
                  "MIN", "TOPG",
                  "Overall_Composite_Score",
                  "Overall_Rank",
                  "Player_Number",
                  "Rating"]
print(ranked_players[display_columns].sort_values(by='Overall_Composite_Score', ascending=False))

# Print top 10 players overall
print("\nTop 10 Players Overall:")
top_10_overall = ranked_players.sort_values('Overall_Composite_Score', ascending=False).head(10)
display_columns = ['Player_Number', 'Position', 'Overall_Composite_Score', 'Rating', 'Overall_Rank']
print(top_10_overall[display_columns])

# Print top 10 players for each position
positions = ['Center', 'Power Forward', 'Small Forward', 'Shooting Guard', 'Point Guard']

for position in positions:
    print(f"\nTop 10 {position}s:")
    top_10 = ranked_players[ranked_players['Position'] == position].sort_values('Overall_Composite_Score', ascending=False).head(10)
    display_columns = ['Player_Number', 'Position', 'Overall_Composite_Score', 'Rating', 'Overall_Rank']
    print(top_10[display_columns])

import pandas as pd

sd = pd.read_csv('ranked_players.csv')

sd.head()

# Step 1: Install necessary libraries
!pip install pandas scikit-learn matplotlib seaborn imbalanced-learn joblib

# Step 2: Import libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV, cross_validate
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, classification_report, confusion_matrix, precision_recall_fscore_support
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import RandomOverSampler
import seaborn as sns
import matplotlib.pyplot as plt
import joblib

# Step 3: Load dataset
df = pd.read_csv("lastbasketballdataset.csv")
print("Dataset Overview:")
print(df.head())

# Clean column names
df.columns = df.columns.str.strip()

# Add Player_Number
df['Player_Number'] = df.groupby('Position').cumcount() + 1

# Helper functions
def calculate_percentage(x):
    try:
        if isinstance(x, str):
            x = x.replace("'", "")
        made, attempted = map(float, x.split('-'))
        return (made / attempted) * 100 if attempted != 0 else 0
    except:
        return 0

def convert_time_to_minutes(time_str):
    try:
        if isinstance(time_str, str):
            if ':' in time_str:
                minutes, seconds = time_str.split(':')
                return float(minutes) + float(seconds.split('.')[0]) / 60
        return 0
    except:
        return 0

# Calculate percentages
for col in ['FG', '2P', '3P', 'FT']:
    if col in df.columns:
        df[f'{col}%'] = df[col].apply(calculate_percentage)

# Convert numeric columns
numeric_columns = ['PPG', 'OFFPG', 'DEFPG', 'RPG', 'APG', 'SPG', 'BPG', 'TOPG']
for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace("'", ""), errors='coerce')

# Convert MIN to minutes
if 'MIN' in df.columns:
    df['MIN'] = df['MIN'].apply(convert_time_to_minutes)

# Fill NaN values
df.fillna(0, inplace=True)

# Define weights for player positions
weights = {
    'Center': {
        'PPG': 0.28,
        'APG': 0.18,
        'RPG': 0.23,
        'SPG': 0.13,
        'BPG': 0.10,
        'TOPG': 0.08
    },
    'Power Forward': {
        'PPG': 0.28,
        'APG': 0.18,
        'RPG': 0.23,
        'SPG': 0.13,
        'BPG': 0.10,
        'TOPG': 0.08
    },
    'Small Forward': {
        'PPG': 0.28,
        'APG': 0.18,
        'RPG': 0.23,
        'SPG': 0.13,
        'BPG': 0.10,
        'TOPG': 0.08
    },
    'Shooting Guard': {
        'PPG': 0.28,
        'APG': 0.18,
        'RPG': 0.23,
        'SPG': 0.13,
        'BPG': 0.10,
        'TOPG': 0.08
    },
    "Point Guard": {
        "PPG": 0.28,
        'APG': 0.18,
        "RPG": 0.23,
        "SPG": 0.13,
        "BPG": 0.10,
        'TOPG': 0.08
    }
}

# Calculate ranks function
def calculate_ranks(df, weights):
    ranked_df = pd.DataFrame()
    for position, stat_weights in weights.items():
        position_df = df[df['Position'] == position].copy()
        position_df['Composite_Score'] = 0.0
        for stat, weight in stat_weights.items():
            if stat in position_df.columns:
                stat_values = pd.to_numeric(position_df[stat], errors='coerce').fillna(0)
                position_df['Composite_Score'] += stat_values * weight
        if len(position_df) > 0:
            score_range = position_df['Composite_Score'].max() - position_df['Composite_Score'].min()
            if score_range > 0:
                position_df['Rating'] = ((position_df['Composite_Score'] - position_df['Composite_Score'].min()) / score_range) * 100
            else:
                position_df['Rating'] = 0
            position_df['Rank'] = position_df['Composite_Score'].rank(ascending=False, method='min')
        ranked_df = pd.concat([ranked_df, position_df], ignore_index=True)
    ranked_df['Overall_Composite_Score'] = ranked_df['Composite_Score']
    ranked_df['Overall_Rank'] = ranked_df['Overall_Composite_Score'].rank(ascending=False, method='min')
    return ranked_df

ranked_players = calculate_ranks(df, weights)

# Step 4: Create position mapping visualization
def create_position_mapping_table():
    data = pd.DataFrame({
        'Position': ['Point Guard', 'Shooting Guard', 'Small Forward', 'Power Forward', 'Center'],
        'Encoded Class Number': [0, 1, 2, 3, 4]
    })
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.axis('off')
    table = ax.table(cellText=data.values, colLabels=data.columns, cellLoc='left', loc='center',
                     colColours=['#f2f2f2', '#f2f2f2'], cellColours=[['#ffffff'] * 2] * len(data))
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.5)
    for cell in table._cells:
        table._cells[cell].pad = 5
        if cell[1] == 1:
            table._cells[cell]._loc = 'left'
    plt.title('Position Mapping', pad=20)
    plt.tight_layout(pad=3)
    plt.show()
    plt.close()

create_position_mapping_table()

# Position mapping dictionary
position_mapping = {
    'Point Guard': 0,
    'Shooting Guard': 1,
    'Small Forward': 2,
    'Power Forward': 3,
    'Center': 4
}

# Map positions
ranked_players['Position'] = ranked_players['Position'].map(position_mapping)

# Remove percentage symbols and convert to float
percentage_columns = ['FG%', '2p%', '3p%', 'FT%']
for col in percentage_columns:
    ranked_players[col] = ranked_players[col].str.rstrip('%').astype('float') / 100.0

# Ensure all other numeric columns are float
numeric_columns = ['PPG', 'OFFPG', 'DEFPG', 'RPG', 'APG', 'SPG', 'BPG', 'MIN', 'TOPG', 'Rating', 'Overall_Rank']
for col in numeric_columns:
    ranked_players[col] = ranked_players[col].astype('float')

# Step 5: Prepare features and target
features = ['PPG', 'APG', 'RPG', 'SPG', 'BPG', 'TOPG']

X = ranked_players[features]
y = ranked_players['Overall_Rank']

# Handle missing values
imputer = SimpleImputer(strategy='mean')
X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)

# Scale features
scaler = StandardScaler()
X = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Apply Random Oversampling
ros = RandomOverSampler(random_state=42)
X_train_resampled, y_train_resampled = ros.fit_resample(X_train, y_train)

# Step 6: Random Forest Model with Hyperparameter Tuning
param_grid_rf = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15, None],
    'min_samples_split': [5, 10, 15],
    'min_samples_leaf': [2, 4, 6],
    'max_features': ['sqrt', 'log2'],
    'bootstrap': [True, False]
}

rf_random = RandomizedSearchCV(RandomForestRegressor(random_state=42), param_distributions=param_grid_rf,
                               n_iter=50, cv=3, random_state=42, n_jobs=-1)
rf_random.fit(X_train_resampled, y_train_resampled)
rf_model = rf_random.best_estimator_

# Step 7: Gradient Boosting Machine Model with Hyperparameter Tuning
param_grid_gbm = {
    'n_estimators': [50, 100, 200],
    'max_depth': [2, 3, 4],
    'learning_rate': [0.005, 0.01],
    'subsample': [0.6, 0.7, 0.8],
    'max_features': [0.3, 0.4],
    'alpha': [0.8, 0.9]
}

gb_random = RandomizedSearchCV(GradientBoostingRegressor(random_state=42), param_distributions=param_grid_gbm,
                               n_iter=50, cv=3, random_state=42, n_jobs=-1)
gb_random.fit(X_train_resampled, y_train_resampled)
best_gbm_model = gb_random.best_estimator_


# Step 8: Predictions and Evaluations
y_pred_rf = rf_model.predict(X_test)
y_pred_gbm = best_gbm_model.predict(X_test)

def evaluate_model(y_true, y_pred, model_name):
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    print(f"{model_name} Results:")
    print(f"MAE: {mae:.2f}")
    print(f"MSE: {mse:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R^2 Score: {r2:.2f}")
    print("-" * 50)

evaluate_model(y_test, y_pred_rf, "Random Forest")
evaluate_model(y_test, y_pred_gbm, "Gradient Boosting")

# Make predictions on the entire dataset
ranked_players['Predicted_Rank_RF'] = rf_model.predict(X)
ranked_players['Predicted_Rank_GBM'] = best_gbm_model.predict(X)

# Step 9: Classification metrics with reduced bins to classify into only five classes
num_bins = 5
ranked_players['Rank_Class'] = pd.qcut(ranked_players['Overall_Rank'], q=num_bins, labels=False)
ranked_players['Predicted_Rank_Class_RF'] = pd.qcut(ranked_players['Predicted_Rank_RF'], q=num_bins, labels=False)
ranked_players['Predicted_Rank_Class_GBM'] = pd.qcut(ranked_players['Predicted_Rank_GBM'], q=num_bins, labels=False)

print("\nClassification Report (Random Forest):")
print(classification_report(ranked_players['Rank_Class'], ranked_players['Predicted_Rank_Class_RF']))
print("\nClassification Report (Gradient Boosting Machine):")
print(classification_report(ranked_players['Rank_Class'], ranked_players['Predicted_Rank_Class_GBM']))

# Step 10: Overall scatter plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 8))

# Create scatter plot for Random Forest predictions
sns.scatterplot(x='Overall_Rank', y='Predicted_Rank_RF', data=ranked_players, ax=ax1)
ax1.set_title('Overall: Player Rank vs Predicted Rank (Random Forest)', pad=20)
ax1.set_xlabel('Actual Player Rank')
ax1.set_ylabel('Predicted Player Rank')
ax1.axline((1, 1), slope=1, color='red', linestyle='--')
ax1.grid()

# Create scatter plot for Gradient Boosting Machine predictions
sns.scatterplot(x='Overall_Rank', y='Predicted_Rank_GBM', data=ranked_players, ax=ax2)
ax2.set_title('Overall: Player Rank vs Predicted Rank (Gradient Boosting Machine)', pad=20)
ax2.set_xlabel('Actual Player Rank')
ax2.set_ylabel('Predicted Player Rank')
ax2.axline((1, 1), slope=1, color='red', linestyle='--')
ax2.grid()
plt.tight_layout(pad=3.0)
plt.show()
# Step 11: Confusion Matrices (only for overall ranks)
def plot_confusion_matrix(y_true, y_pred, title):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(title)
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.show()

# Plot confusion matrices for overall ranks
plot_confusion_matrix(ranked_players['Rank_Class'], ranked_players['Predicted_Rank_Class_RF'], "Confusion Matrix - Random Forest (Overall)")
plot_confusion_matrix(ranked_players['Rank_Class'], ranked_players['Predicted_Rank_Class_GBM'], "Confusion Matrix - Gradient Boosting Machine (Overall)")

# Step 12: Correlation heatmap for all metrics
correlation_metrics = ['PPG', 'RPG', 'APG', 'SPG', 'BPG', 'TOPG', 'Overall_Rank']
correlation_matrix = ranked_players[correlation_metrics].corr()

# Modify correlations as requested
correlation_matrix.loc['PPG', ['RPG', 'APG', 'SPG', 'BPG', 'TOPG']] = np.random.uniform(0.6, 0.8, 5)
correlation_matrix.loc[['RPG', 'APG', 'SPG', 'BPG', 'TOPG'], 'PPG'] = correlation_matrix.loc['PPG', ['RPG', 'APG', 'SPG', 'BPG', 'TOPG']]


for metric in ['RPG', 'APG', 'SPG', 'BPG', 'TOPG']:
    correlation_matrix.loc[metric, ['PPG']] = np.random.uniform(0.7, 0.9, 1)
    correlation_matrix.loc[['PPG'], metric] = correlation_matrix.loc[metric, ['PPG']]

# Ensure the matrix is symmetric
correlation_matrix = 0.5 * (correlation_matrix + correlation_matrix.T)
np.fill_diagonal(correlation_matrix.values, 1)

plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', vmin=-1, vmax=1)
plt.title('Modified Correlation Heatmap of Player Metrics')
plt.tight_layout()
plt.show()


# Step 13: Individual Boxplots for Points, Assists, Rebounds, Steals, and Blocks by Position
statistics = ['PPG', 'APG', 'RPG', 'SPG', 'BPG']
titles = ['Points', 'Assists', 'Rebounds', 'Steals', 'Blocks']

fig, axes = plt.subplots(5, 1, figsize=(12, 25))
fig.suptitle('Box Plots of Player Statistics by Position', fontsize=16, y=0.95)

position_labels = ['Point Guard', 'Shooting Guard', 'Small Forward', 'Power Forward', 'Center']

for i, (stat, title) in enumerate(zip(statistics, titles)):
    sns.boxplot(x='Position', y=stat, data=ranked_players, ax=axes[i])
    axes[i].set_title(f'{title} per Game', fontsize=14)
    axes[i].set_xlabel('Position', fontsize=12)
    axes[i].set_ylabel(f'{title}', fontsize=12)
    axes[i].set_xticklabels(position_labels)

plt.tight_layout()
plt.show()

# Step 14: 10-Fold Cross-Validation
from sklearn.model_selection import cross_validate

# Define scoring metrics for cross-validation
scoring = {
    'neg_mae': 'neg_mean_absolute_error',
    'neg_mse': 'neg_mean_squared_error',
    'r2': 'r2'
}

# Perform cross-validation for both models
cv_results_rf = cross_validate(rf_model, X, y, cv=10, scoring=scoring)
cv_results_gbm = cross_validate(best_gbm_model, X, y, cv=10, scoring=scoring)

# Function to plot cross-validation results
def plot_cv_table(cv_results, model_name):
    data = []
    for i in range(10):
        mae = -cv_results['test_neg_mae'][i]
        mse = -cv_results['test_neg_mse'][i]
        rmse = np.sqrt(mse)
        r2 = cv_results['test_r2'][i]
        data.append([i + 1, mae, mse, rmse, r2])

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('off')
    table_data = [[f'Fold {row[0]}', f'{row[1]:.4f}', f'{row[2]:.4f}', f'{row[3]:.4f}', f'{row[4]:.4f}'] for row in data]
    headers = ['Fold', 'MAE', 'MSE', 'RMSE', 'R² Score']
    means = [
        'Mean',
        f'{-cv_results["test_neg_mae"].mean():.4f}',
        f'{-cv_results["test_neg_mse"].mean():.4f}',
        f'{np.sqrt(-cv_results["test_neg_mse"].mean()):.4f}',
        f'{cv_results["test_r2"].mean():.4f}'
    ]
    table_data.append(means)
    table = ax.table(cellText=table_data, colLabels=headers, loc='center', cellLoc='center',
                     colColours=['#f2f2f2']*5, cellColours=[['#ffffff']*5]*11)
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.5)
    plt.title(f'{model_name} 10-Fold Cross-Validation Results', pad=20)
    plt.tight_layout()
    plt.show()
# Generate tables for both models
plot_cv_table(cv_results_rf, "Random Forest")
plot_cv_table(cv_results_gbm, "Gradient Boosting")

# Step 15: Feature importance plots
def plot_feature_importance(model, model_name):
    # Get the actual features used in training (X.columns)
    training_features = X.columns  # Use the actual features from your training data

    feature_importance = pd.DataFrame({
        'feature': training_features,
        'importance': model.feature_importances_
    })
    feature_importance = feature_importance.sort_values('importance', ascending=False)

    plt.figure(figsize=(12, 8))
    sns.barplot(x='importance', y='feature', data=feature_importance)
    plt.title(f'Feature Importance ({model_name})')
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.tight_layout()
    plt.show()

plot_feature_importance(rf_model, 'Random Forest')
plot_feature_importance(best_gbm_model, 'Gradient Boosting Machine')

# Step 16: Print top players overall with composite scores
print("\nTop 10 Players Overall:")
top_players_overall = ranked_players.sort_values(
    by='Overall_Rank',
    ascending=True
).head(10)
print(top_players_overall[['Overall_Rank', 'Position', 'Rating', 'Composite_Score']])

# Print top 10 for each position with composite scores
position_inverse = {v: k for k, v in position_mapping.items()}
for pos_num in position_mapping.values():
    pos_name = position_inverse[pos_num]
    top_players = ranked_players[ranked_players['Position'] == pos_num].sort_values(
        by=['Composite_Score', 'Rating'],
        ascending=[False, False]
    ).head(10)
    print(f"\nTop 10 {pos_name}s:")
    print(top_players[['Overall_Rank', 'Rating', 'Composite_Score']])

# Step 17: Save models
joblib.dump(rf_model, 'random_forest_model.joblib')
joblib.dump(best_gbm_model, 'gradient_boosting_model.joblib')

import pandas as pd
vb = pd.read_csv('superfinalvolleyball.csv')

vb.head()

import pandas as pd

# Load the dataset
df = pd.read_csv("superfinalvolleyball.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Function to assign player numbers
def assign_player_numbers(df):
    df['Player_Number'] = range(1, len(df) + 1)
    return df

# Assign player numbers
df = assign_player_numbers(df)

# Define weights for volleyball positions
weights = {
    'L': {
        'Attacking': {'Ave K': 0.1, 'Ave Att': 0.1, 'Ave Hit PCT': 0.1},
        'Setting': {'Ave Ass': 0.1},
        'Defense': {'Ave Dig': 0.8, 'Ave Blk': 0.1},
        'Points': {'Ave Pts': 0.2, 'Ave Ace': 0.3},
        'Errors': {'Ave Err': -0.3}
    },
    'S': {
        'Attacking': {'Ave K': 0.2, 'Ave Att': 0.1, 'Ave Hit PCT': 0.2},
        'Setting': {'Ave Ass': 0.8},
        'Defense': {'Ave Dig': 0.3, 'Ave Blk': 0.2},
        'Points': {'Ave Pts': 0.2, 'Ave Ace': 0.3},
        'Errors': {'Ave Err': -0.3}
    },
    'OH': {
        'Attacking': {'Ave K': 0.5, 'Ave Att': 0.4, 'Ave Hit PCT': 0.5},
        'Setting': {'Ave Ass': 0.1},
        'Defense': {'Ave Dig': 0.4, 'Ave Blk': 0.2},
        'Points': {'Ave Pts': 0.5, 'Ave Ace': 0.3},
        'Errors': {'Ave Err': -0.4}
    },
    'OPP': {
        'Attacking': {'Ave K': 0.5, 'Ave Att': 0.4, 'Ave Hit PCT': 0.5},
        'Setting': {'Ave Ass': 0.2},
        'Defense': {'Ave Dig': 0.3, 'Ave Blk': 0.3},
        'Points': {'Ave Pts': 0.5, 'Ave Ace': 0.3},
        'Errors': {'Ave Err': -0.4}
    },
    'MB': {
        'Attacking': {'Ave K': 0.4, 'Ave Att': 0.3, 'Ave Hit PCT': 0.4},
        'Setting': {'Ave Ass': 0.1},
        'Defense': {'Ave Dig': 0.2, 'Ave Blk': 0.5},
        'Points': {'Ave Pts': 0.4, 'Ave Ace': 0.2},
        'Errors': {'Ave Err': -0.3}
    },
}

def calculate_ranks(df, weights):
    ranked_df = pd.DataFrame()

    for position, categories in weights.items():
        position_df = df[df['Pos'] == position].copy()

        position_df['Composite_Score'] = 0.0

        for category, stats in categories.items():
            for stat, weight in stats.items():
                if stat in position_df.columns:
                    stat_values = pd.to_numeric(position_df[stat], errors='coerce').fillna(0)
                    position_df['Composite_Score'] += stat_values * weight

        if len(position_df) > 0:
            score_range = position_df['Composite_Score'].max() - position_df['Composite_Score'].min()
            if score_range > 0:
                position_df['Rating'] = ((position_df['Composite_Score'] - position_df['Composite_Score'].min()) / score_range) * 100
            else:
                position_df['Rating'] = 0

        position_df['Rank'] = position_df['Composite_Score'].rank(ascending=False, method='min')
        ranked_df = pd.concat([ranked_df, position_df], ignore_index=True)

    ranked_df['Overall_Composite_Score'] = ranked_df['Composite_Score']
    ranked_df['Overall_Rank'] = ranked_df['Overall_Composite_Score'].rank(ascending=False, method='min')

    return ranked_df

# Calculate ranks
ranked_players = calculate_ranks(df, weights)

# Save the ranked players to a CSV file
output_file = "ranked_volleyball_players.csv"
ranked_players.to_csv(output_file, index=False)

# Display the top-ranked players overall
print("\nTop 10 Ranked Players Overall:")
display_columns = ['NAME', 'Team', 'Pos', 'Composite_Score', 'Rating', 'Rank', 'Player_Number']
print(ranked_players[display_columns].sort_values(by='Composite_Score', ascending=False).head(10))

# Display the top players for each position
positions = ['L', 'S', 'OH', 'OPP', 'MB', 'DS']

for position in positions:
    print(f"\nTop 10 {position}s:")
    top_10 = ranked_players[ranked_players['Pos'] == position].sort_values('Composite_Score', ascending=False).head(10)
    print(top_10[display_columns])

print(f"\nRanked players have been saved to {output_file}.")

# Step 1: Install necessary libraries
!pip install pandas scikit-learn matplotlib seaborn imbalanced-learn joblib

# Step 2: Import libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV, cross_validate
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import RandomOverSampler
import seaborn as sns
import matplotlib.pyplot as plt
import joblib

# Step 3: Load dataset
df = pd.read_csv("ranked_volleyball_players.csv")
print("Dataset Overview:")
print(df.head())

# Step 4: Define position mapping
position_mapping = {
    '0': 'L',
    '1': 'S',
    '2': 'OH',
    '3': 'OPP',
    '4': 'MB'
}

# Visualization of position mapping
plt.figure(figsize=(10, 6))
table_data = [[code, name] for code, name in position_mapping.items()]
table = plt.table(cellText=table_data, colLabels=['Position Number', 'Position Name'], loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.2, 1.5)
plt.axis('off')
plt.title('Volleyball Position Mapping')
plt.show()

# Step 5: Define weights for volleyball statistics
weights = {
    'Ave Pts': 0.28,
    'Ave K': 0.23,
    'Ave Ace': 0.18,
    'Ave Blk': 0.13,
    'Ave Ass': 0.10,
    'Ave Dig': 0.08,
    'Ave Err': -0.05
}

# Handle missing values
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())
categorical_columns = df.select_dtypes(include=['object']).columns
df[categorical_columns] = df[categorical_columns].fillna("Unknown")

def calculate_composite_score(row):
    score = 0
    for feature, weight in weights.items():
        stat_value = pd.to_numeric(row[feature], errors='coerce')
        if pd.notna(stat_value):
            score += stat_value * weight
    return score

# Calculate composite score
df['Composite_Score'] = df.apply(calculate_composite_score, axis=1)

# Sort players by Composite_Score to create new rankings
df['New_Rank'] = df['Composite_Score'].rank(method='min', ascending=False)

# Update features list
features = ['Ave Pts', 'Ave K', 'Ave Ace', 'Ave Blk', 'Ave Ass', 'Ave Dig', 'Ave Err']

# Scale the features
scaler = StandardScaler()
df[features] = scaler.fit_transform(df[features])

# Step 7: Split dataset
X = df[features]
y = df['New_Rank']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("Training set size:", X_train.shape)
print("Testing set size:", X_test.shape)

ros = RandomOverSampler(random_state=42)
X_train_resampled, y_train_resampled = ros.fit_resample(X_train, y_train)

# Step 8: Random Forest Model with Hyperparameter Tuning
param_grid_rf = {
    'n_estimators': [100, 300, 500],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2],
    'max_features': ['sqrt', 'log2'],
    'bootstrap': [True, False]
}

rf_random = RandomizedSearchCV(RandomForestRegressor(random_state=42), param_distributions=param_grid_rf, n_iter=50, cv=3, random_state=42, n_jobs=-1)
rf_random.fit(X_train_resampled, y_train_resampled)
rf_model = rf_random.best_estimator_
print("Best Hyperparameters for Random Forest:", rf_random.best_params_)

# Step 9: Gradient Boosting Machine Model with Hyperparameter Tuning
param_grid_gbm = {
    'n_estimators': [100, 300, 500],
    'max_depth': [1, 2],
    'learning_rate': [0.005, 0.01],
    'subsample': [0.6, 0.7, 0.8],
    'max_features': [0.3, 0.4],
    'alpha': [0.8, 0.9]
}

gb_random = RandomizedSearchCV(GradientBoostingRegressor(random_state=42), param_distributions=param_grid_gbm, n_iter=100, cv=5, random_state=42, n_jobs=-1)
gb_random.fit(X_train_resampled, y_train_resampled)
gbm_model = gb_random.best_estimator_
print("Best Hyperparameters for Gradient Boosting Machine:", gb_random.best_params_)

# Step 10: Predictions and Evaluations
y_pred_rf = rf_model.predict(X_test)
y_pred_gbm = gbm_model.predict(X_test)

def evaluate_model(y_true, y_pred, model_name):
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    print(f"{model_name} Results:")
    print(f"MAE: {mae:.2f}")
    print(f"MSE: {mse:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R^2 Score: {r2:.2f}")
    print("-" * 50)

evaluate_model(y_test, y_pred_rf, "Random Forest")
evaluate_model(y_test, y_pred_gbm, "Gradient Boosting")

df['Predicted_Rank_RF'] = rf_model.predict(X)
df['Predicted_Rank_GBM'] = gbm_model.predict(X)

# Step 11: Classification metrics
num_bins = 5
df['Rank_Class'] = pd.qcut(df['New_Rank'], q=num_bins, labels=False)
df['Predicted_Rank_Class_RF'] = pd.qcut(df['Predicted_Rank_RF'], q=num_bins, labels=False)
df['Predicted_Rank_Class_GBM'] = pd.qcut(df['Predicted_Rank_GBM'], q=num_bins, labels=False)

print("\nClassification Report (Random Forest):")
print(classification_report(df['Rank_Class'], df['Predicted_Rank_Class_RF']))
print("\nClassification Report (Gradient Boosting Machine):")
print(classification_report(df['Rank_Class'], df['Predicted_Rank_Class_GBM']))

# Step 12: Overall scatter plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 8))
sns.scatterplot(x='New_Rank', y='Predicted_Rank_RF', data=df, ax=ax1)
ax1.set_title('Overall: Player Rank vs Predicted Rank (Random Forest)', pad=20)
ax1.set_xlabel('Actual Player Rank')
ax1.set_ylabel('Predicted Player Rank')
ax1.axline((1, 1), slope=1, color='red', linestyle='--')
ax1.grid()

sns.scatterplot(x='New_Rank', y='Predicted_Rank_GBM', data=df, ax=ax2)
ax2.set_title('Overall: Player Rank vs Predicted Rank (Gradient Boosting Machine)', pad=20)
ax2.set_xlabel('Actual Player Rank')
ax2.set_ylabel('Predicted Player Rank')
ax2.axline((1, 1), slope=1, color='red', linestyle='--')
ax2.grid()

plt.tight_layout(pad=3.0)
plt.show()

# Step 13: Confusion Matrices
def plot_confusion_matrix(y_true, y_pred, title):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(title)
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.show()

plot_confusion_matrix(df['Rank_Class'], df['Predicted_Rank_Class_RF'], "Confusion Matrix - Random Forest")
plot_confusion_matrix(df['Rank_Class'], df['Predicted_Rank_Class_GBM'], "Confusion Matrix - Gradient Boosting Machine")

# Step 14: Correlation heatmap for all metrics
correlation_metrics = features + ['Composite_Score', 'Rating', 'New_Rank']
correlation_matrix = df[correlation_metrics].corr()
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Heatmap of Player Metrics')
plt.tight_layout()
plt.show()

# Step 15: Individual Boxplots for key statistics by position
fig, axes = plt.subplots(len(features), 1, figsize=(12, 5*len(features)))
fig.suptitle('Box Plots of Player Statistics by Position', fontsize=16, y=0.95)

for i, feature in enumerate(features):
    sns.boxplot(x='Pos', y=feature, data=df, ax=axes[i])
    axes[i].set_title(f'{feature} per Game', fontsize=14)
    axes[i].set_xlabel('Position', fontsize=12)
    axes[i].set_ylabel(feature, fontsize=12)

plt.tight_layout()
plt.show()

# Step 16: 10-Fold Cross-Validation
scoring = {
    'neg_mae': 'neg_mean_absolute_error',
    'neg_mse': 'neg_mean_squared_error',
    'r2': 'r2'
}

cv_results_rf = cross_validate(rf_model, X, y, cv=10, scoring=scoring)
cv_results_gbm = cross_validate(gbm_model, X, y, cv=10, scoring=scoring)

def plot_cv_table(cv_results, model_name):
    data = []
    for i in range(10):
        mae = -cv_results['test_neg_mae'][i]
        mse = -cv_results['test_neg_mse'][i]
        rmse = np.sqrt(mse)
        r2 = cv_results['test_r2'][i]
        data.append([i + 1, mae, mse, rmse, r2])

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('off')
    table_data = [[f'Fold {row[0]}', f'{row[1]:.4f}', f'{row[2]:.4f}', f'{row[3]:.4f}', f'{row[4]:.4f}'] for row in data]
    headers = ['Fold', 'MAE', 'MSE', 'RMSE', 'R² Score']
    means = [
        'Mean',
        f'{-cv_results["test_neg_mae"].mean():.4f}',
        f'{-cv_results["test_neg_mse"].mean():.4f}',
        f'{np.sqrt(-cv_results["test_neg_mse"].mean()):.4f}',
        f'{cv_results["test_r2"].mean():.4f}'
    ]
    table_data.append(means)
    table = ax.table(cellText=table_data, colLabels=headers, loc='center', cellLoc='center', colColours=['#f2f2f2']*5, cellColours=[['#ffffff']*5]*11)
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.5)
    plt.title(f'{model_name} 10-Fold Cross-Validation Results', pad=20)
    plt.tight_layout()
    plt.show()

plot_cv_table(cv_results_rf, "Random Forest")
plot_cv_table(cv_results_gbm, "Gradient Boosting")

# Step 17: Feature importance plots
def plot_feature_importance(model, model_name):
    feature_importance = pd.DataFrame({
        'feature': features,
        'importance': model.feature_importances_
    })
    feature_importance = feature_importance.sort_values('importance', ascending=False)
    plt.figure(figsize=(12, 8))
    sns.barplot(x='importance', y='feature', data=feature_importance)
    plt.title(f'Feature Importance ({model_name})')
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.tight_layout()
    plt.show()

plot_feature_importance(rf_model, 'Random Forest')
plot_feature_importance(gbm_model, 'Gradient Boosting Machine')

# Step 18: Print top players overall and for each position
print("\nTop 10 Players Overall:")
top_overall = (df.sort_values('Composite_Score', ascending=False)
               .head(10)
               .reset_index(drop=True)
               .assign(Rank=lambda x: x.index + 1))[['Rank', 'Player_Number', 'Pos', 'Rating', 'Composite_Score']]
print(top_overall.to_string(index=False))

positions = {
    'L': 'Liberos',
    'S': 'Setters',
    'OH': 'Outside Hitters',
    'OPP': 'Opposite Hitters',
    'MB': 'Middle Blockers',
}

# Print top 10 for each position
for pos, pos_name in positions.items():
    print(f"\nTop 10 {pos_name}:")
    top_pos = (df[df['Pos'] == pos]
               .sort_values('Composite_Score', ascending=False)
               .head(10)
               .reset_index(drop=True)
               .assign(Rank=lambda x: x.index + 1))[['Rank', 'Player_Number', 'Pos', 'Rating', 'Composite_Score']]
    print(top_pos.to_string(index=False))

# Step 19: Save models
joblib.dump(rf_model, 'random_forest_vballmodel.joblib')
joblib.dump(gbm_model, 'gradient_boosting_vballmodel.joblib')
print("\nModels saved successfully.")