#!/usr/bin/python
# -*- coding:utf-8 -*-

# TODO
# - Update when things change online

import sys
import os
import logging
from datetime import datetime, timedelta
import time
import traceback
from PIL import Image,ImageDraw,ImageFont
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd4in2
import cal
import trello

logging.basicConfig(level=logging.DEBUG)

def drawEframe(events_list, cards, draw):
    # start top left(left-> rigt, top -> bot) (max 400, 300)
    #draw grid
    grid_x = 170
    grid_y = 70

    draw.line((grid_x, 0, grid_x, 300), fill = 0)
    draw.line((0, grid_y, 170, grid_y), fill = 0)
    #draw date
    draw.text((20,10), today, font=font24, fill = 0)
    draw.text((60, 40), today_weekday, font=font18, fill = 0)
    # draw Trello
    draw.text((235,10), "Min TODO", font=font24, fill = 0)
    draw.line((240, 40, 340, 40), fill = 0)

    trello_y = grid_y - 20
    trello_x = grid_x + 3

    for card in cards:
        print(len(card.name))
        if(len(card.name) < 23):
            draw.text((trello_x, trello_y), "- " + card.name, font = font18, fill = 0)
        else:
            string = trello.splitName(card)
            draw.text((trello_x, trello_y), "- " + string[0], font = font18, fill = 0)
            trello_y += 20
            draw.text((trello_x, trello_y), "  " + string[1], font = font18, fill = 0)
        trello_y += 30
    # draw Calendar
    cal_x = 10
    cal_y = grid_y + 4
    
    count = 0
    for event in events_list:
        event.summary = (event.summary[0:16] + "..") if len(event.summary) > 18 else event.summary
        
        draw.text((cal_x, cal_y), event.summary, font = font18, fill = 0)
        cal_y += 20
        draw.text((cal_x, cal_y), event.start_datetime.strftime("%d-%m"), font = font14, fill = 0)
        cal_y += 20
        
        count += count + 1
        if (count > 5):
            break

    epd.display(epd.getbuffer(Himage))



try:
    # Setup
    logging.info("Setting up")
    
    weekday = ["Søn", "Man", "Tirs", "Ons", "Tors", "Fre", "Lør"]
    today = datetime.now().strftime("%Y-%m-%d")
    today_weekday = weekday[int(datetime.now().strftime("%w"))]
    min5 = 60 * 5
      
    logging.info("init and Clear")
    epd = epd4in2.EPD()
    epd.init()
    epd.Clear()

    font14 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 14)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)

    Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)

    # Get online
    logging.info("Setting up online")

    cards = trello.getTrelloCards()
    old_cards = cards

    my_calendar = cal.getGoogleCalendar()
    events_list = cal.getCommingEventsList(my_calendar) 
    old_events_list = cards

    drawEframe(events_list, cards, draw)

    while(False):
        cards = trello.getTrelloCards()

        my_calendar = cal.getGoogleCalendar()
        events_list = cal.getCommingEventsList(my_calendar) 

        if (old_cards == cards or old_events_list == events_list):
            logging.info("Drawing new board")
            drawEframe(events_list, cards, draw)
            old_events_list = events_list
            old_cards = cards
        print("no")
        time.sleep(5)

    if(False):
        epd.Clear()
        logging.info("Goto Sleep...")
        epd.sleep()
        time.sleep(3)
        epd.Dev_exit()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd4in2.epdconfig.module_exit()
    exit()


