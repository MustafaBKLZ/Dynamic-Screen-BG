
import sys

# Force STA before any other import that might init COM
sys.coinit_flags = 2 # COINIT_APARTMENTTHREADED

import ctypes
from ctypes import wintypes
import comtypes
from comtypes.client import CreateObject
from comtypes import CoCreateInstance, CLSCTX_LOCAL_SERVER, GUID, IUnknown, COMMETHOD, HRESULT

# Define IDesktopWallpaper Interface
# CLSID for DesktopWallpaper coclass
CLSID_DesktopWallpaper = GUID("{C2CF3110-460E-4fc1-B9D0-8A1C0C9CC939}")

class IDesktopWallpaper(IUnknown):
    _iid_ = GUID("{B92B56A9-8B55-4E14-9A89-0199BBB6F93B}")
    _methods_ = [
        COMMETHOD([], HRESULT, "SetWallpaper",
                  (['in'], wintypes.LPCWSTR, "monitorID"),
                  (['in'], wintypes.LPCWSTR, "wallpaper")),
        COMMETHOD([], HRESULT, "GetWallpaper",
                  (['in'], wintypes.LPCWSTR, "monitorID"),
                  (['out'], ctypes.POINTER(wintypes.LPWSTR), "wallpaper")),
        COMMETHOD([], HRESULT, "GetMonitorDevicePathAt",
                  (['in'], ctypes.c_uint, "monitorIndex"),
                  (['out'], ctypes.POINTER(wintypes.LPWSTR), "monitorID")),
        COMMETHOD([], HRESULT, "GetMonitorDevicePathCount",
                  (['out'], ctypes.POINTER(ctypes.c_uint), "count")),
        COMMETHOD([], HRESULT, "GetMonitorRECT",
                  (['in'], wintypes.LPCWSTR, "monitorID"),
                  (['out'], ctypes.POINTER(wintypes.RECT), "displayRect")),
    ]

def debug_com_v2():
    print("--- COM API V2 Debug Start ---")
    print(f"Python Architecture: {'64-bit' if sys.maxsize > 2**32 else '32-bit'}")
    
    try:
        print("Creating DesktopWallpaper object...")
        try:
            # Try simplest way first
            dw = CreateObject(CLSID_DesktopWallpaper, interface=IDesktopWallpaper)
            print("Object created successfully with CreateObject.")
        except Exception as e:
            print(f"CreateObject failed: {e}")
            print("Retrying with CoCreateInstance...")
            dw = CoCreateInstance(CLSID_DesktopWallpaper, IDesktopWallpaper, CLSCTX_LOCAL_SERVER)
            print("Object created successfully with CoCreateInstance.")

        
        count = ctypes.c_uint()
        dw.GetMonitorDevicePathCount(ctypes.byref(count))
        print(f"Monitor Count: {count.value}")
        
        for i in range(count.value):
            try:
                mid_ptr = wintypes.LPWSTR()
                dw.GetMonitorDevicePathAt(i, ctypes.byref(mid_ptr))
                mid = mid_ptr.value
                ctypes.windll.ole32.CoTaskMemFree(mid_ptr) # Good practice to free
                print(f"Monitor {i} ID: {mid}")
            except Exception as e:
                print(f"Error getting monitor {i}: {e}")
                
        print("--- COM API Verify Success ---")

    except Exception as e:
        print(f"FATAL COM ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_com_v2()
