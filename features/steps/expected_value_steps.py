# from behave import given, when, then
# from main2 import expected_values_validation
# import pandas as pd

# @when('expected values are validated')
# def step_impl(context):
#     context.validation_result_df, context.validation_result = expected_values_validation(context.config_file, context.data_file)
#     context.validation_result_df.to_csv('Results/expected_values_validation_result.csv', index=False)

# @then('all values in the specified columns are equal to expected values')
# def step_impl(context):
#     # assert context.validation_result == "All values in expected columns are valid","Expected values validation failed"
#     if "Some values in expected columns are invalid" in context.validation_result:
#         assert False, "Expected values validation failed: Some values in expected columns are invalid"
#     else:
#         assert True, "All values in expected columns are valid"