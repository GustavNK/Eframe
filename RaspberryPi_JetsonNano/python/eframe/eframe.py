#!/usr/bin/python
# -*- coding:utf-8 -*-

# TODO
# - Update when things change online
import sys
import os
import logging
import time
import traceback
from PIL import Image,ImageDraw,ImageFont
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd4in2
import cal
import trello
import sketcher

MIN_5 = 60 * 5

token = "token.pkl"

logging.basicConfig(level=logging.DEBUG)

try:
    # Setup
    logging.info("Setting up")

    logging.info("Init and Clear")
    epd = epd4in2.EPD()
    epd.init()
    epd.Clear()

    Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)

    logging.info("Getting initial Trello cards")
    cards_list = trello.getTrelloCards()

    logging.info("Getting initial Calendar")
    events_list = cal.getEventList(token)
    
    logging.info("Drawing Eframe")
    sketcher.drawEframe(events_list, cards_list, draw)
    epd.display(epd.getbuffer(Himage))

    old_cards_list = cards_list
    old_events_list = events_list
    
    
    while(True):
        logging.info("Getting new Trello Cards")
        cards_list = trello.getTrelloCards()

        logging.info("Getting new Calendar")
        events_list = cal.getEventList(token) 

        if (old_cards_list != cards_list or old_events_list != events_list):
            logging.info("---Drawing new Eframe")
            epd.Clear()
            sketcher.drawEframe(events_list, cards_list, draw)
            epd.display(epd.getbuffer(Himage))

            old_events_list = events_list
            old_cards_list = cards_list

        time.sleep(MIN_5)

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


