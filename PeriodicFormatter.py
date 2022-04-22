import pandas as pd
import xlsxwriter

df = pd.read_json ('items.json') # ler arquivo JSON com os dados
artigos = df.iloc[:,4] # artigos é o dataframe com as colunas referentes aos artigos de cada periodico ligados pelo volume e número 

flat_list = [item for sublist in artigos for item in sublist] # flat_list é a lista com todos os artigos de todos os periódicos
df_artigos = pd.DataFrame(flat_list) # df_artigos é o dataframe com todos os artigos de todos os periódicos
keywords = df_artigos['Palavras-Chave'] # keywords é o dataframe com a coluna referentes a palavras-chave de cada artigo

normalized_df = pd.json_normalize(keywords) # normalized_df é o dataframe com as palavras-chave de cada artigo transformado em colunas

df_artigos = pd.concat([df_artigos, normalized_df], axis=1) # df_artigos aqui é a soma do dataframe com as palavras-chave de cada artigo e os outros atributos dos artigos

df.pop('Artigos') # remove a coluna com os artigos
df_artigos.pop('Palavras-Chave') # remove a coluna com as palavras-chave em formato de lista de cada artigo

writer = pd.ExcelWriter('PontodeAcesso.xlsx', engine='xlsxwriter') # cria um arquivo Excel com o nome PontodeAcesso.xlsx
df.to_excel(writer, sheet_name='Edições') # escreve o dataframe normalDF com as colunas referentes ao nome do periódico, volume, número e capa no arquivo Excel
df_artigos.to_excel(writer, sheet_name='Artigos')  # escreve o dataframe df_artigos com as colunas referentes aos artigos de cada periódico ligados pelo volume e número no arquivo Excel
writer.save() # salva o arquivo Excel