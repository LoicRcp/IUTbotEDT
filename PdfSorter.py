from pdf2image import convert_from_path
from pdf2image import pdfinfo_from_path
import os
from PIL import Image
from pytesseract import *
from dotenv import load_dotenv
import re

load_dotenv(r'./.env')

tesseractPath = os.getenv("tesseractPath")
popplerPath = os.getenv("popplerPath")

if os.name != "posix":
    pytesseract.tesseract_cmd = tesseractPath
else:
    None


def ocr(image):
    sortie = pytesseract.image_to_string(image)

    return sortie.replace('','').replace('\n',' ')

def getTitleInfos(imagePath):
    leftCrop = 50
    topCrop = 40
    rightCrop = 1200
    bottomCrop = 115
    titleInfos = Image.open(imagePath)

    titleInfos = titleInfos.crop((leftCrop, topCrop, rightCrop, bottomCrop))
    titleInfos.save(imagePath, "PNG")

    title = ocr(imagePath)
    print(title)
    return title.replace(" ","").replace("/","_").split("—")


def concatImagesVertically(image1, image2):
    result = Image.new("RGB",(image1.width, image1.height + image2.height))
    result.paste(image1,(0,0))
    result.paste(image2,(0,image1.height))
    return result


def addWatermark(image1):
    watermark = Image.open("watermark.png")
    image1.paste(watermark, (0,0), watermark)
    return image1

def cropForPromos(semaine, jour):

    cropHoraire = (0,114,2284,170)
    cropTitle = (0,0,2284,122)
    cropA1 = (0,189,2284,680)
    cropA2 = (0,680,2284,1100)
    cropAS = (0,1100,2284,1210)
    cropLP = (0,1210,2284,1560)

    pathA1 = rf"./EDT/{semaine}/{jour}/A1"
    pathA2 = rf"./EDT/{semaine}/{jour}/A2"
    pathAS = rf"./EDT/{semaine}/{jour}/AS"
    pathLP = rf"./EDT/{semaine}/{jour}/LP"


    image = Image.open(rf"./EDT/{semaine}/{jour}/{jour}.png")



    for path in [pathA1,pathA2,pathAS,pathLP]:
        try:
            os.mkdir(path, mode=0o777)
        except Exception:
            pass




    horaires = image.crop(cropHoraire)

    concatImagesVertically(image.crop(cropTitle),concatImagesVertically(horaires, image.crop(cropA1))).save(f"{pathA1}/A1.png", "PNG")
    concatImagesVertically(image.crop(cropTitle),concatImagesVertically(horaires, image.crop(cropA2))).save(f"{pathA2}/A2.png", "PNG")
    concatImagesVertically(image.crop(cropTitle),concatImagesVertically(horaires, image.crop(cropAS))).save(f"{pathAS}/AS.png", "PNG")
    concatImagesVertically(image.crop(cropTitle),concatImagesVertically(horaires, image.crop(cropLP))).save(f"{pathLP}/LP.png", "PNG")




def getWeekTotal(semaine):
    for promo in ["A1","A2","AS","LP"]:

        lundi = Image.open(rf"./EDT/{semaine}/lundi/{promo}/{promo}.png")
        mardi = Image.open(rf"./EDT/{semaine}/mardi/{promo}/{promo}.png")
        mercredi = Image.open(rf"./EDT/{semaine}/mercredi/{promo}/{promo}.png")
        jeudi = Image.open(rf"./EDT/{semaine}/jeudi/{promo}/{promo}.png")
        vendredi = Image.open(rf"./EDT/{semaine}/vendredi/{promo}/{promo}.png")
        samedi = Image.open(rf"./EDT/{semaine}/samedi/{promo}/{promo}.png")

        lm = concatImagesVertically(lundi,mardi)
        mj = concatImagesVertically(mercredi,jeudi)
        vs = concatImagesVertically(vendredi,samedi)

        total = concatImagesVertically(concatImagesVertically(lm,mj),vs)

        total = addWatermark(total)
        total.save(rf"./EDT/{semaine}/{promo}Total.png")




def pdfConvert(edtPath):
    if os.name != "posix":
        info = pdfinfo_from_path(edtPath, userpw=None, poppler_path=popplerPath)
    else:
        info = pdfinfo_from_path(edtPath, userpw=None)

    maxPages = info["Pages"]
    images = []
    for page in range(1, maxPages + 1, 10):
        if os.name != "posix":
            images += (convert_from_path(edtPath,dpi=200,first_page=page,last_page=min(page+10-1,maxPages), poppler_path=r'E:\GamesHDD\poppler-20.11.0\bin'))
        else:
            images += (convert_from_path(edtPath,dpi=200,first_page=page,last_page=min(page+10-1,maxPages)))


    for i, image in enumerate(images):
        if i%7 != 0:


            image.save(rf"./EDT/Temp/{i}.png", "PNG")
            titre = getTitleInfos(rf"./EDT/Temp/{i}.png")

            temp = re.compile("([a-zA-Z]+)([0-9]+)")
            titre[1] = temp.match(titre[1]).groups()[0].lower()
            titre[0] = titre[0].lower()

            path = rf"./EDT/{titre[0].lower()}/{titre[1]}"


            print(path)
            try:
                os.makedirs(path, 0o777)
                os.chmod(path, 0o777)
            except FileExistsError:
                None

            image = addWatermark(image)
            image.save(rf"./EDT/{titre[0]}/{titre[1]}/{titre[1]}.png", "PNG")
            cropForPromos(titre[0],titre[1])

            if i%7 == 6:
                getWeekTotal(titre[0])


    print("---pdfConvert: OK---")