import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import serial
import serial.tools.list_ports
import threading
import json
import os
from datetime import datetime
import time

class BluetoothSerialTerminal:
    def __init__(self, root):
        self.root = root
        self.root.title("Bluetooth Serial Terminal")
        self.root.geometry("900x700")
        
        self.serial_port = None
        self.connected_port = None
        self.read_thread = None
        self.running = False
        
        self.message_counter = 0
        
        self.history_file = "device_history.json"
        self.device_history = self.load_history()
        
        self.setup_ui()
        self.load_last_settings()
        self.refresh_ports(auto_connect=True)
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        ttk.Label(main_frame, text="Available COM Ports (Bluetooth & Serial):", font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        device_frame = ttk.Frame(main_frame)
        device_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)
        device_frame.columnconfigure(0, weight=1)
        
        self.device_listbox = tk.Listbox(device_frame, height=6, selectmode=tk.SINGLE)
        self.device_listbox.grid(row=0, column=0, sticky="ew")
        
        scrollbar = ttk.Scrollbar(device_frame, orient=tk.VERTICAL, command=self.device_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.device_listbox.configure(yscrollcommand=scrollbar.set)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        ttk.Button(button_frame, text="Refresh Ports", command=self.refresh_ports).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Connect", command=self.connect_device).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Disconnect", command=self.disconnect_device).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Clear Buffers", command=self.clear_buffers).grid(row=0, column=3, padx=5)
        
        ttk.Label(button_frame, text="Baud Rate:").grid(row=0, column=4, padx=(20, 5))
        self.baud_rate = ttk.Combobox(button_frame, values=["9600", "19200", "38400", "57600", "115200"], width=10, state='readonly')
        self.baud_rate.set("9600")
        self.baud_rate.grid(row=0, column=5, padx=5)
        
        self.status_label = ttk.Label(main_frame, text="Status: Disconnected", foreground="red")
        self.status_label.grid(row=2, column=0, columnspan=2, sticky=tk.E, pady=5)
        
        chat_frame = ttk.LabelFrame(main_frame, text="Communication", padding="5")
        chat_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=10)
        chat_frame.columnconfigure(0, weight=1)
        chat_frame.rowconfigure(0, weight=1)
        
        self.chat_display = scrolledtext.ScrolledText(chat_frame, height=20, state='disabled', wrap=tk.WORD)
        self.chat_display.grid(row=0, column=0, sticky="nsew", pady=5)
        
        self.chat_display.tag_config('sent', foreground='blue')
        self.chat_display.tag_config('received', foreground='green')
        self.chat_display.tag_config('system', foreground='gray')
        
        input_frame = ttk.Frame(chat_frame)
        input_frame.grid(row=1, column=0, sticky="ew", pady=5)
        input_frame.columnconfigure(0, weight=1)
        
        self.input_entry = ttk.Entry(input_frame)
        self.input_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.input_entry.bind('<Return>', lambda e: self.send_data())
        
        send_button_frame = ttk.Frame(input_frame)
        send_button_frame.grid(row=0, column=1)
        
        ttk.Button(send_button_frame, text="Send", command=self.send_data).grid(row=0, column=0, padx=2)
        
        self.line_ending = ttk.Combobox(send_button_frame, values=["None", "\\n", "\\r", "\\r\\n"], width=8, state='readonly')
        self.line_ending.set("\\n")
        self.line_ending.grid(row=0, column=1, padx=2)
        
        ttk.Button(send_button_frame, text="Clear Chat", command=self.clear_chat).grid(row=0, column=2, padx=2)
        
        self.add_to_chat("System: Bluetooth Serial Terminal started", 'system')
        self.add_to_chat("System: Pair your Bluetooth device in Windows Settings first", 'system')
        
    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump(self.device_history, f, indent=2)
    
    def load_last_settings(self):
        if self.device_history:
            last_baud = self.device_history.get('last_baud', '9600')
            self.baud_rate.set(str(last_baud))
    
    def add_to_chat(self, message, tag='system'):
        self.chat_display.configure(state='normal')
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] {message}\n", tag)
        self.chat_display.see(tk.END)
        self.chat_display.configure(state='disabled')
    
    def refresh_ports(self, auto_connect=False):
        self.device_listbox.delete(0, tk.END)
        ports = serial.tools.list_ports.comports()
        
        if not ports:
            self.device_listbox.insert(tk.END, "No COM ports found - Please pair Bluetooth device in Windows Settings")
            self.add_to_chat("System: No COM ports detected", 'system')
        else:
            devices_history = self.device_history.get('devices', {})
            
            for port in ports:
                port_name = port.device
                description = port.description
                
                was_connected = port_name in devices_history
                history_info = devices_history.get(port_name, {})
                device_name = history_info.get('device_name', description)
                
                is_bluetooth = "Bluetooth" in description or "bluetooth" in description.lower()
                
                if was_connected:
                    last_time = history_info.get('last_connected', 'Unknown')
                    if last_time != 'Unknown':
                        try:
                            dt = datetime.fromisoformat(last_time)
                            time_str = dt.strftime("%m/%d %H:%M")
                        except:
                            time_str = "Previously"
                    else:
                        time_str = "Previously"
                    
                    if is_bluetooth:
                        self.device_listbox.insert(tk.END, f"📶 {port_name} - {device_name} [Last: {time_str}]")
                    else:
                        self.device_listbox.insert(tk.END, f"{port_name} - {device_name} [Last: {time_str}]")
                else:
                    if is_bluetooth:
                        self.device_listbox.insert(tk.END, f"📶 {port_name} - {device_name}")
                    else:
                        self.device_listbox.insert(tk.END, f"{port_name} - {device_name}")
            
            self.add_to_chat(f"System: Found {len(ports)} COM port(s)", 'system')
            
            if devices_history:
                self.add_to_chat(f"System: {len(devices_history)} device(s) in connection history", 'system')
        
        if self.device_history:
            last_port = self.device_history.get('last_port')
            if last_port:
                port_found = False
                for i in range(self.device_listbox.size()):
                    entry = self.device_listbox.get(i)
                    port_name = entry.split(' - ')[0].replace('📶 ', '').strip()
                    
                    if port_name == last_port:
                        self.device_listbox.selection_set(i)
                        self.add_to_chat(f"System: Auto-selected last used port: {last_port}", 'system')
                        port_found = True
                        
                        if auto_connect:
                            self.add_to_chat(f"System: Attempting auto-reconnect to {last_port}...", 'system')
                            self.root.after(500, self.connect_device)
                        break
                
                if not port_found and auto_connect:
                    self.add_to_chat(f"System: Last used port {last_port} not available", 'system')
    
    def connect_device(self):
        selection = self.device_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a COM port to connect")
            return
        
        device_info = self.device_listbox.get(selection[0])
        
        if "No COM ports found" in device_info:
            messagebox.showinfo("No Ports", "Please pair your Bluetooth device in Windows Settings first")
            return
        
        port_name = device_info.split(' - ')[0].replace('📶 ', '').strip()
        
        device_name_part = device_info.split(' - ', 1)[1] if ' - ' in device_info else "Unknown Device"
        if '[Last:' in device_name_part:
            device_name = device_name_part.split('[Last:')[0].strip()
        else:
            device_name = device_name_part.strip()
        
        baud_rate = int(self.baud_rate.get())
        
        available_ports = [p.device for p in serial.tools.list_ports.comports()]
        if port_name not in available_ports:
            messagebox.showerror("Port Not Available", f"{port_name} is not available.\n\nThe device may be:\n- Disconnected\n- Already in use by another application\n- Turned off")
            self.add_to_chat(f"System: {port_name} not available for connection", 'system')
            return
        
        try:
            self.serial_port = serial.Serial(
                port=port_name,
                baudrate=baud_rate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1
            )
            
            self.serial_port.reset_input_buffer()
            self.serial_port.reset_output_buffer()
            self.add_to_chat("System: Cleared serial buffers", 'system')
            
            self.message_counter = 0
            
            self.connected_port = port_name
            self.device_history['last_port'] = port_name
            self.device_history['last_baud'] = baud_rate
            
            if 'devices' not in self.device_history:
                self.device_history['devices'] = {}
            
            self.device_history['devices'][port_name] = {
                'device_name': device_name,
                'last_connected': datetime.now().isoformat(),
                'last_baud': baud_rate
            }
            
            self.save_history()
            
            self.status_label.config(text=f"Status: Connected to {device_name} ({port_name}) @ {baud_rate} baud", foreground="green")
            self.add_to_chat(f"System: Connected to {device_name} ({port_name}) at {baud_rate} baud", 'system')
            
            self.running = True
            self.read_thread = threading.Thread(target=self.read_serial, daemon=True)
            self.read_thread.start()
            
        except serial.SerialException as e:
            error_msg = str(e)
            if "PermissionError" in error_msg or "Access is denied" in error_msg:
                messagebox.showerror("Port In Use", f"{port_name} is already open in another application.\n\nPlease close the other application and try again.")
                self.add_to_chat(f"System: {port_name} is in use by another application", 'system')
            else:
                messagebox.showerror("Connection Error", f"Failed to connect: {error_msg}")
                self.add_to_chat(f"System: Connection failed - {error_msg}", 'system')
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
            self.add_to_chat(f"System: Error - {str(e)}", 'system')
    
    def disconnect_device(self):
        if self.serial_port and self.serial_port.is_open:
            self.running = False
            if self.read_thread:
                self.read_thread.join(timeout=2)
            
            self.serial_port.close()
            self.serial_port = None
            self.connected_port = None
            
            self.status_label.config(text="Status: Disconnected", foreground="red")
            self.add_to_chat("System: Disconnected", 'system')
        else:
            messagebox.showinfo("Not Connected", "No device is currently connected")
    
    def clear_buffers(self):
        if self.serial_port and self.serial_port.is_open:
            try:
                bytes_in = self.serial_port.in_waiting
                bytes_out = self.serial_port.out_waiting
                
                self.serial_port.reset_input_buffer()
                self.serial_port.reset_output_buffer()
                
                self.add_to_chat(f"System: Buffers cleared (Input: {bytes_in} bytes, Output: {bytes_out} bytes)", 'system')
                messagebox.showinfo("Buffers Cleared", f"Successfully cleared buffers\n\nInput buffer: {bytes_in} bytes\nOutput buffer: {bytes_out} bytes")
            except Exception as e:
                self.add_to_chat(f"System: Error clearing buffers - {str(e)}", 'system')
                messagebox.showerror("Error", f"Failed to clear buffers: {str(e)}")
        else:
            messagebox.showwarning("Not Connected", "Please connect to a device first")
    
    def clear_chat(self):
        self.message_counter = 0
        self.chat_display.configure(state='normal')
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.configure(state='disabled')
        self.add_to_chat("System: Chat display cleared (message counter reset)", 'system')
    
    def read_serial(self):
        while self.running and self.serial_port and self.serial_port.is_open:
            try:
                if self.serial_port.in_waiting > 0:
                    data = self.serial_port.read(self.serial_port.in_waiting)
                    self.message_counter += 1
                    try:
                        message = data.decode('utf-8', errors='ignore')
                        self.root.after(0, self.add_to_chat, f"📥 RX #{self.message_counter} ({len(data)} bytes): {message}", 'received')
                    except:
                        self.root.after(0, self.add_to_chat, f"📥 RX #{self.message_counter} ({len(data)} bytes, hex): {data.hex()}", 'received')
                else:
                    time.sleep(0.01)
            except serial.SerialException:
                self.root.after(0, self.add_to_chat, "System: Connection lost", 'system')
                self.running = False
                break
            except Exception as e:
                self.root.after(0, self.add_to_chat, f"System: Read error - {str(e)}", 'system')
                break
    
    def send_data(self):
        if not self.serial_port or not self.serial_port.is_open:
            messagebox.showwarning("Not Connected", "Please connect to a device first")
            return
        
        message = self.input_entry.get()
        if not message:
            return
        
        display_msg = message
        ending = self.line_ending.get()
        if ending == "\\n":
            message += "\n"
        elif ending == "\\r":
            message += "\r"
        elif ending == "\\r\\n":
            message += "\r\n"
        
        try:
            data = message.encode('utf-8')
            self.serial_port.write(data)
            self.message_counter += 1
            self.add_to_chat(f"📤 TX #{self.message_counter} ({len(data)} bytes): {repr(display_msg)} + {ending}", 'sent')
            self.input_entry.delete(0, tk.END)
        except serial.SerialException as e:
            self.add_to_chat(f"System: Send error - {str(e)}", 'system')
            messagebox.showerror("Send Error", f"Failed to send: {str(e)}")
        except Exception as e:
            self.add_to_chat(f"System: Error - {str(e)}", 'system')
    
    def on_closing(self):
        if self.serial_port and self.serial_port.is_open:
            self.disconnect_device()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = BluetoothSerialTerminal(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
