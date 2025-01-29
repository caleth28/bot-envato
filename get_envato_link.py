import time
import os
import tempfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Ajusta tu correo y contraseña de Envato
ENVATO_EMAIL = "diseno@peusac.com.pe"
ENVATO_PASSWORD = "Motivate28@"

def get_envato_link(item_url: str) -> str:
    """
    Descarga el recurso de Envato Elements y espera hasta que la descarga se complete.
    Retorna el enlace de descarga directo si está disponible.
    """

    # Configurar la carpeta de descargas
    download_dir = os.path.join(os.getcwd(), "downloads")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Configurar opciones de Chrome
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    
    temp_user_data_dir = tempfile.mkdtemp()
    chrome_options.add_argument(f"--user-data-dir={temp_user_data_dir}")

    # **Asegurar que la ventana de Chrome se abra maximizada**
    chrome_options.add_argument("--start-maximized")  # Expande la ventana a pantalla completa
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 1) Ir a la homepage de Envato
    driver.get("https://elements.envato.com/")
    time.sleep(3)

    # 2) Iniciar sesión
    try:
        sign_in = driver.find_element(By.LINK_TEXT, "Sign In")
    except:
        sign_in = driver.find_element(By.LINK_TEXT, "Iniciar sesión")
    sign_in.click()
    time.sleep(3)

    # Credenciales
    email_input = driver.find_element(By.ID, "username")
    email_input.send_keys(ENVATO_EMAIL)
    time.sleep(1)

    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(ENVATO_PASSWORD)
    password_input.send_keys(Keys.ENTER)
    time.sleep(8)

    # 3) Ir al ítem
    driver.get(item_url)
    time.sleep(5)

    # 4) Botón "Download"
    try:
        download_btn = driver.find_element(By.CSS_SELECTOR, "button[data-testid='button-download']")
        download_btn.click()
        time.sleep(3)
    except Exception as e:
        driver.quit()
        return f"ERROR: No encontré el botón Download en {item_url} - {e}"

    # 5) Seleccionar la opción "Bot"
    try:
        bot_radio = driver.find_element(By.XPATH, "//input[@type='radio' and @value='Bot']")
        bot_radio.click()
        time.sleep(2)
    except Exception as e:
        driver.quit()
        return "No encontré la opción 'Bot' en el modal de proyectos."

    # 6) Botón "Añadir y descargar"
    try:
        add_download_btn = driver.find_element(By.CSS_SELECTOR, "button[data-testid='add-download-button']")
        add_download_btn.click()
        time.sleep(5)
    except Exception as e:
        driver.quit()
        return "No encontré el botón 'Añadir y descargar'."

    # 7) Esperar hasta que la descarga se complete
    download_complete = False
    start_time = time.time()
    while not download_complete:
        time.sleep(1)
        # Verificar si hay algún archivo descargado
        files = os.listdir(download_dir)
        if any(file.endswith(".crdownload") for file in files):
            # Archivo aún en progreso
            continue
        elif len(files) > 0:
            # Archivo descargado completamente
            download_complete = True
        # Si se demora más de 2 minutos, abortar
        if time.time() - start_time > 120:
            driver.quit()
            return "Descarga no se completó en el tiempo esperado."

    # 8) Retornar enlace si está disponible
    all_links = driver.find_elements(By.TAG_NAME, "a")
    final_link = None
    for link in all_links:
        href = link.get_attribute("href")
        if href and "envatousercontent.com" in href:
            final_link = href
            break

    driver.quit()

    if final_link:
        return final_link
    else:
        return f"Descarga completada. Revisa la carpeta: {download_dir}"

# Para probar localmente:
if __name__ == "__main__":
    test_url = "https://elements.envato.com/es/text-animation-toolkit-D8HAYMX"
    link = get_envato_link(test_url)
    print("Link obtenido:", link)
