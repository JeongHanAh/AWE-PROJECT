import pytest
import numpy as np
from models.awe_power_calc import AWEPowerCalculator

def test_awe_power_calculator_initialization():
    """AWEPowerCalculator 클래스 초기화 테스트"""
    awe = AWEPowerCalculator(
        operating_height=300,
        tether_length=350,
        rated_power=100,
        min_wind_speed=3.0,
        max_wind_speed=20.0
    )
    
    assert awe.operating_height == 300
    assert awe.tether_length == 350
    assert awe.rated_power == 100
    assert awe.cut_in_speed == 3.0
    assert awe.cut_out_speed == 20.0
    assert awe.power_coefficient == 0.35

def test_calculate_tether_force():
    """테더 힘 계산 테스트"""
    awe = AWEPowerCalculator(
        operating_height=300,
        tether_length=350,
        rated_power=100,
        min_wind_speed=3.0,
        max_wind_speed=20.0
    )
    
    # 단일 풍속 테스트
    wind_speed = 10
    air_density = 1.225
    force = awe.calculate_tether_force(wind_speed, air_density)
    
    # 양력과 항력 계산 검증
    lift_force = 0.5 * air_density * awe.wing_area * wind_speed**2 * awe.lift_coefficient
    drag_force = 0.5 * air_density * awe.wing_area * wind_speed**2 * awe.drag_coefficient
    expected_force = np.sqrt(lift_force**2 + drag_force**2)
    
    assert np.isclose(force, expected_force)
    
    # 여러 풍속 테스트
    wind_speeds = np.array([5, 10, 15])
    forces = awe.calculate_tether_force(wind_speeds, air_density)
    assert len(forces) == len(wind_speeds)
    assert np.all(forces > 0)

def test_calculate_power():
    """전력 계산 테스트"""
    awe = AWEPowerCalculator(
        operating_height=300,
        tether_length=350,
        rated_power=100,
        min_wind_speed=3.0,
        max_wind_speed=20.0
    )
    
    # 작동 범위 테스트
    wind_speeds = np.array([2, 5, 10, 25])
    power = awe.calculate_power(wind_speeds, 1.225)
    
    # 최소 풍속 미만에서는 전력이 0
    assert np.isclose(power[0], 0)
    
    # 최대 풍속 초과에서는 전력이 0
    assert np.isclose(power[-1], 0)
    
    # 정상 작동 구간에서는 전력이 양수
    assert power[1] > 0
    assert power[2] > 0
    
    # 정격 출력 제한 테스트
    high_wind_speed = np.array([15])
    power = awe.calculate_power(high_wind_speed, 1.225)
    assert power[0] <= awe.rated_power

def test_calculate_power_curve():
    """전력 곡선 계산 테스트"""
    awe = AWEPowerCalculator(
        operating_height=300,
        tether_length=350,
        rated_power=100,
        min_wind_speed=3.0,
        max_wind_speed=20.0
    )
    
    wind_speeds = np.linspace(0, 30, 100)
    speeds, powers = awe.calculate_power_curve(wind_speeds)
    
    assert len(speeds) == len(powers)
    assert np.all(speeds >= 0)
    assert np.all(powers >= 0)
    assert np.all(powers <= awe.rated_power)

def test_calculate_annual_energy():
    """연간 에너지 생산량 계산 테스트"""
    awe = AWEPowerCalculator(
        operating_height=300,
        tether_length=350,
        rated_power=100,
        min_wind_speed=3.0,
        max_wind_speed=20.0
    )
    
    # 24시간 시뮬레이션
    wind_speeds = np.array([5] * 24)  # 24시간 동안 5m/s의 일정한 풍속
    energy = awe.calculate_annual_energy(wind_speeds, time_step=1.0)
    
    # 에너지는 전력의 시간 적분
    power = awe.calculate_power(wind_speeds, 1.225)
    expected_energy = np.sum(power * 1.0)
    assert np.isclose(energy, expected_energy) 