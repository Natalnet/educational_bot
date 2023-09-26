from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from src.nlp import npl
from src.api import cria_log, get_id_resposta, guardar_requisicao, contagem, requisicao_banco, verificar_id, get_resposta, retornar_contagem, guardar_requisicao_erro, comparar_id, get_nome, set_presenca, get_id_banco
import datetime
import json
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="src/templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


class Pergunta(BaseModel): 
    mensagem: str

contador_rep = []


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/pergunta")
def perguntas(pergunta: Pergunta):
    user_respostas = pergunta.mensagem
    resposta = npl(user_respostas)
    id_resposta = get_id_resposta(resposta)
    solict = requisicao_banco(resposta)
    data = datetime.datetime.now()
    
    if resposta == "Infelizmente não encontrei nenhuma resposta para sua pergunta!":    
        cria_log(str(pergunta.mensagem))
        guardar_requisicao_erro(user_respostas, str(data)[0:10:1])
    
    elif solict == None:
        contador = 1
        contador_rep.append(contador)
        id_resposta = get_id_resposta(resposta)
        guardar_requisicao(resposta, id_resposta, str(data)[0:10:1], contador)
    
    elif solict == resposta:
        list = []
        valor = retornar_contagem(resposta)
        list.append(valor)
        contador = list[0] + 1
        id_resposta_banco = verificar_id(resposta)
        contagem(id_resposta_banco, contador)
    
      
    return(resposta)

@app.get("/presenca")
async def registrar_presenca(matricula: int):
    validar = comparar_id(matricula)
    nome = get_nome(matricula)
    aluno_id = get_id_banco(matricula)
    if validar == matricula:
        data = datetime.datetime.now().strftime("%Y-%m-%d")
        set_presenca(data, aluno_id)
        return {"message": f"✅ {nome}, sua presença foi registrada com sucesso!"}
    else:
        return {"message": f"❌ Você não tem permissão para registrar a presença desse usuário!"}
    
