"""
雪花算法ID生成器
Snowflake ID Generator

雪花ID结构（64位）：
- 1位：符号位（0）
- 41位：时间戳（毫秒）
- 10位：数据中心ID + 机器ID
- 12位：序列号
"""

import time
from threading import Lock


class SnowflakeGenerator:
    """雪花算法ID生成器"""
    
    # 定义各部分的位数
    TIMESTAMP_BITS = 41
    DATACENTER_BITS = 5
    MACHINE_BITS = 5
    SEQUENCE_BITS = 12
    
    # 定义最大值
    MAX_DATACENTER_ID = (1 << DATACENTER_BITS) - 1  # 31
    MAX_MACHINE_ID = (1 << MACHINE_BITS) - 1  # 31
    MAX_SEQUENCE = (1 << SEQUENCE_BITS) - 1  # 4095
    
    # 定义偏移量
    MACHINE_SHIFT = SEQUENCE_BITS
    DATACENTER_SHIFT = SEQUENCE_BITS + MACHINE_BITS
    TIMESTAMP_SHIFT = SEQUENCE_BITS + MACHINE_BITS + DATACENTER_BITS
    
    # 时间戳基准点（2020-01-01）
    EPOCH = 1577836800000
    
    def __init__(self, datacenter_id: int = 1, machine_id: int = 1):
        """
        初始化雪花算法生成器
        
        Args:
            datacenter_id: 数据中心ID (0-31)
            machine_id: 机器ID (0-31)
        """
        if not (0 <= datacenter_id <= self.MAX_DATACENTER_ID):
            raise ValueError(f"datacenter_id must be between 0 and {self.MAX_DATACENTER_ID}")
        if not (0 <= machine_id <= self.MAX_MACHINE_ID):
            raise ValueError(f"machine_id must be between 0 and {self.MAX_MACHINE_ID}")
        
        self.datacenter_id = datacenter_id
        self.machine_id = machine_id
        self.sequence = 0
        self.last_timestamp = -1
        self.lock = Lock()
    
    def generate(self) -> int:
        """生成雪花ID"""
        with self.lock:
            current_timestamp = int(time.time() * 1000)
            
            if current_timestamp < self.last_timestamp:
                raise Exception("Clock moved backwards. Refusing to generate ID")
            
            if current_timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & self.MAX_SEQUENCE
                if self.sequence == 0:
                    # 序列号溢出，等待下一毫秒
                    current_timestamp = self._wait_next_millis(self.last_timestamp)
            else:
                self.sequence = 0
            
            self.last_timestamp = current_timestamp
            
            # 组合ID
            timestamp_value = (current_timestamp - self.EPOCH) & ((1 << self.TIMESTAMP_BITS) - 1)
            id_value = (timestamp_value << self.TIMESTAMP_SHIFT) | \
                      (self.datacenter_id << self.DATACENTER_SHIFT) | \
                      (self.machine_id << self.MACHINE_SHIFT) | \
                      self.sequence
            
            return id_value
    
    @staticmethod
    def _wait_next_millis(last_timestamp: int) -> int:
        """等待下一毫秒"""
        current_timestamp = int(time.time() * 1000)
        while current_timestamp <= last_timestamp:
            current_timestamp = int(time.time() * 1000)
        return current_timestamp


# 全局实例
_snowflake_generator = SnowflakeGenerator(datacenter_id=1, machine_id=1)


def generate_snowflake_id() -> int:
    """生成雪花ID的便捷函数"""
    return _snowflake_generator.generate()
