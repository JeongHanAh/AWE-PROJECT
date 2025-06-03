import numpy as np
from typing import Union, Tuple
from models.power_calc import PowerCalculator

class AWEPowerCalculator(PowerCalculator):
    """
    AWE(Airborne Wind Energy) 시스템의 전력 계산을 위한 클래스
    PowerCalculator를 상속받아 AWE 시스템 특성에 맞게 전력 생산량을 계산합니다.
    """
    
    def __init__(self, operating_height: float, tether_length: float,
                 rated_power: float, min_wind_speed: float, max_wind_speed: float,
                 power_coefficient: float = 0.35):
        """
        초기화 함수
        
        Args:
            operating_height: 작동 고도 (m)
            tether_length: 테더 길이 (m)
            rated_power: 정격 출력 (kW)
            min_wind_speed: 최소 작동 풍속 (m/s)
            max_wind_speed: 최대 작동 풍속 (m/s)
            power_coefficient: 전력 계수 (기본값: 0.35)
        """
        super().__init__(
            rated_power=rated_power,
            cut_in_speed=min_wind_speed,
            cut_out_speed=max_wind_speed,
            power_coefficient=power_coefficient
        )
        self.operating_height = float(operating_height)
        self.tether_length = float(tether_length) 