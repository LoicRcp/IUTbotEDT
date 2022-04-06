import imaplib
import email
import os
import time
import logging
import PdfSorter
from dotenv import load_dotenv


logging.basicConfig(format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.INFO,
                    filename="EdtScrapper.log")

logger = logging.getLogger("EdtScrapper")



load_dotenv(r'./.env')

username = os.getenv('Mail')
password = os.getenv('Pass')



def checkMails():
    logging.info("\n------------\nINIT\n------------")

    counter = 0
    imap = imaplib.IMAP4_SSL(
        'imap.gmail.com')  # On créer une classe IMAP avec SSL, pour l'adresse gmail (cf: https://www.systoolsgroup.com/imap/)
    imap.login(username, password)

    folder = imap.select("INBOX")  # On choisi la catégorie "Boite de récéption" de la boite mail

    while True:
        try:
            imap.close()
            imap.logout()

        except:
            None
        time.sleep(1)
        imap = imaplib.IMAP4_SSL(
            'imap.gmail.com')  # On créer une classe IMAP avec SSL, pour l'adresse gmail (cf: https://www.systoolsgroup.com/imap/)
        imap.login(username, password)
        imap.select("INBOX")  # On choisi la catégorie "Boite de récéption" de la boite mail
        try:
            if counter % 300 == 0 and counter != 0:
                imap.close()
                imap.logout()

                time.sleep(20)
                imap = imaplib.IMAP4_SSL(
                    'imap.gmail.com')  # On créer une classe IMAP avec SSL, pour l'adresse gmail (cf: https://www.systoolsgroup.com/imap/)
                imap.login(username, password)
                imap.select("INBOX")  # On choisi la catégorie "Boite de récéption" de la boite mail

            type, data = imap.search(None, 'UNSEEN') #On selectionne uniquement les mails non-lu, mails est un tuple avec les identifiants des mails.
            mail_ids = data[0]
            id_list = mail_ids.split()

            for num in data[0].split():
                typ, data = imap.fetch(num, '(RFC822)')
                raw_email = data[0][1]

                # converts byte literal to string removing b''
                raw_email_string = raw_email.decode('utf-8')
                email_message = email.message_from_string(raw_email_string)


                # downloading attachments
                for part in email_message.walk():
                    # this part comes from the snipped I don't understand yet...
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue

                    fileName = part.get_filename()

                    if (fileName != None) and ("semaine" in fileName.lower()):
                        fileName = fileName.replace('\r','').replace('\n','')
                        logging.info(f"Nouvel EDT trouvé: {fileName}")
                        fp = open(rf"./EDT/{fileName}.pdf", 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()
                        PdfSorter.pdfConvert(rf"./EDT/{fileName}.pdf")


            else:
                print("No new mails :( -",counter)
            time.sleep(60)
            counter+=1
        except Exception as e:
            print(e)
            continue


checkMails()