from flask import Flask, request
import requests
import json
from twilio.twiml.messaging_response import MessagingResponse
from googletrans import Translator

app = Flask(__name__)

@app.route("/")
def hello():
    return "Status Online"

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '')
    #print(incoming_msg)
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    
    if 'Start' in incoming_msg:
        text = f'*SELAMAT DATANG* \n\n*Admin :*\n\n📞 : 089608362721 \n\n🚀 *Fitur* \n\n✅ _Youtube Downloader_ \n✅ _Facebook Downloader_ \n✅ _Instagram Downloader_ \n✅ _Google Search_ \n✅ _Text To Speech_ \n✅ _Stalking Profil Instagram_ \n✅ _Translate_ \n\n\n*Untuk Menampilkan Command Ketik Menu*'
        msg.body(text)
        responded = True
    if 'info covid' in incoming_msg or 'Info covid' in incoming_msg:
        import requests as r, json
        req = r.get('https://coronavirus-19-api.herokuapp.com/countries/indonesia')
        reqq = r.get('https://coronavirus-19-api.herokuapp.com/countries/world')
        jss = reqq.json()
        js = req.json()
        text = f'*--- Data Covid-19 Indonesia ---*\n\n*Terkonfirmasi :* *{js["cases"]} Orang* \n*Kasus Hari Ini :* *{js["todayCases"]} Orang* \n*Dalam Perawatan :* *{js["active"]} Orang* \n*Sembuh :* *{js["recovered"]} Orang* \n*Meninggal :* *{js["deaths"]} Orang* \n\n*--- Data Covid-19 Global ---* \n\n*Terkonfirmasi :* *{jss["cases"]} Orang* \n*Kasus Hari Ini :* *{jss["todayCases"]} Orang* \n*Dalam Perawatan :* *{js["active"]} Orang* \n*Sembuh :* *{jss["recovered"]} Orang* \n*Meninggal :* *{jss["deaths"]} Orang*'
        msg.body(text)
        responded = True
    
    if 'Menu' in incoming_msg or 'menu' in incoming_msg:
        text = f'*PERINTAH BOT :*  \n\n*1. info covid* (Informasi Coronavirus) \n\n*2. /JS* <kota> Jadwal Sholat  \n\n*3. /SY* <url> : Youtube Search\n\n*4. /YT* <url> : Youtube Downloader\n\n*5. /FB* <url> : Facebook Downloader\n\n*6. /IG* _<url>_ : Instagram Downloader\n\n*7. /FL* <url> : Download Video Fb Ukuran BIG\n\n*8. /GL* _<query>_ : Google Search\n\n*9. /SG* _<usrname>_ : Get Info Instagram\n\n*10. /TTS* <Text> : Text To Speech\n\n*11. /TR-id-en* <text> : Translate ID > ENG\n\n*12. /TR-en-id* <text> : Translate ENG > ID\n\n*13. /TR-id-kor* <text> : Translate ID > Korea\n\n*14. /C* : Cek Cuaca Lokasi Kamu\n\n*15. /TR-kor-id* <text> : Translate Korea > ID\n\n'
        msg.body(text)
        responded = True
        
    if '/FB' in incoming_msg:
        import requests as r
        import re
        par = incoming_msg[3:]
        html = r.get(par)
        video_url = re.search('sd_src:"(.+?)"', html.text).group(1)
        msg.media(video_url)
        responded = True
    
    if '/IG' in incoming_msg:
        import requests as r
        par = incoming_msg[3:]
        a = r.get(par+'?__a=1')
        b = a.json()
        c = b['graphql']['shortcode_media']
        d = (c['video_url']) 
        msg.media(d)
        responded = True  
        
    if '/GL' in incoming_msg:
        from googlesearch import search
        query = incoming_msg[3:]
        for i in search(query, tld="com", num=10, stop=10, pause=2):
            text = f'==========Results==========\n\n *Reff* : '+i
            msg.body(text)
            responded = True
            
    if '/TR-en-id' in incoming_msg:
        par = incoming_msg[9:]
        translator = Translator()
        result = translator.translate(par, src='en', dest='id')
        msg.body(result.text)
        responded = True

    if '/TR-id-en' in incoming_msg:
        par = incoming_msg[9:]
        translator = Translator()
        result = translator.translate(par, src='id', dest='en')
        msg.body(result.text)
        responded = True

    if '/TR-id-kor' in incoming_msg:
        par = incoming_msg[10:]
        translator = Translator()
        result = translator.translate(par, src='id', dest='ko')
        msg.body(result.text)
        responded = True

    if '/TR-kor-id' in incoming_msg:
        par = incoming_msg[10:]
        translator = Translator()
        result = translator.translate(par, src='ko', dest='id')
        msg.body(result.text)
        responded = True

    if '/FL' in incoming_msg:
        import requests as r
        import re
        par = incoming_msg[3:]
        html = r.get(par)
        video_url = re.search('sd_src:"(.+?)"', html.text).group(1)
        reqq = r.get('http://tinyurl.com/api-create.php?url='+video_url)
        msg.body('*VIDEO BERHASIL DI CONVERT*\n\nLINK : ' +reqq.text+'\n\n_Cara Download Lihat Foto Diatas_')
        msg.media('https://user-images.githubusercontent.com/58212770/78709692-47566900-793e-11ea-9b48-69c72f9bec1e.png')
        responded = True
        
    if '/TTS' in incoming_msg:
        par = incoming_msg[5:]
        msg.media('https://api.farzain.com/tts.php?id='+par+'&apikey=l57LMkqcnQTCUNP7BxoTgtcO8&')
        responded = True

    if '/SG' in incoming_msg:
        import requests 
        import json
        par = incoming_msg[4:]
        p = requests.get('http://api.farzain.com/ig_profile.php?id='+par+'&apikey=l57LMkqcnQTCUNP7BxoTgtcO8')
        js = p.json()['info']
        ms = (js['profile_pict'])
        jp = p.json()['count']
        text = f'Nama : *{js["full_name"]}* \nUsername : {js["username"]} \nBio : *{js["bio"]}* \nSitus Web : *{js["url_bio"]}* \nPengikut : *{jp["followers"]}* \nMengikuti : *{jp["following"]}* \nTotal Postingan : *{jp["post"]}* '
        msg.body(text)
        msg.media(ms)
        responded = True

    if '/YT' in incoming_msg:
        import pafy
        import requests as r
        par = incoming_msg[4:]
        audio = pafy.new(par)
        gen = audio.getbestaudio(preftype='m4a')
        genn = audio.getbestvideo(preftype='mp4')
        req = r.get('http://tinyurl.com/api-create.php?url='+gen.url)
        popo = r.get('http://tinyurl.com/api-create.php?url='+genn.url)
        msg.body('_=========================_\n\n     _Video Berhasil Diconvert_\n\n_=========================_\n\n''*'+gen.title+'*''\n\n*Link Download Music* :' +req.text+'\n\n*Link Download Video* :' +popo.text)
        responded = True
        
    if '/SY' in incoming_msg:
        import requests as r
        par = incoming_msg[3:]
        req = r.get('http://api.farzain.com/yt_search.php?id='+par+'&apikey=l57LMkqcnQTCUNP7BxoTgtcO8&')
        js = req.json()[1]
        text = f'*Judul* :  _{js["title"]}_ \n\n*Url Video* : _{js["url"]}_\n\n*Video ID* : _{js["videoId"]}\n\n_Note : Jika Ingin Download Video Ini Atau Convert Ke Musik, Salin Link Diatas Dan Gunakan Command /YT_'
        msg.body(text)
        msg.media((js['videoThumbs']))
        responded = True
        
    if '/C' in incoming_msg:
        import requests as r
        import json
        par = incoming_msg[3:]
        req = r.get('http://api.farzain.com/cuaca.php?id='+par+'&apikey=l57LMkqcnQTCUNP7BxoTgtcO8')
        js = req.json()["respon"]
        text = f'*Status Cuaca di tempat Kamu*\n\n*Kota* : {js["tempat"]} \n*Cuaca* : {js["cuaca"]} \n*Suhu* : {js["suhu"]} \n*Kelembapan* : {js["kelembapan"]} \n*Angin* : {js["angin"]} \n\n*Status Cuaca : Clouds = Berawan / Rain = Hujan*'
        msg.body(text)
        responded = True
  
    if  '/JS' in incoming_msg:
        import requests as r
        par = incoming_msg[3:]
        req = r.get('http://api.farzain.com/shalat.php?id='+par+'&apikey=l57LMkqcnQTCUNP7BxoTgtcO8')
        js = req.json()['respon']
        text = f'*Waktu Sholat untuk lokasi Kamu :* \n\n*Subuh*  : {js["shubuh"]} \n*Dzuhur* : {js["dzuhur"]} \n*Ashar*   : {js["ashar"]} \n*Magrib*  : {js["maghrib"]} \n*Isya*  : {js["isya"]}'
        msg.body(text)
        responded = True

    if 'jadwal-imsak' in incoming_msg:
       msg.media('https://user-images.githubusercontent.com/58212770/80048733-35c6b100-853b-11ea-8043-ec0614a40039.jpeg') 
       responded = True

       
    if '!' in incoming_msg:
       import requests as r
       us = incoming_msg[2:]
       import requests
       import json
       url = 'https://wsapi.simsimi.com/190410/talk/'
       body = {
         'utext': us, 
         'lang': 'id',
         'country': ['ID'],
         'atext_bad_prob_max': '0.7'

        }
       headers = {
         'content-type': 'application/json', 
         'x-api-key': 'LKgWy5I-HoG8K0CmpWl.SNncus1UOpwBiA1XAZzA'
         }
       r = requests.post(url, data=json.dumps(body), headers=headers)
       js = r.json()
       msg.body(js['atext'])
       responded = True


    if responded == False:
        msg.body('Mohon maaf kak ada kesalahan di antara Kita.')

    return str(resp)

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
