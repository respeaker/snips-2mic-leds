## snips-2mic-leds

The skill to control the LEDs of the Respeaker 2 Mic Hat

### Setup

1. Use `sam` to install the skill
   ```
   sam install actions -g https://github.com/respeaker/snips-2mic-leds.git
   ```

2. Login Raspberry Pi and enable GPIO, I2C and SPI access permissions

   ```
   sudo usermod -a -G spi,gpio,audio,i2c _snips-skills
   sudo usermod -a -G snips-skills-admin $USER
   sudo systemctl restart snips-skill-server.service
   ```



