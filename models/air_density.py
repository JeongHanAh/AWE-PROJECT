import numpy as np
from typing import Union, List

class AirDensity:
    """
    고도에 따른 공기 밀도 변화를 계산하는 클래스
    국제 표준 대기 모델을 기반으로 합니다.
    """
    
    def __init__(self, sea_level_density: float = 1.225,
                 temperature_lapse_rate: float = 0.0065,
                 sea_level_temperature: float = 288.15):
        """
        초기화 함수
        
        Args:
            sea_level_density: 해수면 공기 밀도 (kg/m³)
            temperature_lapse_rate: 온도 감소율 (K/m)
            sea_level_temperature: 해수면 온도 (K)
        """
        self.sea_level_density = sea_level_density
        self.temperature_lapse_rate = temperature_lapse_rate
        self.sea_level_temperature = sea_level_temperature
        self.g = 9.80665  # 중력 가속도 (m/s²)
        self.R = 287.05   # 공기의 기체 상수 (J/kg·K)
    
    def calculate_temperature(self, height: Union[float, List[float], np.ndarray]) -> Union[float, np.ndarray]:
        """
        주어진 고도에서의 온도를 계산합니다.
        
        Args:
            height: 계산할 고도 (미터)
            
        Returns:
            계산된 온도 (K)
        """
        height = np.asarray(height)
        return self.sea_level_temperature - self.temperature_lapse_rate * height
    
    def calculate_density(self, height: Union[float, List[float], np.ndarray]) -> Union[float, np.ndarray]:
        """
        주어진 고도에서의 공기 밀도를 계산합니다.
        
        Args:
            height: 계산할 고도 (미터)
            
        Returns:
            계산된 공기 밀도 (kg/m³)
        """
        height = np.asarray(height)
        temperature = self.calculate_temperature(height)
        
        # 대기압 계산 (Pa)
        pressure = 101325 * (1 - self.temperature_lapse_rate * height / self.sea_level_temperature) ** (self.g / (self.R * self.temperature_lapse_rate))
        
        # 이상 기체 법칙을 사용하여 밀도 계산
        density = pressure / (self.R * temperature)
        
        return density
    
    def calculate_density_profile(self, heights: np.ndarray) -> np.ndarray:
        """
        여러 고도에서의 공기 밀도 프로파일을 계산합니다.
        
        Args:
            heights: 계산할 고도 배열 (미터)
            
        Returns:
            각 고도에서의 공기 밀도 배열 (kg/m³)
        """
        return self.calculate_density(heights)
