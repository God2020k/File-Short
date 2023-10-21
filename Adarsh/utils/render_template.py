from Adarsh.vars import Var
from Adarsh.bot import StreamBot
from Adarsh.utils.human_readable import humanbytes
from Adarsh.utils.file_properties import get_file_ids
from Adarsh.server.exceptions import InvalidHash
import urllib.parse
import aiofiles
import logging
import aiohttp


async def render_page(id, secure_hash):
    file_data = await get_file_ids(StreamBot, int(Var.BIN_CHANNEL), int(id))
    if file_data.unique_id[:6] != secure_hash:
        logging.debug(f'link hash: {secure_hash} - {file_data.unique_id[:6]}')
        logging.debug(f"Invalid hash for message with - ID {id}")
        raise InvalidHash
    src = urllib.parse.urljoin(Var.URL, f'{secure_hash}{str(id)}')
    
    if str(file_data.mime_type.split('/')[0].strip()) == 'video':
        async with aiofiles.open('Adarsh/template/req.html') as r:
            heading = 'Watch {}'.format(file_data.file_name)
            tag = file_data.mime_type.split('/')[0].strip()
            html = (await r.read()).replace('tag', tag) % (heading, file_data.file_name, src)
    elif str(file_data.mime_type.split('/')[0].strip()) == 'audio':
        async with aiofiles.open('Adarsh/template/req.html') as r:
            heading = 'Listen {}'.format(file_data.file_name)
            tag = file_data.mime_type.split('/')[0].strip()
            html = (await r.read()).replace('tag', tag) % (heading, file_data.file_name, src)
    else:
        async with aiofiles.open('Adarsh/template/dl.html') as r:
            async with aiohttp.ClientSession() as s:
                async with s.get(src) as u:
                    heading = 'Download {}'.format(file_data.file_name)
                    file_size = humanbytes(int(u.headers.get('Content-Length')))
                    html = (await r.read()) % (heading, file_data.file_name, src, file_size)
    current_url = f'{Var.URL}/{str(id)}/{file_data.file_name}?hash={secure_hash}'
   html_code = f'''
   <p>
    <center><h5>Click on 👇 button to watch/download in your favorite player</h5></center>
    <center>
        <div onclick="mx_player()" class="card card-body col-lg-3  col-5 bg-dark text-secondary text-center justify-content-center align-items-center hover:shadow-md hover:shadow-gray-400 hover:translate-y-[-5px] transition transition-all duration-300 wow animate__animated animate__fadeInRight">
                                <svg class="wow animate__animated animate__shakeX animate__delay-2s" xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="50" height="50" viewBox="0 0 64 64"><circle cx="32" cy="32" r="28" fill="#ffeb9b"></circle><circle cx="32" cy="32" r="21" fill="#f9dd8f"></circle><path fill="#8d6c9f" d="M32,6c14.336,0,26,11.664,26,26S46.336,58,32,58S6,46.336,6,32S17.664,6,32,6 M32,4	C16.536,4,4,16.536,4,32s12.536,28,28,28s28-12.536,28-28S47.464,4,32,4L32,4z"></path><path fill="#fff8ee" d="M42.5,31.134l-17-9.815c-0.667-0.385-1.5,0.096-1.5,0.866v19.63c0,0.77,0.833,1.251,1.5,0.866 l17-9.815C43.167,32.481,43.167,31.519,42.5,31.134z"></path><path fill="#8d6c9f" d="M25,43.818c-0.344,0-0.688-0.09-1-0.271c-0.626-0.361-1-1.009-1-1.732v-19.63 c0-0.723,0.374-1.371,1-1.732c0.623-0.362,1.371-0.363,2,0l17,9.815v0c0.626,0.361,1,1.009,1,1.732s-0.374,1.371-1,1.732l-17,9.815 C25.687,43.728,25.343,43.818,25,43.818z M25,22.185v19.63L42,32l0.5-0.866L42,32L25,22.185z"></path><g><path fill="#8d6c9f" d="M53.596,37.162c-0.063,0-0.126-0.006-0.189-0.018l-1.964-0.376 c-0.542-0.104-0.897-0.628-0.794-1.17c0.104-0.542,0.627-0.898,1.171-0.793l1.964,0.376c0.542,0.104,0.897,0.628,0.794,1.17 C54.485,36.829,54.066,37.162,53.596,37.162z"></path><path fill="#8d6c9f" d="M51.997,42.133c-0.139,0-0.28-0.029-0.415-0.091l-1.819-0.832 c-0.502-0.229-0.723-0.823-0.493-1.325c0.229-0.501,0.82-0.726,1.325-0.493l1.819,0.832c0.502,0.229,0.723,0.823,0.493,1.325 C52.739,41.916,52.377,42.133,51.997,42.133z"></path><path fill="#8d6c9f" d="M49.278,46.59c-0.216,0-0.435-0.07-0.618-0.214l-1.571-1.237c-0.434-0.342-0.508-0.97-0.167-1.404 c0.343-0.433,0.97-0.51,1.405-0.167l1.571,1.237c0.434,0.342,0.508,0.97,0.167,1.404C49.867,46.459,49.574,46.59,49.278,46.59z"></path><path fill="#8d6c9f" d="M45.591,50.28c-0.296,0-0.589-0.131-0.787-0.381l-1.237-1.571 c-0.341-0.434-0.267-1.063,0.167-1.404c0.436-0.343,1.063-0.266,1.405,0.167l1.237,1.571c0.341,0.434,0.267,1.063-0.167,1.404 C46.025,50.21,45.807,50.28,45.591,50.28z"></path><path fill="#8d6c9f" d="M41.134,52.998c-0.38,0-0.742-0.217-0.91-0.584l-0.832-1.819c-0.229-0.502-0.009-1.096,0.493-1.325 c0.504-0.233,1.096-0.008,1.325,0.493l0.832,1.819c0.229,0.502,0.009,1.096-0.493,1.325 C41.414,52.969,41.272,52.998,41.134,52.998z"></path><path fill="#8d6c9f" d="M36.161,54.595c-0.47,0-0.89-0.333-0.981-0.812l-0.377-1.964c-0.104-0.542,0.252-1.066,0.794-1.17 c0.54-0.105,1.066,0.251,1.171,0.793l0.377,1.964c0.104,0.542-0.252,1.066-0.794,1.17C36.287,54.589,36.224,54.595,36.161,54.595z"></path></g></svg>
                                Mx Player 
                            </div>
      <br>  <div class="col-lg-6 col-10 d-flex justify-center items-center flex-wrap pb-3 gap-2 wow animate__animated animate__fadeIn">
                            <div onclick="vlc_player()" class="card card-body col-lg-3  col-5 bg-dark text-secondary text-center justify-content-center align-items-center hover:shadow-md hover:shadow-gray-400 hover:translate-y-[-5px] transition transition-all duration-300 wow animate__animated animate__fadeInLeft">
                                <svg class="wow animate__animated animate__shakeX  animate__delay-1s" xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="50" height="50" viewBox="0 0 64 64"><linearGradient id="d2lfkA6lemjIH1JdWslHIa_74320_gr1" x1="32" x2="32" y1="16.021" y2="39.25" gradientUnits="userSpaceOnUse" spreadMethod="reflect"><stop offset=".437" stop-color="#6dc7ff"></stop><stop offset="1" stop-color="#e6abff"></stop></linearGradient><path fill="url(#d2lfkA6lemjIH1JdWslHIa_74320_gr1)" d="M32,31.25c2.891,0,5.255-0.323,6.939-0.712l2.409,7.664C37.765,39.116,33.881,39.25,32,39.25 c-1.88,0-5.765-0.134-9.347-1.049l2.408-7.663C26.745,30.927,29.11,31.25,32,31.25z M32.5,24.25c1.554,0,2.999-0.141,4.343-0.38 l-2.429-7.729c-0.587,0.063-1.211,0.109-1.914,0.109c-1.1,0-2.062-0.092-2.876-0.229l-2.404,7.651 C28.816,24.034,30.574,24.25,32.5,24.25z"></path><linearGradient id="d2lfkA6lemjIH1JdWslHIb_74320_gr2" x1="32.105" x2="32.105" y1="7.415" y2="56" gradientUnits="userSpaceOnUse" spreadMethod="reflect"><stop offset="0" stop-color="#1a6dff"></stop><stop offset="1" stop-color="#c822ff"></stop></linearGradient><path fill="url(#d2lfkA6lemjIH1JdWslHIb_74320_gr2)" d="M56.903,50.041l-2.216-10.779c-0.513-2.265-2.52-3.847-4.881-3.847H45.09l-8.059-24.451 c-0.7-2.123-2.726-3.549-5.04-3.549c-2.314,0-4.339,1.426-5.039,3.549l-8.058,24.451h-4.491c-2.362,0-4.369,1.582-4.885,3.866 L7.31,50.021c-0.327,1.442,0.019,2.937,0.947,4.099C9.212,55.314,10.645,56,12.19,56h39.828c1.545,0,2.979-0.685,3.934-1.88 C56.88,52.958,57.226,51.464,56.903,50.041z M19.096,41.19l9.755-29.601c0.429-1.301,1.69-2.175,3.14-2.175s2.711,0.874,3.14,2.175 l9.774,29.655c0.201,0.72,0.088,1.331-0.357,1.923c-1.509,2.001-6.32,3.246-12.557,3.247c-0.004,0-0.007,0-0.011,0 c-6.223,0-11.017-1.229-12.511-3.208C19,42.586,18.886,41.933,19.096,41.19z M54.39,52.872C53.816,53.589,52.952,54,52.019,54H12.19 c-0.934,0-1.798-0.411-2.371-1.128C9.39,52.334,9.181,51.677,9.202,51H17v-2H9.561l0.411-2H14v-2h-3.616l1.089-5.297 c0.3-1.326,1.532-2.288,2.93-2.288h3.832l-1.05,3.188c-0.392,1.376-0.154,2.693,0.689,3.81c1.921,2.544,7.062,4.003,14.106,4.003 c0.003,0,0.008,0,0.011,0c7.06-0.002,12.219-1.476,14.153-4.044c0.823-1.093,1.058-2.37,0.678-3.694 c-0.003-0.013-0.007-0.025-0.011-0.038l-1.062-3.224h4.058c1.397,0,2.63,0.962,2.926,2.269L53.825,45H50v2h4.236l0.411,2H47v2h8.008 C55.029,51.671,54.821,52.332,54.39,52.872z"></path></svg> 
                                VLC Player <br>
                         <br>   </div>    
                          <div onclick="playit_player()" class="card card-body col-lg-3  col-5 bg-dark text-secondary text-center justify-content-center align-items-center hover:shadow-md hover:shadow-gray-400 hover:translate-y-[-5px] transition transition-all duration-300 wow animate__animated animate__fadeInLeft">
                                <svg class="wow animate__animated animate__shakeX  animate__delay-1s " xmlns="http://www.w3.org/2000/svg" width="50" height="50" viewBox="0 0 48 48" id="b"><defs><style>.c{fill:none;stroke:#22abbd;stroke-linecap:round;stroke-linejoin:round;}</style></defs><path class="c" d="m17,32.5v5c0,2.7614-2.2386,5-5,5h0c-2.7614,0-5-2.2386-5-5"/><path class="c" d="m7,37.5c0-2.7614,2.2386-5,5-5h25c2.2,0,4-1.8,4-4V9.5c0-2.2-1.8-4-4-4H11c-2.2,0-4,1.8-4,4v28"/><path class="c" d="m29.1876,18.467l-9.1448-5.2652c-.822-.4733-1.8482.12-1.8482,1.0685v10.5304c0,.9485,1.0262,1.5418,1.8482,1.0685l9.1448-5.2652c.8237-.4742.8237-1.6628,0-2.137Z"/></svg>
                                Play-it <br>
                      <br>      </div>
       
    </center>
</p>
</p>
<center>
    <h2>
        <a href="https://telegram.dog/+kc6bYRCsWdlhOTI1">
            <img src="https://graph.org/file/b57cdba982191a25db535.jpg" alt="Rkbotz" width="150" height="75">
        </a>
    </h2>
</center>

'''

html += html_code    
    return html
