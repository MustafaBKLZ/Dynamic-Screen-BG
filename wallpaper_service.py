import os
import ctypes
import json
import logging
from ctypes import wintypes
from PIL import Image
import tempfile

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# WinAPI Constants & Types
user32 = ctypes.windll.user32
SPI_SETDESKWALLPAPER = 0x0014
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02

class MONITORINFOEX(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("rcMonitor", wintypes.RECT),
        ("rcWork", wintypes.RECT),
        ("dwFlags", wintypes.DWORD),
        ("szDevice", wintypes.WCHAR * 32)
    ]

class WallpaperService:
    def __init__(self):
        self.monitors = []
        self.config_file = "monitor_config.json"
        
        self.log_callback = None
        
        # Load config dictionary: { "monitor_name": { "images": [], "interval": 60, "enabled": True, "last_index": 0 } }
        self.configs = self.load_configs()
        
        # Initialize monitors
        self.detect_monitors()

    def set_log_callback(self, callback):
        self.log_callback = callback
        
    def _log(self, message):
        # Only log if logging is enabled in app settings
        app_settings = self.get_app_settings()
        if app_settings.get('show_logs', True):
            logger.info(message)
            if self.log_callback:
                self.log_callback(message)

    def load_configs(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Ensure app_settings exists
                    if 'app_settings' not in data:
                        data['app_settings'] = {'language': 'tr', 'show_logs': True}
                    return data
            except Exception as e:
                logger.error(f"Config load error: {e}")
        return {'app_settings': {'language': 'tr', 'show_logs': True}}

    def save_configs(self):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.configs, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Config save error: {e}")
    
    def get_app_settings(self):
        """Get global app settings"""
        return self.configs.get('app_settings', {'language': 'tr', 'show_logs': True})
    
    def update_app_settings(self, key, value):
        """Update a global app setting"""
        if 'app_settings' not in self.configs:
            self.configs['app_settings'] = {}
        self.configs['app_settings'][key] = value
        self.save_configs()
        self._log(f"App setting updated: {key} = {value}")

    def detect_monitors(self):
        """Detects monitors using WinAPI and stores their rects."""
        self.monitors = []
        
        def enum_monitor_callback(hmonitor, hdc, rect, data):
            info = MONITORINFOEX()
            info.cbSize = ctypes.sizeof(MONITORINFOEX)
            user32.GetMonitorInfoW(hmonitor, ctypes.byref(info))
            
            name = info.szDevice
            r = info.rcMonitor
            width = r.right - r.left
            height = r.bottom - r.top
            
            self.monitors.append({
                'name': name,
                'handle': hmonitor,
                'rect': (r.left, r.top, r.right, r.bottom), # Left, Top, Right, Bottom
                'width': width,
                'height': height,
                'x': r.left,
                'y': r.top
            })
            return True

        ENUM_MONITOR_PROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_ulong, ctypes.c_ulong, ctypes.POINTER(wintypes.RECT), ctypes.c_double)
        user32.EnumDisplayMonitors(None, None, ENUM_MONITOR_PROC(enum_monitor_callback), 0)
        
        # Ensure config entries exist for all detected monitors
        for m in self.monitors:
            if m['name'] not in self.configs:
                self.configs[m['name']] = {
                    "images": [],
                    "interval": 60,
                    "enabled": False,
                    "last_index": 0
                }
        self.save_configs()
        self._log(f"Detected {len(self.monitors)} monitors.")

    def get_config(self, monitor_name):
        return self.configs.get(monitor_name, {})

    def update_config(self, monitor_name, key, value):
        if monitor_name in self.configs:
            self.configs[monitor_name][key] = value
            self.save_configs()
            self._log(f"Updated {monitor_name}: {key} -> {value}")

    def add_image(self, monitor_name, path):
        if monitor_name in self.configs and path not in self.configs[monitor_name]['images']:
            self.configs[monitor_name]['images'].append(path)
            self.save_configs()
            self._log(f"Added image to {monitor_name}")
            return True
        return False

    def remove_image(self, monitor_name, path):
         if monitor_name in self.configs and path in self.configs[monitor_name]['images']:
            self.configs[monitor_name]['images'].remove(path)
            self.save_configs()
            self._log(f"Removed image from {monitor_name}")
            return True
         return False

    def move_image(self, monitor_name, index, direction):
        if monitor_name in self.configs:
            images = self.configs[monitor_name]['images']
            new_index = index + direction
            if 0 <= new_index < len(images):
                images[index], images[new_index] = images[new_index], images[index]
                self.save_configs()
                self._log(f"Reordered images in {monitor_name}")
                return True
        return False
        
    def shift_image(self, monitor_name, src_index, dest_index):
        if monitor_name in self.configs:
            images = self.configs[monitor_name]['images']
            if 0 <= src_index < len(images) and 0 <= dest_index < len(images):
                item = images.pop(src_index)
                images.insert(dest_index, item)
                self.save_configs()
                self._log(f"Moved image {src_index} -> {dest_index}")
                return True
        return False

    def generate_stitched_wallpaper(self, current_images_map):
        """
        Creates a stitched wallpaper.
        current_images_map: dict { "monitor_name": "path/to/image.jpg" }
        """
        if not self.monitors:
            return None

        # Calculate bounding box of all monitors
        min_x = min(m['x'] for m in self.monitors)
        min_y = min(m['y'] for m in self.monitors)
        max_x = max(m['rect'][2] for m in self.monitors)
        max_y = max(m['rect'][3] for m in self.monitors)
        
        total_width = max_x - min_x
        total_height = max_y - min_y
        
        canvas = Image.new('RGB', (total_width, total_height), (0, 0, 0))
        
        for m in self.monitors:
            img_path = current_images_map.get(m['name'])
            
            # Helper to paste image correctly
            paste_x = m['x'] - min_x
            paste_y = m['y'] - min_y
            
            if img_path and os.path.exists(img_path):
                try:
                    img = Image.open(img_path)
                    # Resize/Crop to fill monitor
                    
                    # Calculate target aspect ratio
                    target_ratio = m['width'] / m['height']
                    img_ratio = img.width / img.height
                    
                    if img_ratio > target_ratio:
                        # Image is wider, crop sides
                        new_height = m['height']
                        new_width = int(new_height * img_ratio)
                    else:
                        # Image is taller, crop top/bottom
                        new_width = m['width']
                        new_height = int(new_width / img_ratio)
                        
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # Center crop
                    left = (new_width - m['width']) / 2
                    top = (new_height - m['height']) / 2
                    right = (new_width + m['width']) / 2
                    bottom = (new_height + m['height']) / 2
                    
                    img = img.crop((left, top, right, bottom))
                    
                    canvas.paste(img, (paste_x, paste_y))
                except Exception as e:
                    self._log(f"Error processing image {img_path}: {e}")
            else:
                # If no image or invalid, maybe paste a placeholder or just leave black
                pass
                
        output_path = os.path.join(tempfile.gettempdir(), "stitched_wallpaper.png")
        try:
             canvas.save(output_path, "PNG")
             return output_path
        except Exception as e:
            self._log(f"Error saving stitched wallpaper: {e}")
            return None

    def set_system_wallpaper(self, path):
        if not path or not os.path.exists(path):
            return
            
        abs_path = os.path.abspath(path)
        # 1. Set wallpaper style to Tile (Tiled) which is required for span connection
        # Registry: HKEY_CURRENT_USER\Control Panel\Desktop -> WallpaperStyle=0, TileWallpaper=1
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, "0")
            winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, "1")
            winreg.CloseKey(key)
        except Exception as e:
            self._log(f"Registry Set Error: {e}")

        # 2. Call API
        user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, abs_path, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)
        self._log(f"Wallpaper updated.")

# Singleton Instance
service = WallpaperService()
