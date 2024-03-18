import os
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Legend for decoding component codes
legend = {
    'c': 'Condensateur',
    'r': 'Résistance',
    'sw': 'Switch Bouton',
    'V-AVON/voltage check': 'Voltage',
    'Pt': 'Point Circuit',
    'Z': 'Circuit Intégré',
    'Sp': 'Switch Pro',
    'T': 'Transformateur',
    'E': 'Jumper',
    'Q': 'Transistor',
    'L': 'Bobine',
    'Cr/ds': 'Diode',
    'P': 'Switch',
    '1%': 'Carte 1',
    '2%': 'Carte 2'
}

def clean_component_name(component):
    # Remove numbers from the component name
    return ''.join([i for i in component if not i.isdigit()])

def load_data(main_folder_path, selected_dates):
    # Create a DataFrame to store data for the selected dates
    all_data = pd.DataFrame()

    # Load data for each selected date and concatenate into a single DataFrame
    for selected_date in selected_dates:
        # List all files for the selected date
        files_for_date = [file for file in os.listdir(main_folder_path) if selected_date in file]

        # Load data for each file and concatenate into a single DataFrame
        for file_name in files_for_date:
            file_path = os.path.join(main_folder_path, file_name)
            with open(file_path, 'r') as file:
                lines = file.readlines()

            defect_data = []
            for line in lines:
                if "%" in line:
                    parts = line.strip().split()
                    defect_type = " ".join(parts[:-1])
                    defect_count = int(parts[-1])
                    defect_data.append({'DefectType': legend.get(defect_type, defect_type), 'DefectCount': defect_count})

            # Add a new column to store the file name (component date)
            defect_data_df = pd.DataFrame(defect_data)
            defect_data_df['ComponentDate'] = file_name.split('.')[0]
            all_data = pd.concat([all_data, defect_data_df])

    # Clean up the component names
    all_data['DefectType'] = all_data['DefectType'].apply(clean_component_name)

    return all_data

def main():
    # Streamlit app title
    st.title('Electronic Defects Dashboard')

    # Specify the folder containing the data files
    main_folder_path = 'data'  # Update with your actual main folder path

    # Multiselect to choose multiple dates
    selected_dates = st.sidebar.multiselect('Select Dates', os.listdir(main_folder_path))
    st.set_option('deprecation.showPyplotGlobalUse', False)


    # Check if at least one date is selected
    if selected_dates:
        # Load data for all selected dates
        all_data = load_data(main_folder_path, selected_dates)

        # Check if the dataset is not empty before creating the plots
        if not all_data.empty:
            # Create a pivot table for the fheatmap
            heatmap_data = all_data.pivot_table(index='DefectType', columns='ComponentDate', values='DefectCount', fill_value=0)

            # Show heatmap
            st.subheader('Heatmap - Defects Distribution Across Components and Dates')
            sns.set(font_scale=0.8)  # Adjust font size for better readability
            plt.figure(figsize=(14, 8))
            sns.heatmap(heatmap_data.astype(float), annot=True, fmt='.0f', cmap='viridis', cbar_kws={'label': 'Defect Count'})
            plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
            st.pyplot()

            # Bar chart showing total defects for each component type
            st.subheader('Total Defects by Component Type (Across Selected Dates)')
            total_defects = all_data.groupby('DefectType')['DefectCount'].sum()
            st.bar_chart(total_defects)

            # Line chart showing trend of defects for specific components over time
            st.subheader('Defect Trend Over Time (Select Components)')
            selected_components = st.multiselect('Select Components', all_data['DefectType'].unique())
            if selected_components:
                defect_trend_data = all_data[all_data['DefectType'].isin(selected_components)]
                plt.figure(figsize=(12, 6))
                sns.lineplot(x='ComponentDate', y='DefectCount', hue='DefectType', data=defect_trend_data, marker='o')
                plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
                st.pyplot()
            else:
                st.info('Select at least one component to view its trend.')

            # Bar chart showing the percentage of defects for each component between Carte 1 and Carte 2
            st.subheader('Percentage of Defects - Carte 1 vs. Carte 2')
            percentage_defects = all_data.groupby(['DefectType', 'ComponentDate']).agg(
                {'DefectCount': 'sum'}).groupby('DefectType').apply(
                lambda x: x / x.sum() * 100).reset_index(level=0)
               
            sns.barplot(x='DefectType', y='DefectCount', hue='ComponentDate', data=percentage_defects)
            plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
            st.pyplot()

            # Bar chart showing the occurrence of each component across all selected dates
            st.subheader('Occurrence of Components Across Selected Dates')
            component_occurrence = all_data.groupby(['DefectType', 'ComponentDate']).size().unstack(fill_value=0)
            sns.barplot(x=component_occurrence.columns, y=component_occurrence.sum(), palette='viridis')
            plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
            st.pyplot()

        else:
            st.warning("Selected dates have no data.")

    else:
        st.warning("Please select at least one date.")

if __name__ == '__main__':
    main()

