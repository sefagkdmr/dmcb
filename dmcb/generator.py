# Package: dmcb
from io import BytesIO
from socket import error, herror, gaierror, timeout
from struct import pack
from time import time
import socket
import requests

from PIL import Image, ImageDraw

from dmcb import font, network, get_path




# Parse the background texture
texture = Image.open(get_path('static/texture.png'))
texture = texture.resize((60, 60))
texture = texture.point(lambda p: p * 0.20)


def _repeat(image, pattern):
    ''' Repeat the pattern over the image
    '''
    iw, ih = image.size
    pw, ph = pattern.size
    x = 0
    while x < iw:
        y = 0
        while y < ih:
            image.paste(pattern, (x, y))
            y += ph
        x += pw
    return image


def banner(name, adress, port=25565):
    # Get all info
    server_name = font.parse(name)
    if port != 25565:
        server_adress = font.parse('§8' + adress + '§7:§8' + str(port))
    else:
        server_adress = font.parse('§8' + adress)
    


    try:


        
        
        if port == 19132:
            type = "bedrock"
        else:
            type = "java"
        link = 'http://api.mcstatus.io/v2/status/'+ type +'/' + adress + ':' + str(port)
        global body
        body = requests.get(link, verify=False )
        body = body.json()
        global motd
        global online
        online = body['online']
        online = str(online)
        print("ONLINE MI SERVER HE SOYLE BANA AMK: " +online)
        if online == "False":
            motd = "§4Can't reach this server"
        else: 
            motd = body['motd']['raw']
            motd = str(motd).encode().decode('utf-8')
        

        motd = "§7" + motd
        if '\n' in motd:
            motd = motd.split('\n')
            
        else:
            if len(motd) > 45:
                motd = [motd[:45], motd[45:]]
            else:
                motd = [motd]
                
        
        info = network.get_server_info(adress, port=port)
        players = font.parse('§7' + str(info['players']['online']) +
                             '§8/§7' + str(info['players']['max']))


        if port != 19132:
            ping = parse_ping(info['ping'])
            icon = info['favicon']
        else:
            ping = 0
            icon = None
        if icon is not None:
            icon = Image.open(icon).convert('RGBA')
            icon.load()
        else:
            icon = Image.open(get_path('static/icon.png')).convert('RGBA')

    except (error, herror, gaierror, timeout, AssertionError):

        response = requests.get('https://api.mcsrvstat.us/icon/' + adress)
        img = Image.open(BytesIO(response.content))
        port = str(port)
        if port == "19132" and online == "True":
            info = body
            motd = motd
            players = font.parse('§7' + str(info['players']['online']) +
                                '§8/§7' + str(info['players']['max']))
            ping = 0
            icon = img
        else:
            motd = ["§4Can't reach server"]
            players = []
            icon =Image.open(get_path('static/icon.png')).convert('RGBA')
            ping = -1
    # Create the image, and past the texture on it
    icon_size = 64
    margin = 5
    width = 620
    heigth = icon_size + margin*2
    text_offset = icon_size + margin*2
    text_size = 20
    if icon is None:
        width = width - icon_size - margin
        text_offset = margin

    image = Image.new('RGB', (width, heigth))
    _repeat(image, texture)
    drawer = ImageDraw.Draw(image)

    y_offset = int(margin + (icon_size - text_size*3)/2)
    font.render((text_offset, y_offset), server_name, image)
    font.render((text_offset, y_offset + text_size),
                font.parse(motd[0]), image)
    if len(motd) > 1:
        font.render((text_offset, y_offset + text_size*2),
                    font.parse(motd[1]), image)

    adress_width = font.get_width(server_adress)
    font.render_small((width-margin-adress_width, 60), server_adress, image)

    if icon is not None:
        image.paste(icon, (5, 5), mask=icon)

    render_ping(drawer, (width-margin - 20, margin), ping)

    players_width = font.get_width(players)
    font.render((width-margin-20-margin-players_width, margin), players, image)

    # Save the image to a BytesIO fake file and return it
    mem_file = BytesIO()
    image.save(mem_file, 'PNG')
    del image
    mem_file.seek(0)
    return mem_file


def render_ping(drawer, xy, ping):
    ''' Render the ping to the supplied Drawer object
    '''
    x, y = xy
    black_foreground = (91, 91, 91)
    black_background = (56, 56, 56)
    green_foreground = (0, 255, 33)
    green_background = (0, 135, 15)
    if (ping == 1):
        fills = [green_background, green_foreground, black_background,
                 black_foreground, black_background, black_foreground,
                 black_background, black_foreground, black_background,
                 black_foreground]
    elif (ping == 2):
        fills = [green_background, green_foreground, green_background,
                 green_foreground, black_background, black_foreground,
                 black_background, black_foreground, black_background,
                 black_foreground]
    elif (ping == 3):
        fills = [green_background, green_foreground, green_background,
                 green_foreground, green_background, green_foreground,
                 black_background, black_foreground, black_background,
                 black_foreground]
    elif (ping == 4):
        fills = [green_background, green_foreground, green_background,
                 green_foreground, green_background, green_foreground,
                 green_background, green_foreground, black_background,
                 black_foreground]
    elif (ping == 5):
        fills = [green_background, green_foreground, green_background,
                 green_foreground, green_background, green_foreground,
                 green_background, green_foreground, green_background,
                 green_foreground]
    else:
        fills = [black_background, black_foreground, black_background,
                 black_foreground, black_background, black_foreground,
                 black_background, black_foreground, black_background,
                 black_foreground]

    drawer.rectangle([(x+1*2, y+5*2), (x + 2*2-1, y+7*2-1)], fill=fills[0])
    drawer.rectangle([(x+0*2, y+4*2), (x + 1*2-1, y+6*2-1)], fill=fills[1])
    drawer.rectangle([(x+3*2, y+4*2), (x + 4*2-1, y+7*2-1)], fill=fills[2])
    drawer.rectangle([(x+2*2, y+3*2), (x + 3*2-1, y+6*2-1)], fill=fills[3])
    drawer.rectangle([(x+5*2, y+3*2), (x + 6*2-1, y+7*2-1)], fill=fills[4])
    drawer.rectangle([(x+4*2, y+2*2), (x + 5*2-1, y+6*2-1)], fill=fills[5])
    drawer.rectangle([(x+7*2, y+2*2), (x + 8*2-1, y+7*2-1)], fill=fills[6])
    drawer.rectangle([(x+6*2, y+1*2), (x + 7*2-1, y+6*2-1)], fill=fills[7])
    drawer.rectangle([(x+9*2, y+1*2), (x + 10*2-1, y+7*2-1)], fill=fills[8])
    drawer.rectangle([(x+8*2, y+0*2), (x + 9*2-1, y+6*2-1)], fill=fills[9])

    if(ping == -1):
        fill = (170, 0, 0)
        drawer.line([(x+4, y), (x+10*2-5, y+6*2-1)], fill=fill, width=1)
        drawer.line([(x+3, y), (x+10*2-6, y+6*2-1)], fill=fill, width=1)
        drawer.line([(x+4, y+6*2-1), (x+10*2-5, y)], fill=fill, width=1)
        drawer.line([(x+5, y+6*2-1), (x+10*2-4, y)], fill=fill, width=1)

    # Return the size
    return (9*2-1, 6*2-1)


def parse_ping(ping):
    ''' Parse a ping in ms to a format readable by render_ping
    '''
    if ping > 0 and ping < 150:
        return 5
    elif ping < 300:
        return 4
    elif ping < 600:
        return 3
    elif ping < 1000:
        return 2
    elif ping > 0:
        return 1
    return -1
