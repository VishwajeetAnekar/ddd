
def unique_value_validation(df1, df2):
    composite_key_df1 = df1['PHARMACY_TRANSACTION_ID'].astype(str) + df1['PHARMACY_PATIENT_ID'].astype(str)
    unique_ids_df1 = composite_key_df1.value_counts()
    repeated_ids_df1 = unique_ids_df1[unique_ids_df1 > 1].index.tolist()

    composite_key_df2 = df2['PHARMACY_TRANSACTION_ID'].astype(str) + df2['PHARMACY_PATIENT_ID'].astype(str)
    unique_ids_df2 = composite_key_df2.value_counts()
    repeated_ids_df2 = unique_ids_df2[unique_ids_df2 > 1].index.tolist()

    result_rows = []
    for transaction_id, patient_id in zip(df1['PHARMACY_TRANSACTION_ID'], df1['PHARMACY_PATIENT_ID']):
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

    for transaction_id, patient_id in zip(df2['PHARMACY_TRANSACTION_ID'], df2['PHARMACY_PATIENT_ID']):
        composite_key = str(transaction_id) + str(patient_id)
        if composite_key in repeated_ids_df2:
            result_rows.append({'Column Name': 'PHARMACY_TRANSACTION_ID_PHARMACY_PATIENT_ID',
                                'Status': 'Fail',
                                'Repeated Value': composite_key,
                                'Details': 'Common Value found in File 2'})
        else:
            result_rows.append({'Column Name': 'PHARMACY_TRANSACTION_ID_PHARMACY_PATIENT_ID',
                                'Status': 'Pass',
                                'Repeated Value': composite_key,
                                'Details': 'ID is unique to File 2'})

    result_df = pd.DataFrame(result_rows)

    if any(row['Status'] == 'Fail' for row in result_rows):
        return result_df, "Error: Repeated values found in one or both files"
    else:
        return result_df, "Success: No repeated values found in either file"
