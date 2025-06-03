import numpy as np
from typing import Union, Tuple, List

class PowerCalculator:
    """
    풍력 발전 시스템의 전력 계산을 위한 기본 클래스
    풍속과 시스템 특성을 기반으로 전력 생산량을 계산합니다.
    """
    
    def __init__(self, rated_power: float, cut_in_speed: float, cut_out_speed: float,
                 power_coefficient: float = 0.4):
        """
        초기화 함수
        
        Args:
            rated_power: 정격 출력 (kW)
            cut_in_speed: 컷인 풍속 (m/s)
            cut_out_speed: 컷아웃 풍속 (m/s)
            power_coefficient: 전력 계수 (기본값: 0.4)
        """
        self.rated_power = float(rated_power)
        self.cut_in_speed = float(cut_in_speed)
        self.cut_out_speed = float(cut_out_speed)
        self.power_coefficient = float(power_coefficient)
        
    def calculate_power(self, wind_speed: Union[float, np.ndarray],
                       air_density: Union[float, np.ndarray] = 1.225) -> np.ndarray:
        """
        주어진 풍속에서의 전력 생산량을 계산합니다.
        
        Args:
            wind_speed: 풍속 (m/s)
            air_density: 공기 밀도 (kg/m³)
            
        Returns:
            전력 생산량 배열 (kW)
        """
        # 입력값을 numpy 배열로 변환
        wind_speed = np.asarray(wind_speed, dtype=float)
        air_density = np.asarray(air_density, dtype=float)
        
        # 배열 크기가 다른 경우 브로드캐스팅
        if wind_speed.shape != air_density.shape:
            air_density = np.full_like(wind_speed, air_density)
        
        # 기본 전력 계산 (P ∝ ρv³)
        power = self.power_coefficient * air_density * wind_speed**3
        
        # 컷인/컷아웃 풍속 조건 적용
        power = np.where((wind_speed >= self.cut_in_speed) & 
                        (wind_speed <= self.cut_out_speed),
                        power, 0.0)
        
        # 정격 출력 제한
        power = np.minimum(power, self.rated_power)
        
        return power
    
    def calculate_power_curve(self, wind_speeds: np.ndarray,
                            air_density: float = 1.225) -> Tuple[np.ndarray, np.ndarray]:
        """
        풍속에 따른 전력 곡선을 계산합니다.
        
        Args:
            wind_speeds: 풍속 배열 (m/s)
            air_density: 공기 밀도 (kg/m³)
            
        Returns:
            (풍속 배열, 전력 생산량 배열) 튜플
        """
        wind_speeds = np.asarray(wind_speeds, dtype=float)
        power = self.calculate_power(wind_speeds, air_density)
        return wind_speeds, power
    
    def calculate_annual_energy(self, wind_speeds: np.ndarray,
                              air_density: float = 1.225,
                              time_step: float = 1.0) -> float:
        """
        연간 에너지 생산량을 계산합니다.
        
        Args:
            wind_speeds: 시간별 풍속 배열 (m/s)
            air_density: 공기 밀도 (kg/m³)
            time_step: 시간 간격 (시간)
            
        Returns:
            연간 에너지 생산량 (kWh)
        """
        wind_speeds = np.asarray(wind_speeds, dtype=float)
        power = self.calculate_power(wind_speeds, air_density)
        energy = np.sum(power * time_step)
        return float(energy)
