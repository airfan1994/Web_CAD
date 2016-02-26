import ctypes
import struct
ll = ctypes.cdll.LoadLibrary
lib = ll("./maze.so")
s=struct.Struct('60i')
ret=lib.maze(120,300,1,1,4,4)
r=ctypes.string_at(ret,s.size)
print (s.unpack(r))


