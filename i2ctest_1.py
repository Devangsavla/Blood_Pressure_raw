
import smbus
import time

# 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
bus = smbus.SMBus(1)

#7 bit address (will be left shifted to add the read write bit)
i2c_address = 0x57
i2c_mode_write = 0x02
i2c_led_conf = 0x09
i2c_op_data_buffer = 0x05

#LED Current config
led_current_red = 3
led_current_ir = 3

#
bus.write_byte_data(i2c_address, 0, i2c_mode_write)
bus.write_byte_data(i2c_address, i2c_led_conf, (led_current_red << 4) | led_current_ir)

target = open("heartbeat_log.csv","a")

for i in range(1000):
	time.sleep(0.1)
	x = bus.read_i2c_block_data(i2c_address, i2c_op_data_buffer, 0x04)
	print(x)
	target.write(str(x))
	target.write('\n')
