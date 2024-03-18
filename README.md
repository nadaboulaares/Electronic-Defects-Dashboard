# Electronic-Defects-Dashboard
Electronic Defects Dashboard
This Streamlit application provides a dashboard for visualizing and analyzing electronic defects data across different components and dates. It allows users to explore the distribution of defects, total defects by component type, defect trends over time, percentage of defects between different dates, and occurrence of components across selected dates.

Requirements
Python 3.x
Streamlit
Pandas
Seaborn
Matplotlib
Installation
Clone or download this repository to your local machine.

Install the required packages using pip:

bash
Copy code
pip install -r requirements.txt
Usage
Ensure you have your data files organized in a folder named 'data' within the same directory as the script.

Run the Streamlit application:

bash
Copy code
streamlit run dash_c.py
Once the application starts, you'll see the dashboard interface.

Select one or more dates from the sidebar to load data for analysis.

Explore the various visualizations provided in the dashboard, including heatmap, bar charts, and line charts.

Customize the analysis by selecting specific components or dates for deeper insights.

Functionality
Heatmap - Defects Distribution Across Components and Dates
This visualization shows the distribution of defects across different components and dates using a heatmap.

Total Defects by Component Type (Across Selected Dates)
This bar chart displays the total number of defects for each component type across the selected dates.

Defect Trend Over Time (Select Components)
Users can select specific components to visualize their defect trend over time using a line chart.

Percentage of Defects - Carte 1 vs. Carte 2
This visualization compares the percentage of defects for each component between two different dates (Carte 1 and Carte 2) using a grouped bar chart.

Occurrence of Components Across Selected Dates
This bar chart illustrates the occurrence of each component across all selected dates, providing insights into component reliability and frequency of defects.

Customization
Update the legend dictionary (legend) to decode component codes according to your dataset.
Adjust the main folder path (main_folder_path) to point to the directory containing your data files.
Contributors
Nada Boulares
License
This project is licensed under the MIT License.

