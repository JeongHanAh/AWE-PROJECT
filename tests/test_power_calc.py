import pytest
import numpy as np
from models.power_calc import PowerCalculator

def test_power_calculator_initialization():
    """PowerCalculator 클래스 초기화 테스트"""
    pc = PowerCalculator(
        rotor_diameter=90,
        hub_height=80,
        rated_power=2000,
        cut_in_speed=3.5,
        cut_out_speed=25
    )
    
    assert pc.rotor_diameter == 90
    assert pc.hub_height == 80
    assert pc.rated_power == 2000
    assert pc.cut_in_speed == 3.5
    assert pc.cut_out_speed == 25
    assert pc.power_coefficient == 0.4
    assert np.isclose(pc.rotor_area, np.pi * (90/2) ** 2)
    assert np.isclose(pc.betz_limit, 16/27)

def test_calculate_theoretical_power():
    """이론적 전력 계산 테스트"""
    pc = PowerCalculator(
        rotor_diameter=90,
        hub_height=80,
        rated_power=2000,
        cut_in_speed=3.5,
        cut_out_speed=25
    )
    
    # 단일 풍속 테스트
    wind_speed = 10
    air_density = 1.225
    power = pc.calculate_theoretical_power(wind_speed, air_density)
    
    # 이론적 전력 계산식 검증
    expected_power = (0.5 * air_density * pc.rotor_area * wind_speed**3 * 
                     pc.power_coefficient * pc.betz_limit) / 1000
    assert np.isclose(power, expected_power)
    
    # 여러 풍속 테스트
    wind_speeds = np.array([5, 10, 15])
    powers = pc.calculate_theoretical_power(wind_speeds, air_density)
    assert len(powers) == len(wind_speeds)
    assert np.all(powers > 0)

def test_calculate_actual_power():
    """실제 전력 계산 테스트"""
    pc = PowerCalculator(
        rotor_diameter=90,
        hub_height=80,
        rated_power=2000,
        cut_in_speed=3.5,
        cut_out_speed=25
    )
    
    # 컷인/컷아웃 풍속 테스트
    wind_speeds = np.array([2, 5, 10, 30])
    power = pc.calculate_actual_power(wind_speeds, 1.225)
    
    # 컷인 풍속 미만에서는 전력이 0
    assert np.isclose(power[0], 0)
    
    # 컷아웃 풍속 초과에서는 전력이 0
    assert np.isclose(power[-1], 0)
    
    # 정상 작동 구간에서는 전력이 양수
    assert power[1] > 0
    assert power[2] > 0
    
    # 정격 출력 제한 테스트
    high_wind_speed = np.array([20])
    power = pc.calculate_actual_power(high_wind_speed, 1.225)
    assert power[0] <= pc.rated_power

def test_calculate_power_curve():
    """전력 곡선 계산 테스트"""
    pc = PowerCalculator(
        rotor_diameter=90,
        hub_height=80,
        rated_power=2000,
        cut_in_speed=3.5,
        cut_out_speed=25
    )
    
    wind_speeds = np.linspace(0, 30, 100)
    speeds, powers = pc.calculate_power_curve(wind_speeds)
    
    assert len(speeds) == len(powers)
    assert np.all(speeds >= 0)
    assert np.all(powers >= 0)
    assert np.all(powers <= pc.rated_power)

def test_calculate_annual_energy():
    """연간 에너지 생산량 계산 테스트"""
    pc = PowerCalculator(
        rotor_diameter=90,
        hub_height=80,
        rated_power=2000,
        cut_in_speed=3.5,
        cut_out_speed=25
    )
    
    # 24시간 시뮬레이션
    wind_speeds = np.array([5] * 24)  # 24시간 동안 5m/s의 일정한 풍속
    energy = pc.calculate_annual_energy(wind_speeds, time_step=1.0)
    
    # 에너지는 전력의 시간 적분
    power = pc.calculate_actual_power(wind_speeds, 1.225)
    expected_energy = np.sum(power * 1.0)
    assert np.isclose(energy, expected_energy)
