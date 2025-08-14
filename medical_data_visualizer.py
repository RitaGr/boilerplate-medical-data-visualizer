import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv('/workspace/boilerplate-medical-data-visualizer/medical_examination.csv')

# 2
bmi = df['weight'] / pow(df['height'] / 100,2)
df['overweight'] = np.select([(bmi > 25), (bmi <= 25)],[1,0])
# 3
df['cholesterol'] = np.select([(df['cholesterol'] == 1), (df['cholesterol'] > 1)], [0,1])
df['gluc'] = np.select([(df['gluc'] == 1), (df['gluc'] > 1)], [0,1])
# 4
def draw_cat_plot():
    # 5
    df_cat = pd.melt(df, id_vars='cardio' , value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])
    # 6
    df_cat['total'] = 1
    df_cat = df_cat.groupby(['cardio', 'variable', 'value'], as_index = False).count()
    # 7
    # 8
    fig = sns.catplot(data=df_cat, x='variable', y='total', hue='value', kind='bar', col='cardio').fig
    # 9
    fig.savefig('catplot.png')
    return fig

# 10
def draw_heat_map():
    # 11
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) &
                (df['height'] >= df['height'].quantile(0.025)) &
                (df['height'] <= df['height'].quantile(0.975)) &
                (df['weight'] >= df['weight'].quantile(0.025)) &
                (df['weight'] <= df['weight'].quantile(0.975)) ]
    # 12
    corr = df_heat.corr(method="pearson")

    # 13
    mask = np.triu(corr)

    # 14
    fig, ax = plt.subplots(figsize=(12,12))

    # 15
    sns.heatmap(corr, linewidths = 1, center=0, vmin= -0.08, vmax= 0.32, annot= True, square = True, mask=mask, fmt= ".1f", cbar_kws= {"shrink": 0.4, "ticks": np.arange(-0.08, 0.24 + 0.001, 0.08)})

    # 16
    fig.savefig('heatmap.png')
    return fig
