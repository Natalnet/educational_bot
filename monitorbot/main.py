import settings
import discord
from discord.ext import commands
import requests
from discord import utils, app_commands, ui
from discord.ext.commands import Context
from re import A
import datetime
from api import get_aluno_id, get_nome, set_presenca, comparar_id, add_id, get_id, reset_id, get_turma, add_resposta, cria_aluno, cria_pergunta, le_logs, deleta_logs, get_log, get_teste, cria_permissao, verificar_permissao, get_frequencia, get_miniteste, consolidar_turma, get_permissao_id, remover_permissao, get_porcentagem_letras, get_total_alunos_responderam, cria_aluno, verificar_info
from colorama import Back, Fore, Style
import time
import os
import json
import xlsxwriter
import typing
import pandas as pd
import random

logger = settings.logging.getLogger('bot')

def run():
    
    intents = discord.Intents.all()
    intents.message_content = True
    
    bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)
    
    @bot.event
    async def on_ready():
        prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
        logger.info(prfx + " 🤖 Bot iniciado com sucesso! " + Fore.YELLOW + bot.user.name)
        logger.info(prfx + " 🤖 ID do bot: " + Fore.YELLOW + str(bot.user.id))
        logger.info(prfx + " 🤖 Versão do Discord: " + Fore.YELLOW + discord.__version__)
        await bot.tree.sync()
          
    @bot.tree.command(name="consolidarturma", description="Consolidar turma no banco de dados.")
    async def consolidarturma(interaction: discord.Interaction, turma: str):
        turma = str(turma)
        id_user = interaction.user.id
        userstring = str(id_user)
        user_comparado = verificar_permissao(userstring)
        if user_comparado == str(id_user):
            consolidar_turma(turma)
            await interaction.response.send_message(f"✅​ Turma {turma} consolidada com sucesso!", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌​ Você não tem permissão para usar esse comando!", ephemeral=True)
            
            
    @bot.event
    async def on_member_remove(member: discord.Member):
    # Esta função é chamada quando um usuário sai do servidor
        guild = member.guild
        canal = discord.utils.get(guild.channels,id=603318662228607018)
        embed = discord.Embed(title=f'Até logo, {member.name}#{member.discriminator} deixou o servidor.', color=0x0000FF)
        embed.set_author(name=member.name, icon_url=member.avatar)
        await canal.send(embed=embed)

    ##603318662228607018
    @bot.event
    async def on_member_join(member: discord.Member):
        guild = member.guild
        canal = discord.utils.get(guild.channels,id=603318662228607018)
        embed = discord.Embed(title=f'Olá {member.name} seja bem-vindo(a) ao servidor de LOP! \nQualquer dúvida use /ajuda \nLembre-se de respeitar as regras do servidor, promovendo um ambiente amigável e construtivo para todos.', color=0x0000FF)
        embed.set_author(name=member.name, icon_url=member.avatar)
        await canal.send(embed=embed)
        
    
    #verifica as informações do usuário informado
    @bot.tree.command(name="userinfo", description="Mostra informações do usuário.")
    async def info(interaction: discord.Interaction, member:discord.Member=None):
        id_user = interaction.user.id
        userstring = str(id_user)
        user_comparado = verificar_permissao(userstring)
        if user_comparado == str(id_user):
            if member == None:
                member = interaction.user
            roles = [role for role in member.roles]
            id = member.id
            nome_verificar, cargo_verificar = verificar_info(id)

            if nome_verificar is None: 
                try:
                    matricula = get_id(id)
                    nome = get_nome(matricula)
                    turma = get_turma(matricula)

                except:
                    matricula = "Não cadastrado"
                    nome = "Não cadastrado"
                    turma = "Não cadastrado"

            else:
                matricula = id
                nome = nome_verificar
                turma = cargo_verificar
            embed = discord.Embed(title="📄 Informações do usuário:", color=0x0000FF, timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=member.avatar)
            embed.add_field(name="🆔 ID:", value=member.id)
            embed.add_field(name="👤 Nome:", value=nome)
            embed.add_field(name="🎓 Matrícula:", value=matricula)
            embed.add_field(name="🏷️ Nick:", value=f"{member.name}#{member.discriminator}")
            embed.add_field(name="🗂️ Turma:", value=turma)
            embed.add_field(name="📅 Criado em:", value=member.created_at.strftime("%#d %B %Y "))
            embed.add_field(name="🚪 Entrou em:", value=member.joined_at.strftime("%a, %#d %B %Y "))
            embed.add_field(name=f"💼 Cargos ({len(roles)})", value=" ".join([role.mention for role in roles]))
            #embed.add_field(name="💤 Status:", value=member.status)
            embed.add_field(name="🤖 Bot:", value=member.bot)
            await interaction.response.send_message(embed=embed)
        
        else:
            await interaction.response.send_message(f"❌​ {interaction.user}, você não tem permissão para usar esse comando!")
    
    
    @bot.tree.command(name="myuser", description="Mostra informações do seu usuário.")
    async def myuser(interaction: discord.Interaction):
        member: discord.Member = None
        member = interaction.user
        roles = [role for role in member.roles]
        id = member.id

        # Try to get information using verificar_info
        nome_verificar, cargo_verificar = verificar_info(id)

        if nome_verificar is None: 
            try:
                matricula = get_id(id)
                nome = get_nome(matricula)
                turma = get_turma(matricula)

            except:
                matricula = "Não cadastrado"
                nome = "Não cadastrado"
                turma = "Não cadastrado"

        else:
            matricula = id
            nome = nome_verificar
            turma = cargo_verificar
            
        embed = discord.Embed(title="📄 Informações do seu usuário:", color=0x0000FF, timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name="🆔 ID:", value=member.id)
        embed.add_field(name="👤 Nome:", value=nome)
        embed.add_field(name="🎓 Matrícula:", value=matricula)
        embed.add_field(name="🏷️ Nick:", value=f"{member.name}#{member.discriminator}")
        embed.add_field(name="🗂️ Turma:", value=turma)
        embed.add_field(name="📅 Criado em:", value=member.created_at.strftime("%#d %B %Y "))
        embed.add_field(name="🚪 Entrou em:", value=member.joined_at.strftime("%a, %#d %B %Y "))
        #embed.add_field(name=f"Cargos ({len(roles)})", value=" ".join([role.mention for role in roles]))
        #embed.add_field(name="Status:", value=member.status)
        embed.add_field(name="🤖 Bot:", value=member.bot)
        await interaction.response.send_message(embed=embed)
    
    # classe para mostrar os botões do miniteste.   
    class ButtonsFor(discord.ui.View):
        def __init__(self, nome):
            super().__init__(timeout=None)
            self.respondido = False
            self.nome_miniteste = nome
        @discord.ui.button(label="A", style=discord.ButtonStyle.blurple, custom_id="9")
        async def miniteste9(self, interaction: discord.Interaction, Button: discord.ui.Button, member:discord.Member=None):
            if member == None:
                member = interaction.user
            if not self.respondido:
                self.respondido = True
                id = member.id
                matricula = get_id(id)
                puxar_aluno = get_aluno_id(matricula)
                add_resposta(puxar_aluno, self.nome_miniteste, 'A')
                await interaction.response.send_message(content=f"{member.name} sua respotas foi registrada! 🔹")
            else:
                await interaction.response.send_message(content=f"{member.name} sua respotas ja foi registrada! 🔺")
    
        @discord.ui.button(label="B", style=discord.ButtonStyle.blurple, custom_id="10")
        async def miniteste10(self, interaction: discord.Interaction, Button: discord.ui.Button, member:discord.Member=None):
            if member == None:
                member = interaction.user
            if not self.respondido:
                self.respondido = True
                id = member.id
                matricula = get_id(id)
                puxar_aluno = get_aluno_id(matricula)
                add_resposta(puxar_aluno, self.nome_miniteste, 'B')
                await interaction.response.send_message(content=f"{member.name} sua respotas foi registrada! 🔹")
            else:
                await interaction.response.send_message(content=f"{member.name} sua respotas ja foi registrada! 🔺")
    
        @discord.ui.button(label="C", style=discord.ButtonStyle.blurple, custom_id="11")
        async def miniteste11(self, interaction: discord.Interaction, Button: discord.ui.Button, member:discord.Member=None):
            if member == None:
                member = interaction.user
            if not self.respondido:
                self.respondido = True
                id = member.id
                matricula = get_id(id)
                puxar_aluno = get_aluno_id(matricula)
                add_resposta(puxar_aluno, self.nome_miniteste, 'C')
                await interaction.response.send_message(content=f"{member.name} sua respotas foi registrada! 🔹")
            else:
                await interaction.response.send_message(content=f"{member.name} sua respotas ja foi registrada! 🔺")
        
        @discord.ui.button(label="D", style=discord.ButtonStyle.blurple, custom_id="12")
        async def miniteste12(self, interaction: discord.Interaction, Button: discord.ui.Button, member:discord.Member=None):
            if member == None:
                member = interaction.user
            if not self.respondido:
                self.respondido = True
                id = member.id
                matricula = get_id(id)
                puxar_aluno = get_aluno_id(matricula)
                add_resposta(puxar_aluno, self.nome_miniteste, 'D')
                await interaction.response.send_message(content=f"{member.name} sua respotas foi registrada! 🔹")
            else:
                await interaction.response.send_message(content=f"{member.name} sua respotas ja foi registrada! 🔺")
    
    # função que chama a classe e apresenta o miniteste3.
    @bot.tree.command(name="miniteste", description="Teste de conhecimento!")
    async def miniteste(interaction: discord.Interaction, message: str):

        teste = get_teste(message)

        respostas = ""

        if(teste != None):
            for item in teste['resposta'].values():
                respostas = respostas + item + '\n'
            embed2 = discord.Embed(title=teste['pergunta'], description=respostas, color=0x0000FF)
            await interaction.response.send_message(embed=embed2, view=ButtonsFor("T"+message))
        else:
            await interaction.response.send_message(content=f"{interaction.user} este teste não existe, digite um teste válido!")
    
    
    # classe para mostrar os botões das redes sociais.   
    class ButtonsTwo(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
        @discord.ui.button(label="Youtube", style=discord.ButtonStyle.red, custom_id="5")
        async def redes1(self, interaction: discord.Interaction, Button: discord.ui.Button):
            await interaction.response.send_message(content="Canal do professor: https://www.youtube.com/@orivaldo 🟥")
        
        @discord.ui.button(label="Email", style=discord.ButtonStyle.blurple, custom_id="6")
        async def redes2(self, interaction: discord.Interaction, Button: discord.ui.Button):
            await interaction.response.send_message(content="Email do professor: orivaldo@gmail.com 📨")
        
        @discord.ui.button(label="Github", style=discord.ButtonStyle.green, custom_id="7")
        async def redes3(self, interaction: discord.Interaction, Button: discord.ui.Button):
            await interaction.response.send_message(content="Github do professor: https://github.com/orivaldosantana/ECT2203LoP 🐱‍👤")
    
    # função que chama a classe e apresenta a redes sociais do professor.    
    @bot.tree.command(name="redes", description="Redes sociais do professor!")
    async def redes(interaction: discord.Interaction):
        embed4 = discord.Embed(title="Aqui estão as redes sociais do professor Orivaldo!", color=0x0000FF)
        await interaction.response.send_message(embed=embed4, view=ButtonsTwo())

    
    # função pergunta.
    @bot.command()
    async def pergunta(ctx, *, input_mensagem=''):
        input_mensagem = ctx.message.content
        input_mensagem = input_mensagem.replace("!pergunta", '')

        r = requests.post('http://apibot.orivaldo.net:8000/pergunta', json={
        "mensagem": input_mensagem
    })
        await ctx.send(f"Olá ***{ctx.author.name}*** achamos essa resposta para você,\n{r.json()}")
    
    # função para cadastrar o id do discord ao usuário no banco de dados. ex: /cadastrar matricula
    @bot.tree.command(description="Cadastrar a matricula do aluno no banco de dados!")
    async def cadastrar(interaction: discord.Interaction, matricula: str):
        id = str(interaction.user.id)
        aluno_id = get_aluno_id(matricula)
        validar = comparar_id(matricula)
        nome = get_nome(matricula)
        if validar == 0 or validar == None or validar == "0":
            add_id(aluno_id, id)
            await interaction.response.send_message(f"✅​ {nome}, seu id foi registrada com sucesso!")
        else:
            await interaction.response.send_message(f"❌​ {interaction.user}, você não tem permissão para registrar o id desse usuário!")
    
    # função que cadastra a presença do aluno ao banco de dados.
    @bot.command(aliases=['presença'])
    async def presenca(ctx):
        id = str(ctx.author.id)
        matricula = get_id(id)
        validar = comparar_id(matricula)
        aluno_id = get_aluno_id(matricula)
        nome = get_nome(matricula)
        print(id)
        print(validar)
        if validar == matricula:
            data = datetime.datetime.now()
            #data = data.strftime("%d-%x-%y")
            set_presenca(str(data)[0:10:1], aluno_id)
            await ctx.send(f"✅​ {nome}, sua presença foi registrada com sucesso!")
        else:
            await ctx.send(f"❌​ {ctx.author.name}, você não tem permissão para registrar a presença desse usuário!")
    
    # função que reseta o id do usuário no banco de dados. ex: !resetarid matricula
    @bot.tree.command(description="Resetar o id do aluno no banco de dados!")
    async def resetarid(interaction: discord.Interaction, matricula: str):
        id_user = interaction.user.id
        userstring = str(id_user)
        user_comparado = verificar_permissao(userstring)
        if user_comparado == str(id_user):
            aluno_id = get_aluno_id(matricula)
            if matricula != None:
                reset_id(aluno_id)
                await interaction.response.send_message(f"✅​ {interaction.user}, o id do usuário foi resetado com sucesso!")
            else:
                await interaction.response.send_message(f"❌​ {interaction.user}, você não tem permissão para resetar o id desse usuário!")
        else:
            await interaction.response.send_message(f"❌​ {interaction.user}, você não tem permissão para resetar o id desse usuário!")
    
    # função para mostrar os comandos de ajuda.     
    @bot.tree.command(description="Comandos do Bot!")
    async def ajuda(interaction: discord.Interaction):
        embedVar = discord.Embed(title="Comandos", description="Lista de comandos disponíveis para alunos", color="#10DDA7")
        embedVar.add_field(name="/cadastrar {matricula}", value="use esse comando para se cadastrar no banco de dados e poder colocar sua presença", inline=False)
        embedVar.add_field(name="!pergunta", value="o comando utlizado para perguntar algo ao bot, lembrando que mensagens diretas ao bot serão tratadas como perguntas diretamente se não elas não contém um comando específico", inline=False)
        embedVar.add_field(name="!presença", value="use esse comando para registrar sua presença no dia", inline=False)
        embedVar.add_field(name="/miniteste {0-17}", value="Começa um miniteste", inline=False)
        embedVar.add_field(name="/redes", value="o comando mostra a redes sociais do professor Orivaldo", inline=False)
        embedVar.add_field(name="/comandos", value="mostra os comandos para monitores e professores", inline=False)
        await interaction.response.send_message(embed=embedVar)    
    
    # função para mostrar os comandos dos monitores e professores.
    @bot.tree.command(description="Ver os comandos do Bot para Monitor e Professor!")
    async def comandos(interaction: discord.Interaction):
        id_user = interaction.user.id
        userstring = str(id_user)
        user_comparado = verificar_permissao(userstring)
        if user_comparado == str(id_user):
            embedVar = discord.Embed(title="Comandos", description="Lista de comandos disponíveis para Monitores e Professores", color="00FF80")
            embedVar.add_field(name="!pergunta", value="o comando utlizado para perguntar algo ao bot, lembrando que mensagens diretas ao bot serão tratads como perguntas diretamente se não elas não contém um comando específico", inline=False)
            embedVar.add_field(name="/cadastrar {matricula}", value="use esse comando para cadastrar seu id no banco de dados", inline=False)
            embedVar.add_field(name="/resetarid {matricula}", value="use esse comando para resetar o id no banco de dados", inline=False)
            embedVar.add_field(name="!presenca", value="use esse comando para registrar sua presença no dia", inline=False)
            embedVar.add_field(name="/criaraluno", value="o comando cria um aluno no banco de dados", inline=False)
            embedVar.add_field(name="/criapergunta", value="o comando cria uma pergunta e resposta no banco de dados", inline=False)
            embedVar.add_field(name="/responderlog", value="o comando responde um log armazenado no banco de dados e cria uma pergunta e resposta", inline=False)
            embedVar.add_field(name="/puxarlog", value="o comando puxa os log armazenado no banco de dados e cria uma pergunta e resposta", inline=False)
            embedVar.add_field(name="/miniteste", value="Começa um teste sobre Algoritimos", inline=False)
            embedVar.add_field(name="/userinfo", value="o comando mostra informações de determinado membro do servidor", inline=False)
            embedVar.add_field(name="/redes", value="o comando mostra a redes sociais do professor Orivaldo", inline=False)
            embedVar.add_field(name="/darpermissao", value="o comando da permissão para o usuário conseguir usar os comandos do bot", inline=False)
            embedVar.add_field(name="/removerpermissao", value="o comando remove a permissão do usuário", inline=False)
            embedVar.add_field(name="/consolidarturma", value="o comando da permissão para consolidar a turma no banco de dados", inline=False)
            embedVar.add_field(name="/resultadominiteste", value="o comando mostra os resultados do miniteste informado", inline=False)
            embedVar.add_field(name="!uparturma", value="o comando envia o arquivo com as informações dos alunos para o banco de dados", inline=False)
            await interaction.response.send_message(embed=embedVar)
        else:
            await interaction.response.send_message(f"❌​ {interaction.user}, você não tem permissão para usar esse comando!")
    
    
    # classe de modal para criar um aluno.
    class MyModal(discord.ui.Modal, title="Criar Aluno"):
        nome = discord.ui.TextInput(label="Nome", placeholder="Digite o nome completo do aluno", min_length=1, max_length=100)
        matricula = discord.ui.TextInput(label="Matricula", placeholder="Digite a matrícula do aluno", min_length=1, max_length=100)
        turma = discord.ui.TextInput(label="Turma", placeholder="Digite a turma do aluno", min_length=1, max_length=100)
        
        async def on_submit(self, interaction: discord.Interaction):
            nome = self.nome.value
            matricula = self.matricula.value
            turma = self.turma.value
            cria_aluno(nome, matricula, turma, 0)
            await interaction.response.send_message(f"Aluno {nome} criado com sucesso! ✅​", ephemeral=True)
    
    # função que chama a classe e mostra o modal para criar o aluno no banco de dados.    
    @bot.tree.command(description="Cria um aluno no banco de dados")
    async def criaraluno(interaction: discord.Interaction):
        id_user = interaction.user.id
        userstring = str(id_user)
        user_comparado = verificar_permissao(userstring)
        if user_comparado == str(id_user):
            mymodal = MyModal()
            await interaction.response.send_modal(mymodal)
        else:
            await interaction.response.send_message(f"❌​ {interaction.user}, você não tem permissão para usar esse comando!")
            
    
    # classe de modal para criar pergunta.
    class MyModalP(discord.ui.Modal, title="Criar Pergunta"):
        pergunta = discord.ui.TextInput(label="Pergunta", placeholder="Digite a pergunta", min_length=1, max_length=100)
        resposta = discord.ui.TextInput(label="Resposta", placeholder="Digite a resposta", min_length=1, max_length=100)
        
        async def on_submit(self, interaction: discord.Interaction):
            perguntas = self.pergunta.value
            respostas = self.resposta.value
            cria_pergunta(perguntas, respostas)
            await interaction.response.send_message(f"Pergunta <{perguntas}> criada com sucesso! ✅​", ephemeral=True)
    
    # função que chama a classe e mostra o modal para criar pergunta no banco de dados.      
    @bot.tree.command(description="Cria uma pergunta e resposta no banco de dados")
    async def criarpergunta(interaction: discord.Interaction):
        id_user = interaction.user.id
        userstring = str(id_user)
        user_comparado = verificar_permissao(userstring)
        if user_comparado == str(id_user):
            mymodal = MyModalP()
            await interaction.response.send_modal(mymodal)
        else:
            await interaction.response.send_message(f"❌​ {interaction.user}, você não tem permissão para usar esse comando!")
        
    @bot.tree.command(description="Baixa a presença dos alunos")
    async def baixarpresenca(interaction: discord.Interaction):
        id_user = interaction.user.id
        userstring = str(id_user)
        user_comparado = verificar_permissao(userstring)
        if user_comparado == str(id_user):
            #Faz a requisição das frequências
            freq = get_frequencia()
            
            #cria a lista de dias nos quais foram registradas frequências
            dias = []

            for matricula in freq:
                for dia in freq[matricula]:
                    if dia not in dias:
                        dias.append(dia)

            dias = sorted(dias)

            #Cria a planilha e define o nome da página
            workbook = xlsxwriter.Workbook('presenca.xlsx')
            pag = workbook.add_worksheet(name = 'frequências')

            #imprime o cabeçalho
            pag.write(0, 0, "Aluno")

            for i in range(len(dias)):
                pag.write(0, i+1, dias[i])
            
            #imprime matriculas
            posicao = 1
            for matricula in freq:
                pag.write(posicao, 0, matricula)
                posicao+=1
            
            #preenche tudo com zero

            for i in range(len(dias)):
                for j in range(len(freq)):
                    pag.write(j+1, i+1, 0)

            #imprime as frequencias
            posicao = 1
            for matricula in freq:
                for dia in freq[matricula]:
                    indice = dias.index(dia)
                    pag.write(posicao, indice+1, 1)
                posicao+=1

            workbook.close()

            await interaction.response.send_message('Arquivo xlsx gerado com sucesso.')
            await interaction.response.send_message(file=discord.File('presenca.xlsx'))
            
            os.remove('presenca.xlsx')
        
        else:
            await interaction.response.send_message(f"❌​ {interaction.user}, você não tem permissão para usar esse comando!")
    
    
    # função para puxar os logs de perguntas sem respostas na API.
    @bot.tree.command(description="puxar os logs do banco de dados")
    async def puxarlogs(interaction: discord.Interaction):
        id_user = interaction.user.id
        userstring = str(id_user)
        user_comparado = verificar_permissao(userstring)
        if user_comparado == str(id_user):
            log = le_logs().json()
            logs_json = json.dumps(log, indent=4)
            
            await interaction.response.send_message(logs_json)
        else:
            await interaction.response.send_message(f"❌​ {interaction.user}, você não tem permissão para usar esse comando!")
    
    # classe para responder o log em aberto.
    class MyModalLogs(discord.ui.Modal, title="Responder Logs"):
        pergunta = discord.ui.TextInput(label="Pergunta", placeholder="Digite a pergunta", min_length=1, max_length=100)
        resposta = discord.ui.TextInput(label="Resposta", placeholder="Digite a resposta", min_length=1, max_length=100)
        log_pergunta = discord.ui.TextInput(label="Pergunta do log", placeholder="Digite o id do log", min_length=1, max_length=100)
        log_id = discord.ui.TextInput(label="Id do log (obs: -id)", placeholder="Digite o id do log", min_length=1, max_length=100)
        
        async def on_submit(self, interaction: discord.Interaction):
            perguntas = self.pergunta.value
            respostas = self.resposta.value
            logs_p = self.log_pergunta.value
            logs_id = self.log_id.value

            id_logs = get_log(logs_p)
            if id_logs == logs_id:
                deleta_logs(logs_id)
                cria_pergunta(perguntas, respostas)
                await interaction.response.send_message(f"Log <{logs_id}> respondido com sucesso! ✅​", ephemeral=True)
            else: 
                await interaction.response.send_message(f"Log <{logs_id}> não encontrado! ❌​", ephemeral=True)
    
    # função que chama a classe e mostra o modal para responder os logs no banco de dados.      
    @bot.tree.command(description="Responde os logs do bot em aberto")
    async def responderlog(interaction: discord.Interaction):
        id_user = interaction.user.id
        userstring = str(id_user)
        user_comparado = verificar_permissao(userstring)
        if user_comparado == str(id_user):
            myModalLog = MyModalLogs()
            await interaction.response.send_modal(myModalLog)
        else:
            await interaction.response.send_message(f"❌​ {interaction.user}, você não tem permissão para usar esse comando!")
    
        
    @bot.tree.command(description="Dar permissão para um usuário")
    async def darpermissao(interaction: discord.Interaction, member: discord.Member, cargo: str):
        id_user = interaction.user.id
        userstring = str(id_user)
        user_comparado = verificar_permissao(userstring)
        if user_comparado == str(id_user):
            nome = member.name
            id = member.id
            cargo = cargo.upper()
            cria_permissao(nome, cargo, id)
            await interaction.response.send_message(f"Permissão para {nome} criada com sucesso! ✅​", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌​ {interaction.user}, você não tem permissão para usar esse comando!")
            
    @bot.tree.command(description="Dar permissão para um usuário")
    async def removerpermissao(interaction: discord.Interaction, member: discord.Member):
        id_user = interaction.user.id
        userstring = str(id_user)
        user_comparado = verificar_permissao(userstring)
        if user_comparado == str(id_user):
            nome = member.name
            id_member = member.id
            id_banco = verificar_permissao(str(id_member))
            id_permi = get_permissao_id(id_banco)
            remover_permissao(id_permi)
            await interaction.response.send_message(f"Permissão para {nome} removida com sucesso! ✅​", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌​ {interaction.user}, você não tem permissão para usar esse comando!")
            
    
    #Puxa as informações dos alunos.
    @bot.tree.command(name="veruser", description="Mostra seu perfil no servidor.")
    async def veruser(interaction: discord.Interaction):
        member: discord.Member
        member = interaction.user
        #roles = [role for role in member.roles]
        id = value=member.id
        matricula = get_id(id)
        nome = get_nome(int(matricula))
        turma = get_turma(int(matricula))
        embed = discord.Embed(title="Informações do seu usuário", description=f"Aqui estão as informações do seu usuário.", color=0x0000FF, timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Nome:", value=nome)
        embed.add_field(name="Matrícula:", value=matricula)
        embed.add_field(name="Nick:", value=f"{member.name}#{member.discriminator}")
        embed.add_field(name="Turma:", value=turma)
        embed.add_field(name="Criado em:", value=member.created_at.strftime("%#d %B %Y "))
        embed.add_field(name="Entrou em:", value=member.joined_at.strftime("%a, %#d %B %Y "))
        #embed.add_field(name=f"Cargos ({len(roles)})", value=" ".join([role.mention for role in roles]))
        await interaction.response.send_message(embed=embed)

            
            
    @bot.tree.command(name="resultadominiteste", description="Veja os resultados dos miniteste!")
    async def resultadosminiteste(interaction: discord.Interaction, teste: str):
        vteste = 'T'+teste
        porcentagem = get_porcentagem_letras(vteste)
        total_alunos = get_total_alunos_responderam(vteste)
        teste = get_teste(teste)
        respostas = ""
        id_user = interaction.user.id
        userstring = str(id_user)
        user_comparado = verificar_permissao(userstring)
        if user_comparado == str(id_user):
        
            if(teste != None):
                for chave, item in teste['resposta'].items():
                    respostas = respostas + item + " " + str(porcentagem[chave]) + "%"  + '\n' 
                respostas = respostas + '\n' + "Total de alunos que responderam: " + str(total_alunos)
                embed2 = discord.Embed(title=teste['pergunta'], description=respostas, color=0x0000FF)
                await interaction.response.send_message(embed=embed2)
            else:
                await interaction.response.send_message(content=f"{interaction.user} este teste não existe, digite um teste válido!")
        
        else:
            await interaction.response.send_message(f"❌​ {interaction.user}, você não tem permissão para usar esse comando!")
        
        
        
    @bot.command(name="uparturma", description="Sobe a turma para o banco de dados!")
    async def uparturma(ctx):
        id_user = ctx.author.id
        userstring = str(id_user)
        user_comparado = verificar_permissao(userstring)
        if user_comparado == str(id_user):
            if ctx.message.attachments:
                anexo = ctx.message.attachments[0]
                
                nome_do_arquivo = anexo.filename
                
                await anexo.save(anexo.filename)  # Salva o arquivo localmente
                
                try:
                    planilha = pd.read_csv(anexo.filename)

                    for index, row in planilha.iterrows():
                        nome = row['Nome']
                        matricula = row['Matrícula']
                        turma = row['sub_turma']
                        cria_aluno(nome, matricula, turma)

                    await ctx.send(f"Turma upada com sucesso para o banco de dados: {nome_do_arquivo} ✅​")
                except Exception as e:
                    await ctx.send(f"Ocorreu um erro ao processar o arquivo: {e} ❌")
                
                # Remover o arquivo local após usá-lo
                os.remove(anexo.filename)
            else:
                await ctx.send("Nenhum arquivo anexado.")
        
        else:
            await ctx.send(f"❌​ {ctx.author.mention}, você não tem permissão para usar esse comando!")
    
    # classe para mostrar os botões do miniteste.   
    class ButtonSorteio(discord.ui.View):
        def __init__(self, participantes):
            super().__init__(timeout=None)
            self.respondido = False
            self.participantes = participantes
        @discord.ui.button(label="Participar", style=discord.ButtonStyle.green, custom_id="participar_sorteio")
        async def participar_sorteio(self, interaction: discord.Interaction, Button: discord.ui.Button, member:discord.Member=None):
            if member == None:
                member = interaction.user
            if not self.respondido:
                self.respondido = True
                id = member.id
                if id not in self.participantes:
                    self.participantes.append(id)
                    await interaction.response.send_message(content=f"{member.name} entrou no sorteio! 🎁 ")
            else:
                await interaction.response.send_message(content=f"{member.name} sua respotas ja foi registrada! 🎲")
    
        @discord.ui.button(label="Encerrar", style=discord.ButtonStyle.red, custom_id="encerrar_sorteio")
        async def encerrar_sorteio(self, interaction: discord.Interaction, Button: discord.ui.Button, member:discord.Member=None):
            if member == None:
                member = interaction.user
                id_user = interaction.user.id
                userstring = str(id_user)
                user_comparado = verificar_permissao(userstring)
                if user_comparado == str(id_user):
                    if self.participantes:
                        winner_id = random.choice(self.participantes)
                        winner = await bot.fetch_user(winner_id)
                        await interaction.response.send_message(content=f"O sorteio foi encerrado! O vencedor é: **{winner.mention}** 🏆")
                        self.participants = []
                    else:
                        await interaction.response.send_message(content="Não há participantes no sorteio. 🚫")

                else:
                    await interaction.response.send_message(content=f"{member.name} você não tem permissão para usar esse comando! 🔺")
    
    @bot.tree.command(name="sorteio", description="Realize um sorteio")
    async def sorteio(interaction: discord.Interaction):
        id_user = interaction.user.id
        userstring = str(id_user)
        user_comparado = verificar_permissao(userstring)
        if user_comparado == str(id_user):
            participantes = []
            embedSorteio = discord.Embed(
                title="➡ Sorteio! ⬅",
                description="Clique no botão abaixo para ter a chance de particpiar e ganhar um incrível prêmio! 🍀",
                color=0x0000FF
            )
            await interaction.response.send_message(embed=embedSorteio, view=ButtonSorteio(participantes))
        else:
            await interaction.response.send_message(f"❌​ {interaction.user}, você não tem permissão para usar esse comando!")
        
    bot.run(settings.TOKEN_BOT, root_logger=True)

if __name__ == '__main__':
    run()