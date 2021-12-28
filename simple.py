#!/usr/bin/env python3

# Program je v Pythonu3
# Pusti se primo na rpi jednoduse na prikazovem radku v adresari kde je program napsany:
# ./simple.py

import time

from PIL import Image, ImageDraw
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas

## https://pillow.readthedocs.io/en/latest/reference/ImageDraw.html#module-PIL.ImageDraw
## https://luma-core.readthedocs.io/en/latest/intro.html
## https://luma-led-matrix.readthedocs.io/en/latest/intro.html

if __name__ == "__main__":
    try:
        # Vytvori objekt ktery umozni komunikovat s matici pomoci GPIO pinu. Koukni na
        # https://www.etechnophiles.com/wp-content/uploads/2021/01/R-Pi-4-GPIO-Pinout.jpg
        # My budeme pouzivat SPI0 (raspberry jich ma 2). 
        serial = spi(port=0, device=0, gpio=noop())

        # Vytvori objekt zarizeni - nasi LED matice. Musime mu dat spi objekt, pres ktery by mel mluvit.
        # Dale mu rikame ze mame v zarizeni 4 matice, a ze jsou od vyrobce otocene o 90 stupnu.
        device = max7219(serial, cascaded=4, block_orientation=-90, rotate=0, blocks_arranged_in_reverse_order=False)

        # Vytvorime si objekt Obrazku na ktery budeme kreslit a pak jej zobrazime na matici.
        img = Image.new('1', (32,8), color=0)

        # Toto nam vytvori objekt Obrazku ktery umi ruzne prikazy pro kresleni
        draw = ImageDraw.Draw(img)

        # .point je prikaz (volani metody na objektu) aby nakreslil puntik na souradnici 3,2 a barvou 1.
        # LED matrix ma jenom 2 barvy: 1 ... cervena, 0 ... vypnuto.
        # Tady jsou dalsi metody pro kresleni:
        # https://pillow.readthedocs.io/en/latest/reference/ImageDraw.html#module-PIL.ImageDraw
        draw.point((3, 3), fill=1)
        
        # Toto nakresli obdelnik s rohy (1,1) a (30,6). 
        draw.rectangle([(1,1), (30,6)], fill=None, outline=1, width=1)

        # Toto prikaze obrazku at se dokonci kresleni. 
        img.show()

        # Toto rekne nasi matici aby tam zobrazila obrazek co jsme nakreslili
        device.display(img)

        # Toto porad dokola nic nedela, aby neskoncil program. Vypne se to az se ukonci program, 
        # na prikazove radce Ctrl-C.
        while True:
            noop

    except KeyboardInterrupt:
        pass
