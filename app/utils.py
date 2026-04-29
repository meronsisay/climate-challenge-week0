import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("Set2")

# Country list
COUNTRIES = ['Ethiopia', 'Kenya', 'Nigeria', 'Sudan', 'Tanzania']
DATA_PATH = '../data/'


def load_all_data(data_path=DATA_PATH):
    """Load all cleaned CSV files from data directory"""
    data_frames = []
    
    for country in COUNTRIES:
        country_lower = country.lower()
        try:
            df = pd.read_csv(f'{data_path}{country_lower}_clean.csv')
            df['Country'] = country
            df['Date'] = pd.to_datetime(df['Date'])
            data_frames.append(df)
        except FileNotFoundError:
            print(f"Warning: {country_lower}_clean.csv not found")
    
    if data_frames:
        combined = pd.concat(data_frames, ignore_index=True)
        combined['Year'] = combined['Date'].dt.year
        combined['Month'] = combined['Date'].dt.month
        return combined
    return pd.DataFrame()


def filter_data(df, countries, year_range):
    """Filter dataframe by selected countries and year range"""
    if df.empty:
        return df
    filtered = df[df['Country'].isin(countries)]
    filtered = filtered[(filtered['Year'] >= year_range[0]) & 
                        (filtered['Year'] <= year_range[1])]
    return filtered


def get_summary_statistics(df):
    """Calculate summary statistics for temperature and precipitation"""
    if df.empty:
        return pd.DataFrame(), pd.DataFrame()
    
    temp_stats = df.groupby('Country')['T2M'].agg([
        ('Mean (°C)', 'mean'),
        ('Median (°C)', 'median'),
        ('Std Dev (°C)', 'std'),
        ('Min (°C)', 'min'),
        ('Max (°C)', 'max')
    ]).round(2)
    
    precip_stats = df.groupby('Country')['PRECTOTCORR'].agg([
        ('Mean (mm/day)', 'mean'),
        ('Median (mm/day)', 'median'),
        ('Std Dev (mm/day)', 'std'),
        ('Min (mm/day)', 'min'),
        ('Max (mm/day)', 'max')
    ]).round(2)
    
    return temp_stats, precip_stats


def plot_temperature_trend(df):
    """Create temperature trend line chart"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for country in df['Country'].unique():
        country_data = df[df['Country'] == country]
        monthly_avg = country_data.groupby('Date')['T2M'].mean().reset_index()
        ax.plot(monthly_avg['Date'], monthly_avg['T2M'], label=country, linewidth=2)
    
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Temperature (°C)', fontsize=12)
    ax.set_title('Monthly Temperature Trends by Country', fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig


def plot_precipitation_boxplot(df):
    """Create precipitation boxplot"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Prepare data for boxplot
    countries_list = sorted(df['Country'].unique())
    data_to_plot = []
    labels = []
    
    for country in countries_list:
        country_data = df[df['Country'] == country]['PRECTOTCORR'].dropna()
        if len(country_data) > 0:
            data_to_plot.append(country_data)
            labels.append(country)
    
    if data_to_plot:
        bp = ax.boxplot(data_to_plot, labels=labels, patch_artist=True)
        
        # Color the boxes
        colors = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854']
        for patch, color in zip(bp['boxes'], colors[:len(data_to_plot)]):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
    
    ax.set_xlabel('Country', fontsize=12)
    ax.set_ylabel('Precipitation (mm/day)', fontsize=12)
    ax.set_title('Precipitation Distribution by Country', fontsize=14, fontweight='bold')
    ax.set_yscale('log')
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


def plot_extreme_heat(df):
    """Create extreme heat bar chart"""
    heat_data = df[df['T2M_MAX'] > 35].groupby(['Country', 'Year']).size().reset_index(name='Extreme_Heat_Days')
    
    fig, ax = plt.subplots(figsize=(12, 5))
    
    if not heat_data.empty:
        # Pivot for grouped bar chart
        pivot_heat = heat_data.pivot(index='Year', columns='Country', values='Extreme_Heat_Days').fillna(0)
        pivot_heat.plot(kind='bar', ax=ax, width=0.8)
    else:
        ax.text(0.5, 0.5, 'No extreme heat days recorded', 
                transform=ax.transAxes, ha='center', va='center')
    
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Days (T2M_MAX > 35°C)', fontsize=12)
    ax.set_title('Extreme Heat Days per Year', fontsize=14, fontweight='bold')
    ax.legend(title='Country', bbox_to_anchor=(1, 1))
    ax.grid(True, alpha=0.3, axis='y')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


def plot_drought(df):
    """Create drought bar chart for consecutive dry days"""
    def max_consecutive_dry_days(group):
        group = group.sort_values('Date')
        is_dry = (group['PRECTOTCORR'] < 1).astype(int)
        max_streak = 0
        current = 0
        for dry in is_dry:
            if dry == 1:
                current += 1
                max_streak = max(max_streak, current)
            else:
                current = 0
        return max_streak
    
    # Calculate per country per year
    dry_data = []
    for country in df['Country'].unique():
        country_data = df[df['Country'] == country]
        for year in sorted(df['Year'].unique()):
            year_data = country_data[country_data['Year'] == year]
            max_dry = max_consecutive_dry_days(year_data) if len(year_data) > 0 else 0
            dry_data.append({'Country': country, 'Year': year, 'Max_Dry_Days': max_dry})
    
    dry_df = pd.DataFrame(dry_data)
    
    fig, ax = plt.subplots(figsize=(12, 5))
    
    # Pivot for grouped bar chart
    pivot_dry = dry_df.pivot(index='Year', columns='Country', values='Max_Dry_Days')
    pivot_dry.plot(kind='bar', ax=ax, width=0.8)
    
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Maximum Consecutive Dry Days', fontsize=12)
    ax.set_title('Drought Duration per Year (Precipitation < 1mm)', fontsize=14, fontweight='bold')
    ax.legend(title='Country', bbox_to_anchor=(1, 1))
    ax.grid(True, alpha=0.3, axis='y')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


def plot_correlation_heatmap(df):
    """Create correlation heatmap"""
    numeric_cols = ['T2M', 'T2M_MAX', 'T2M_MIN', 'T2M_RANGE', 
                    'PRECTOTCORR', 'RH2M', 'WS2M', 'WS2M_MAX', 'PS', 'QV2M']
    
    # Filter to only columns that exist in df
    available_cols = [col for col in numeric_cols if col in df.columns]
    corr_matrix = df[available_cols].corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create heatmap
    im = ax.imshow(corr_matrix, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')
    
    # Add colorbar
    plt.colorbar(im, ax=ax, label='Correlation')
    
    # Set labels
    ax.set_xticks(range(len(available_cols)))
    ax.set_yticks(range(len(available_cols)))
    ax.set_xticklabels(available_cols, rotation=45, ha='right', fontsize=9)
    ax.set_yticklabels(available_cols, fontsize=9)
    ax.set_title('Correlation Matrix of Climate Variables', fontsize=14, fontweight='bold')
    
    # Add correlation values
    for i in range(len(available_cols)):
        for j in range(len(available_cols)):
            text_color = "white" if abs(corr_matrix.iloc[i, j]) > 0.5 else "black"
            ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                   ha="center", va="center", color=text_color, fontsize=8)
    
    plt.tight_layout()
    return fig