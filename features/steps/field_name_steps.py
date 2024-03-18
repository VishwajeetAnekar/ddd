from behave import given, when, then
from main2 import field_name_validation
import pandas

@when(u'field name are validated')
def step_impl(context):
    context.validation_result, context.validation_result_df = field_name_validation(
        context.config_file, context.data_file)
    context.validation_result.to_csv('Results/field_name_validation_result.csv', index=False)

@then(u'all fields are validated')
def step_impl(context):
    assert context.validation_result == "Success: All columns found in CSV file", "Column names do not match"


