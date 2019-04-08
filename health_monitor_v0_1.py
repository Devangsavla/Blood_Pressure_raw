import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import smbus
import time


SPI_PORT   = 0
SPI_DEVICE = 0

bus = smbus.SMBus(1)
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

def ppg_init():
	DEVICE_ADDRESS = 0x57      #7 bit address (will be left shifted to add the read write bit)
	DEVICE_REG_MODE1 = 0x02
	MODE_CONFIG=0x06
	SPO2_CONFIG=0x07
	led_current_red = 3
	led_current_ir = 3
	
	#Add comments for use of all these 4 lines below.
	bus.write_byte_data(DEVICE_ADDRESS, MODE_CONFIG,0x40) #Reset
	bus.write_byte_data(DEVICE_ADDRESS, MODE_CONFIG, DEVICE_REG_MODE1)
	bus.write_byte_data(DEVICE_ADDRESS, 0, DEVICE_REG_MODE1)
	bus.write_byte_data(DEVICE_ADDRESS, 0x09, (led_current_red << 4) | led_current_ir)

#We will make these 2 functions merged into 1 later for reading all values
def ppg_read(samples, wait_time):
	ppg_sum = 0
	for i in range(samples):
		ppg_raw[i] = bus.read_i2c_block_data(DEVICE_ADDRESS, 0x05, 0x04)
		ppg_sum = ppg_sum + ppg_raw[i][0]
		time.sleep(wait_time)
	ppg_average = round(ppg_sum/samples)
	return ppg_average

# *channel is optional argument. If not speficied in function call it will be default 1st channel
def fs_read(samples,wait_time,*channel = 1)
	fs_sum = 0
	for i in range(samples):
		fs_sum = fs_sum + mcp.read_adc(0)
		time.sleep(wait_time)
	fs_average = round(fs_sum/samples)
	return fs_average

while 1:
	ppg_init()
	#Store timestamp
	readings[0] = time.time()
	#store ppg value
	readings[1] = ppg_read(5,0.1)
	#store fs value
	readings[2] = fs_read(5,0.1)

	with open("health_log.csv", 'w') as health_log:
		health_log.write(str(readings))
		health_log.write('\n')

#Not sure if averaging the readings is the best way to go ahead. we can do trial error and find out.