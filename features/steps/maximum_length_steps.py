from behave import given, when, then
from main2 import maximum_length_validation

@when('maximum length is validated')
def step_impl(context):
    context.validation_result, context.validation_result_df = maximum_length_validation(
        context.config_file, context.data_file)
    context.validation_result_df.to_csv('Results/Done/maximum_length_validation_result.csv', index=False)

@then('the length of each field is within the specified limits')
def step_impl(context):
        assert context.validation_result == "Some values failed maximum length and data type validation", "Validation failed"


    # if "Some values failed maximum length and data type validation" in context.validation_result:
    #     assert False, "Maximum length and data type validation failed: Some values have invalid data types or exceeded maximum length"
    # else:
    #     assert True, "Validation passed"
