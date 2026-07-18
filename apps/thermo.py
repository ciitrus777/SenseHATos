from sense_emu import SenseHat
sense = SenseHat()

temp = round(sense.get_temperature()*10)/10
sense.show_message(str(temp) + "'C", scroll_speed=0.1)