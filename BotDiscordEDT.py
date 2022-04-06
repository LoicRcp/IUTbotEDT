import discord
import os
import datetime
from PIL import Image
from io import BytesIO
import logging
from dotenv import load_dotenv
import random
load_dotenv(r'./.env')




logging.basicConfig(format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.INFO,
                    filename="EdtBotLogs.log")

logger = logging.getLogger("EdtBotLogs")



client = discord.Client()

botToken = os.getenv('botToken')

jours = ["lundi","mardi","mercredi","jeudi","vendredi","samedi", "dimanche"]
promos = ["A1","A2","AS","LP"]




@client.event
async def on_ready():
    global botReady
    botReady = True
    print("Bot ready !")

@client.event
async def on_message(message):
    if message.content.startswith("!edthelp"):
        helpmess = """```Aide pour les commandes du bot EDT:
        
        !edt (numSemaine) (jour) (promo)
        
        LES ARGUMENTS SONT OPTIONNELS
        Le bot est capable de déterminer quel semaine on est, quel jour, et dans quelle promo vous êtes.
        
        numSemaine: Affiche la semaine correspondante au numéro - 0:56
        Jour: Affiche le jour correspondant - [lundi, mardi, mercredi, jeudi, vendredi, samedi]
        promo: Affiche l'emploi du temps de la promo en question - [A1, A2, AS, LP]
        
        
        
        Exemples:
        
        !edt
        !edt 36 mardi A1
        !edt mercredi A2
        !edt LP
        etc...
        ```
        """

        await message.channel.send(helpmess)

    elif message.content.startswith("!edt"):
        logging.info(f"{message.author.name} requested '{message.content}'")
        messageText = message.content.split(" ")
        try:
            for role in message.author.roles:
                if role.name.split("-")[0].upper() in promos:
                    promo = role.name.split("-")[0]
            semaine = datetime.datetime.now().isocalendar()[1]
        except Exception as e:
            logging.info(f"Error with {message.author.name}: {e}")
        try:
            if datetime.datetime.now().isocalendar()[2] == 7:
                semaine+=1
        except Exception as e:
            logging.info(f"Error with {message.author.name}: {e}")
        try:
            if datetime.datetime.now().isocalendar()[2] == 7:
                jour = jours[0]
            elif (int(datetime.datetime.now().hour) >= 20):
                jour = jours[datetime.datetime.now().isocalendar()[2]]
            else:
                jour = jours[datetime.datetime.now().isocalendar()[2] - 1]
        except Exception as e:
            logging.info(f"Error with {message.author.name}: {e}")

        total = False

        plusCounter = 0
        secretMeme = False
        uwuFilter = False

        # for i in range(len(messageText)):
            # messageText[i] = messageText[i].replace('"', '').replace("'", "")

        for elem in messageText:
            if elem.isnumeric():
                semaine = elem
            if elem.lower() in jours:
                jour = elem
            if elem.upper() in promos:
                promo = elem.upper()
            if "total" in elem.lower():
                total = True
            if "+" in elem.lower():
                plusCounter += elem.lower().count('+')
            if "meme" in elem:
                secretMeme = True
            if "uwu" in elem.lower():
                uwuFilter = True

        if total:
            semaine = str(int(semaine) + int(plusCounter%6))
        else:
            if jour.isnumeric():
                jour = jours[datetime.datetime.now().isocalendar()[2] - 1 + plusCounter%6] 
            else:
                jour = jours[(jours.index(jour) + plusCounter)%6]
            semaine = str(int(semaine)+ int(plusCounter/6))

        print(messageText)
        print(semaine, jour, promo)

        value = random.randrange(1,20)


        if int(semaine) < 10:
            semaine = '0' + semaine

        if secretMeme:



            """
        #if (value == 1 or toz and not total):
            imageNb = random.randrange(1,8)
            with BytesIO() as image_binary:
                bonsoirnon = Image.open(f"./meme/Dormir {imageNb}.jpg")
                bonsoirnon.save(image_binary, "JPEG")
                image_binary.seek(0)
                text = "franchement la flemme..."
                if toz:
                    text = "Il n'y a pas d'EDT le dimanche..."
                await message.channel.send(text,file=discord.File(image_binary, "dormir.jpg"))

            """



            images = os.listdir("./meme/meme/")
            imageName = images[random.randrange(0,len(images))]
            # imageName = "a_lancienne.mp4"
            with BytesIO() as image_binary:
                
                if ("png" in imageName):
                    img = Image.open(f"./meme/meme/{imageName}")
                    img.save(image_binary, "PNG")

                elif ("jpg" in imageName):
                    img = Image.open(f"./meme/meme/{imageName}")
                    img.save(image_binary, "JPEG")

                elif ("mp4") in imageName:

                    print(f"./meme/meme/{imageName}.mp4")

                    await message.channel.send(file=discord.File(f"./meme/meme/{imageName}", "meme.mp4"))
                    return
                image_binary.seek(0)
                # text = "franchement la flemme..."
            
                await message.channel.send(file=discord.File(image_binary, "dormir.jpg"))


        else:
            try:
                if total:

                    print("edtTotal")

                    edt = Image.open(rf"./EDT/semaine{semaine}/{promo}Total.png")
                    if uwuFilter:
                        if promo == "A1":
                            uwuFilter = Image.open(r"./UwuFiltreTotal1A.png")
                        else:
                            uwuFilter = Image.open(r"./UwuFiltreTotal.png")
                        edt.paste(uwuFilter,(0,0),uwuFilter)

                    with BytesIO() as image_binary:
                        edt.save(image_binary, "PNG")
                        image_binary.seek(0)

                        await message.channel.send(file=discord.File(image_binary, "EDT.png"))
                    return

                edt = Image.open(rf"./EDT/semaine{semaine}/{jour}/{promo}/{promo}.png")
                
                if uwuFilter:
                    if promo == "A1":
                        uwuFilter = Image.open(r"./UwuFiltre1A.png")
                    else:
                        uwuFilter = Image.open(r"./UwuFiltre.png")
                    edt.paste(uwuFilter,(0,0),uwuFilter)


                with BytesIO() as image_binary:
                    edt.save(image_binary, "PNG")
                    image_binary.seek(0)
                    

                    await message.channel.send(file=discord.File(image_binary, "EDT.png"))

                    logging.info(f"semaine {semaine} jour {jour} promo {promo} sent to {message.author.name}")
            

            except FileNotFoundError as e:
                print(e)
                with BytesIO() as image_binary:
                    bonsoirnon = Image.open(f"./voyance.jpg")
                    bonsoirnon.save(image_binary, "JPEG")
                    image_binary.seek(0)
                    await message.channel.send("ZirmaVoyance bonsoir que puis-je pour vous... ?",file=discord.File(image_binary, "voyance.jpg"))      




client.run(botToken)
