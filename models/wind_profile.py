import numpy as np
from typing import Union, List

class WindProfile:
    """
    고도에 따른 풍속 프로파일을 계산하는 클래스
    지상 풍속을 기반으로 고도별 풍속을 계산합니다.
    타워 쉐도우 효과를 포함합니다.
    """
    
    def __init__(self, reference_height: float = 10.0,
                 reference_speed: float = 2.0,  # 지상 10m에서의 풍속
                 power_law_exponent: float = 0.14,
                 tower_diameter: float = 4.0):  # 타워 직경 (미터)
        """
        초기화 함수
        
        Args:
            reference_height: 기준 고도 (미터)
            reference_speed: 기준 고도에서의 풍속 (m/s)
            power_law_exponent: 지수 법칙 지수 (기본값: 0.14)
            tower_diameter: 타워 직경 (미터)
        """
        self.reference_height = reference_height
        self.reference_speed = reference_speed
        self.power_law_exponent = power_law_exponent
        self.tower_diameter = tower_diameter
        
        # 타워 쉐도우 효과 상수
        self.shadow_length = 5.0  # 타워 직경의 5배까지 영향
        self.max_shadow_effect = 0.3  # 최대 30% 풍속 감소
    
    def calculate_wind_speed(self, height: Union[float, np.ndarray],
                           distance_from_tower: float = 0.0) -> Union[float, np.ndarray]:
        """
        주어진 고도에서의 풍속을 계산합니다.
        지수 법칙과 타워 쉐도우 효과를 고려합니다.
        
        Args:
            height: 고도 (미터)
            distance_from_tower: 타워로부터의 수평 거리 (미터)
            
        Returns:
            해당 고도에서의 풍속 (m/s)
        """
        # 기본 풍속 계산 (지수 법칙)
        wind_speed = self.reference_speed * (height / self.reference_height) ** self.power_law_exponent
        
        # 타워 쉐도우 효과 계산
        if distance_from_tower < self.shadow_length * self.tower_diameter:
            # 타워로부터의 거리에 따른 쉐도우 효과 계산
            shadow_factor = (1 - distance_from_tower / (self.shadow_length * self.tower_diameter))
            shadow_effect = self.max_shadow_effect * shadow_factor
            
            # 풍속 감소 적용
            wind_speed = wind_speed * (1 - shadow_effect)
        
        return wind_speed
    
    def calculate_wind_speeds(self, heights: np.ndarray,
                            distance_from_tower: float = 0.0) -> np.ndarray:
        """
        여러 고도에서의 풍속을 계산합니다.
        
        Args:
            heights: 고도 배열 (미터)
            distance_from_tower: 타워로부터의 수평 거리 (미터)
            
        Returns:
            각 고도에서의 풍속 배열 (m/s)
        """
        return self.calculate_wind_speed(heights, distance_from_tower)
    
    def calculate_wind_profile(self, heights: np.ndarray,
                             distance_from_tower: float = 0.0) -> np.ndarray:
        """
        여러 고도에서의 풍속 프로파일을 계산합니다.
        
        Args:
            heights: 계산할 고도 배열 (미터)
            distance_from_tower: 타워로부터의 수평 거리 (미터)
            
        Returns:
            각 고도에서의 풍속 배열 (m/s)
        """
        return self.calculate_wind_speed(heights, distance_from_tower)
    
    def get_wind_shear(self, height: float,
                      distance_from_tower: float = 0.0) -> float:
        """
        주어진 고도에서의 풍속 전단을 계산합니다.
        
        Args:
            height: 계산할 고도 (미터)
            distance_from_tower: 타워로부터의 수평 거리 (미터)
            
        Returns:
            풍속 전단 (m/s/m)
        """
        # 기본 풍속 전단 계산
        wind_shear = (self.power_law_exponent * self.reference_speed * 
                     (height / self.reference_height) ** (self.power_law_exponent - 1) / 
                     self.reference_height)
        
        # 타워 쉐도우 효과가 있는 경우 전단도 감소
        if distance_from_tower < self.shadow_length * self.tower_diameter:
            shadow_factor = (1 - distance_from_tower / (self.shadow_length * self.tower_diameter))
            shadow_effect = self.max_shadow_effect * shadow_factor
            wind_shear *= (1 - shadow_effect)
        
        return wind_shear
