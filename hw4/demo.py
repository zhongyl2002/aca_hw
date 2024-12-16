# 使用了一些科技😋快速完成

# BTB包含的域：pc of a branch & predicted pc
# Only predicted taken brach stores in BTB

BPB_SIZE = 1024  # BPB 表大小 
BTB_SIZE = 256   # BTB 表大小
MAX_HISTORY = 3  # BPB 2-bit 计数器最大值

class BranchPredictor:
    def __init__(self):
        # 初始化 BPB: 1K项，每个项是一个2-bit计数器
        self.BPB = [2] * BPB_SIZE
        
        # 初始化 BTB: 使用字典存储分支 PC 和目标地址
        self.BTB = {}

    # BPB 功能：根据分支地址预测跳转方向
    def predict_direction(self, branch_address):
        index = branch_address % BPB_SIZE
        prediction = self.BPB[index]
        return prediction >= 2

    # BTB 功能：根据分支地址查询目标地址
    def get_target_address(self, branch_address):
        return self.BTB.get(branch_address % BTB_SIZE, None)

    # 更新 BPB：根据实际跳转结果更新 2-bit 计数器
    def update_bpb(self, branch_address, taken):
        index = branch_address % BPB_SIZE
        if taken:
            if self.BPB[index] < MAX_HISTORY:
                self.BPB[index] += 1
        else:
            if self.BPB[index] > 0:
                self.BPB[index] -= 1

    # 更新 BTB：仅当 BPB 预测跳转且实际发生跳转时更新
    def update_btb(self, branch_address, target_address, taken):
        if taken:
            # 如果 BTB 超出大小限制，移除最老的项 (简单 FIFO 策略)
            if len(self.BTB) >= BTB_SIZE:
                self.BTB.pop(next(iter(self.BTB)))
            
            # 更新 BTB 表项
            self.BTB[branch_address] = target_address

    def display_btb(self):
        """
        打印 BTB 内容，用于调试。
        """
        print("BTB Contents:")
        for pc, target in self.BTB.items():
            print(f"Branch PC: {pc:#06x}, Predicted PC: {target:#06x}")
        print("-" * 40)


# 模拟分支预测器
if __name__ == "__main__":
    predictor = BranchPredictor()
    
    # 模拟分支指令和跳转行为
    # 格式：(分支 PC, 目标 PC, 是否跳转)
    branches = [
        (0x1000, 0x2000, True),
        (0x1004, 0x3000, True),
        (0x1008, None, False),
        (0x100C, 0x4000, True),
        (0x1010, None, False),
    ]

    for branch_pc, target_pc, taken in branches:
        print(f"Branch PC: {branch_pc:#06x}, Taken: {taken}")
        
        # 预测分支方向
        predicted_taken = predictor.predict_direction(branch_pc)
        print(f"  Predicted Direction: {'TAKEN' if predicted_taken else 'NOT TAKEN'}")
        
        # 如果预测跳转，查询 BTB 获取目标地址
        if predicted_taken:
            target_address = predictor.get_target_address(branch_pc)
            if target_address:
                print(f"  Predicted Target Address: {target_address:#06x}")
            else:
                print("  No Target Address in BTB")

        # 更新 BPB 和 BTB
        predictor.update_bpb(branch_pc, taken)
        if taken and target_pc is not None:
            predictor.update_btb(branch_pc, target_pc, taken)
            print(f"  BTB Updated: {branch_pc:#06x} -> {target_pc:#06x}")

        print("-" * 50)

    # 打印最终 BTB 表内容
    predictor.display_btb()
