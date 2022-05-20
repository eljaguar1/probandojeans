from pyrogram import Client, types, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ChatPermissions
import asyncio
import os
from pydownloader.downloader import Downloader
from cfg import*
from utils import sizeof_fmt, get_file_size, createID, TGDownloaderProgress
import zipfile
import datos


#Progreso de descarga
async def progress_download(downloader, filename, currentBits, totalBits, speed, args): #, stop=False
    try:
        message = args[0]
        msg = args[1]
        dlinfo = datos.descarga(filename, totalBits, currentBits, speed)
        await message.edit(dlinfo)
    except Exception as ex:
        print(str(ex))
    pass

# Función de descarga
async def ddl(app, msg, message, url, file_name=''):
    downloader = Downloader()
    file = await downloader.download_url(url, progressfunc=progress_download, args=(message, msg))
    if file:
        await process_file(app, msg, message, file)
    else:
        await message.edit('》Error en la descarga :(')


async def process_file(app, msg, message, file):
    await message.edit('》Procesando Archivo(s)...')
    file_size = get_file_size(file)
    max_file_size = 1024 * 1024 * 1999
    file_upload_count = 0
    client = None
    findex = 0
    if file_size > max_file_size:
        #cominfo = datos.cromprimiendo(file,file_size,max_file_size)
        await message.edit('Comprimiendo...')
        zipname = str(file).split('.')[0] + createID()
        mult_file = zipfile.MultiFile(zipname,max_file_size)
        zip = zipfile.ZipFile(mult_file,  mode='w', compression=zipfile.ZIP_DEFLATED)
        zip.write(file)
        zip.close()
        mult_file.close()
        await message.edit('》Enviando a Telegram...')
        await app.send_document(msg.chat.id, open(zipname, 'rb'), caption=msg.caption)
    else:
        await message.edit('》Enviando a Telegram...')
        await app.send_document(msg.chat.id, open(file, 'rb'), caption=msg.caption)
    await message.edit('》Proceso Completo')

async def principal(args):

    app: Client = args[0]
    msg: types.Message = args[1]
   
    message_text = msg.text
    #message = None

    message = await app.send_message(msg.chat.id, '》Procesando...')


    if '/start' in message_text:
        await message.edit(f'Bot para descargas.\n\nEnlaces Soportados:\n\n》URL de descarga Directas.\n》Google Play (no carpetas).\n》MediaFire (no carpetas).')
            
    elif 'http' in message_text:
        url = message_text
        await ddl(app, msg, message ,url, file_name='')
    
    else:
        await message.edit('》Error')


def main():

    print('\nRun...\n')

    tg = Client( 
        "pyro.dl", api_id= API_ID, api_hash= API_HASH, bot_token= TOKEN)

    @tg.on_message(filters.text)
    async def start(app: tg, msg: types.Message):

        await principal(args=(app, msg))


    tg.run()
    #tg.send_message(CHANNEL, "》 @PyroFiles_Bot Se inicio")
    #loop: asyncio.AbstractEventLoop = asyncio.get_event_loop_policy().get_event_loop()
    #loop.run_forever()

if __name__ == '__main__': 
   main()
