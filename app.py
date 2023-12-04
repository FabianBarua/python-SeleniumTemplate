from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os

service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
load_dotenv()
user = os.getenv("USER")
psw = os.getenv("PASSWORD")
url = os.getenv("URL")


#ACA CARGAR LAS FECHAS
fecha_inicio = "01/11/2023"
fecha_fin = "30/11/2023"

def txt_to_list(file_path):
    with open(file_path, 'r') as file:
        return file.read().splitlines()

driver.get(url)

wait = WebDriverWait(driver, 10)
user_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="frm-login"]/form/div[1]/input')))
user_input.send_keys(user)

pass_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="frm-login"]/form/div[2]/input')))
pass_input.send_keys(psw)

login_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="frm-login"]/form/button')))
login_btn.click()

productos_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side-menu"]/li[13]/a')))
productos_btn.click()

time.sleep(2)

productos_btn_sub = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side-menu"]/li[13]/ul/li[1]')))
productos_btn_sub.click()

files_to_process = ['codigos.txt']

for file in files_to_process:
    prods = txt_to_list(file)
    prods = list(map(int, prods))
    for code in prods:
        print(f"Cargando {code}")
        try:

            search = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="DataTableGrid18listar_filter"]/label/input')))
            search.clear()
            search.send_keys(code)

            time.sleep(3)

            id = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="DataTableGrid18listar"]/tbody/tr/td[1]')))
            id = int(id.text) + 1
            print(id)

            acao = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="DataTableGrid18listar"]/tbody/tr/td[18]/div/button')))
            acao.click()
            time.sleep(0.1)

            precooferta = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="DataTableGrid18listar"]/tbody/tr/td[18]/div/ul/li[7]')))
            precooferta.click()
            
            time.sleep(3)

            generar = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ListItem0"]/td[4]/button')))
            generar.click()


            script = f'document.evaluate("/html/body/div[3]/div/div/div[2]/div/div/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td/form/div[1]/div[1]/div/input", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.value = "{fecha_inicio}";'
            driver.execute_script(script)

            
            script = f'document.evaluate("/html/body/div[3]/div/div/div[2]/div/div/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td/form/div[1]/div[2]/div/input", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.value = "{fecha_fin}";'
            driver.execute_script(script)

            check = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td/form/div[2]/div[1]/div[1]/input')))
            check.click()


            campo_desconto = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td/form/div[2]/div[3]/input')))
            campo_desconto.clear()
            campo_desconto.send_keys('1200')

            boton_salvar = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td/form/div[3]/div/button')))
            boton_salvar.click()
            time.sleep(3)

            cerrar = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="modalDefault"]/div/div/div[1]/button')))
            cerrar.click()
            print("----------------------------------finalizado----------------------------------")
            time.sleep(3)
        except:
            try:
                cerrar = driver.find_element(By.XPATH, '//*[@id="modalDefault"]/div/div/div[1]/button')
                cerrar.click()
            except:
                pass  # El botón de cierre no existe, continuar sin hacer nada

            with open('errores.txt', 'a') as error_file:
                error_file.write(f"Error: {code}\n")


driver.quit()
