def expected_values_validation(config_df, data_df):
    result_rows = []
    for txn_id in data_df['PHARMACY_TRANSACTION_ID'].unique():
        txn_df = data_df[data_df['PHARMACY_TRANSACTION_ID'] == txn_id]
        for _, config_row in config_df.iterrows():
            col = config_row['Field Name']
            requirement = config_row['Requirement']
            if requirement.lower() in ['c', '']:
                continue

            expected_values_str = str(config_row['Expected Value/s (comma separated)']).strip('""')


            if expected_values_str.lower() in ['nan', '']:
                continue

            expected_values = [val.strip() for val in expected_values_str.split(',') if val.strip() != '']
            if col not in txn_df.columns:
                result_rows.append({
                    "PHARMACY_TRANSACTION_ID": txn_id,
                    "Column Name": col,
                    "Required Field (Y/N)": requirement,
                    "Expected Values": expected_values_str,
                    "Value": "",
                    "Status": "Fail",
                    "Comments": "Column not found in the CSV file"
                })
                continue

            for _, row in txn_df.iterrows():
                col_value = row[col] if col in row.index else None

                if requirement.lower() == 'n' and (pd.isna(col_value) or col_value == ""):
                    continue

                if requirement.lower() == 'y' and (pd.isna(col_value) or col_value == ""):
                    result_rows.append({
                        "PHARMACY_TRANSACTION_ID": txn_id,
                        "Column Name": col,
                        "Required Field (Y/N)": requirement,
                        "Expected Values": expected_values_str,
                        "Value": col_value,
                        "Status": "Fail",
                        "Comments": "Value is empty, but requirement is 'Y'"

                    })
                elif col_value is not None and str(col_value) not in expected_values:
                    result_rows.append({
                        "PHARMACY_TRANSACTION_ID": txn_id,
                        "Column Name": col,
                        "Required Field (Y/N)": requirement,
                        "Expected Values": expected_values_str,
                        "Value": col_value,
                        "Status": "Fail",
                        "Comments": "Value does not match expected values"

                    })
    result_df = pd.DataFrame(result_rows)

    if not result_df.empty and "Fail" in result_df["Status"].values:
        return result_df, "Some values in expected columns are invalid"
    else:
        return pd.DataFrame(columns=['PHARMACY_TRANSACTION_ID', 'Column Name', 'Required Field (Y/N)', 'Expected Values', 'Value', 'Status', 'Comments']), "All transactions passed"
