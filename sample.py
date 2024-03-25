import pandas as pd

def required_field_validation(config_df, csv_df):
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
    return result_df

config_file_path = pd.read_csv('CSV files\cccc.csv')
csv_file_path = pd.read_csv('CSV files\demo.csv')
result_df = required_field_validation(config_file_path, csv_file_path)
result_df.to_csv('testing.csv')
