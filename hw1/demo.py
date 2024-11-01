import numpy as np

class registerFile:
    def __init__(self):
        self.registers = np.array([0]*32, dtype=np.int32)
    
    def read(self, registerON1, registerON2=None):
        if registerON2 == None:
            return self.registers[registerON1]
        else:
            return self.registers[registerON1], self.registers[registerON2]
    
    def write(self, registerON, value):
        self.registers[registerON] = value


class memory:
    def __init__(self, size=1024):
        self.space = np.array([0]*size, dtype=np.int8)

    def read(self, address):
        if(address < 0 or address >= len(self.space)):
            raise Exception("Out of bounds")
        # 8位有符号整数实现：
        return self.space[address]
        # 32位整数、小端法实现：
        # return      (self.space[address+3] << 24) \
        #         +   (self.space[address+2] << 16) \
        #         +   (self.space[address+1] << 8) \
        #         +   (self.space[address])

    def write(self, address, value):
        if(address < 0 or address >= len(self.space)):
            raise Exception("Out of bounds")
        # 8位有符号整数实现：
        self.space[address] = value
        # 32位有符号整数、小端法实现：
        # self.space[address], self.space[address + 1], self.space[address + 2], self.space[address + 3] \
        # = value & 0xff, (value >> 8) & 0xff, (value >> 16) & 0xff, (value >> 24) & 0xff


mem = memory()
regs = registerFile()

# 初始化#0=20, r1=-25
mem.write(0, 20)
mem.write(1, -25)  

# 模拟汇编代码
regs.write(1, mem.read(0))
regs.write(2, mem.read(1))
regs.write(3, regs.read(1) + regs.read(2))
mem.write(3, regs.read(3))

print(regs.read(1), regs.read(2), regs.read(3))
print(mem.read(3))
'''
输出结果：
20 -25 -5
-5
'''