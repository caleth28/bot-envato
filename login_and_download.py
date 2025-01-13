import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

ENVATO_EMAIL = "diseno@peusac.com.pe"
ENVATO_PASSWORD = "Motivate28@"


def wait_for_downloads(download_dir):
    """
    Espera hasta que la carpeta de descargas no contenga archivos parciales.
    """
    print("Esperando a que se complete la descarga...")
    while any(filename.endswith(".crdownload") for filename in os.listdir(download_dir)):
        time.sleep(1)
    print("Descarga completada.")


def download_envato(item_url: str):
    """
    1) Abre Chrome + cookies/credenciales, inicia sesión en Envato.
    2) Va a 'item_url', selecciona proyecto 'Bot', y descarga.
    3) El archivo se guarda directamente en una carpeta local sin preguntar.
    """
    # 1) Carpeta donde guardaremos las descargas
    download_dir = os.path.join(os.getcwd(), "downloads")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # 2) Configurar opciones de Chrome
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,  # Carpeta de descargas
        "download.prompt_for_download": False,       # No preguntar
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    # Evitar que la ventana se cierre automáticamente
    chrome_options.add_experimental_option("detach", True)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # 3) Ir a la homepage Envato Elements
        driver.get("https://elements.envato.com/")
        time.sleep(3)

        # 4) Log in
        try:
            sign_in_btn = driver.find_element(By.LINK_TEXT, "Sign In")
        except:
            sign_in_btn = driver.find_element(By.LINK_TEXT, "Iniciar sesión")
        sign_in_btn.click()
        time.sleep(3)

        email_input = driver.find_element(By.ID, "username")
        email_input.send_keys(ENVATO_EMAIL)
        time.sleep(1)

        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys(ENVATO_PASSWORD)
        password_input.send_keys(Keys.ENTER)
        time.sleep(8)

        # 5) Ir al ítem
        driver.get(item_url)
        time.sleep(5)

        # 6) Botón "Download" (data-testid='button-download')
        download_btn = driver.find_element(By.CSS_SELECTOR, "button[data-testid='button-download']")
        download_btn.click()
        time.sleep(3)

        # 7) Seleccionar "Bot" (radio value="Bot")
        bot_radio = driver.find_element(By.XPATH, "//input[@type='radio' and @value='Bot']")
        bot_radio.click()
        time.sleep(2)

        # 8) Clic en “Añadir y descargar”
        add_download_btn = driver.find_element(By.CSS_SELECTOR, "button[data-testid='add-download-button']")
        add_download_btn.click()

        # 9) Esperar hasta que la descarga se complete
        wait_for_downloads(download_dir)

        print(f"Descarga completada. Revisa la carpeta: {download_dir}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Opcional: No cerrar automáticamente el navegador si es necesario
        # driver.quit()
        pass

    return download_dir
