import wiringpi

wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(1,1)

while wiringpi.analogRead(0) < 100:
	pass

wiringpi.digitalWrite(1,1)