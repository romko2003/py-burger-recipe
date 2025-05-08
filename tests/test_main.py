from abc import ABC

import pytest


from app.main import Validator, BurgerRecipe


@pytest.mark.parametrize(
    "ingredients",
    [[2, 0, 0, 1, 0, "ketchup"],
     [2, 1, 2, 2, 1, "mayo"],
     [3, 2, 3, 3, 2, "burger"]],
)
def test_burger_consists_of_right_ingredients(ingredients):
    burger = BurgerRecipe(*ingredients)
    components = ["buns", "cheese", "tomatoes", "cutlets", "eggs", "sauce"]
    assert [getattr(burger, component) for component in components] == ingredients, (
        f"'burger' ingredients {' '.join(components)} should equal to {ingredients}, "
        f"when 'burger' is created by 'BurgerRecipe(*{ingredients})'"
    )


@pytest.mark.parametrize("method", ["__set_name__", "__get__", "__set__", "validate"])
def test_four_methods_should_be_in_validator(method):
    assert method in Validator.__dict__, f"Method {method} should be in Validator"


def test_validator_is_abstract():
    assert issubclass(Validator, ABC), "Validator should be abstract class"


def test_validate_is_abstract_method():
    assert "validate" in Validator.__abstractmethods__


@pytest.mark.parametrize(
    "ingredient",
    ["cheese", "tomatoes", "cutlets", "eggs", "buns"],
)
def test_number_instance_has_attrs(ingredient):
    attrs = {"min_value", "max_value", "protected_name"}
    assert attrs.issubset(
        set(BurgerRecipe.__dict__[ingredient].__dict__.keys())
    ), f"Descriptor Number for {ingredient} should have such attributes {attrs}"


def test_one_of_instance_has_attrs():
    attributes = {"options", "protected_name"}
    assert attributes.issubset(
        set(BurgerRecipe.__dict__["sauce"].__dict__.keys())
    ), f"Descriptor OneOf for `sauce` should have such attributes {attributes}"


@pytest.mark.parametrize(
    "attr,protected_attr",
    [
        ("cheese", "_cheese"),
        ("tomatoes", "_tomatoes"),
        ("cutlets", "_cutlets"),
        ("eggs", "_eggs"),
        ("buns", "_buns"),
        ("sauce", "_sauce"),
    ],
)
def test_validator_protected_name(attr, protected_attr):
    assert (
        BurgerRecipe.__dict__[attr].__dict__["protected_name"] == protected_attr
    ), f"For attribute '{attr}' descriptor Validator should create 'protected_name' equals to '{protected_attr}'"


@pytest.mark.parametrize(
    "ingredient", ["_cheese", "_tomatoes", "_cutlets", "_eggs", "_buns", "_sauce"]
)
def test_ingredients_in_dir_burger(ingredient):
    burger = BurgerRecipe(2, 1, 1, 1, 1, "ketchup")
    assert ingredient in burger.__dict__, (
        f"'burger' should have protected attribute {ingredient} "
        "if 'burger' is instance of BurgerRecipe"
    )


@pytest.mark.parametrize(
    "ingredients",
    [
        ["1", 1, 1, 1, 2, "ketchup"],
        [lambda x: x, 1, 1, 1, 2, "ketchup"],
        [ValueError, 1, 1, 1, 2, "ketchup"],
        [None, 1, 1, 1, 2, "ketchup"],
    ],
)
def test_incorrect_type_of_ingredient(ingredients):
    with pytest.raises(TypeError) as e:
        BurgerRecipe(*ingredients)
    assert (
        str(e.value) == "Quantity should be integer."
    ), "Text of the 'TypeError' should equal to 'Quantity should be integer.'"


def test_incorrect_type_of_sauce():
    with pytest.raises(ValueError) as e:
        BurgerRecipe(2, 1, 1, 1, 1, "mustard")
    assert (
        str(e.value) == "Expected mustard to be one of ('ketchup', 'mayo', 'burger')."
    ), "Text of the 'ValueError' should equal to 'Expected mustard to be one of ('ketchup', 'mayo', 'burger')."


@pytest.mark.parametrize(
    "ingredients",
    [
        [4, 1, 1, 1, 1, "ketchup"],
        [1, 1, 1, 1, 1, "ketchup"],
        [2, -1, 1, 1, 1, "ketchup"],
        [2, 3, 1, 1, 1, "ketchup"],
        [2, 1, -1, 1, 1, "ketchup"],
        [2, 1, 4, 1, 1, "ketchup"],
        [2, 1, 1, 0, 1, "ketchup"],
        [2, 1, 1, 4, 1, "ketchup"],
        [2, 1, 1, 1, -1, "ketchup"],
        [2, 1, 1, 1, 3, "ketchup"],
    ],
)
def test_ingredient_out_of_range(ingredients):
    with pytest.raises(ValueError):
        BurgerRecipe(*ingredients)
        pytest.fail(msg="Text of the 'ValueError' should equal to "
                        "Quantity should not be less than attribute minvalue "
                        "and greater than attribute maxvalue.")
