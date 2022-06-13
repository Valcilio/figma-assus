from selenium import webdriver
import shutil
from webdriver_manager.chrome import ChromeDriverManager
import time
import zipfile

class SantWebscrapping():

    def __init__(self, dest: str, **kwargs):
        self.dest = dest

    def move_unzip(self, file, path_zip, **kwargs):
        # salvando self
        self.file = file
        self.path_zip = path_zip
        
        # rodando métodos
        self.move_file()
        self.unzip_file()

    def webscrapping(self, **kwargs):
            # definindo webdriver
            navegador = webdriver.Chrome(ChromeDriverManager().install())

            # baixando arquivo
            navegador.get("https://www.santander.com.br/analise-economica")
            navegador.find_element_by_xpath('//*[@id="projecoes"]/content-page/div[2]/download-list/div/div/product-accordion-content-downloads/div/product-accordion-content-download/a').click()

            # esperando três segundos e fechando o bowser
            time.sleep(3)
            navegador.close()
            
    def move_file(self, **kwargs):
            # movendo de downloads para
            try: 
                shutil.move(self.file, self.dest)
            except Exception as e:
                pass

    def unzip_file(self, **kwargs):
            # fazendo o unzip dos arquivos
            Zip_ref = zipfile.ZipFile(self.path_zip, 'r')
            Zip_ref.extractall(self.dest)
            Zip_ref.close()