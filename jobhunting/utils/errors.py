from scrapper_boilerplate import TelegramBot


def send_error_to_telegram(error:str, driver:object, title:str, telegram:TelegramBot):
    """
    Send error to telegram

    :param error: Error message
    :param driver: Webdriver
    :param title: error title
    :param telegram: Telegram bot
    :return: None
    """
    error_file = f"{title}_error.png"
    driver.save_screenshot(error_file)
    telegram.send_message(f"ERRO! url: {driver.current_url}")
    telegram.send_message(str(error))
    telegram.send_file(error_file)
