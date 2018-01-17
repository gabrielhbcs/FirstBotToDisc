import discord
from discord.ext import commands
import asyncio
import random

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='?', description=description)
voice = discord.VoiceClient
client = discord.Client
link = []
tocandoMusica = False
conectado = False
pausado = False
contadorAtual = 0
canceriginando = False


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def botlixo():
    await bot.say(random.choice(['sou dos mesmos criadores do flymunity, oq c esperava? =/',':c',":(((",':((',':(','desguba','disgurba','eu sei que pareço dota 2, diguba','eu fracassei, it wont happen again','eu sou um lixo','me mata pls', 'eu sou um bostinha',':(','não foi intencional']))

@bot.command()
async def roll(dice : str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)

@bot.command(description='Serve para escolher entre opções separadas por vírgulas')
async def choose(*,choices : str):
    """Escolhe dentre várias opções"""
    choices = choices.split(',')
    print(choices)
    await bot.say(random.choice(choices))

@bot.command()
async def concha():
    await bot.say(random.choice(['Sei lá','Tenta de novo mais tarde','nah','lul','nope','talvez','claro','Kappa','sim','talvez algum dia']))

@bot.command(pass_context=True)
async def join(ctx):
    global voice
    global conectado
    try:
        voice = await bot.join_voice_channel(ctx.message.author.voice.voice_channel)
        conectado = True
    except Exception:
        print(Exception)
        await bot.say("Você precisa estar em um canal de voz que eu possa entrar :D")

@bot.command(pass_context=True)
async def leave(ctx):
    global voice
    global conectado
    global tocandoMusica
    global contadorAtual
    try:
        await voice.disconnect()
        conectado = False
        tocandoMusica = False
        contadorAtual = 0
    except Exception:
        voice = await bot.join_voice_channel(ctx.message.author.voice.voice_channel)
        await voice.disconnect()
        conectado = False
        tocandoMusica = False
        contadorAtual = 0

@bot.command(pass_context=True)
async def play(ctx):

    aux = ctx.message.content.split();
    global player
    global link
    global tocandoMusica
    global conectado
    global voice
    link.append(aux[1])
    print(list(link))
    if (not conectado):
        try:
            voice = await bot.join_voice_channel(ctx.message.author.voice.voice_channel)
            conectado = True
        except:
            await bot.say("Você precisa estar em um canal de voz que eu possa entrar :D")
    if(not tocandoMusica):
        await tocar(link[0])

async def tocar(url):
    global client
    global player
    global tocandoMusica
    global conectado
    global link
    global pulando
    global contadorAtual
    player = await voice.create_ytdl_player(url)
    player.start()
    tocandoMusica = True
    while not player.is_done():
        await asyncio.sleep(1)
        contadorAtual += 1
    await pular()
    tocandoMusica = False

async def pular():
    global link
    global pulando
    global tocandoMusica
    global contadorAtual
    contadorAtual = 0
    if (len(link) > 0):
        pulando = False
        await tocar(link[0])
    else:
        tocandoMusica = False

@bot.command(pass_context=True)
async def skip():
    global tocandoMusica
    global player

    link.pop(0)
    if(tocandoMusica):
        player.stop()
        tocandoMusica = False
    else:
        bot.say("Não tenho nada para pular")
    print("Link: "+str(link))

@bot.command(pass_context=True)
async def pause(ctx):
    global pausado
    global player
    if (not pausado):
        player.pause()
        pausado = True
    else:
        await bot.say("Eu não to cantando mano, pra despausar use ?unpause")

@bot.command(pass_context=True)
async def unpause(ctx):
    global pausado
    global player
    if (pausado):
        player.resume()
        pausado = False
    else:
        await bot.say("Já to cantando cara, ta lokão?")

@bot.command(pass_context=True)
async def stop():
    global link
    global player
    global tocandoMusica
    player.stop()
    tocandoMusica = False
    link = []

@bot.command(pass_context=True)
async def debugg():
    global tocandoMusica
    global voice
    global link
    global pausado
    resp = "Tocando: "+str(tocandoMusica) + "\nLista de músicas: " + str(link) + "\nPausado: " + str(pausado)
    await bot.say(resp)

@bot.command(pass_context=True)
async def tocando():
    global tocandoMusica
    global link
    global player
    global contadorAtual
    if (tocandoMusica):
        duracao = player.duration
        duracaoatual = converterTempo(contadorAtual)
        duracaofinal = converterTempo(duracao)
        resp = "Vídeo:\t\t\t\t\t"+str(player.title)+"\nLink:\t\t\t\t\t\t"+str(link[0])+"\nDuração:\t\t\t\t"+str(duracaofinal)+" ( "+str(duracaoatual)+" )"+"\nLikes/Dislikes: \t"+str(player.likes)+"/"+str(player.dislikes)+"\n\nDescrição:\n"+str(player.description)
        await bot.send_message(resp)
    else:
        await bot.say("Não estou tocando nada no momento")

@bot.command(pass_context=True)
async def cherut(ctx):
    resp = ""
    for i in range(random.randint(1,15)):
        resp += "<:cherut:306955740118122497> "
    await bot.say(resp)

def converterTempo(duracao):
    duracaoMin = "00"
    if duracao > 60:
        if (duracao // 60 > 9):
            duracaoSegs = str(duracao % 60)
        else:
            duracaoSegs = "0" + str(duracao % 60)
    else:
        if (duracao > 9):
            duracaoSegs = str(duracao % 60)
        else:
            duracaoSegs = "0" + str(duracao % 60)
    duracao //= 60
    if duracao > 60:
        if (duracao // 60 > 9):
            duracaoMin = str(duracao % 60)
        else:
            duracaoMin = "0" + str(duracao % 60)
    duracao //= 60
    if (duracao > 9):
        duracaofinal = str(duracao) + ":" + duracaoMin + ":" + duracaoSegs
    else:
        duracaofinal = "0"+str(duracao) + ":" + duracaoMin + ":" + duracaoSegs
    return duracaofinal

@bot.command(pass_context=True)
async def roleta(ctx):
    listaMembros = []
    listaMembrosOnline = []
    for member in ctx.message.server.members:
        listaMembros.append(member)
    resp = random.choice(["rip... ","Adivinha qm morreu? ... ","KKKKKKKKK OLHAM QM SE FUDEU ... ","Bah, qm achou diferente? ... "])
    for member in listaMembros:
        if (str(member.status) == "online"):
            listaMembrosOnline.append(member)
    randNumber = random.randint(0,len(listaMembrosOnline) - 1)
    resp += str(listaMembrosOnline[randNumber])
    resp = resp[:-5]
    resp += random.choice([" ...rip"," ...achar diferente era burrice kkkkkkkkk",' ...KKKKKKKKKKKKKK'," ...aiai"])
    await bot.say(resp)

@bot.command()
async def kappa():
    await bot.say("https://i.ytimg.com/vi/NPvAVBZGcGY/maxresdefault.jpg")


@bot.command(pass_context=True)
async def cancer(ctx):
    global voice
    global conectado
    global canceriginando
    if not canceriginando:
        canceriginando = True
        ch = ctx.message.author.voice.voice_channel
        try:
            voice = await bot.join_voice_channel(ch)
            conectado = True
        except Exception:
            print(Exception)
            await bot.say("Você precisa estar em um canal pra eu canceriginar :D")
        await asyncio.sleep(0.2)
        for i in range(random.randint(2,10)):
            if conectado:
                await voice.disconnect()
                conectado = False
                await asyncio.sleep(0.1)
            else:
                voice = await bot.join_voice_channel(ch)
                conectado = True
                await asyncio.sleep(0.1)
        if conectado:
            await voice.disconnect()
            conectado = False
        try:
            await bot.say("não me ban gugu (:")
        except Exception:
            pass
        canceriginando = False
    else:
        await bot.say("lul já to fazendo isso")

bot.run('')

