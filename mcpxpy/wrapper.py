from ctypes import (
    c_float, cdll, c_int, c_char_p, c_void_p, c_bool,
    c_short, c_uint8, create_string_buffer,
)
from pathlib import Path
import platform

import requests

from .structs import RequestFrame, Prefix, Device
from .exceptions import DeviceAddressException, RecivePacketException, McProtocolException


class McpX():
    API_URL = "https://api.github.com/repos/YudaiKitamura/McpX/releases/latest"
    LINUX_LIB_FILENAME = "McpXInterop-linux-x64.so"
    WIN_LIB_FILENAME = "McpXInterop-win-x64.dll"

    def __init__(
            self, 
            ip: str,
            port: int,
            password: str = None,
            is_ascii: bool = False,
            is_udp: bool = False,
            request_frame: RequestFrame = RequestFrame.E3):
        
        lib_path = self._ensure_library_downloaded()
        self.lib = cdll.LoadLibrary(lib_path)

        self.lib.plc_connect.argtypes = [c_char_p, c_int, c_char_p, c_bool, c_bool, c_int]
        self.lib.plc_connect.restype = c_int

        self.lib.plc_close.argtypes = [c_int]
        self.lib.plc_close.restype = None

        self.lib.batch_read_bool.argtypes = [c_int, c_void_p, Device, c_int]
        self.lib.batch_read_bool.restype = c_int

        self.lib.batch_read_float.argtypes = [c_int, c_void_p, Device, c_int]
        self.lib.batch_read_float.restype = c_int

        self.lib.batch_write_short.argtypes = [c_int, c_void_p, Device, c_int]
        self.lib.batch_write_short.restype = c_int

        self.conn_id = self.lib.plc_connect(create_string_buffer(ip.encode("ascii")), port, password, is_ascii, is_udp, request_frame)

    def _ensure_library_downloaded(self) -> Path:
        system = platform.system().lower()
        arch = platform.machine()

        if system == "linux":
            filename = self.LINUX_LIB_FILENAME
        elif system == "windows":
            filename = self.WIN_LIB_FILENAME
        else:
            raise RuntimeError(f"Unsupported OS: {system}")

        cache_dir = Path(__file__).parent / ".cache"
        lib_path = cache_dir / filename

        if lib_path.exists():
            return lib_path

        response = requests.get(self.API_URL)
        release = response.json()

        asset_url = next(
            (asset["browser_download_url"] for asset in release["assets"]
             if asset["name"] == filename),
            None
        )

        if not asset_url:
            raise RuntimeError(f"{filename} not found in latest release.")

        cache_dir.mkdir(parents=True, exist_ok=True)
        with open(lib_path, "wb") as f:
            f.write(requests.get(asset_url).content)

        return lib_path

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        self.lib.plc_close(self.conn_id)
    
    def batch_read_short(
            self, 
            prefix: Prefix,
            address: str,
            length: int) -> list[int]:
        
        short_read_array = (c_short * length)()

        device = Device(
            Prefix=prefix,
            Address=address.encode("ascii")
        )

        self.__has_error(
            result=self.lib.batch_read_short(self.conn_id, short_read_array, device, length)
        )

        return list(short_read_array)
    
    def batch_write_short(
            self, 
            prefix: Prefix,
            address: str,
            values: list[int]) -> None:
        
        ShortArray = c_short * len(values)
        short_write_array = ShortArray(*values)

        device = Device(
            Prefix=prefix,
            Address=address.encode("ascii")
        )

        self.__has_error(
            result=self.lib.batch_write_short(self.conn_id, short_write_array, device, len(values))
        )

    def __has_error(self, result: int) -> None:
        if (result == -1):
            raise DeviceAddressException()
        elif (result == -2):
            raise RecivePacketException()
        elif (result == -3):
            raise McProtocolException()
