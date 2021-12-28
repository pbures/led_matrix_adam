#!/usr/bin/env python3
import time

import numpy as np
from PIL import Image, ImageDraw
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
#from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

import yfinance as yf

tickers = ['NFLX', 'MSFT', 'ATVI', 'AWAY', 'JETS']

def get_current_price(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    return todays_data['Close'][0]

def show_ticker(device, ticker):
        price=get_current_price(ticker)
        pricestr = "%.1f" % (price)

        show_message(device, "%s:" %(ticker), fill="white", font=proportional(CP437_FONT))
        with canvas(device) as draw:
            text(draw, (2, 0), pricestr, fill="white", font=proportional(CP437_FONT))

def sync_draw(device,loc,fill):
    with canvas(device) as draw:
        draw.point(loc,fill=fill)

## https://pillow.readthedocs.io/en/latest/reference/ImageDraw.html#module-PIL.ImageDraw
## https://luma-core.readthedocs.io/en/latest/intro.html
## https://luma-led-matrix.readthedocs.io/en/latest/intro.html

if __name__ == "__main__":
    try:
        serial = spi(port=0, device=0, gpio=noop())
        device = max7219(serial, cascaded=4, block_orientation=-90, rotate=0, blocks_arranged_in_reverse_order=False)

        start_angle = 0
        end_angle = 360 
        delta = 5
        increment = delta

        for i in range(5000):
            img = Image.new('1', (32,8), color=0)
            draw = ImageDraw.Draw(img)

            draw.pieslice([((i/4) % 24), 0, ((i/4) % 24) + 8, 8], start_angle, end_angle ,fill=1)
            draw.point((((i/4) % 24) + 3, 2), fill=0)

            if start_angle > 90:
                increment = -1 * delta
            if start_angle <= 0:
                increment = delta  

            start_angle = start_angle + increment
            end_angle = end_angle - increment

            img.show()
            device.display(img)
            print("%i .. %i" % (start_angle, end_angle))
            time.sleep(0.01)

        time.sleep(1)

        while True:
            for t in tickers:
                show_ticker(device, t)
                time.sleep(3)

    except KeyboardInterrupt:
        pass
