# Pico W code (save as main.py on the Pico W)
import machine
import time
import sys
import select

# Setup onboard LED
led = machine.Pin("LED", machine.Pin.OUT)

def main():
    print("Pico W LED control ready")
    led.off()
    
    while True:
        try:
            if sys.stdin in select.select([sys.stdin], [],[], 0)[0]:
                # Read from UART/USB
                command = sys.stdin.readline().strip()
                print(command,"tady")
                
                # Process command
                if command == "1":
                    led.value(1)
                    print("LED ON")
                elif command == '0':
                    led.value(0)
                    print("LED OFF")
                    
        except Exception as e:
            print("Error:", e)
            time.sleep(0.1)  # Prevent tight loop on error

if __name__ == "__main__":
    main()