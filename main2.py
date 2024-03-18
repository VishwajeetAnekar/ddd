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
        validation_result = "Success: Column names match"
    else:
        validation_result = "Error: Column names do not match"

    return result_df, validation_result


def unique_value_validation(df1, df2):
    unique_ids_df1 = df1["PHARMACY_TRANSACTION_ID"].value_counts()
    repeated_ids_df1 = unique_ids_df1[unique_ids_df1 > 1].index.tolist()

    unique_ids_df2 = df2["PHARMACY_TRANSACTION_ID"].value_counts()
    repeated_ids_df2 = unique_ids_df2[unique_ids_df2 > 1].index.tolist()

    result_rows = []
    for transaction_id in df1["PHARMACY_TRANSACTION_ID"]:
        if transaction_id in repeated_ids_df1:
            result_rows.append({'Column Name': 'PHARMACY_TRANSACTION_ID',
                                'Status': 'Fail',
                                'Repeated Value': transaction_id,
                                'Details': f'Common Value found in File 1'})
        else:
            result_rows.append({'Column Name': 'PHARMACY_TRANSACTION_ID',
                                'Status': 'Pass',
                                'Repeated Value': transaction_id,
                                'Details': f'ID is unique to File 1'})

    for transaction_id in df2["PHARMACY_TRANSACTION_ID"]:
        if transaction_id in repeated_ids_df2:
            result_rows.append({'Column Name': 'PHARMACY_TRANSACTION_ID',
                                'Status': 'Fail',
                                'Repeated Value': transaction_id,
                                'Details': f'Common Value found in File 2'})
        else:
            result_rows.append({'Column Name': 'PHARMACY_TRANSACTION_ID',
                                'Status': 'Pass',
                                'Repeated Value': transaction_id,
                                'Details': f'ID is unique to File 2'})

    result_df = pd.DataFrame(result_rows)

    if any(row['Status'] == 'Fail' for row in result_rows):
        return result_df, "Error: Repeated values found in one or both files"
    else:
        return result_df, "Success: No repeated values found in either file"


def required_fields_validation(config_df, data_df):
    required_columns = config_df[config_df['Requirement']
                                 == 'Y']['Field Name'].tolist()
    missing_columns = []

    for txn_id in data_df['PHARMACY_TRANSACTION_ID'].unique():
        txn_df = data_df[data_df['PHARMACY_TRANSACTION_ID'] == txn_id]
        for col in required_columns:
            if col not in txn_df.columns:
                missing_columns.append({
                    "PHARMACY_TRANSACTION_ID": txn_id,
                    "Column Name": col,
                    "Required Field (Y/N)": "Y",
                    "Value": " ",
                    "Status": "Fail",
                    "Details": "Column is missing"
                })
            else:
                if txn_df[col].isnull().values.any():
                    missing_columns.append({
                        "PHARMACY_TRANSACTION_ID": txn_id,
                        "Column Name": col,
                        "Required Field (Y/N)": "Y",
                        "Value": txn_df[col].iloc[0],
                        "Status": "Fail",
                        "Details": f"Field has empty values"
                    })
                else:
                    missing_columns.append({
                        "PHARMACY_TRANSACTION_ID": txn_id,
                        "Column Name": col,
                        "Required Field (Y/N)": "Y",
                        "Value": txn_df[col].iloc[0],
                        "Status": "Pass",
                        "Details": "Required field have value"
                    })

        for col in txn_df.columns:
            if col not in required_columns:
                missing_columns.append({
                    "PHARMACY_TRANSACTION_ID": txn_id,
                    "Column Name": col,
                    "Required Field (Y/N)": "N",
                    "Value": txn_df[col].iloc[0],
                    "Status": "Pass",
                    "Details": f"Non-required field"
                })

    result_df = pd.DataFrame(missing_columns)
    result_df = result_df[['PHARMACY_TRANSACTION_ID', 'Column Name',
                           'Required Field (Y/N)', 'Value', 'Status', 'Details']]
    error_message = "Error: Required fields are missing or have empty values"
    for _, row in result_df.iterrows():
        if row['Status'] == 'Fail':
            break
    else:
        error_message = "Success: All required fields have values"
    return result_df, error_message


def expected_values_validation(config_df, data_df):
    result_rows = []

    for txn_id in data_df['PHARMACY_TRANSACTION_ID'].unique():
        txn_df = data_df[data_df['PHARMACY_TRANSACTION_ID'] == txn_id]
        for _, config_row in config_df.iterrows():
            col = config_row['Field Name']
            # expected values for the current column as a string
            expected_values_str = str(
                config_row['Expected Value/s (comma separated)']).strip('""')
            # list containing the individual expected values after splitting and stripping the string.
            expected_values = [val.strip() for val in expected_values_str.split(
                ',') if val.strip().lower() != 'nan']

            if col not in txn_df.columns:
                result_rows.append({
                    "PHARMACY_TRANSACTION_ID": txn_id,
                    "Column Name": col,
                    "Expected Values": expected_values_str,
                    "Status": "Pass",
                    "Value": "",
                    "Details": f"Column not found"
                })
                continue

            for index, row in txn_df.iterrows():
                col_value = row[col] if col in row.index else None
                if pd.isnull(col_value) or (expected_values_str.lower() == 'nan' and col_value == ""):
                    status = "Pass"
                    details = "Column value is valid"
                elif expected_values and col_value not in expected_values:
                    status = "Fail"
                    details = "Column value is not valid"
                else:
                    status = "Pass"
                    details = "Column value is valid"

                result_rows.append({
                    "PHARMACY_TRANSACTION_ID": txn_id,
                    "Column Name": col,
                    "Expected Values": expected_values_str,
                    "Status": status,
                    "Value": col_value,
                    "Details": details
                })

    result_df = pd.DataFrame(result_rows)
    result_df = result_df[['PHARMACY_TRANSACTION_ID', 'Column Name',
                           'Expected Values', 'Value', 'Status', 'Details']]

    validation_result = "All values in expected columns are valid" if (
        result_df['Status'] == 'Pass').all() else result_df.to_string(index=False)

    return result_df, validation_result


def white_space_validation(df):
    result_data = []

    for txn_id in df['PHARMACY_TRANSACTION_ID'].unique():
        txn_df = df[df['PHARMACY_TRANSACTION_ID'] == txn_id]
        for col in df.columns:
            for index, value in txn_df[col].items():
                # if value = string and contains whitespace
                # (isinstance(value, int) and re.search(r'^\s|\s$|\s{2,}', str(value))):

                if isinstance(value, str) and re.search(r'^\s|\s$|\s{2,}', value):
                    details = "Whitespace found"
                    result_data.append({
                        "PHARMACY_TRANSACTION_ID": txn_id,
                        "Column Name": col,
                        "Value": value,
                        "Status": "Fail",
                        "Details": details
                    })
                else:
                    result_data.append({
                        "PHARMACY_TRANSACTION_ID": txn_id,
                        "Column Name": col,
                        "Value": value,
                        "Status": "Pass",
                        "Details": "No unneccessary whitespace"
                    })

    result_df = pd.DataFrame(result_data)

    if result_df['Status'].eq('Pass').all():
        validation_result = "Success: There are no spaces in the column values."
    else:
        validation_result = result_df.to_string(index=False)

    return result_df, validation_result


def duplicate_keys_validation(df):
    column_names = df.columns.tolist()
    status_list = ["Pass"] * len(column_names)
    details_list = ["Unique Column"] * len(column_names)
    duplicates_checked = set()

    for i, col_name in enumerate(column_names):
        # This slices the list of column names starting from the next index after the current column (i + 1).
        # This ensures that we are only checking the columns that come after the current column.

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
    col_dtype_map = dict(
        zip(config_file['Field Name'].str.lower(), config_file['Data Type']))

    result_data = []

    for txn_id, txn_df in csv_file.groupby('PHARMACY_TRANSACTION_ID'):
        for col in txn_df.columns:
            col_lower = col.lower()
            dtype = col_dtype_map.get(col_lower)
            if dtype is None:
                error_message = f"Column not found in config"
                result_data.append(
                    (txn_id, col, "Not Specified", "", "Pass", error_message))
                continue

            col_values = txn_df[col].astype(str)

            for value in col_values:
                if value.lower() == 'nan':
                    continue

                if not value.strip():
                    error_message = f"Empty value in column"
                    result_data.append(
                        (txn_id, col, dtype, value, "Fail", error_message))
                    continue

                if re.match(r'DATE\(\d+\)', dtype):
                    length = int(re.search(r'\((\d+)\)', dtype).group(1))
                    value = value.replace('.0', '')

                    if len(value) != length or not re.match(r'^\d+$', value):
                        error_message = f"Invalid date format"
                        result_data.append(
                            (txn_id, col, dtype, value, "Fail", error_message))
                        continue

                    try:
                        datetime.strptime(value, '%Y%m%d')
                    except ValueError:
                        error_message = f"Invalid date format"
                        result_data.append(
                            (txn_id, col, dtype, value, "Fail", error_message))
                        continue

                elif re.match(r'DATETIME\(\d+\)', dtype):
                    length = int(
                        re.search(r'DATETIME\((\d+)\)', dtype).group(1))
                    value_str = str(value).strip().replace('.0', '')

                    if len(value_str) != length:
                        error_message = f"Invalid datetime format"
                        result_data.append(
                            (txn_id, col, dtype, value_str, "Fail", error_message))
                        continue

                elif dtype.startswith('DOUBLE'):
                    if not value.replace('.0', '').replace('.', '').isnumeric():
                        error_message = f"Invalid double format"
                        result_data.append(
                            (txn_id, col, dtype, value, "Fail", error_message))
                        continue

                elif dtype.startswith('VARCHAR'):
                    length = int(re.search(r'\((\d+)\)', dtype).group(1))

                    if len(value) > length:
                        error_message = f"Exceeded length limit"
                        result_data.append(
                            (txn_id, col, dtype, value, "Fail", error_message))
                        continue

                elif dtype.startswith('INTEGER'):
                    if not value.replace('.0', '').isnumeric() and value.strip() != '':
                        error_message = f"Invalid number format"
                        result_data.append(
                            (txn_id, col, dtype, value, "Fail", error_message))
                        continue

                elif dtype.startswith('NUMERIC'):
                    match = re.search(r'\((\d+),(\d+)\)', dtype)

                    if match:
                        length, decimal_length = map(int, match.groups())

                        if not re.match(r'^\d+(\.\d+)?$', value):
                            error_message = f"Invalid numeric format"
                            result_data.append(
                                (txn_id, col, dtype, value, "Fail", error_message))
                            continue

                        int_part, dec_part = value.split(
                            '.') if '.' in value else (value, '')

                        if len(int_part) > length or len(dec_part) > decimal_length:
                            error_message = f"Exceeded length limit or invalid decimal format"
                            result_data.append(
                                (txn_id, col, dtype, value, "Fail", error_message))
                            continue

                elif dtype.startswith('TIMESTAMP'):
                    try:
                        datetime.strptime(value, '%Y%m%d %H:%M:%S')
                    except ValueError:
                        error_message = f"Invalid timestamp format"
                        result_data.append(
                            (txn_id, col, dtype, value, "Fail", error_message))
                        continue

                result_data.append(
                    (txn_id, col, dtype, value, "Pass", "Valid data"))

    validation_result_df = pd.DataFrame(result_data, columns=[
                                        "PHARMACY_TRANSACTION_ID", "Column Name", "Data Type", "Value", "Status", "Details"])

    if validation_result_df['Status'].eq('Pass').all():
        return "All test cases passed successfully", validation_result_df
    else:
        return "Some test cases failed. Please check the output for more details", validation_result_df


def field_name_validation(config_df, csv_df):
    result_data = []

    config_columns = set(config_df['Field Name'].str.lower())
    csv_columns = set(csv_df.columns.str.lower())

    for col in config_columns:
        if col in csv_columns:
            result_data.append({
                "Field Name": col,
                "Column name from CSV file": col,
                "Result": "Pass",
                "Comments": "Column exists in CSV file"
            })
        else:
            result_data.append({
                "Field Name": col,
                "Column name from CSV file": None,
                "Result": "Fail",
                "Comments": "Column does not exist in CSV file"
            })

    for col in csv_columns:
        if col not in config_columns:
            result_data.append({
                "Field Name": None,
                "Column name from CSV file": col,
                "Result": "Fail",
                "Comments": "Column not found in configuration"
            })

    result_df = pd.DataFrame(result_data, columns=["Field Name", "Column name from CSV file", "Result", "Comments"])

    if result_df['Result'].eq('Pass').all():
        validation_result = "Success: All columns found in CSV file"
    else:
        validation_result = "Error: Some columns not found in CSV file"

    return result_df, validation_result
