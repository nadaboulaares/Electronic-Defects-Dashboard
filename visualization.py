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

def load_data(file_path):
    # Read the content of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    defect_data = []
    for line in lines:
        if "%" in line:
            parts = line.strip().split()
            defect_type = " ".join(parts[:-1])
            defect_count = int(parts[-1])
            defect_data.append({'DefectType': legend.get(defect_type, defect_type), 'DefectCount': defect_count})

    return pd.DataFrame(defect_data)

def main():
    # Streamlit app title
    st.title('Electronic Defects Dashboard')

    # Specify the folder containing the data files
    main_folder_path = 'data'  # Update with your actual main folder path

    # Dropdown to select a specific file
    selected_file = st.sidebar.selectbox('Select Data File', os.listdir(main_folder_path))

    # Check if the selected item is a file
    if os.path.isfile(os.path.join(main_folder_path, selected_file)):
        # Extract date from the filename
        date_str = selected_file.split('.')[0]
        date = pd.to_datetime(date_str, format='%d%m%y', errors='coerce')

        # Load data from the selected file
        file_path = os.path.join(main_folder_path, selected_file)
        data = load_data(file_path)

        # Create a heatmap for defects across different components for the selected date
        st.subheader(f'Heatmap - Defects Across Different Components for {date.strftime("%Y-%m-%d")}')
        pivot_data = data.pivot_table(index='DefectType', columns='DefectCount', aggfunc='size', fill_value=0)
        
        # Create the heatmap
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(pivot_data, annot=True, cmap='viridis', fmt='d', cbar_kws={'label': 'Defect Count'}, ax=ax)
        
        # Pass the figure explicitly to st.pyplot
        st.pyplot(fig)

    else:
        st.info(f"Selected item '{selected_file}' is not a file. Please choose a file.")

if __name__ == '__main__':
    main()
