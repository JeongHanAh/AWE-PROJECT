import pytest
import numpy as np
from models.wind_profile import WindProfile

def test_wind_profile_initialization():
    """WindProfile 클래스 초기화 테스트"""
    wp = WindProfile(reference_height=10, reference_speed=5.0)
    assert wp.reference_height == 10
    assert wp.reference_speed == 5.0
    assert wp.power_law_exponent == 0.14

def test_calculate_wind_speed():
    """풍속 계산 테스트"""
    wp = WindProfile(reference_height=10, reference_speed=5.0)
    
    # 단일 고도 테스트
    wind_speed = wp.calculate_wind_speed(20)
    expected_speed = 5.0 * (20/10) ** 0.14
    assert np.isclose(wind_speed, expected_speed)
    
    # 여러 고도 테스트
    heights = np.array([10, 20, 30])
    wind_speeds = wp.calculate_wind_speed(heights)
    expected_speeds = np.array([5.0, 5.0 * (20/10) ** 0.14, 5.0 * (30/10) ** 0.14])
    assert np.allclose(wind_speeds, expected_speeds)

def test_calculate_wind_profile():
    """풍속 프로파일 계산 테스트"""
    wp = WindProfile(reference_height=10, reference_speed=5.0)
    heights = np.linspace(10, 100, 10)
    profile = wp.calculate_wind_profile(heights)
    
    assert len(profile) == len(heights)
    assert np.all(profile > 0)  # 모든 풍속이 양수여야 함
    assert np.all(np.diff(profile) > 0)  # 고도가 증가할수록 풍속도 증가해야 함

def test_get_wind_shear():
    """풍속 전단 계산 테스트"""
    wp = WindProfile(reference_height=10, reference_speed=5.0)
    shear = wp.get_wind_shear(20)
    
    # 풍속 전단은 양수여야 함
    assert shear > 0
    
    # 고도가 증가할수록 전단은 감소해야 함
    shear_high = wp.get_wind_shear(100)
    assert shear > shear_high 