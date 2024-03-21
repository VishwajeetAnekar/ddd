from behave import given, when, then
from csv_paths import *
from main2 import column_name_match


@when(u'I compare the CSV files for Column Names')
def step_impl(context):
    context.validation_result, context.validation_result_df = column_name_match(
        context.data_file, context.data_file2)
    context.validation_result_df.to_csv('Results/column_name_validation_result.csv', index=False)

@then(u'the Column names should match')
def step_impl(context):
    assert context.validation_result == "Success: Column names match","Expected values validation failed"
