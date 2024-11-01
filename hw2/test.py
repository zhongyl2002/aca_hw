def sign_extend(value: int, bit_width: int) -> int:
    """
    对指定宽度的有符号整数进行符号扩展。
    
    参数:
    value (int): 需要扩展的数值（假定是一个有符号整数）。
    bit_width (int): 输入的位宽，例如 8, 16, 等。

    返回:
    int: 扩展后的 32 位有符号整数。
    """
    # 确保输入位宽是一个正整数
    if bit_width <= 0:
        raise ValueError("位宽必须是一个正整数")

    # 计算符号位的位置
    sign_bit = 1 << (bit_width - 1)

    # 检查符号位是否为 1
    if value & sign_bit:
        # 扩展高位为 1
        return value | (~((1 << bit_width) - 1))
    else:
        # 高位保持为 0
        return value & ((1 << bit_width) - 1)

# 测试例子
print(bin(sign_extend(0b10010110, 16)))  # 对 8 位数进行符号扩展，结果应该是 -106
print(bin(sign_extend(0b00010110, 16)))  # 对 8 位数进行符号扩展，结果应该是 22
print((sign_extend(0b1000000000000010, 32)))  # 对 16 位数进行符号扩展，结果应该是 -32766
