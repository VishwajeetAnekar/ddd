import pandas as pd
import re
from datetime import datetime


def column_count_validation(df1, df2):
    col_count_df1 = df1.shape[1]
    col_count_df2 = df2.shape[1]

    if col_count_df1 != col_count_df2:
        error_message = f"Number of columns are not equal. ({col_count_df1}) and ({col_count_df2})"
        status = "Fail"
    else:
        success_message = "Both files have the same number of columns"
        status = "Pass"
        error_message = None

    result_df = pd.DataFrame({"Feature": 'Column Count Validation',
                              "Columns in CSV 1": [col_count_df1],
                              "Columns in CSV 2": [col_count_df2],
                              "Status": [status],
                              "Result": [error_message if status == 'Fail' else success_message]})

    return result_df, error_message if status == 'Fail' else success_message


def row_count_validation(df1, df2):
    row_count_df1 = df1.shape[0]
    row_count_df2 = df2.shape[0]

    if row_count_df1 != row_count_df2:
        error_message = f"Number of rows are not equal. ({row_count_df1}) and ({row_count_df2})"
        status = "Fail"
    else:
        success_message = "Both files have the same number of rows"
        status = "Pass"
        error_message = None

    result_df = pd.DataFrame({"Feature": 'Row Count Validation',
                              "Rows in CSV 1": [row_count_df1],
                              "Rows in CSV 2": [row_count_df2],
                              "Status": [status],
                              "Result": [error_message if status == 'Fail' else success_message]})

    return result_df, error_message if status == 'Fail' else success_message


def column_name_match(df1, df2):
    result_data = []

    for col1 in df1.columns:
        if col1 in df2.columns:
            status = "Pass"
            result_message = "Column names match"
        else:
            status = "Fail"
            result_message = "Column names do not match"

        result_data.append({
            "Column in CSV 1": col1,
            "Column in CSV 2": col1 if status == "Pass" else None,
            "Status": status,
            "Result": result_message
        })

    for col2 in df2.columns:
        if col2 not in df1.columns:
            result_data.append({
                "Column in CSV 1": None,
                "Column in CSV 2": col2,
                "Status": "Fail",
                "Result": "Column names do not match"
            })

    result_df = pd.DataFrame(result_data, columns=[
                             "Column in CSV 1", "Column in CSV 2", "Status", "Result"])

    if result_df['Status'].eq('Pass').all():
        return "Success: Column names match", result_df
    else:
        return "Error: Column names do not match", result_df


def unique_value_validation(df1, df2):
    unique_ids_df1 = df1['PHARMACY_TRANSACTION_ID'].value_counts()
    repeated_ids_df1 = unique_ids_df1[unique_ids_df1 > 1].index.tolist()

    result_rows = []

    for transaction_id in df1['PHARMACY_TRANSACTION_ID'].unique():
        if transaction_id in repeated_ids_df1:
            result_rows.append({
                'PHARMACY_TRANSACTION_ID': transaction_id,
                'Status': 'Fail',
                'Details': 'Common Value found'
            })
        else:
            result_rows.append({
                'PHARMACY_TRANSACTION_ID': transaction_id,
                'Status': 'Pass',
                'Details': 'Unique value'
            })

    result_df = pd.DataFrame(result_rows, columns=['PHARMACY_TRANSACTION_ID', 'Status', 'Details'])

    if any(row['Status'] == 'Fail' for row in result_rows):
        return result_df, "Error: Repeated values found in File 1"
    else:
        return result_df, "Success: No repeated values found in File 1"


def required_fields_validation(config_df, csv_df):
    required_columns = config_df[config_df['Requirement'].isin(['Y', 'C'])]['Field Name'].tolist()
    validation_results = []

    for field_name in required_columns:
        is_required = config_df.loc[config_df['Field Name'] == field_name, 'Requirement'].iloc[0] == 'Y'
        
        if field_name in csv_df.columns:
            for idx, value in csv_df[field_name].items():
                txn_id = csv_df.at[idx, 'PHARMACY_TRANSACTION_ID']

                if pd.isna(value):
                    validation_results.append({
                        'PHARMACY_TRANSACTION_ID': txn_id,
                        'Column Name': field_name,
                        'Required Field (Y/N)': 'Y' if is_required else 'C',
                        'Value': 'Missing',
                        'Status': 'Fail',
                        'Details': f"{field_name} is a required field and is missing value."
                    })
                elif not is_required and value == 'C':
                    validation_results.append({
                        'PHARMACY_TRANSACTION_ID': txn_id,
                        'Column Name': field_name,
                        'Required Field (Y/N)': 'C',
                        'Value': value,
                        'Status': 'Fail',
                        'Details': f"{field_name} is a conditional field and has an invalid value: {value}."
                    })
        else:
            validation_results.append({
                'PHARMACY_TRANSACTION_ID': '',
                'Column Name': field_name,
                'Required Field (Y/N)': 'Y' if is_required else 'C',
                'Value': 'NA',
                'Status': 'Fail',
                'Details': f"{field_name} is a required field but does not exist in the CSV file."
            })

    result_df = pd.DataFrame(validation_results, columns=[
                            'PHARMACY_TRANSACTION_ID', 'Column Name', 'Required Field (Y/N)', 'Value', 'Status', 'Details'])

    if not result_df.empty:
        return result_df, "Some required fields are missing or have invalid values"
    else:
        return pd.DataFrame(columns=['PHARMACY_TRANSACTION_ID', 'Column Name', 'Required Field (Y/N)', 'Value', 'Status', 'Details']), "All transactions passed"


def white_space_validation(config_df, csv_df):
    result_data = []

    for col in csv_df.columns:
        for idx, value in csv_df[col].items():
            if pd.isna(value):
                continue
            if isinstance(value, str) and re.search(r'^\s|\s$|\s{2,}', value):
                result_data.append({
                    "PHARMACY_TRANSACTION_ID": csv_df.loc[idx, 'PHARMACY_TRANSACTION_ID'],
                    "Column Name": col,
                    "Value": value,
                    "Status": "Fail",
                    "Details": "Whitespace found"
                })

    result_df = pd.DataFrame(result_data)

    if not result_df.empty and "Fail" in result_df["Status"].values:
        return result_df, "Some values have unnecessary white space"
    else:
        return pd.DataFrame(columns=['PHARMACY_TRANSACTION_ID', 'Column Name', 'Value', 'Status', 'Details']), "All transactions passed"


def duplicate_keys_validation(df):
    column_names = df.columns.tolist()
    duplicates = {}
    result_data = []

    for col in column_names:
        base_col = col.split('.')[0].lower()
        if base_col in duplicates:
            duplicates[base_col].append(col)
        else:
            duplicates[base_col] = [col]

    for col in column_names:
        base_col = col.split('.')[0].lower()
        if len(duplicates[base_col]) > 1:
            result_data.append({
                "Column Name": col,
                "Status": "Fail",
                "Details": f"Duplicate Column found in {', '.join(duplicates[base_col])}"
            })
        else:
            result_data.append({
                "Column Name": col,
                "Status": "Pass",
                "Details": "Unique Column"
            })

    result_df = pd.DataFrame(result_data)

    if result_df['Status'].eq('Pass').all():
        validation_result = "Success: No duplicate columns found"
    else:
        validation_result = result_df[result_df['Status'] == 'Fail'].to_string(
            index=False)

    return result_df, validation_result


def maximum_length_validation(config_file, csv_file):
    config_dict = {row['Field Name']: row['Data Type'] for _, row in config_file.iterrows()}
    result_data = []

    for col_name, dtype in config_dict.items():
        if col_name not in csv_file.columns:
            result_data.append(
                ("", col_name, "", dtype, "", "Fail", f"Column '{col_name}' not found in the CSV file"))
            continue

        col_values = csv_file[col_name].astype(str)
        
        if re.match(r'DATE\(\d+\)', dtype):
            length = int(re.search(r'\((\d+)\)', dtype).group(1))
            for idx, value in col_values.items():
                txn_id = csv_file.at[idx, 'PHARMACY_TRANSACTION_ID']

                if pd.isna(value) or value.lower() == 'nan' or not value.strip():
                    continue

                value = value.replace('.0', '')

                if length == 8:
                    if len(value) != length or not re.match(r'^\d+$', value):
                        result_data.append(
                            (txn_id, col_name, "", dtype, value, "Fail", "Invalid date format"))
                        continue

                    try:
                        datetime.strptime(value, '%Y%m%d')
                    except ValueError:
                        result_data.append(
                            (txn_id, col_name, "", dtype, value, "Fail", "Invalid date format"))
                        continue

                elif length == 14:
                    try:
                        datetime.strptime(value, '%Y%m%d %H:%M:%S')
                    except ValueError:
                        result_data.append(
                            (txn_id, col_name, "", dtype, value, "Fail", "Invalid date format"))
                        continue

        elif re.match(r'DATETIME\(\d+\)', dtype):
            length = int(re.search(r'DATETIME\((\d+)\)', dtype).group(1))
            for idx, value in col_values.items():
                txn_id = csv_file.at[idx, 'PHARMACY_TRANSACTION_ID']
                value_str = str(value).strip().replace('.0', '')

                if not value_str:
                    continue

                if len(value_str) != length:
                    result_data.append(
                        (txn_id, col_name, "", dtype, value_str, "Fail", "Invalid datetime format"))
                    continue

        elif dtype.startswith('DOUBLE'):
            for idx, value in col_values.items():
                txn_id = csv_file.at[idx, 'PHARMACY_TRANSACTION_ID']

                if pd.isna(value) or value.lower() == 'nan' or not value.strip():
                    continue

                if not re.match(r'^-?\d+(\.\d+)?$', value):
                    result_data.append(
                        (txn_id, col_name, "", dtype, value, "Fail", "Invalid double format"))
                    continue

        elif dtype.startswith('VARCHAR'):
            length = int(re.search(r'\((\d+)\)', dtype).group(1))
            for idx, value in col_values.items():
                txn_id = csv_file.at[idx, 'PHARMACY_TRANSACTION_ID']

                if pd.isna(value) or value.lower() == 'nan':
                    continue

                if not value.strip():
                    continue

                if len(value) > length:
                    result_data.append(
                        (txn_id, col_name, "", dtype, value, "Fail", "Exceeded length limit"))
                    continue

        elif dtype.startswith('TIMESTAMP'):
            for idx, value in col_values.items():
                txn_id = csv_file.at[idx, 'PHARMACY_TRANSACTION_ID']

                if pd.isna(value) or value.lower() == 'nan':
                    continue

                try:
                    datetime.strptime(value, '%Y%m%d %H:%M:%S')
                except ValueError:
                    result_data.append(
                        (txn_id, col_name, "", dtype, value, "Fail", "Invalid timestamp format"))
                    continue

    validation_result_df = pd.DataFrame(result_data, columns=[
                                        "PHARMACY_TRANSACTION_ID", "Column Name", "Requirement", "Data Type", "Value", "Status", "Details"])

    if validation_result_df['Status'].eq('Fail').any():
        return "Some test cases failed. Please check the output for more details", validation_result_df
    else:
        return "All test cases passed successfully", validation_result_df


