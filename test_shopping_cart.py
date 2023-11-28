import pytest
from selenium import webdriver
from practical_task_2_cart.page_objects_2 import LoginPage
from practical_task_2_cart.page_objects_2 import HomePage
from practical_task_2_cart.page_objects_2 import CartPage
from practical_task_2_cart.page_objects_2 import CheckoutPage
from practical_task_2_cart.page_objects_2 import CompletePage


@pytest.fixture(scope="module")
def setup():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


users_credentials = [
    {"username": "standard_user", "password": "secret_sauce"},
    {"username": "problem_user", "password": "secret_sauce"},
    {"username": "performance_glitch_user", "password": "secret_sauce"},
    {"username": "error_user", "password": "secret_sauce"},
    {"username": "visual_user", "password": "secret_sauce"},
    ]


@pytest.mark.parametrize("user_credentials", users_credentials)
def test_with_all_users(setup, user_credentials):
    username = user_credentials["username"]
    password = user_credentials["password"]

    driver = setup
    driver.get("https://www.saucedemo.com/")
    login_page = LoginPage(driver)
    login_page.enter_username(username)
    login_page.enter_password(password)
    login_page.click_login_button()
    assert "https://www.saucedemo.com/inventory.html" in driver.current_url

    test_add_to_cart(driver)
    test_checkout(driver)
    test_complete_checkout(driver)


def test_add_to_cart(setup):
    driver = setup
    driver.get("https://www.saucedemo.com/inventory.html")
    home_page = HomePage(driver)
    cart_page = CartPage(driver)
    for i in range(len(home_page.products)):
        home_page.add_to_cart(i)
    home_page.click_cart_button()
    cart_items = cart_page.get_cart_items()
    cart_product_names = [item.split('\n')[1] for item in cart_items]
    assert set(home_page.products) == set(cart_product_names)


def test_checkout(setup):
    driver = setup
    driver.get("https://www.saucedemo.com/cart.html")
    cart_page = CartPage(driver)
    checkout_page = CheckoutPage(driver)
    cart_page.click_checkout_button()
    checkout_page.enter_first_name("A")
    checkout_page.enter_last_name("A")
    checkout_page.enter_zip_code("A")
    checkout_page.click_continue_button()
    checkout_product_names = [item.split('\n')[0] for item in checkout_page.get_product_info()]
    assert checkout_product_names == [item.split('\n')[1] for item in cart_page.get_cart_items()]


def test_complete_checkout(setup):
    driver = setup
    driver.get("https://www.saucedemo.com/checkout-step-two.html")
    complete_page = CompletePage(driver)
    complete_page.click_finish_button()
    assert complete_page.get_thank_you_message() == "Thank you for your order!"
