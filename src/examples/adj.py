<<<<<<< HEAD
# importando context
import context as c

# importando classes
from etl.bacen_etl     import BacenETL         as bl
from etl.data_combine  import DataCombine      as de
from etl.santander_etl import SantanderETL     as sl
from etl.sant_wg       import SantWebscrapping as sg

# chamando classe de Webscrapping (Santander)
pipe_sg = sg(c.DATA_EXT_FLD)
pipe_sg.webscrapping()
scrapped_data = c.get_last_file(r"C:\Users\oev100285\Downloads", r"Projeções_\d+\.zip")
path_zip = c.get_last_file(c.DATA_EXT_FLD, r'Projeções_\d+\.zip')
pipe_sg.move_unzip(scrapped_data, path_zip)

# chamando a classe do Santander
excel_path = c.get_last_file(c.DATA_EXT_FLD, r'MACROECO_ENG \d+\.xlsx')
pipe_sl = sl(excel_path, c.DATA_PROC_FLD)

# chamando a classe do Bacen
pipe_bl = bl()

# rodando as classes
df_sl = pipe_sl.run()
df_bl = pipe_bl.run()

# chamando a classe de merge
pipe_de = de(c.REPORT_FLD, df_sl, df_bl)

# rodando o merge
pipe_de.run()
