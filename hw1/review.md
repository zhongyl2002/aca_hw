# 作业一回顾

## 教材内容回顾

### 计算机类型的分类

不同设备在预算、需求方面存在不同

- 物联网设备
- 移动设备
- 桌面计算机
- 服务器、集群/仓库级计算机

### 并行度与并行体系结构分类

指令集分类，RISC-V指令集详细介绍

软件并行分类：

- DLP
- TLP

硬件并行分类：

- ILP
- 线程级并行
- 请求级并行

并行体系结构分类：

- SISD
- SIMD
- MISD
- MIMD

### 计算机体系结构的定义

不同时期定义有所不同，现在包含编程模型、操作系统、ISA、微体系结构、电路、算法

### 提升性能的方法

1. 充分利用并行
2. 利用局部性原理
3. Amdahl定律，关注重点
4. 提升常用场景性能

处理器性能评价方法，量化指标


## 博客内容评价

这篇文章主要是关于当时即将发布的Intel 11代移动端cpu的介绍文章。

该芯片较上一代使用了新的核心架构—Willow Cove cores，新增了Xe LP graphics、媒体引擎、支持8k播放的播放引擎、支持4k90的IPU6，增大了L3级缓存，增加LPDDR5支持。

文中列举了与友商的对比数据，横向比较。

文中提到“与10代Ice Lake芯片上的10nm工艺相比，性能提升了大约17-18%”，验证了课本展示的芯片性能进步幅度

这篇文章提到了我当时忽略的内容：使用集成显卡支持ai需求、芯片安全，这些在当时选电脑时没有特别关注