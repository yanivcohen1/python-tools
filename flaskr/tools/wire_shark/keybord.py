import os
import pyshark
import matplotlib.pyplot as plt

# usb.src 2.5.1(keybord) 2.7.3(mouse)
# usb.dst host
# usb.transfer_type 0x01
# usbhid.data 00001a0000000000

def parse_hid_data(hid_data):
    """
    Convert HID report data to readable key presses.
    """
    HID_KEYCODES = {
        0x04: 'a', 0x05: 'b', 0x06: 'c', 0x07: 'd', 0x08: 'e',
        0x09: 'f', 0x0A: 'g', 0x0B: 'h', 0x0C: 'i', 0x0D: 'j',
        0x0E: 'k', 0x0F: 'l', 0x10: 'm', 0x11: 'n', 0x12: 'o',
        0x13: 'p', 0x14: 'q', 0x15: 'r', 0x16: 's', 0x17: 't',
        0x18: 'u', 0x19: 'v', 0x1A: 'w', 0x1B: 'x', 0x1C: 'y',
        0x1D: 'z', 0x1E: '1', 0x1F: '2', 0x20: '3', 0x21: '4',
        0x22: '5', 0x23: '6', 0x24: '7', 0x25: '8', 0x26: '9', 0x27: '0',
        0x28: 'Enter', 0x29: 'Esc', 0x2A: 'Backspace', 0x2B: 'Tab', 0x2C: 'Space',
        0x2D: '-', 0x2E: '=', 0x2F: '[', 0x30: ']', 0x31: '\\', 0x32: '#',
        0x33: ';', 0x34: "'", 0x35: '`', 0x36: ',', 0x37: '.', 0x38: '/',
        0x39: 'CapsLock', 0x3A: 'F1', 0x3B: 'F2', 0x3C: 'F3', 0x3D: 'F4',
        0x3E: 'F5', 0x3F: 'F6', 0x40: 'F7', 0x41: 'F8', 0x42: 'F9',
        0x43: 'F10', 0x44: 'F11', 0x45: 'F12'
    }

    keys = []
    for byte in hid_data:
        key_code = int(byte, 16)
        if key_code in HID_KEYCODES:
            keys.append(HID_KEYCODES[key_code])

    return ''.join(keys)

def capture_usb_keyboard(pcap_file):
    cap = pyshark.FileCapture(pcap_file) # display_filter="usb.capdata"
    keybord = []
    for packet in cap:
        try:
            # 0x01: Interrupt transfer -> using wireshark copy -> fildName: usb.transfer_type
            if hasattr(packet, 'usb') and int(packet.usb.transfer_type, 0) == 1:
                # 2.5.1(keybord) 2.7.3(mouse)
                if packet.usb.src == "2.5.1" and hasattr(packet, 'DATA'):
                    # using wireshark copy -> fildName: usbhid.data
                    hid_data = packet.data.usbhid_data.split(':')
                    # Convert hex string to integer
                    keys = parse_hid_data(hid_data)
                    if keys:
                        keybord.append(keys)
        except Exception as e:
            print(f"Error processing packet: {e}")

    return keybord

if __name__ == "__main__":
    # pcap_file = "/mnt/data/mouse.pcap"
    current_directory = os.path.dirname(__file__)
    # pcap_file = current_directory + "/mouse.pcap"
    pcap_file = current_directory + "/keybord_yaniv.pcapng"
    print("user write:", ''.join(capture_usb_keyboard(pcap_file)))
    # save_position_to_file(x_data, y_data)
    # print(x_data, y_data)
    # plot_mouse_movements(x_data, y_data)

# https://www.amazon.com/Wacom-Bamboo-Splash-Tablet-CTL471/dp/B0089VGPII

# Byte Index	Value (Hex)	Meaning
# 0	01	Button state (1 means left button pressed)
# 1	80	X movement (0x80 in signed 8-bit is -128)
# 2	00	Y movement (0x00 in signed 8-bit is 0)
# 3	FD	Wheel movement (0xFD in signed 8-bit is -3)
# Mouse Position Movement:
# X movement: 0x80 (interpreted as -128 in signed 8-bit format)
# Y movement: 0x00 (interpreted as 0)
# Scroll movement: -3 (if relevant)
