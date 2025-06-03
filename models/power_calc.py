import numpy as np
from typing import Union, Tuple, List

class PowerCalculator:
    """
    풍력 발전기의 전력 계산을 위한 기본 클래스
    지상형 터빈과 AWE 시스템 모두에 적용 가능
    """
    
    def __init__(self, power_coefficient: float = 0.4,
                 area: float = 1000.0,  # 로터/날개 면적 (m²)
                 cycle_efficiency: float = 0.9,  # 전체 효율
                 system_type: str = "ground",  # "ground" 또는 "awe"
                 # AWE 시스템 특성 (system_type이 "awe"일 때만 사용)
                 lift_coefficient: float = 1.2,
                 drag_coefficient: float = 0.1,
                 tether_drag_coefficient: float = 0.2,
                 tether_length: float = 350.0):
        """
        초기화 함수
        
        Args:
            power_coefficient: 전력 계수 (기본값: 0.4)
            area: 로터/날개 면적 (m²)
            cycle_efficiency: 전체 효율
            system_type: 시스템 유형 ("ground" 또는 "awe")
            lift_coefficient: 양력 계수 (AWE 시스템용)
            drag_coefficient: 항력 계수 (AWE 시스템용)
            tether_drag_coefficient: 테더 항력 계수 (AWE 시스템용)
            tether_length: 테더 길이 (m) (AWE 시스템용)
        """
        self.power_coefficient = float(power_coefficient)
        self.area = float(area)
        self.cycle_efficiency = float(cycle_efficiency)
        self.system_type = system_type
        
        # AWE 시스템 특성
        if system_type == "awe":
            self.lift_coefficient = float(lift_coefficient)
            self.drag_coefficient = float(drag_coefficient)
            self.tether_drag_coefficient = float(tether_drag_coefficient)
            self.tether_length = float(tether_length)
    
    def calculate_effective_glide_ratio(self) -> float:
        """
        AWE 시스템의 유효 글라이드 비율을 계산합니다.
        G_e = C_L / (C_D + C_T * (l / A_kite))
        
        Returns:
            유효 글라이드 비율
        """
        if self.system_type != "awe":
            return 0.0
            
        # 테더 항력 항 계산
        # 테더 항력은 날개 면적의 제곱근에 비례
        tether_drag_term = self.tether_drag_coefficient * (self.tether_length / np.sqrt(self.area))
        
        # 유효 글라이드 비율 계산
        glide_ratio = self.lift_coefficient / (self.drag_coefficient + tether_drag_term)
        
        # 글라이드 비율이 너무 낮은 경우 최소값 적용
        return max(glide_ratio, 5.0)
    
    def calculate_power(self, wind_speed: Union[float, np.ndarray],
                       air_density: Union[float, np.ndarray] = 1.225,
                       theta: float = 0.0) -> np.ndarray:
        """
        주어진 풍속에서의 전력 생산량을 계산합니다.
        P_mech = 0.5 * rho * A * V^3 * C_p
        P_elec = eta * P_mech
        
        Args:
            wind_speed: 풍속 (m/s)
            air_density: 공기 밀도 (kg/m³)
            theta: 테더 각도 (rad) (AWE 시스템용)
            
        Returns:
            전력 생산량 배열 (kW)
        """
        # 입력값을 numpy 배열로 변환
        wind_speed = np.asarray(wind_speed, dtype=float)
        air_density = np.asarray(air_density, dtype=float)
        
        # 단일 값인 경우 1차원 배열로 변환
        if wind_speed.ndim == 0:
            wind_speed = np.array([wind_speed])
        if air_density.ndim == 0:
            air_density = np.array([air_density])
        
        # 배열 크기가 다른 경우 브로드캐스팅
        if wind_speed.shape != air_density.shape:
            air_density = np.full_like(wind_speed, air_density)
        
        # AWE 시스템의 경우 전력 계수 계산
        if self.system_type == "awe":
            glide_ratio = self.calculate_effective_glide_ratio()
            # AWE 시스템의 전력 계수 계산
            # C_p = (4/27) * C_L * G_e * cos^3(theta)
            power_coefficient = (4/27) * self.lift_coefficient * glide_ratio * np.cos(theta)**3
        else:
            power_coefficient = self.power_coefficient
        
        # 기계적 전력 계산 (W)
        mechanical_power = 0.5 * air_density * self.area * wind_speed**3 * power_coefficient
        
        # 전기적 전력 계산 (W)
        electrical_power = self.cycle_efficiency * mechanical_power
        
        # W -> kW 변환
        electrical_power = electrical_power / 1000
        
        return electrical_power
    
    def calculate_power_curve(self, wind_speeds: np.ndarray,
                            air_density: float = 1.225,
                            theta: float = 0.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        풍속별 전력 곡선을 계산합니다.
        
        Args:
            wind_speeds: 풍속 배열 (m/s)
            air_density: 공기 밀도 (kg/m³)
            theta: 테더 각도 (rad) (AWE 시스템용)
            
        Returns:
            (풍속 배열, 전력 배열) 튜플
        """
        power = self.calculate_power(wind_speeds, air_density, theta)
        return wind_speeds, power
    
    def calculate_annual_energy(self, wind_speeds: np.ndarray,
                              air_density: float = 1.225,
                              time_step: float = 1.0,
                              theta: float = 0.0) -> float:
        """
        연간 에너지 생산량을 계산합니다.
        
        Args:
            wind_speeds: 풍속 배열 (m/s)
            air_density: 공기 밀도 (kg/m³)
            time_step: 시간 간격 (시간)
            theta: 테더 각도 (rad) (AWE 시스템용)
            
        Returns:
            연간 에너지 생산량 (kWh)
        """
        power = self.calculate_power(wind_speeds, air_density, theta)
        return np.sum(power * time_step)
