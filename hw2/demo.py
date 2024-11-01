import numpy as np

class registerFile:
    def __init__(self):
        self.registers = {i: np.int32(0) for i in range(32)}
        self.registers['pc'] = np.int32(0)
        self.registers['ir'] = np.int32(0)
    
    def read(self, registerON1, registerON2=None):
        if registerON2 == None:
            return self.registers[registerON1]
        else:
            return self.registers[registerON1], self.registers[registerON2]
    
    def write(self, registerON, value):
        self.registers[registerON] = value


class memory:
    def __init__(self, size=1024):
        self.space = bytearray(size)

    def read(self, address):
        if(address & 0x3 != 0):
            raise Exception("Misaligned")
        if(address < 0 or address >= len(self.space)):
            raise Exception("Out of bounds")
        return int.from_bytes(self.space[address:address+4], byteorder='little', signed=True)

    def write(self, address, value):
        if(address & 0x3 != 0):
            raise Exception("Misaligned")
        if(address < 0 or address >= len(self.space)):
            raise Exception("Out of bounds")
        value_in_bytes = value.to_bytes(4, byteorder='little', signed=True)
        self.space[address:address+4] = value_in_bytes


# 因为是在高级语言中，运算时会自动补全
def signExtend(value):
    return value


if __name__=="__main__":
    reg = registerFile()
    mem = memory()

    # mem和reg的用法测试
    # print(reg.read('pc'))
    # print(reg.read(1))
    # mem.write(0, 20)
    # print(mem.read(0))
    # print(bin(mem.read(0))[2:].zfill(32)[-5:])
    # mem.write(4, int(-25))
    # print(mem.read(4))

    # print(bin(5))
    # print(type(bin(5)))

    """
    汇编代码：
    000: lw      x1,100(x0)
    x2初始化为2
    004: add     x3,x1,x2
    008: addi    x4,1(x3)
    012: beq     x4,x4,4
    ...
    020: jal     x5,8
    ...
    032: HALT(停机)

    100: 值 1
    """
    reg.write(2, 2)
    mem.write(100, 1)
    mem.write(0, 0x06402083)
    mem.write(4, 0x002081b3)
    mem.write(8, 0x00118213)
    mem.write(12, 0x00420463)
    mem.write(20, 0x010002ef)

    while True:
        # 取指
        pc = reg.read('pc')
        # print("pc = ", pc)
        ir = mem.read(pc)
        pc += 4
        # 译码
        # print("ir = ", ir)
        opcode = ir & 0x7f
        # print("opcode = ", hex(opcode))
        rs1, rs2, rd, imm = 0, 0, 0, 0
        # lw
        if(opcode == 0x03):
            rd = (ir >> 7) & 0x1f
            rs1 = (ir >> 15) & 0x1f
            imm = (ir >> 20)
        # add
        elif(opcode == 0x33):
            rd = (ir >> 7) & 0x1f
            rs1 = (ir >> 15) & 0x1f
            rs2 = (ir >> 20) & 0x1f
            # print("ID_rs1 = ", rs1)
            # print("ID_rs2 = ", rs2)
        # addi
        elif(opcode == 0x13):
            rd = (ir >> 7) & 0x1f
            rs1 = (ir >> 15) & 0x1f
            imm = (ir >> 20)
        # beq
        elif(opcode == 0x63):
            rs1 = (ir >> 15) & 0x1f
            rs2 = (ir >> 20) & 0x1f
            imm = ((ir >> 8) & 0xf) + (((ir >> 25) & 0x3f) << 4) + (((ir >> 7) & 0x1) << 10) + ((ir >> 31) << 11)
        # jal
        elif(opcode == 0x6f):
            rd = (ir >> 7) & 0x1f
            imm = ((ir >> 21) & 0x3ff) + (((ir >> 20) & 0x1) << 10) + (((ir >> 12) & 0xff) << 11) + (((ir >> 31) & 0x1) << 19)
        # 到达终点
        elif(opcode == 0x00):
            break
        else:
            raise Exception("Unknown opcode")
        
        rs1 = reg.read(rs1)
        rs2 = reg.read(rs2)
        
        # 执行
        # lw
        rdt, pct = 0, 0
        if(opcode == 0x03):
            rdt = rs1 + imm
            # print("EXE_rdt = ", rdt)
        # add
        elif(opcode == 0x33):
            rdt = rs1 + rs2
            # print("EXE_rdt = ", rdt)
        # addi
        elif(opcode == 0x13):
            rdt = rs1 + imm
        # beq
        elif(opcode == 0x63):
            pct = pc + imm
            if rs1 == rs2:
                pc = pct
        # jal
        elif(opcode == 0x6f):
            rdt = pc
            pc = pc + imm

        # 访存
        # lw
        if(opcode == 0x03):
            rdt = mem.read(rdt)
            # print("MEM_rdt = ", rdt)

        # 写回
        # beq
        if(opcode != 0x63):
            reg.write(rd, rdt)
        reg.write('pc', pc)

    print(reg.read(1))
    print(reg.read(2))
    print(reg.read(3))
    print(reg.read(4))
    print(reg.read(5))
    print("pc = ", pc)
