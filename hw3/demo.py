class instructionStatusItem:
    def __init__(self, instruction:str, latency:int):
        self.instruction = instruction
        self.issue = -1
        self.read = -1
        self.execute = -1
        self.write = -1
        self.latency = latency
        self.fuId = -1


class functionUnitStatusItem:
    def __init__(self, name:str, type:str):
        self.name = name
        self.type = type
        self.busy = False
        self.op = ""
        self.fi = -1
        self.fj = -1
        self.fk = -1
        self.qj = ""
        self.qk = ""
        self.rj = False
        self.rk = False
        self.leftCycle = 0

    def reset(self):
        self.busy = False
        self.op = ""
        self.fi = -1
        self.fj = -1
        self.fk = -1
        self.qj = ""
        self.qk = ""
        self.rj = False
        self.rk = False
        self.leftCycle = 0


class registerStatus:
    def __init__(self):
        self.regStatus = {f"F{i}": "null" for i in range(16)}


# 检查是否结束
def checkEnd(instructionStatus:list[instructionStatusItem]):
    for i in range(6):
        if(instructionStatus[i].write == -1):
            return False
    return True


# 检查结构冒险
def checkStruct(functionUnitStatus, op):
    if(op == "L.D" and (not functionUnitStatus[0].busy)):
        return 0
    elif(op == "MUL.D" and (not functionUnitStatus[1].busy)):
        return 1
    elif(op == "MUL.D" and (not functionUnitStatus[2].busy)):
        return 2
    elif((op == "ADD.D" or op == "SUB.D") and (not functionUnitStatus[3].busy)):
        return 3
    elif(op == "DIV.D" and (not functionUnitStatus[4].busy)):
        return 4
    else:
        return -1


# 检查WAR
def checkWAR(instructionStatus:list[instructionStatusItem], functionUnitStatus:list[functionUnitStatusItem], rd:str, iid:int):
    for i in range(6):
        if(instructionStatus[i].issue != -1 and instructionStatus[i].read == -1):
            if(functionUnitStatus[instructionStatus[i].fuId].op == "L.D"):
                if((functionUnitStatus[instructionStatus[i].fuId].rj == True) and (functionUnitStatus[instructionStatus[i].fuId].fj == rd)):
                    return False
            else:
                if((functionUnitStatus[instructionStatus[i].fuId].rj == True and functionUnitStatus[instructionStatus[i].fuId].rk == True) and\
                   (functionUnitStatus[instructionStatus[i].fuId].fj == rd or functionUnitStatus[instructionStatus[i].fuId].fk == rd)):
                    return False
    return True


# WB阶段后更新功能单元表格
def updateAWB(instructionStatus:list[instructionStatusItem], functionUnitStatus:list[functionUnitStatusItem], rd:str, iid:int):
    for i in range(6):
        if(instructionStatus[i].issue != -1 and instructionStatus[i].read == -1):
            if((functionUnitStatus[instructionStatus[i].fuId].rj == False) and (functionUnitStatus[instructionStatus[i].fuId].fj == rd)):
                functionUnitStatus[instructionStatus[i].fuId].qj = "null"
                functionUnitStatus[instructionStatus[i].fuId].rj = True
            if(functionUnitStatus[instructionStatus[i].fuId].op != "L.D"):
                if((functionUnitStatus[instructionStatus[i].fuId].rk == False) and (functionUnitStatus[instructionStatus[i].fuId].fk == rd)):
                    functionUnitStatus[instructionStatus[i].fuId].qk = "null"
                    functionUnitStatus[instructionStatus[i].fuId].rk = True
            print("-->>update AWB :")


# 输出显示表格数据
def display(cycleNumber:int, instructionStatus:list[instructionStatusItem], functionUnitStatus:list[functionUnitStatusItem], regs:registerStatus):
    print("========\nCycle: ", cycleNumber)
    print("instruction\t\t\tissue\t\tread\t\texecute\t\twrite")
    for i in range(6):
        print(instructionStatus[i].instruction, "\t\t\t", instructionStatus[i].issue, "\t\t", instructionStatus[i].read, "\t\t", instructionStatus[i].execute, "\t\t", instructionStatus[i].write)
    print("leftCycle\t\t\tname\t\tbusy\t\top\t\tfi\t\tfj\t\tfk\t\tqj\t\tqk\t\trj\t\trk")
    for i in range(5):
        print(functionUnitStatus[i].leftCycle, "\t\t\t", functionUnitStatus[i].name, "\t\t", functionUnitStatus[i].busy, "\t\t", functionUnitStatus[i].op, "\t\t", functionUnitStatus[i].fi, "\t\t", functionUnitStatus[i].fj, "\t\t", functionUnitStatus[i].fk, "\t\t", functionUnitStatus[i].qj, "\t\t", functionUnitStatus[i].qk, "\t\t", functionUnitStatus[i].rj, "\t\t", functionUnitStatus[i].rk)
    print("regStatus")
    for i in regs.regStatus.keys():
        print(i, end="\t")
    print("\n")
    for i in regs.regStatus.values():
        print(i, end="\t")
    print("\n")


if __name__=="__main__":
    instructionStatus = [
                            instructionStatusItem("L.D F6,34(R2)", 1),      \
                            instructionStatusItem("L.D F2,45(R3)", 1),      \
                            instructionStatusItem("MUL.D F0,F2,F4", 10),    \
                            instructionStatusItem("SUB.D F8,F2,F6", 2),     \
                            instructionStatusItem("DIV.D F10,F0,F6", 40),   \
                            instructionStatusItem("ADD.D F6,F8,F2", 2),     \
                        ]
    currentInstruction = 0

    functionUnitStatus = [
                            functionUnitStatusItem("Integer", "Integer"),   \
                            functionUnitStatusItem("Mult1", "Mult"),        \
                            functionUnitStatusItem("Mult2", "Mult"),        \
                            functionUnitStatusItem("Add", "Add"),           \
                            functionUnitStatusItem("Divide", "Divide"),     \
                        ]

    regs = registerStatus()
    regs.regStatus["R2"] = "null"
    regs.regStatus["R3"] = "null"

    cycleNumber = 1

    while not checkEnd(instructionStatus):

        # 译码逻辑
        if(currentInstruction != 6):
            op = instructionStatus[currentInstruction].instruction.split(" ")[0]
            rd = instructionStatus[currentInstruction].instruction.split(" ")[1].split(",")[0]
            rj = instructionStatus[currentInstruction].instruction.split(" ")[1].split(",")[1]
            if(op == "L.D"):
                rj = rj.split("(")[1].split(")")[0]
            if(op != "L.D"):
                rk = instructionStatus[currentInstruction].instruction.split(" ")[1].split(",")[2]

            # print("========\nCycle: ", cycleNumber)
            # print("op = ", op, "rd = ", rd, "rj = ", rj, end=" ")
            # if(op != "L.D"):
            #     print("rk = ", rk, end=" ")
            # print("\n")
            # currentInstruction += 1
            # continue

            # Issue——检查结构冒险和WAW
            fuId = checkStruct(functionUnitStatus, op)
            if(regs.regStatus[rd] == "null" and fuId != -1):
                # 指令状态更新
                instructionStatus[currentInstruction].issue = cycleNumber
                instructionStatus[currentInstruction].fuId = fuId

                # 功能单元状态更新
                functionUnitStatus[fuId].busy = True
                functionUnitStatus[fuId].op = op
                functionUnitStatus[fuId].fi = rd
                functionUnitStatus[fuId].fj = rj
                if(regs.regStatus[rj] == "null"):
                    functionUnitStatus[fuId].qj = "null"
                    functionUnitStatus[fuId].rj = True
                else:
                    functionUnitStatus[fuId].qj = regs.regStatus[rj]
                    functionUnitStatus[fuId].rj = False
                # rk特殊处理
                if(op != "L.D"):
                    functionUnitStatus[fuId].fk = rk
                    if(regs.regStatus[rk] == "null"):
                        functionUnitStatus[fuId].qk = "null"
                        functionUnitStatus[fuId].rk = True
                    else:
                        functionUnitStatus[fuId].qk = regs.regStatus[rk]
                        functionUnitStatus[fuId].rk = False

                # 寄存器状态更新
                regs.regStatus[rd] = functionUnitStatus[fuId].name

                currentInstruction += 1
        
        # Read——检查RAW
        for i in range(6):
            if(instructionStatus[i].issue != -1 and instructionStatus[i].read == -1 and instructionStatus[i].issue < cycleNumber):
                if(functionUnitStatus[instructionStatus[i].fuId].op != "L.D" and functionUnitStatus[instructionStatus[i].fuId].rj and functionUnitStatus[instructionStatus[i].fuId].qj):
                    # 指令状态表
                    instructionStatus[i].read = cycleNumber
                    # 功能单元状态表
                    functionUnitStatus[instructionStatus[i].fuId].rj = False
                    functionUnitStatus[instructionStatus[i].fuId].rk = False
                elif(functionUnitStatus[instructionStatus[i].fuId].rj):
                    # 指令状态表
                    instructionStatus[i].read = cycleNumber
                    # 功能单元状态表
                    functionUnitStatus[instructionStatus[i].fuId].rj = False
                functionUnitStatus[instructionStatus[i].fuId].leftCycle = instructionStatus[i].latency


        # Execute——更新剩余周期数
        for i in range(6):
            if(instructionStatus[i].read != -1 and instructionStatus[i].execute == -1 and instructionStatus[i].read < cycleNumber):
                functionUnitStatus[instructionStatus[i].fuId].leftCycle -= 1
                if(functionUnitStatus[instructionStatus[i].fuId].leftCycle == 0):
                    instructionStatus[i].execute = cycleNumber


        # WB——检查WAR(变No之前不能写) & 更新Rj、Rk
        for i in range(6):
            if(instructionStatus[i].execute != -1 and instructionStatus[i].write == -1 and instructionStatus[i].execute < cycleNumber):
                if(checkWAR(instructionStatus, functionUnitStatus, functionUnitStatus[instructionStatus[i].fuId].fi, i)):
                    # 指令状态表
                    instructionStatus[i].write = cycleNumber
                    # 寄存器状态表
                    regs.regStatus[functionUnitStatus[instructionStatus[i].fuId].fi] = "null"
                    print("-->>update regs :", functionUnitStatus[instructionStatus[i].fuId].fi)
                    # 功能单元状态表id
                    updateAWB(instructionStatus, functionUnitStatus, functionUnitStatus[instructionStatus[i].fuId].fi, i)

                    # for j in range(6):
                    #     print("---->i = ", i)
                    #     print("---->j = ", j)
                    #     if(instructionStatus[j].issue != -1 and instructionStatus[j].read == -1):
                    #         print("hellllllo")
                    #         if((functionUnitStatus[instructionStatus[j].fuId].rj == False) and (functionUnitStatus[instructionStatus[j].fuId].fj == rd)):
                    #             functionUnitStatus[instructionStatus[j].fuId].qj = "null"
                    #             functionUnitStatus[instructionStatus[j].fuId].rj = True
                    #         if(functionUnitStatus[instructionStatus[j].fuId].op != "L.D"):
                    #             if((functionUnitStatus[instructionStatus[j].fuId].rk == False) and (functionUnitStatus[instructionStatus[j].fuId].fk == rd)):
                    #                 functionUnitStatus[instructionStatus[j].fuId].qk = "null"
                    #                 functionUnitStatus[instructionStatus[j].fuId].rk = True
                    #         print("-->>update AWB :")
                    functionUnitStatus[instructionStatus[i].fuId].reset()

        display(cycleNumber, instructionStatus, functionUnitStatus, regs)
        cycleNumber += 1
        
