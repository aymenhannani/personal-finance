import pandas as pd

# Define the file path (example file path, you can replace with the actual one)
file_path = r'C:\Users\Aymen\Documents\Projects\personalFinance\data.xlsm'

# Read the Excel file with headers starting at row 5 (index 4) and extracting columns from C to G
df = pd.read_excel(file_path, header=4, usecols="C:G")

