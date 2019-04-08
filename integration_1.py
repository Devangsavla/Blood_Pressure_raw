# ppg sensor interface
import smbus
import time

output_values[][]

target = open("heartbeat_log.csv","a")

bus = smbus.SMBus(1)

def ppg_init():
	DEVICE_ADDRESS = 0x57      #7 bit address (will be left shifted to add the read write bit)
	DEVICE_REG_MODE1 = 0x02
	MODE_CONFIG=0x06
	SPO2_CONFIG=0x07
	led_current_red = 3
	led_current_ir = 3
	
	bus.write_byte_data(DEVICE_ADDRESS, MODE_CONFIG,0x40) #Reset
	bus.write_byte_data(DEVICE_ADDRESS, MODE_CONFIG, DEVICE_REG_MODE1)
	bus.write_byte_data(DEVICE_ADDRESS, 0, DEVICE_REG_MODE1)
	bus.write_byte_data(DEVICE_ADDRESS, 0x09, (led_current_red << 4) | led_current_ir)

def ppg_read(samples, wait_time):
	ppg_sum = 0
	for i in range(samples):
		time.sleep(wait_time)
		x[i] = bus.read_i2c_block_data(DEVICE_ADDRESS, 0x05, 0x04)
		ppg_sum = ppg_sum + x[i][0]
	ppg_average = round(ppg_sum/samples)
	return ppg_average

ppg_init()
x = ppg_read(5,0.1)

print(x)

# fsr interfacing

SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
target = open("fsr_log.csv","a")

print('Reading MCP3008 values, press Ctrl-C to quit...')

# Print nice channel column headers.

print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
print('-' * 57)

# Main program loop.

while True:
    # Read all the ADC channel values in a list.
    values = [0]*8
    for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
        values[i] = mcp.read_adc(i)
	target.write(str(values[i]))
	target.write('\n')
    # Print the ADC values.
    print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
    # Pause for half a second.
    time.sleep(0.1)
