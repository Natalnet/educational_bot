import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords

# Função para criar o modelo de Bag of Words a partir de uma lista de frases
def create_bag_of_words(phrases_list, max_features=150):
    # Verifica se a lista de frases está vazia e lança um erro em caso positivo
    if not phrases_list:
        raise ValueError("a lista de frases não pode estar vazia.")

    # Cria um objeto CountVectorizer que transforma os textos em vetores de contagem
    cv = CountVectorizer(max_features=max_features)
    
    # Ajusta o modelo CountVectorizer com as frases fornecidas e transforma os textos em uma matriz esparsa(maioria preenchida com zero) de contagens
    X = cv.fit_transform(phrases_list).toarray()
    
    # Retorna a matriz esparsa de contagens e o objeto CountVectorizer treinado
    return X, cv

# Função para converter uma frase em um vetor TF-IDF
def string_to_tfidf(phrase, cv):
    # Verifica se a frase está vazia e lança um erro em caso positivo
    if not phrase:
        raise ValueError("frase não pode estar vazia.")

    # Obtém as palavras (features) aprendidas durante o treinamento do modelo CountVectorizer
    feature_names = cv.get_feature_names_out()
    
    # Usa uma expressão regular para obter todas as palavras da frase em letras minúsculas
    phrase_words = re.findall(r'\b\w+\b', phrase.lower())
    
    # Conta o número de ocorrências de cada palavra da lista de palavras da frase na lista de palavras aprendidas
    tfidf_vector = [phrase_words.count(word) for word in feature_names]
    
    # Retorna o vetor TF-IDF da frase como um array numpy
    return np.array(tfidf_vector)


 # Função para pré-processar o texto removendo caracteres especiais, transformando em letras minúsculas, aplicando stemmer e removendo stopwords
def clear_phrases(text, stemmer, stop_words):

    # Converte o texto em letras minúsculas
    text = text.lower()
    
    # Substitui caracteres não alfabéticos por espaço em branco
    text = re.sub('[^a-zA-Záàâãéèêíïóôõöúçñ]', ' ', text)
    
    # Divide o texto em palavras
    text = text.split()
    
    # Aplica o stemmer em cada palavra da lista de palavras e remove as stopwords
    text = [stemmer.stem(word) for word in text if word not in stop_words]
    
    # Retorna o texto pré-processado como uma string com as palavras juntadas por espaço
    return ' '.join(text)

# Preprocessing setup
stemmer = SnowballStemmer('portuguese')
# Cria um objeto SnowballStemmer para a língua portuguesa (para stemming)

# Cria um conjunto de stopwords para a língua portuguesa

# O código prepara funções para criar um modelo Bag of Words, converter frases em vetores TF-IDF e realizar pré-processamento em texto em português. As funções são projetadas para serem usadas em tarefas de processamento de linguagem natural (PLN), como classificação de texto, análise de sentimento, etc. As funções são úteis para representar textos em formato numérico para aplicação de algoritmos de aprendizado de máquina que requerem entradas numéricas.
pt_stopwords = set(stopwords.words('portuguese'))