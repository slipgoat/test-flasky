import allure
import assertpy
from assertpy.assertpy import AssertionBuilder


def assert_that(value, description: str = None) -> AssertionBuilder:
    if description is not None:
        with allure.step(f"Check {description}"):
            return assertpy.assert_that(value, description)
    return assertpy.assert_that(value, description)
