import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Create DataFrame
df = pd.DataFrame({
    # 'algorithm': ['max_idle', 'max_score', 'greedy_control_5_5', 'greedy_control_5_10', 'greedy_control_5_50', 'greedy_control_10_5', 'greedy_control_10_10', 'greedy_control_10_50'],
    'algorithm': ['max_score', 'aor_pairing_Loyalty', 'aor_pairing_Sales', 'greedy_control_5_5', 'greedy_control_5_10',
                  'greedy_control_5_50', 'greedy_control_10_5', 'greedy_control_10_10', 'greedy_control_10_50'],
    # 'fairness': [0.751, 0.726582452, 0.727119993, 0.748974619, 0.729480249, 0.755689585, 0.750521862, 0.757418856],
    'fairness': [0.726582452, 0.7522, 0.7371, 0.727119993, 0.748974619, 0.729480249, 0.755689585, 0.750521862,
                 0.757418856],
    # 'business_value': [1.01, 1.323, 1.346, 1.367, 1.356, 1.339, 1.343, 1.346]
    'business_value': [1.323, 1.205, 1.234, 1.346, 1.367, 1.356, 1.339, 1.343, 1.320]
})

# Separate 'greedy' and 'greedy_control' data
# max_idle_df = df[df['algorithm'] == 'max_idle']
max_score_df = df[df['algorithm'] == 'max_score']
aor_pairing_Loyalty_df = df[df['algorithm'] == 'aor_pairing_Loyalty']
aor_pairing_Sales_df = df[df['algorithm'] == 'aor_pairing_Sales']
greedy_control_df = df[df['algorithm'].str.contains('greedy_control')]

# Sort 'greedy_control' by 'max_min_fairness' to ensure the lineplot is correct
greedy_control_df = greedy_control_df.sort_values('fairness')

# Customizeable sizes
title_font_size = 20
label_font_size = 16
scatter_size = 50
text_size = 10

plt.figure(figsize=(10, 6))

# Plot points
# sns.scatterplot(data=max_idle_df, x='fairness', y='business_value', color='green', label='max_idle', s=scatter_size)
sns.scatterplot(data=max_score_df, x='fairness', y='business_value', color='red', label='max_score', s=scatter_size)
sns.scatterplot(data=aor_pairing_Loyalty_df, x='fairness', y='business_value', color='purple', label='aor_pairing_Loyalty',
                s=scatter_size)
sns.scatterplot(data=aor_pairing_Sales_df, x='fairness', y='business_value', color='green', label='aor_pairing_Sales',
                s=scatter_size)
sns.scatterplot(data=greedy_control_df, x='fairness', y='business_value', color='blue', label='greedy_control',
                s=scatter_size)

# Draw lineplot for 'greedy_control' points
sns.lineplot(data=greedy_control_df, x='fairness', y='business_value', color='blue')

# Add text
for i in range(greedy_control_df.shape[0]):
    plt.text(x=greedy_control_df.fairness.iloc[i],
             y=greedy_control_df.business_value.iloc[i],
             s=f'({greedy_control_df.algorithm.iloc[i].split("_")[2]}, {greedy_control_df.algorithm.iloc[i].split("_")[3]})',
             size=text_size)

plt.text(x=max_score_df.fairness.iloc[0],
         y=max_score_df.business_value.iloc[0],
         s='max_score',
         size=text_size)

plt.text(x=aor_pairing_Loyalty_df.fairness.iloc[0],
         y=aor_pairing_Loyalty_df.business_value.iloc[0],
         s='aor_pairing_Loyalty',
         size=text_size)

plt.text(x=aor_pairing_Sales_df.fairness.iloc[0],
         y=aor_pairing_Sales_df.business_value.iloc[0],
         s='aor_pairing_Sales',
         size=text_size)

# Add vertical and horizontal dotted lines at the 'max_score' point
plt.axvline(x=max_score_df.fairness.iloc[0], color='r', linestyle='--')
plt.axhline(y=max_score_df.business_value.iloc[0], color='r', linestyle='--')

plt.title("Value-Fairness Trade-off Curve", fontsize=title_font_size)
plt.xlabel("Fairness", fontsize=label_font_size)
plt.ylabel("Business Value", fontsize=label_font_size)
plt.ylim(bottom=1.00, top=1.5)  # Set y-axis start from 1.00
# plt.xlim(right=1.00)
plt.legend(fontsize=label_font_size)
plt.show()
