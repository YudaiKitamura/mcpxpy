from mcpxpy import *

with McpX("192.168.12.88", 10001, is_udp=True) as mcpx:
    mcpx.batch_write_short(Prefix.D, "0", [1, 2, 3, 4])
    a = mcpx.batch_read_short(Prefix.D, "0", 4)

    print("Values:", list(a))
    