from behave import given, when, then
from main2 import required_fields_validation
import pandas as pd

from csv_paths import *


@given('a configuration file')
def step_impl(context):
    context.config_file = pd.read_csv(config_file)


@given('a csv file')
def step_impl(context):
    context.data_file = pd.read_csv(latest_extract)


@when('required fields are validated')
def step_impl(context):
    context.validation_result_df, context.validation_result = required_fields_validation(
        context.config_file, context.data_file)

    context.validation_result_df.to_csv(
        'Results/Done/required_fields_validation_result.csv', index=False)



@then('all required fields have values')
def step_impl(context):
    if "Some required fields are missing" in context.validation_result:
        assert False, "Required fields validation failed: Some required fields are missing"
    else:
        assert True, "Required fields validation passed"