from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    USERNAME = (By.ID, 'user-name')
    PASSWORD = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, 'login-button')

    def __init__(self, driver):
        self.driver = driver

    def enter_username(self, username):
        username_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.USERNAME))
        username_field.send_keys(username)

    def enter_password(self, password):
        password_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.PASSWORD))
        password_field.send_keys(password)

    def click_login_button(self):
        login_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        login_button.click()


class HomePage:
    PRODUCT_NAMES = (By.CSS_SELECTOR, 'div.inventory_item_name')
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, 'button.btn_inventory')
    CART_BUTTON = (By.CSS_SELECTOR, 'a.shopping_cart_link')

    def __init__(self, driver):
        self.driver = driver

    @property
    def products(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.PRODUCT_NAMES))
        return [product.text for product in self.driver.find_elements(*self.PRODUCT_NAMES)]

    def add_to_cart(self, index):
        WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(self.ADD_TO_CART_BUTTONS))
        add_to_cart_buttons = self.driver.find_elements(*self.ADD_TO_CART_BUTTONS)
        add_to_cart_buttons[index].click()

    def click_cart_button(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.CART_BUTTON))
        self.driver.find_element(*self.CART_BUTTON).click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(CartPage.CART_ITEMS))


class CartPage:
    CART_ITEMS = (By.CSS_SELECTOR, 'div.cart_item')
    CHECKOUT_BUTTON = (By.ID, 'checkout')

    def __init__(self, driver):
        self.driver = driver

    def get_cart_items(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(self.CART_ITEMS))
        return [item.text.replace('\n1\n', '\n', 1) for item in self.driver.find_elements(*self.CART_ITEMS)]

    def click_checkout_button(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.CHECKOUT_BUTTON))
        self.driver.find_element(*self.CHECKOUT_BUTTON).click()
        WebDriverWait(self.driver, 10).until(EC.url_contains('checkout-step-one.html'))


class CheckoutPage:
    FIRST_NAME = (By.ID, 'first-name')
    LAST_NAME = (By.ID, 'last-name')
    ZIP_CODE = (By.ID, 'postal-code')
    CONTINUE_BUTTON = (By.ID, 'continue')
    PRODUCT_INFO = (By.CSS_SELECTOR, 'div.cart_item_label')
    TOTAL = (By.CSS_SELECTOR, 'div.summary_total_label')

    def __init__(self, driver):
        self.driver = driver

    def enter_first_name(self, first_name):
        first_name_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.FIRST_NAME))
        first_name_field.send_keys(first_name)

    def enter_last_name(self, last_name):
        last_name_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.LAST_NAME))
        last_name_field.send_keys(last_name)

    def enter_zip_code(self, zip_code):
        zip_code_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.ZIP_CODE))
        zip_code_field.send_keys(zip_code)

    def click_continue_button(self):
        continue_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.CONTINUE_BUTTON))
        continue_button.click()

    def get_product_info(self):
        return [product_info.text for product_info
                in WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(self.PRODUCT_INFO))]

    def get_total_price(self):
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.TOTAL)).text


class CompletePage:
    FINISH_BUTTON = (By.ID, 'finish')
    THANK_YOU_MESSAGE = (By.CSS_SELECTOR, 'h2.complete-header')

    def __init__(self, driver):
        self.driver = driver

    def click_finish_button(self):
        finish_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.FINISH_BUTTON))
        finish_button.click()

    def get_thank_you_message(self):
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.THANK_YOU_MESSAGE)).text
