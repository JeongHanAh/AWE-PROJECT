import numpy as np
from models.power_calc import PowerCalculator
from models.awe_power_calc import AWEPowerCalculator
from models.wind_profile import WindProfile
from models.air_density import AirDensity

def run_simulation():
    """풍력 발전 시스템 시뮬레이션을 실행합니다."""
    
    # 시뮬레이션 설정
    duration = 10  # 10분
    time_step = 1  # 1분 간격
    
    # 풍속 프로파일 설정 (지상 10m에서 4m/s)
    wind_profile = WindProfile(
        reference_height=10.0,
        reference_speed=4.0,  # 지상 10m에서의 풍속을 4m/s로 증가
        power_law_exponent=0.14,
        tower_diameter=4.0  # 타워 직경 4m
    )
    
    # 공기 밀도 설정
    air_density = AirDensity(
        sea_level_density=1.225,
        temperature_lapse_rate=0.0065,
        sea_level_temperature=288.15
    )
    
    # 지상형 풍력 발전기 설정 (허브 높이 80m)
    ground_turbine = PowerCalculator(
        rated_power=100,  # 100kW
        cut_in_speed=2.5,  # 컷인 풍속을 2.5m/s로 낮춤
        cut_out_speed=20.0,
        power_coefficient=0.4
    )
    
    # AWE 시스템 설정 (작동 고도 300m)
    awe_system = AWEPowerCalculator(
        operating_height=300,
        tether_length=350,
        rated_power=100,  # 100kW
        min_wind_speed=2.5,  # 최소 풍속을 2.5m/s로 낮춤
        max_wind_speed=20.0,
        power_coefficient=0.35
    )
    
    # 시간 포인트 생성
    time_points = np.arange(0, duration, time_step)
    
    # 지상 10m에서의 풍속 생성 (4m/s 기준, 20% 변동)
    ground_wind_speeds = np.random.normal(
        loc=wind_profile.reference_speed,
        scale=wind_profile.reference_speed * 0.2,
        size=len(time_points)
    )
    ground_wind_speeds = np.maximum(ground_wind_speeds, 0)
    
    # 지상형 터빈 높이(80m)에서의 풍속 계산 (타워 쉐도우 효과 고려)
    # 로터가 타워로부터 20m 떨어져 있다고 가정
    turbine_wind_speeds = np.array([wind_profile.calculate_wind_speed(80.0, distance_from_tower=20.0)] * len(time_points))
    
    # AWE 시스템 높이(300m)에서의 풍속 계산
    awe_wind_speeds = np.array([wind_profile.calculate_wind_speed(300.0)] * len(time_points))
    
    # 지상형 풍력 발전기 전력 계산
    ground_power = ground_turbine.calculate_power(turbine_wind_speeds)
    
    # AWE 시스템 전력 계산
    awe_power = awe_system.calculate_power(awe_wind_speeds)
    
    # 누적 전력 생산량 계산
    ground_cumulative_power = np.cumsum(ground_power * time_step)
    awe_cumulative_power = np.cumsum(awe_power * time_step)
    
    # 결과 출력
    print("\n=== 풍력 발전 시스템 시뮬레이션 결과 ===")
    print(f"시뮬레이션 기간: {duration}분")
    print(f"시간 간격: {time_step}분")
    print(f"\n지상 10m 풍속: {wind_profile.reference_speed:.2f} m/s")
    print(f"터빈 높이(80m) 풍속: {turbine_wind_speeds[0]:.2f} m/s (타워 쉐도우 효과 포함)")
    print(f"AWE 시스템 높이(300m) 풍속: {awe_wind_speeds[0]:.2f} m/s")
    
    print("\n지상형 풍력 발전기:")
    print(f"평균 전력: {np.mean(ground_power):.2f} kW")
    print(f"최대 전력: {np.max(ground_power):.2f} kW")
    print(f"총 에너지 생산량: {ground_cumulative_power[-1]:.2f} kWh")
    
    print("\nAWE 시스템:")
    print(f"평균 전력: {np.mean(awe_power):.2f} kW")
    print(f"최대 전력: {np.max(awe_power):.2f} kW")
    print(f"총 에너지 생산량: {awe_cumulative_power[-1]:.2f} kWh")
    
    # 시간별 전력 생산량 출력
    print("\n시간별 전력 생산량:")
    print("시간(분) | 지상형(kW) | 누적(kWh) | AWE(kW) | 누적(kWh)")
    print("-" * 55)
    for t, g_power, g_cum, a_power, a_cum in zip(time_points, ground_power, ground_cumulative_power, 
                                               awe_power, awe_cumulative_power):
        print(f"{t:6.0f} | {g_power:9.2f} | {g_cum:9.2f} | {a_power:7.2f} | {a_cum:9.2f}")

if __name__ == "__main__":
    run_simulation()
