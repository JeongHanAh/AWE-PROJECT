import numpy as np
from typing import Union, List

class AirDensity:
    """
    고도에 따른 공기 밀도를 계산하는 클래스
    지수 감소 모델을 사용하여 공기 밀도를 계산합니다.
    """
    
    def __init__(self, sea_level_density: float = 1.225,
                 temperature_lapse_rate: float = 0.04,
                 sea_level_temperature: float = 288.15):
        """
        초기화 함수
        
        Args:
            sea_level_density: 해수면 공기 밀도 (kg/m³)
            temperature_lapse_rate: 온도 감소율 (K/m)
            sea_level_temperature: 해수면 온도 (K)
        """
        self.sea_level_density = float(sea_level_density)
        self.temperature_lapse_rate = float(temperature_lapse_rate)
        self.sea_level_temperature = float(sea_level_temperature)
    
    def calculate_density(self, height: float) -> float:
        """
        주어진 고도에서의 공기 밀도를 계산합니다.
        rho(z) = rho_0 * exp(-(a / T0) * z)
        
        Args:
            height: 고도 (m)
            
        Returns:
            공기 밀도 (kg/m³)
        """
        return self.sea_level_density * np.exp(-(self.temperature_lapse_rate / 
                                                self.sea_level_temperature) * height)
    
    def calculate_densities(self, heights: np.ndarray) -> np.ndarray:
        """
        여러 고도에서의 공기 밀도를 계산합니다.
        
        Args:
            heights: 고도 배열 (m)
            
        Returns:
            각 고도에서의 공기 밀도 배열 (kg/m³)
        """
        return np.array([self.calculate_density(h) for h in heights])
