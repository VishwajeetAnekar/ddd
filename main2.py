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


# def unique_value_validation(df1, df2):
#     unique_ids_df1 = df1["PHARMACY_TRANSACTION_ID"].value_counts()
#     repeated_ids_df1 = unique_ids_df1[unique_ids_df1 > 1].index.tolist()

#     unique_ids_df2 = df2["PHARMACY_TRANSACTION_ID"].value_counts()
#     repeated_ids_df2 = unique_ids_df2[unique_ids_df2 > 1].index.tolist()

#     result_rows = []
#     for transaction_id in df1["PHARMACY_TRANSACTION_ID"]:
#         if transaction_id in repeated_ids_df1:
#             result_rows.append({'Column Name': 'PHARMACY_TRANSACTION_ID',
#                                 'Status': 'Fail',
#                                 'Repeated Value': transaction_id,
#                                 'Details': f'Common Value found in File 1'})
#         else:
#             result_rows.append({'Column Name': 'PHARMACY_TRANSACTION_ID',
#                                 'Status': 'Pass',
#                                 'Repeated Value': transaction_id,
#                                 'Details': f'ID is unique to File 1'})

#     for transaction_id in df2["PHARMACY_TRANSACTION_ID"]:
#         if transaction_id in repeated_ids_df2:
#             result_rows.append({'Column Name': 'PHARMACY_TRANSACTION_ID',
#                                 'Status': 'Fail',
#                                 'Repeated Value': transaction_id,
#                                 'Details': f'Common Value found in File 2'})
#         else:
#             result_rows.append({'Column Name': 'PHARMACY_TRANSACTION_ID',
#                                 'Status': 'Pass',
#                                 'Repeated Value': transaction_id,
#                                 'Details': f'ID is unique to File 2'})

#     result_df = pd.DataFrame(result_rows)

#     if any(row['Status'] == 'Fail' for row in result_rows):
#         return result_df, "Error: Repeated values found in one or both files"
#     else:
#         return result_df, "Success: No repeated values found in either file"

def unique_value_validation(df1, df2):
    composite_key_df1 = df1['PHARMACY_TRANSACTION_ID'].astype(
        str) + df1['STATUS_DATE'].astype(str)
    unique_ids_df1 = composite_key_df1.value_counts()
    repeated_ids_df1 = unique_ids_df1[unique_ids_df1 > 1].index.tolist()

    composite_key_df2 = df2['PHARMACY_TRANSACTION_ID'].astype(
        str) + df2['STATUS_DATE'].astype(str)
    unique_ids_df2 = composite_key_df2.value_counts()
    repeated_ids_df2 = unique_ids_df2[unique_ids_df2 > 1].index.tolist()

    result_rows = []
    for transaction_id, patient_id in zip(df1['PHARMACY_TRANSACTION_ID'], df1['STATUS_DATE']):
        composite_key = str(transaction_id) + str(patient_id)
        if composite_key in repeated_ids_df1:
            result_rows.append({'Column Name': 'PHARMACY_TRANSACTION_ID_PHARMACY_PATIENT_ID',
                                'Status': 'Fail',
                                'Repeated Value': composite_key,
                                'Details': 'Common Value found in File 1'})
        else:
            result_rows.append({'Column Name': 'PHARMACY_TRANSACTION_ID_PHARMACY_PATIENT_ID',
                                'Status': 'Pass',
                                'Repeated Value': composite_key,
                                'Details': 'ID is unique to File 1'})

    # for transaction_id, patient_id in zip(df2['PHARMACY_TRANSACTION_ID'], df2['PHARMACY_PATIENT_ID']):
    #     composite_key = str(transaction_id) + str(patient_id)
    #     if composite_key in repeated_ids_df2:
    #         result_rows.append({'Column Name': 'PHARMACY_TRANSACTION_ID_PHARMACY_PATIENT_ID',
    #                             'Status': 'Fail',
    #                             'Repeated Value': composite_key,
    #                             'Details': 'Common Value found in File 2'})
    #     else:
    #         result_rows.append({'Column Name': 'PHARMACY_TRANSACTION_ID_PHARMACY_PATIENT_ID',
    #                             'Status': 'Pass',
    #                             'Repeated Value': composite_key,
    #                             'Details': 'ID is unique to File 2'})

    result_df = pd.DataFrame(result_rows)

    if any(row['Status'] == 'Fail' for row in result_rows):
        return result_df, "Error: Repeated values found in one or both files"
    else:
        return result_df, "Success: No repeated values found in either file"


# def required_fields_validation(config_df, data_df):
#     required_columns = config_df[config_df['Requirement']
#                                  == 'Y']['Field Name'].tolist()
#     result_df = []
#     data_df['PHARMACY_TRANSACTION_ID'] = data_df['PHARMACY_TRANSACTION_ID'].astype(str)
#     data_df['PHARMACY_PATIENT_ID'] = data_df['PHARMACY_PATIENT_ID'].astype(str)

#     data_df['Primary Key'] = data_df['PHARMACY_TRANSACTION_ID'] + '_' + data_df['PHARMACY_PATIENT_ID']

#     for txn_id in data_df['Primary Key'].unique():
#         txn_df = data_df[data_df['Primary Key'] == txn_id]
#         for col in required_columns:
#             if col not in txn_df.columns:
#                 result_df.append({
#                     "PHARMACY_TRANSACTION_ID": txn_id.split('_')[0],
#                     "PHARMACY_PATIENT_ID": txn_id.split('_')[1],
#                     "Column Name": col,
#                     "Column Name": col,
#                     "Required Field (Y/N)": "Y",
#                     "Value": " ",
#                     "Status": "Fail",
#                     "Comments": "Column is missing"
#                 })
#             else:
#                 if txn_df[col].isnull().values.any():
#                     result_df.append({
#                         "PHARMACY_TRANSACTION_ID": txn_id.split('_')[0],
#                         "PHARMACY_PATIENT_ID": txn_id.split('_')[1],
#                         "Column Name": col,
#                         "Required Field (Y/N)": "Y",
#                         "Value": txn_df[col].iloc[0],
#                         "Status": "Fail",
#                         "Comments": f"Field has empty values"
#                     })

#     result_df = pd.DataFrame(result_df)

#     if not result_df.empty and "Fail" in result_df["Status"].values:
#         return result_df, "Some required fields are missing"
#     else:
#         return pd.DataFrame(columns=['PHARMACY_TRANSACTION_ID','PHARMACY_PATIENT_ID', 'Column Name', 'Required Field (Y/N)', 'Value', 'Status', 'Comments']), "All transactions passed"

def required_fields_validation(config_df, csv_df):
    validation_results = []
    for index, row in config_df.iterrows():
        field_name = row['Field Name']
        is_required = row['Requirement'] == 'Y'
        if field_name in csv_df.columns:
            if is_required:
                for idx, value in csv_df[field_name].items():
                    if pd.isna(value):
                        validation_results.append({
                            'PHARMACY_TRANSACTION_ID': csv_df.loc[idx, 'PHARMACY_TRANSACTION_ID'],
                            'Column Name': field_name,
                            'Required Field (Y/N)': 'Y',
                            'Value': 'Missing',
                            'Status': 'Fail',
                            'Details': f"{field_name} is a required field and is missing value."
                        })
                    else:
                        validation_results.append({
                            'PHARMACY_TRANSACTION_ID': csv_df.loc[idx, 'PHARMACY_TRANSACTION_ID'],
                            'Column Name': field_name,
                            'Required Field (Y/N)': 'Y',
                            'Value': value,
                            'Status': 'Pass',
                            'Details': f"{field_name} is a required field and has a value."
                        })
        else:
            validation_results.append({
                'PHARMACY_TRANSACTION_ID': '',
                'Column Name': field_name,
                'Required Field (Y/N)': 'Y',
                'Value': 'NA',
                'Status': 'Fail',
                'Details': f"{field_name} is a required field but does not exist in the CSV file."
            })
    result_df = pd.DataFrame(validation_results)
    result_df = result_df[['PHARMACY_TRANSACTION_ID', 'Column Name',
                           'Required Field (Y/N)', 'Value', 'Status', 'Details']]
    result_df = pd.DataFrame(result_df)

    if not result_df.empty and "Fail" in result_df["Status"].values:
        return result_df, "Some required fields are missing"
    else:
        return pd.DataFrame(columns=['PHARMACY_TRANSACTION_ID', 'Column Name', 'Required Field (Y/N)', 'Value', 'Status', 'Details']), "All transactions passed"


# def expected_values_validation(config_df, data_df):
#     result_rows = []
#     for txn_id in data_df['PHARMACY_TRANSACTION_ID'].unique():
#         txn_df = data_df[data_df['PHARMACY_TRANSACTION_ID'] == txn_id]
#         for _, config_row in config_df.iterrows():
#             col = config_row['Field Name']

#             expected_values_str = str(
#                 config_row['Expected Value/s (comma separated)']).strip('""')

#             if expected_values_str.lower() in ['nan', '']:
#                 continue

#             expected_values = [val.strip() for val in expected_values_str.split(
#                 ',') if val.strip() != '']
#             if col not in txn_df.columns:
#                 result_rows.append({
#                     "PHARMACY_TRANSACTION_ID": txn_id,
#                     "Column Name": col,
#                     "Expected Values": expected_values_str,
#                     "Value": "",
#                     "Status": "Fail",
#                     "Comments": "Column not found in the CSV file"
#                 })
#                 continue

#             for _, row in txn_df.iterrows():
#                 col_value = row[col] if col in row.index else None
#                 if pd.isnull(col_value) or col_value == "":
#                     continue

#                 elif col_value is not None and str(col_value) not in expected_values:
#                     result_rows.append({
#                         "PHARMACY_TRANSACTION_ID": txn_id,
#                         "Column Name": col,
#                         "Expected Values": expected_values_str,
#                         "Value": col_value,
#                         "Status": "Fail",
#                         "Comments": "Value does not match expected values"
#                     })
#     result_df = pd.DataFrame(result_rows)

#     if not result_df.empty and "Fail" in result_df["Status"].values:
#         return result_df, "Some values in expected columns are invalid"
#     else:
#         return pd.DataFrame(columns=['PHARMACY_TRANSACTION_ID', 'Column Name', 'Expected Values', 'Value', 'Status', 'Comments']), "All transactions passed"


def expected_values_validation(config_df, data_df):
    result_rows = []

    for txn_id in data_df['PHARMACY_TRANSACTION_ID'].unique():
        txn_df = data_df[data_df['PHARMACY_TRANSACTION_ID'] == txn_id]

        for _, config_row in config_df.iterrows():
            col_name = config_row['Field Name']
            requirement = config_row['Requirement']
            expected_values_str = str(
                config_row['Expected Value/s (comma separated)']).strip('""')

            if requirement in ['Y', 'C']:
                if col_name not in txn_df.columns:
                    result_rows.append({
                        "PHARMACY_TRANSACTION_ID": txn_id,
                        "Column Name": col_name,
                        "Requirement": requirement,
                        "Expected Values": expected_values_str,
                        "Value": "",
                        "Status": "Fail",
                        "Comments": "Column not found in the CSV file"
                    })
                    continue

                col_values = txn_df[col_name]

                if expected_values_str.lower() in ['nan', '', None]:
                    continue

                expected_values = [val.strip() for val in expected_values_str.split(
                    ',') if val.strip() != '']

                for _, col_value in col_values.items():
                    if pd.isnull(col_value) or col_value == "":
                        result_rows.append({
                            "PHARMACY_TRANSACTION_ID": txn_id,
                            "Column Name": col_name,
                            "Requirement": requirement,
                            "Expected Values": expected_values_str,
                            "Value": "",
                            "Status": "Fail",
                            "Comments": "No value provided in CSV for required column"
                        })
                        continue

                    elif str(col_value) not in expected_values:
                        result_rows.append({
                            "PHARMACY_TRANSACTION_ID": txn_id,
                            "Column Name": col_name,
                            "Requirement": requirement,
                            "Expected Values": expected_values_str,
                            "Value": col_value,
                            "Status": "Fail",
                            "Comments": "Value does not match expected values"
                        })

    result_df = pd.DataFrame(result_rows, columns=[
                             'PHARMACY_TRANSACTION_ID', 'Column Name', 'Requirement', 'Expected Values', 'Value', 'Status', 'Comments'])

    if not result_df.empty and "Fail" in result_df["Status"].values:
        return result_df, "Some values in expected columns are invalid"
    else:
        return pd.DataFrame(columns=['PHARMACY_TRANSACTION_ID', 'Column Name', 'Requirement', 'Expected Values', 'Value', 'Status', 'Comments']), "All transactions passed"


# def white_space_validation(df):
#     result_data = []
#     for txn_id in df['PHARMACY_TRANSACTION_ID'].unique():
#         txn_df = df[df['PHARMACY_TRANSACTION_ID'] == txn_id]
#         for col in df.columns:
#             for _, value in txn_df[col].items():
#                 if isinstance(value, str) and re.search(r'^\s|\s$|\s{2,}', value):
#                     result_data.append({
#                         "PHARMACY_TRANSACTION_ID": txn_id,
#                         "Column Name": col,
#                         "Value": value,
#                         "Status": "Fail",
#                         "Details": "Whitespace found"
#                     })
#     result_df = pd.DataFrame(result_data)
#     if not result_df.empty and "Fail" in result_df["Status"].values:
#         return result_df, "Some values has unnecessary white space"
#     else:
#         return pd.DataFrame(columns=['PHARMACY_TRANSACTION_ID', 'Column Name', 'Value', 'Status', 'Details']), "All transactions passed"

# def white_space_validation( config_df,csv_df):
#     result_data = []

#     required_columns = config_df[config_df['Requirement'].isin(['Y', 'C'])]['Field Name']

#     for col in required_columns:
#         for idx, value in csv_df[col].items():
#             if isinstance(value, str) and re.search(r'^\s|\s$|\s{2,}', value):
#                 result_data.append({
#                     "PHARMACY_TRANSACTION_ID": csv_df.loc[idx, 'PHARMACY_TRANSACTION_ID'],
#                     "Column Name": col,
#                     "Value": value,
#                     "Status": "Fail",
#                     "Details": "Whitespace found"
#                 })
#     result_df = pd.DataFrame(result_data)

#     if not result_df.empty and "Fail" in result_df["Status"].values:
#         return result_df, "Some values have unnecessary white space"
#     else:
#         return pd.DataFrame(columns=['PHARMACY_TRANSACTION_ID', 'Column Name', 'Value', 'Status', 'Details']), "All transactions passed"

def white_space_validation(config_df, csv_df):
    result_data = []
    required_columns = config_df[config_df['Requirement'].isin(
        ['Y', 'C'])]['Field Name']

    for col in required_columns:
        if col in csv_df.columns:
            for idx, value in csv_df[col].items():
                if isinstance(value, str) and re.search(r'^\s|\s$|\s{2,}', value):
                    result_data.append({
                        "PHARMACY_TRANSACTION_ID": csv_df.loc[idx, 'PHARMACY_TRANSACTION_ID'],
                        "Column Name": col,
                        "Value": value,
                        "Status": "Fail",
                        "Details": "Whitespace found"
                    })
        else:
            result_data.append({
                "PHARMACY_TRANSACTION_ID": '',
                "Column Name": col,
                "Value": 'NA',
                "Status": "Fail",
                "Details": f"{col} is a required field but does not exist in the CSV file."
            })

    result_df = pd.DataFrame(result_data)

    if not result_df.empty and "Fail" in result_df["Status"].values:
        return result_df, "Some values have unnecessary white space"
    else:
        return pd.DataFrame(columns=['PHARMACY_TRANSACTION_ID', 'Column Name', 'Value', 'Status', 'Details']), "All transactions passed"


def duplicate_keys_validation(df):
    column_names = df.columns.tolist()
    status_list = ["Pass"] * len(column_names)
    details_list = ["Unique Column"] * len(column_names)
    duplicates_checked = set()

    for i, col_name in enumerate(column_names):
        if f"{col_name}.1" in column_names[i + 1:]:
            if col_name not in duplicates_checked:
                status_list[i] = "Fail"
                details_list[i] = "Duplicate Columns found"
                duplicates_checked.add(col_name)
        elif '.1' in col_name:
            column_names[i] = None

    result_df = pd.DataFrame({
        "Column Name": column_names,
        "Status": status_list,
        "Details": details_list
    })
    result_df = result_df.dropna(subset=["Column Name"])

    if result_df['Status'].eq('Pass').all():
        validation_result = "Success: No duplicate columns found"
    else:
        validation_result = result_df.to_string(index=False)

    return result_df, validation_result


def maximum_length_validation(config_file, csv_file):
    required_columns = config_file[config_file['Requirement'].isin(['Y', 'C'])]

    result_data = []

    for _, row in required_columns.iterrows():
        col_name = row['Field Name']
        dtype = row['Data Type']
        requirement = row['Requirement']

        if col_name not in csv_file.columns:
            error_message = f"Column '{col_name}' not found in the CSV file"
            result_data.append(
                ("", col_name, requirement, dtype, "", "Fail", error_message))
            continue

        col_values = csv_file[col_name].astype(str)

        for idx, value in col_values.items():
            txn_id = csv_file.at[idx, 'PHARMACY_TRANSACTION_ID']

            if pd.isna(value) or value.lower() == 'nan':
                value = ""

            if not value.strip():
                error_message = f"Empty value in column"
                result_data.append(
                    (txn_id, col_name, requirement, dtype, value, "Fail", error_message))
                continue

            if re.match(r'DATE\(\d+\)', dtype):
                length = int(re.search(r'\((\d+)\)', dtype).group(1))
                value = value.replace('.0', '')

                if length == 8:
                    if len(value) != length or not re.match(r'^\d+$', value):
                        error_message = f"Invalid date format"
                        result_data.append(
                            (txn_id, col_name, requirement, dtype, value, "Fail", error_message))
                        continue

                    try:
                        datetime.strptime(value, '%Y%m%d')
                    except ValueError:
                        error_message = f"Invalid date format"
                        result_data.append(
                            (txn_id, col_name, requirement, dtype, value, "Fail", error_message))
                        continue

                elif length == 14:
                    try:
                        datetime.strptime(value, '%Y%m%d %H:%M:%S')
                    except ValueError:
                        error_message = f"Invalid date format"
                        result_data.append(
                            (txn_id, col_name, requirement, dtype, value, "Fail", error_message))
                        continue

            elif re.match(r'DATETIME\(\d+\)', dtype):
                length = int(re.search(r'DATETIME\((\d+)\)', dtype).group(1))
                value_str = str(value).strip().replace('.0', '')

                if len(value_str) != length:
                    error_message = f"Invalid datetime format"
                    result_data.append(
                        (txn_id, col_name, requirement, dtype, value_str, "Fail", error_message))
                    continue

            elif dtype.startswith('DOUBLE'):
                if not value.replace('.0', '').replace('.', '').isnumeric():
                    error_message = f"Invalid double format"
                    result_data.append(
                        (txn_id, col_name, requirement, dtype, value, "Fail", error_message))
                    continue

            elif dtype.startswith('VARCHAR'):
                length = int(re.search(r'\((\d+)\)', dtype).group(1))

                if len(value) > length:
                    error_message = f"Exceeded length limit"
                    result_data.append(
                        (txn_id, col_name, requirement, dtype, value, "Fail", error_message))
                    continue

            elif dtype.startswith('INTEGER'):
                if not value.replace('.0', '').isnumeric() and value.strip() != '':
                    error_message = f"Invalid number format"
                    result_data.append(
                        (txn_id, col_name, requirement, dtype, value, "Fail", error_message))
                    continue

            elif dtype.startswith('TIMESTAMP'):
                try:
                    datetime.strptime(value, '%Y%m%d %H:%M:%S')
                except ValueError:
                    error_message = f"Invalid timestamp format"
                    result_data.append(
                        (txn_id, col_name, requirement, dtype, value, "Fail", error_message))
                    continue

    validation_result_df = pd.DataFrame(result_data, columns=[
                                        "PHARMACY_TRANSACTION_ID", "Column Name", "Requirement", "Data Type", "Value", "Status", "Details"])

    if validation_result_df['Status'].eq('Fail').any():
        return "Some test cases failed. Please check the output for more details", validation_result_df
    else:
        return "All test cases passed successfully", validation_result_df

# def maximum_length_validation(config_file, csv_file):
#     col_dtype_map = dict(
#         zip(config_file['Field Name'].str.lower(), config_file['Data Type']))

#     result_data = []

#     for txn_id, txn_df in csv_file.groupby('PHARMACY_TRANSACTION_ID'):
#         for col in txn_df.columns:
#             col_lower = col.lower()
#             dtype = col_dtype_map.get(col_lower)
#             if dtype is None:
#                 error_message = f"Column not found in config"
#                 result_data.append(
#                     (txn_id, col, "Not Specified", "", "Pass", error_message))
#                 continue

#             col_values = txn_df[col].astype(str)

#             for value in col_values:
#                 if value.lower() == 'nan':
#                     continue

#                 if not value.strip():
#                     error_message = f"Empty value in column"
#                     result_data.append(
#                         (txn_id, col, dtype, value, "Fail", error_message))
#                     continue

#                 if re.match(r'DATE\(\d+\)', dtype):
#                     length = int(re.search(r'\((\d+)\)', dtype).group(1))
#                     value = value.replace('.0', '')

#                     if length == 8:
#                         if len(value) != length or not re.match(r'^\d+$', value):
#                             error_message = f"Invalid date format"
#                             result_data.append(
#                                 (txn_id, col, dtype, value, "Fail", error_message))
#                             continue

#                         try:
#                             datetime.strptime(value, '%Y%m%d')
#                         except ValueError:
#                             error_message = f"Invalid date format"
#                             result_data.append(
#                                 (txn_id, col, dtype, value, "Fail", error_message))
#                             continue

#                     elif length == 14:
#                         try:
#                             datetime.strptime(value, '%Y%m%d %H:%M:%S')
#                         except ValueError:
#                             error_message = f"Invalid date format"
#                             result_data.append(
#                                 (txn_id, col, dtype, value, "Fail", error_message))
#                             continue

#                 elif re.match(r'DATETIME\(\d+\)', dtype):
#                     length = int(
#                         re.search(r'DATETIME\((\d+)\)', dtype).group(1))
#                     value_str = str(value).strip().replace('.0', '')

#                     if len(value_str) != length:
#                         error_message = f"Invalid datetime format"
#                         result_data.append(
#                             (txn_id, col, dtype, value_str, "Fail", error_message))
#                         continue

#                 elif dtype.startswith('DOUBLE'):
#                     if not value.replace('.0', '').replace('.', '').isnumeric():
#                         error_message = f"Invalid double format"
#                         result_data.append(
#                             (txn_id, col, dtype, value, "Fail", error_message))
#                         continue

#                 elif dtype.startswith('VARCHAR'):
#                     length = int(re.search(r'\((\d+)\)', dtype).group(1))

#                     if len(value) > length:
#                         error_message = f"Exceeded length limit"
#                         result_data.append(
#                             (txn_id, col, dtype, value, "Fail", error_message))
#                         continue

#                 elif dtype.startswith('INTEGER'):
#                     if not value.replace('.0', '').isnumeric() and value.strip() != '':
#                         error_message = f"Invalid number format"
#                         result_data.append(
#                             (txn_id, col, dtype, value, "Fail", error_message))
#                         continue

#                 elif dtype.startswith('TIMESTAMP'):
#                     try:
#                         datetime.strptime(value, '%Y%m%d %H:%M:%S')
#                     except ValueError:
#                         error_message = f"Invalid timestamp format"
#                         result_data.append(
#                             (txn_id, col, dtype, value, "Fail", error_message))
#                         continue

#     validation_result_df = pd.DataFrame(result_data, columns=[
#                                         "PHARMACY_TRANSACTION_ID", "Column Name", "Data Type", "Value", "Status", "Details"])

#     if validation_result_df['Status'].eq('Pass').all():
#         return "All test cases passed successfully", validation_result_df
#     else:
#         return "Some test cases failed. Please check the output for more details", validation_result_df


# def maximum_length_validation(config_file, csv_file):
#     col_dtype_map = dict(
#         zip(config_file['Field Name'], config_file['Data Type']))

#     result_data = []

#     required_columns = config_file[config_file['Requirement'].isin(['Y', 'C'])]

#     for _, row in required_columns.iterrows():
#         col = row['Field Name']
#         dtype = col_dtype_map.get(col)

#         if dtype is None:
#             error_message = f"Column not found in config"
#             result_data.append(
#                 ("", col, "Not Specified", "", "Fail", error_message, row['Requirement']))
#             continue

#         if col not in csv_file.columns:
#             error_message = f"Column '{col}' not found in the CSV file"
#             result_data.append(
#                 ("", col, dtype, "", "Fail", error_message, row['Requirement']))
#             continue

#         col_values = csv_file[col].astype(str)

#         for index, value in col_values.items():
#             if value.lower() == 'nan':
#                 error_message = f"Missing required value in column"
#                 result_data.append(
#                     (index, col, dtype, value, "Fail", error_message, row['Requirement']))
#                 continue

#             if not value.strip():
#                 error_message = f"Empty value in column"
#                 result_data.append(
#                     (index, col, dtype, value, "Fail", error_message, row['Requirement']))
#                 continue

#             if dtype == 'DATE(14)':
#                 if not (re.match(r'^\d{8} \d{2}:\d{2}:\d{2}$', value) or re.match(r'^\d{14}$', value)):
#                     error_message = f"Invalid date format. Expected formats: YYYYMMDD HH:MM:SS or YYYYMMDDHHMMSS"
#                     result_data.append(
#                         (index, col, dtype, value, "Fail", error_message, row['Requirement']))
#                 else:
#                     try:
#                         if len(value) == 14:
#                             datetime.strptime(value, '%Y%m%d%H%M%S')
#                         else:
#                             datetime.strptime(value, '%Y%m%d %H:%M:%S')
#                         result_data.append(
#                             (index, col, dtype, value, "Pass", "", row['Requirement']))
#                     except ValueError:
#                         error_message = f"Invalid date format. Expected formats: YYYYMMDD HH:MM:SS or YYYYMMDDHHMMSS"
#                         result_data.append(
#                             (index, col, dtype, value, "Fail", error_message, row['Requirement']))

#     validation_result_df = pd.DataFrame(result_data, columns=[
#                                         "PHARMACY_TRANSACTION_ID", "Column Name", "Data Type", "Value", "Status", "Details", "Requirement"])

#     if validation_result_df['Status'].eq('Pass').all():
#         return "All test cases passed successfully", validation_result_df
#     else:
#         return "Some test cases failed. Please check the output for more details", validation_result_df


def field_name_validation(config_df, csv_df):
    config_columns = config_df['Field Name'].tolist()

    csv_columns = csv_df.columns.tolist()

    result_data = []

    for col in config_columns:
        if col in csv_columns:
            result_data.append({
                "Config Column": col,
                "CSV Column": col,
                "Status": "Pass",
                "Details": "Column found in both config and CSV files"
            })
        else:
            result_data.append({
                "Config Column": col,
                "CSV Column": "",
                "Status": "Fail",
                "Details": "Column present in config file but not in CSV file"
            })

    for col in csv_columns:
        if col not in config_columns:
            result_data.append({
                "Config Column": "",
                "CSV Column": col,
                "Status": "Fail",
                "Details": "Column present in CSV file but not in config file"
            })

    result_df = pd.DataFrame(result_data, columns=[
                             "Config Column", "CSV Column", "Status", "Details"])

    if result_df['Status'].eq('Pass').all():
        return "All columns found", result_df
    else:
        return "Some test cases failed. Please check the output for more details", result_df
