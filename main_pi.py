from picamera2 import Picamera2
import cv2
import pytesseract
import numpy as np
import csv
import time
import re
import serial

def setup_pico_connection():
    """Setup serial connection to Pico W"""
    try:
        ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        print("Connected to Pico W")
        return ser
    except Exception as e:
        print(f"Failed to connect to Pico W: {str(e)}")
        return None

def load_approved_texts(csv_file='approved_texts.csv'):
    """Load approved texts from CSV file"""
    try:
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            approved_texts = [row[0].strip() for row in reader]
            print(f"Loaded {len(approved_texts)} approved texts")
            return approved_texts
    except FileNotFoundError:
        example_texts = ['ROCK', 'PYTHON', 'PI']
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            for text in example_texts:
                writer.writerow([text])
        print(f"Created example {csv_file} with sample texts")
        return example_texts

def find_matching_text(detected_text, approved_texts):
    """Find any approved text within the detected text"""
    detected_text = re.sub(r'[^A-Za-z0-9]', '', detected_text.upper())
    matches = []
    
    for approved_text in approved_texts:
        clean_approved = re.sub(r'[^A-Za-z0-9]', '', approved_text.upper())
        if clean_approved in detected_text:
            matches.append(approved_text)
    
    return matches

def setup_camera():
    try:
        picam2 = Picamera2()
        config = picam2.create_preview_configuration(
            main={"size": (1280, 720), "format": "RGB888"}
        )
        picam2.configure(config)
        return picam2
    except Exception as e:
        print(f"Camera setup error: {str(e)}")
        return None

def process_frame(frame):
    height, width = frame.shape[:2]
    start_y = int(height * 0.3)
    end_y = int(height * 0.7)
    start_x = int(width * 0.3)
    end_x = int(width * 0.7)
    roi = frame[start_y:end_y, start_x:end_x]
    
    if len(roi.shape) == 3 and roi.shape[2] == 3:
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    
    gray = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)
    gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((2,2), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    
    return binary, (start_x, start_y, end_x, end_y)

def main():
    try:
        # Setup Pico W connection
        pico_serial = setup_pico_connection()
        if pico_serial is None:
            print("Warning: Proceeding without Pico W connection")
        
        # Load approved texts
        approved_texts = load_approved_texts()
        
        picam2 = setup_camera()
        if picam2 is None:
            print("Failed to initialize camera")
            return
            
        picam2.start()
        
        print("\nControls:")
        print("'q' - Quit")
        print("'r' - Reload approved texts from CSV")
        
        last_detection_time = 0
        detection_cooldown = 1.0  # Seconds between detection attempts
        pause_duration = 10.0  # Seconds to pause after successful detection
        is_paused = False
        pause_start_time = 0
        
        while True:
            frame = picam2.capture_array()
            frame = cv2.flip(frame, 0)  # Vertical flip
            frame = cv2.flip(frame, 1)  # Horizontal flip
            
            display = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Draw ROI rectangle
            height, width = frame.shape[:2]
            start_x = int(width * 0.3)
            end_x = int(width * 0.7)
            start_y = int(height * 0.3)
            end_y = int(height * 0.7)
            cv2.rectangle(display, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
            
            current_time = time.time()
            
            # Handle pause state
            if is_paused:
                time_remaining = int(pause_duration - (current_time - pause_start_time))
                if time_remaining <= 0:
                    is_paused = False
                    if pico_serial:
                        pico_serial.write(b'0\n')  # Turn LED off after pause
                        print("Pause ended, LED turned off")
                else:
                    # Show countdown
                    cv2.rectangle(display, (0, 0), (width, 40), (0, 0, 0), -1)
                    cv2.putText(display, f"Paused: {time_remaining}s remaining", 
                              (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
            # Real-time text detection when not paused
            elif current_time - last_detection_time >= detection_cooldown:
                processed, roi_coords = process_frame(frame)
                
                custom_config = r'--oem 3 --psm 6'
                detected_text = pytesseract.image_to_string(processed, config=custom_config)
                detected_text = detected_text.strip()
                
                if len(detected_text) > 2:
                    matched_texts = find_matching_text(detected_text, approved_texts)
                    
                    # Show detection results on screen
                    cv2.rectangle(display, (0, 0), (width, 80), (0, 0, 0), -1)
                    cv2.putText(display, f"Detected: {detected_text}", (10, 30), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                    
                    if matched_texts:
                        cv2.putText(display, f"Matches: {', '.join(matched_texts)}", (10, 70), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                        if pico_serial:
                            pico_serial.write(b'1\n')
                            print(f"Match found: {matched_texts}")
                            is_paused = True
                            pause_start_time = current_time
                    else:
                        cv2.putText(display, "No matches", (10, 70), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                
                last_detection_time = current_time
            
            cv2.imshow("Text Detection", display)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('r'):
                approved_texts = load_approved_texts()
                print("\nReloaded approved texts")
            elif key == ord('q'):
                if pico_serial:
                    pico_serial.write(b'0\n')  # Ensure LED is off before quitting
                break
                
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if 'pico_serial' in locals() and pico_serial:
            pico_serial.close()
        if 'picam2' in locals() and picam2 is not None:
            picam2.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()