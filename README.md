<img src="logo.svg" alt="logo" />
<br>
<p>
  <img alt="Python" src="https://img.shields.io/pypi/pyversions/mcpxpy.svg" />
  <img alt="PyPI" src="https://img.shields.io/pypi/v/mcpxpy.svg" />
  <img alt="License" src="https://img.shields.io/pypi/l/mcpxpy.svg" />
</p>

**mcpxpy is a Python wrapper for [McpX](https://github.com/YudaiKitamura/McpX),  
a .NET library for communicating with Mitsubishi Electric PLCs using the MC protocol.**

This package allows Python applications to communicate with Mitsubishi PLCs via a high-performance native interface  
powered by Ahead-of-Time (AOT) compiled shared libraries (`.so` / `.dll`) using `ctypes`.

> ⚡ **By leveraging AOT-compiled binaries, mcpxpy achieves near-native performance**,  
> making it highly efficient for real-time or high-frequency communication tasks.

> ⚠️ **This library is currently under active development and not yet production-ready.**  
> APIs and behavior may change without notice.

## Installation
### PyPI
```sh
pip install -i https://test.pypi.org/simple/ mcpxpy
```

## Example Usage 
```python
from mcpxpy import *

# Connect to PLC by specifying IP and port
with McpX("192.168.12.88", 10000) as mcpx:
    # Read 7000 words starting from D1000
    d_list = mcpx.batch_read_short(Prefix.D, "1000", 7000)

    # Write 1234 to D0 and 5678 to D1 as signed 16-bit shorts
    mcpx.batch_write_short(Prefix.D, "0", [1234, 5678])
```

## Supported Protocols
- TCP
- UDP
- 3E frame (binary code)
- 3E frame (ASCII code)
- 4E frame (binary code)
- 4E frame (ASCII code)
