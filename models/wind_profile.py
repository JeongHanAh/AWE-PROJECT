import numpy as np
from typing import Union, List

class WindProfile:
    """
    고도에 따른 풍속 변화를 계산하는 클래스
    지수 법칙(Power Law)을 사용하여 풍속 프로파일을 계산합니다.
    """
    
    def __init__(self, reference_height: float, reference_speed: float,
                 power_law_exponent: float = 0.14, tower_diameter: float = 4.0):
        """
        초기화 함수
        
        Args:
            reference_height: 기준 고도 (m)
            reference_speed: 기준 고도에서의 풍속 (m/s)
            power_law_exponent: 지수 법칙 지수 (기본값: 0.14)
                               - 지상형 터빈: 0.1-0.2
                               - AWE 시스템: 0.1-0.15
            tower_diameter: 타워 직경 (m)
        """
        self.reference_height = float(reference_height)
        self.reference_speed = float(reference_speed)
        self.power_law_exponent = float(power_law_exponent)
        self.tower_diameter = float(tower_diameter)
        
    def calculate_wind_speed(self, height: float, time: float = 0.0) -> float:
        """
        주어진 고도와 시간에서의 풍속을 계산합니다.
        
        Args:
            height: 계산할 고도 (m)
            time: 시간 (분)
            
        Returns:
            계산된 풍속 (m/s)
        """
        # 기본 풍속 계산 (파워 로우 모델)
        base_speed = self.reference_speed * (height / self.reference_height) ** self.power_law_exponent
        
        # 시간에 따른 풍속 변동 추가 (사인파)
        time_variation = 0.2 * self.reference_speed * np.sin(2 * np.pi * time / 60)  # 1시간 주기
        
        # 난류 효과 추가 (가우시안 노이즈)
        turbulence = 0.1 * self.reference_speed * np.random.normal(0, 1)
        
        # 최종 풍속 계산
        wind_speed = base_speed + time_variation + turbulence
        
        # 풍속이 음수가 되지 않도록 보정
        return max(wind_speed, 0.1)
    
    def calculate_wind_speeds(self, heights: np.ndarray, time: float = 0.0) -> np.ndarray:
        """
        여러 고도에서의 풍속을 계산합니다.
        
        Args:
            heights: 고도 배열 (m)
            time: 시간 (분)
            
        Returns:
            각 고도에서의 풍속 배열 (m/s)
        """
        return np.array([self.calculate_wind_speed(h, time) for h in heights])
    
    def calculate_wind_profile(self, heights: np.ndarray, time: float = 0.0) -> np.ndarray:
        """
        여러 고도에서의 풍속 프로파일을 계산합니다.
        
        Args:
            heights: 계산할 고도 배열 (m)
            time: 시간 (분)
            
        Returns:
            각 고도에서의 풍속 배열 (m/s)
        """
        return self.calculate_wind_speeds(heights, time)
    
    def get_wind_shear(self, height: float, time: float = 0.0) -> float:
        """
        주어진 고도에서의 풍속 전단을 계산합니다.
        
        Args:
            height: 계산할 고도 (m)
            time: 시간 (분)
            
        Returns:
            풍속 전단 (m/s/m)
        """
        # 기본 풍속 전단 계산
        wind_shear = (self.power_law_exponent * self.reference_speed * 
                     (height / self.reference_height) ** (self.power_law_exponent - 1) / 
                     self.reference_height)
        
        # 시간에 따른 전단 변동 추가
        time_variation = 0.1 * wind_shear * np.sin(2 * np.pi * time / 60)
        
        return wind_shear + time_variation
