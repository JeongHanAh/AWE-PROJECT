import numpy as np
import matplotlib.pyplot as plt
from models.power_calc import PowerCalculator
from models.wind_profile import WindProfile
from models.air_density import AirDensity

def run_simulation():
    """풍력 발전 시스템 시뮬레이션을 실행합니다."""
    
    # 시뮬레이션 파라미터
    duration = 10  # 분
    time_step = 1  # 분
    
    # 풍속 프로파일 설정
    wind_profile = WindProfile(
        reference_height=10,  # 기준 높이 (m)
        reference_speed=4.0,  # 기준 풍속 (m/s)
        power_law_exponent=0.2  # 지수 법칙 지수
    )
    
    # 공기 밀도 계산기
    air_density = AirDensity()
    
    # 지상형 터빈 전력 계산기
    ground_calculator = PowerCalculator(
        power_coefficient=0.4,
        area=100.0,  # 로터 면적 (m²)
        cycle_efficiency=0.9,
        system_type="ground"
    )
    
    # AWE 시스템 전력 계산기
    awe_calculator = PowerCalculator(
        power_coefficient=0.4,
        area=50.0,  # 날개 면적 (m²)
        cycle_efficiency=0.85,
        system_type="awe",
        lift_coefficient=1.2,
        drag_coefficient=0.1,
        tether_drag_coefficient=0.2,
        tether_length=350.0
    )
    
    # 시간 배열 생성
    time_points = np.arange(0, duration, time_step)
    
    # 각 시간별 풍속 계산
    ground_wind_speeds = np.array([wind_profile.calculate_wind_speed(80, t) for t in time_points])
    awe_wind_speeds = np.array([wind_profile.calculate_wind_speed(300, t) for t in time_points])
    
    # 각 시간별 공기 밀도 계산
    ground_air_density = np.array([air_density.calculate_density(80) for _ in time_points])
    awe_air_density = np.array([air_density.calculate_density(300) for _ in time_points])
    
    # 전력 계산
    ground_power = ground_calculator.calculate_power(ground_wind_speeds, ground_air_density)
    awe_power = awe_calculator.calculate_power(awe_wind_speeds, awe_air_density)
    
    # 누적 에너지 계산 (kWh)
    ground_energy = np.sum(ground_power * time_step / 60)  # 분 -> 시간 변환
    awe_energy = np.sum(awe_power * time_step / 60)  # 분 -> 시간 변환
    
    # 결과 출력
    print("\n풍력 발전 시스템 시뮬레이션 결과:")
    print(f"시뮬레이션 기간: {duration}분")
    print(f"시간 간격: {time_step}분")
    print("\n풍속:")
    print(f"10m 높이: {wind_profile.calculate_wind_speed(10, 0):.2f} m/s")
    print(f"80m 높이 (지상형): {ground_wind_speeds[0]:.2f} m/s")
    print(f"300m 높이 (AWE): {awe_wind_speeds[0]:.2f} m/s")
    
    print("\n공기 밀도:")
    print(f"80m 높이: {ground_air_density[0]:.3f} kg/m³")
    print(f"300m 높이: {awe_air_density[0]:.3f} kg/m³")
    
    print("\n지상형 터빈:")
    print(f"평균 출력: {np.mean(ground_power):.2f} kW")
    print(f"최대 출력: {np.max(ground_power):.2f} kW")
    print(f"총 에너지 생산량: {ground_energy:.2f} kWh")
    
    print("\nAWE 시스템:")
    print(f"평균 출력: {np.mean(awe_power):.2f} kW")
    print(f"최대 출력: {np.max(awe_power):.2f} kW")
    print(f"총 에너지 생산량: {awe_energy:.2f} kWh")
    
    print("\n시간별 전력 생산량:")
    print("시간(분) | 지상형(kW) | AWE(kW)")
    print("-" * 35)
    for t, g_p, a_p in zip(time_points, ground_power, awe_power):
        print(f"{t:6.1f} | {g_p:9.2f} | {a_p:7.2f}")

    # 분당 전력 생산량 그래프
    plt.figure(figsize=(12, 6))
    plt.plot(time_points, ground_power, 'b-', label='Ground Wind Turbine', linewidth=2)
    plt.plot(time_points, awe_power, 'r-', label='AWE System', linewidth=2)
    
    # 그래프 스타일 설정
    plt.title('Hourly Power Output Comparison', fontsize=14, pad=15)
    plt.xlabel('Time (minutes)', fontsize=12)
    plt.ylabel('Power (kW)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    
    # y축 범위 설정 (0부터 시작)
    plt.ylim(bottom=0)
    
    # 그래프 여백 조정
    plt.tight_layout()
    
    # 그래프 저장
    plt.savefig('power_production_comparison.png', dpi=300, bbox_inches='tight')
    
    # 그래프 표시
    plt.show()

if __name__ == "__main__":
    run_simulation()
