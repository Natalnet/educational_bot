import requests
import json

urlBD = "https://monitor-bot-88c17-default-rtdb.firebaseio.com/"
## carregando url da api do firebase
# with open('config.json') as f:
#     config = json.load(f)
#     urlBD = config['url_api']

def cria_pergunta(pergunta, resposta):

  #cria um dicionário com a pergunta e a resposta
  dicionario_pergunta = {'pergunta': pergunta, 'resposta': resposta}

  #transforma o dicionário em json
  json_pergunta = json.dumps(dicionario_pergunta)

  #faz a requisição do tipo post na api
  requisicao = requests.post(f'{urlBD}/perguntas/.json', data = json_pergunta)

  #verifica se a requisição foi bem sucedida (200)
  return(requisicao.status_code == 200)

def edita_pergunta(id, pergunta='pergunta padrao', resposta='resposta padrao'):

  #edita apenas a resposta
  #cria um dicionário com a resposta
  if(pergunta == 'pergunta padrao'): dicionario_pergunta = {'resposta': resposta}
  #edita apenas a pergunta
  #cria um dicionário com a pergunta
  elif(resposta == 'resposta padrao'): dicionario_pergunta = {'pergunta': pergunta} 
  #edita a pergunta e a resposta
  #cria um dicionário com a pergunta e a resposta
  else: dicionario_pergunta = {'pergunta': pergunta, 'resposta': resposta}

  #transforma o dicionário em json  
  json_pergunta = json.dumps(dicionario_pergunta)
  #faz a requisição do tipo patch na api
  requisicao = requests.patch(f'{urlBD}/perguntas/{id}/.json', data = json_pergunta)

  #verifica se a requisição foi bem sucedida (200)
  return(requisicao.status_code == 200)

def deleta_pergunta(id):
  #deleta a pergunta com o id correspondente
  requisicao = requests.delete(f'{urlBD}/perguntas/{id}/.json')

  #verifica se a requisição foi bem sucedida (200)
  return(requisicao.status_code == 200)

def le_perguntas():
  #le perguntas
  requisicao = requests.get(f'{urlBD}/perguntas/.json')
  
  return(requisicao)

def get_id(pergunta):
  requisicao = le_perguntas()

  for id in requisicao.json():
    if pergunta == requisicao.json()[id]['pergunta']:
      return(id)
    
def cria_log(log):
     
  #cria um dicionário com o log
  dicionario_logs = {'log': log}

  #transforma o dicionário em json
  json_logs = json.dumps(dicionario_logs)

  #faz a requisição do tipo post na api
  requisicao = requests.post(f'{urlBD}/logs/.json', data = json_logs)

  #verifica se a requisição foi bem sucedida (200)
  return(requisicao.status_code == 200)

def get_id_resposta(resposta):
      
  requisicao = requests.get(f'{urlBD}/perguntas/.json')

  data = requisicao.json()

  for item in data:
      if isinstance(item, dict) and item.get('resposta') == resposta:
          return item['id']

  return None

    
    
def guardar_requisicao(resposta, id_pergunta, data, contador):
    
  #cria um dicionário com a pergunta e a resposta
  dicionario_pergunta = {'resposta': resposta, 'id': id_pergunta, 'data': data, 'contagem': contador}

  #transforma o dicionário em json
  json_pergunta = json.dumps(dicionario_pergunta)

  #faz a requisição do tipo post na api
  requisicao = requests.post(f'{urlBD}/requisicao/.json', data = json_pergunta)

  #verifica se a requisição foi bem sucedida (200)
  return(requisicao.status_code == 200)

def get_resposta(resposta):
  requisicao = le_perguntas()

  for id in requisicao.json():
    if resposta == requisicao.json()[id]['resposta']:
      return(resposta)
    

def le_requisicao():
      #le perguntas
    requisicao = requests.get(f'{urlBD}/requisicao/.json')
    return(requisicao)


def contagem(id, contador):
      
  dicionario_frequencia = {"contagem": contador}

  #transforma o dicionário em json  
  json_freq = json.dumps(dicionario_frequencia)

  #faz a requisição do tipo post na api
  requisicao = requests.patch(f'{urlBD}/requisicao/{id}/.json', data = json_freq)
  
  
def verificar_id(resposta):
  requisicao = le_requisicao()

  for id in requisicao.json():
    if resposta == requisicao.json()[id]['resposta']:
      return(id)
    
def requisicao_banco(resposta):
  requisicao = le_requisicao()

  for id in requisicao.json():
    if resposta == requisicao.json()[id]['resposta']:
      return(requisicao.json()[id]['resposta'])
    
def retornar_contagem(resposta):
  requisicao = le_requisicao()

  for id in requisicao.json():
    if resposta == requisicao.json()[id]['resposta']:
      return(requisicao.json()[id]['contagem'])
    
    
def guardar_requisicao_erro(resposta, data):
  Error = 'Erro'
  #cria um dicionário com a pergunta e a resposta
  dicionario_pergunta = {'Processo': Error ,'resposta': resposta, 'data': data}

  #transforma o dicionário em json
  json_pergunta = json.dumps(dicionario_pergunta)

  #faz a requisição do tipo post na api
  requisicao = requests.post(f'{urlBD}/requisicao/.json', data = json_pergunta)

  #verifica se a requisição foi bem sucedida (200)
  return(requisicao.status_code == 200)

def le_alunos():

  requisicao = requests.get(f'{urlBD}/alunos/.json')
  
  return(requisicao)

def get_nome(matricula):
  requisicao = le_alunos()

  matricula = int(matricula)

  for id in requisicao.json():
    if matricula == requisicao.json()[id]["matricula"]:
      return(requisicao.json()[id]["nome"])
    
def comparar_id(matricula):
    requisicao = le_alunos()
    matricula = int(matricula)
    
    for id in requisicao.json():
        if matricula == requisicao.json()[id]['matricula']:
            return matricula
    
    return False
  
def get_id_banco(matricula):
  requisicao = le_alunos()

  id_d = int(matricula)

  for id in requisicao.json():
    if id_d == requisicao.json()[id]['matricula']:
      return(requisicao.json()[id]["id"])