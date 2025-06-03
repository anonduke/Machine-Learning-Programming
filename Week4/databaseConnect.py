import pandas as pd
import psycopg2
import seaborn as sns
import matplotlib.pyplot as plt

class DatabaseConnector:
    def __init__(self, conn_str):
        self.conn_str = conn_str
        self.conn = None

    def connect(self):
        self.conn = psycopg2.connect(self.conn_str)

    def fetch_employees(self):
        if self.conn is None:
            self.connect()
        df = pd.read_sql_query("SELECT * FROM employees;", self.conn)
        return df

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

def process_salary_data(df):
    # Extract start year from start_date
    df['start_year'] = pd.to_datetime(df['start_date']).dt.year
    
    # Group by position and start_year, calculate average salary
    grouped_data = df.groupby(['position', 'start_year'])['salary'].mean().reset_index()
    
    # Find highest and lowest average salaries
    max_salary = grouped_data['salary'].max()
    min_salary = grouped_data['salary'].min()
    max_group = grouped_data.loc[grouped_data['salary'].idxmax()]
    min_group = grouped_data.loc[grouped_data['salary'].idxmin()]
    
    return grouped_data, max_group, min_group

def create_grouped_bar_chart(grouped_data, max_group, min_group):
    # Set seaborn style for better aesthetics
    sns.set_style("whitegrid")
    
    # Create grouped bar chart
    plt.figure(figsize=(12, 6))
    bar_plot = sns.barplot(
        data=grouped_data,
        x='position',
        y='salary',
        hue='start_year',
        palette='deep'  # Distinct colors for each year
    )
    
    # Customize the chart
    plt.title('Average Salary by IT Position and Start Year', fontsize=14, pad=15)
    plt.xlabel('IT Position', fontsize=12)
    plt.ylabel('Average Salary (USD)', fontsize=12)
    plt.legend(title='Start Year', loc='upper right')
    
    # Rotate x-axis labels if there are many positions
    plt.xticks(rotation=45, ha='right')
    
    # Find bar positions for annotations
    bars = bar_plot.patches
    bar_positions = [(bar.get_x() + bar.get_width() / 2, bar.get_height()) for bar in bars]
    bar_labels = [(row['position'], row['start_year']) for _, row in grouped_data.iterrows()]
    
    # Annotate highest average
    max_pos_year = (max_group['position'], max_group['start_year'])
    for i, (pos, year) in enumerate(bar_labels):
        if pos == max_group['position'] and year == max_group['start_year']:
            x, y = bar_positions[i]
            plt.text(
                x, y + 5000,  # Slightly above the bar
                f'Highest: ${max_group["salary"]:.2f}\n{max_group["position"]}, {max_group["start_year"]}',
                ha='center', va='bottom', fontsize=10, color='red',
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='red')
            )
    
    # Annotate lowest average
    min_pos_year = (min_group['position'], min_group['start_year'])
    for i, (pos, year) in enumerate(bar_labels):
        if pos == min_group['position'] and year == min_group['start_year']:
            x, y = bar_positions[i]
            plt.text(
                x, y + 5000,  # Slightly above the bar
                f'Lowest: ${min_group["salary"]:.2f}\n{min_group["position"]}, {min_group["start_year"]}',
                ha='center', va='bottom', fontsize=10, color='blue',
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='blue')
            )
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Show the plot
    plt.show()

if __name__ == "__main__":
    conn_str = "postgresql://neondb_owner:npg_UqaINtrs5Q7z@ep-damp-cherry-a8rxh7tr-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"
    db = DatabaseConnector(conn_str)
    db.connect()
    df = db.fetch_employees()
    grouped_data, max_group, min_group = process_salary_data(df)
    print("Grouped Data:\n", grouped_data)
    print("\nHighest Average:", max_group['position'], max_group['start_year'], max_group['salary'])
    print("Lowest Average:", min_group['position'], min_group['start_year'], min_group['salary'])
    create_grouped_bar_chart(grouped_data, max_group, min_group)
    db.close()