import os
import sys
from datetime import datetime
from PIL import Image,ImageDraw,ImageFont
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
import trello

weekday = ["Søndag", "Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag"]
today = datetime.now().strftime("%Y-%m-%d")
today_weekday = weekday[int(datetime.now().strftime("%w"))]


font14 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 14)
font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)

def drawEframe(events_list, cards_list, draw):
    # start top left(left-> rigt, top -> bot) (max 400, 300)
    # Draw grid
    grid_x = 170
    grid_y = 70

    draw.line((grid_x, 0, grid_x, 300), fill = 0)
    draw.line((0, grid_y, 170, grid_y), fill = 0)
    
    # Draw date
    draw.text((20,10), today, font=font24, fill = 0)
    draw.text((55, 40), today_weekday, font=font18, fill = 0)
    
    # Draw Trello
    draw.text((235,10), "Min TODO", font=font24, fill = 0)
    draw.line((240, 40, 340, 40), fill = 0)

    trello_y = grid_y - 20
    trello_x = grid_x + 3

    for card in cards_list:
        if(len(card.name) < 23):
            draw.text((trello_x, trello_y), "- " + card.name, font = font18, fill = 0)
        else:
            string = trello.splitName(card)
            draw.text((trello_x, trello_y), "- " + string[0], font = font18, fill = 0)
            trello_y += 20
            draw.text((trello_x, trello_y), "  " + string[1], font = font18, fill = 0)
        trello_y += 30
    
    # Draw Calendar
    cal_x = 10
    cal_y = grid_y + 4
    
    count = 0
    for event in events_list:
        summary = (event.summary[0:16] + "..") if len(event.summary) > 18 else event.summary
        
        draw.text((cal_x, cal_y), summary, font = font18, fill = 0)
        cal_y += 20

        draw.text((cal_x, cal_y), event.start_datetime.strftime("%H:%M - %d/%m"), font = font14, fill = 0)
        
        cal_y += 20

        count += 1
        if (count >= 5):
            break

    