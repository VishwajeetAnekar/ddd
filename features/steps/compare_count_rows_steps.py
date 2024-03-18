from behave import given, when, then
import pandas as pd
from csv_paths import *
from main2 import row_count_validation


@when(u'I compare the CSV files for rows')
def step_impl(context):
    context.validation_result_df, context.validation_result = row_count_validation(
        context.data_file, context.data_file2)
    context.validation_result_df.to_csv('Results/row_count_validation_result.csv', index=False)

@then(u'the number of rows should be the same')
def step_impl(context):
    assert context.validation_result.startswith("Both files"), f"Error: {context.validation_result}"

