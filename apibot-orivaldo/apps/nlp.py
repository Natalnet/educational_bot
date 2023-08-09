import nltk
import numpy as np
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

nltk.download('stopwords')

from apps.api import le_perguntas
from apps.text_processing import clear_phrases, create_bag_of_words, string_to_tfidf

# Função para encontrar o índice da frase mais parecida no bag_of_words ao query_vector
def find_most_similar_index(query_vector, bag_of_words):
    # Cria um array numpy indicando a similaridade da consulta com cada uma das outras frases
    similarities = np.array([np.inner(query_vector, np.array(frase)) for frase in bag_of_words])
    
    # Se a similaridade máxima for zero, significa que nenhuma frase semelhante foi encontrada
    if similarities.max() == 0:
        return None
    
    # Retorna o índice correspondente ao maior valor de similaridade
    return similarities.argmax()

# Função para processar uma determinada pergunta e encontrar uma resposta relevante no conjunto de dados
def npl(pergunta):
    # Assumindo que esta função lê dados contendo perguntas e respostas
    data = le_perguntas()
    
    try:
        # Extrai todas as perguntas e respostas dos dados
        lista_perguntas = [data.json()[id]['pergunta'] for id in data.json() if 'pergunta' in data.json()[id]]
        lista_respostas = [data.json()[id]['resposta'] for id in data.json() if 'resposta' in data.json()[id]]
    except KeyError:
        return "Erro: formato de dados inválido."
    
    # Inicializa um Porter Stemmer e uma lista de stopwords em português
    ps = PorterStemmer()
    all_stopwords = stopwords.words('portuguese') 

    # Preprocess the input question to remove stopwords and perform stemming
    pergunta_limpa = clear_phrases(pergunta, ps, all_stopwords)

    # Crie um saco de palavras (arco) e um vetorizador de contagem (cv) a partir da lista de perguntas (lista perguntas)
    bow, cv = create_bag_of_words(lista_perguntas)

    # Transforme a pergunta de entrada em um vetor TF-IDF (frase vetorial) usando o countvectorizer (cv)
    vetor_frase = string_to_tfidf(pergunta_limpa, cv)

    # Encontre o índice da pergunta mais semelhante no bag_of_words
    index = find_most_similar_index(vetor_frase, bow)

    # Se nenhuma pergunta semelhante for encontrada (semelhança é zero), retorna uma mensagem indicando que nenhuma resposta foi encontrada
    if index is None:
        return "Infelizmente não encontrei nenhuma resposta para sua pergunta!"

    # Caso contrário, retorne a resposta correspondente de lista_respostas
    return lista_respostas[index]