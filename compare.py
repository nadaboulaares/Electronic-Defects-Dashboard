import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

def load_data(main_folder_path, selected_date):
    # List all files for the selected date
    files_for_date = [file for file in os.listdir(main_folder_path) if selected_date in file]

    # Create a DataFrame to store data for the selected date
    date_data = pd.DataFrame()

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
        date_data = pd.concat([date_data, defect_data_df])

    return date_data

def main():
    # Streamlit app title
    st.title('Electronic Defects Dashboard')

    # Specify the folder containing the data files
    main_folder_path = 'data'  # Update with your actual main folder path

    # Multiselect to choose multiple dates
    selected_dates = st.sidebar.multiselect('Select Dates', os.listdir(main_folder_path))

    # Check if at least one date is selected
    if selected_dates:
        # Create a DataFrame to store data for all selected dates
        all_data = pd.DataFrame()

        # Load data for each selected date and concatenate into a single DataFrame
        for selected_date in selected_dates:
            data = load_data(main_folder_path, selected_date)
            all_data = pd.concat([all_data, data])

        # Show total defects for each component type across all selected dates
        st.subheader('Total Defects by Component Type (Across Selected Dates)')
        total_defects_all_dates = all_data.groupby(['ComponentDate', 'DefectType'])['DefectCount'].sum().unstack().fillna(0)
        st.bar_chart(total_defects_all_dates)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        # Show distribution of defects across different components for all selected dates
        st.subheader('Distribution of Defects (Across Selected Dates)')
        plt.figure(figsize=(12, 8))
        sns.barplot(x='DefectType', y='DefectCount', hue='ComponentDate', data=all_data, palette='viridis')
        plt.xticks(rotation=45, ha="right")
        st.pyplot()

    else:
        st.warning("Please select at least one date.")

if __name__ == '__main__':
    main()
