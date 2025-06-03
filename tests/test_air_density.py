import pytest
import numpy as np
from models.air_density import AirDensity

def test_air_density_initialization():
    """AirDensity 클래스 초기화 테스트"""
    ad = AirDensity()
    assert ad.sea_level_density == 1.225
    assert ad.temperature_lapse_rate == 0.0065
    assert ad.sea_level_temperature == 288.15

def test_calculate_temperature():
    """온도 계산 테스트"""
    ad = AirDensity()
    
    # 해수면 온도 테스트
    temp_sea_level = ad.calculate_temperature(0)
    assert np.isclose(temp_sea_level, 288.15)
    
    # 고도에 따른 온도 감소 테스트
    heights = np.array([0, 1000, 2000])
    temps = ad.calculate_temperature(heights)
    assert np.all(np.diff(temps) < 0)  # 고도가 증가할수록 온도는 감소해야 함

def test_calculate_density():
    """공기 밀도 계산 테스트"""
    ad = AirDensity()
    
    # 해수면 밀도 테스트
    density_sea_level = ad.calculate_density(0)
    assert np.isclose(density_sea_level, 1.225, rtol=1e-2)
    
    # 고도에 따른 밀도 감소 테스트
    heights = np.array([0, 1000, 2000])
    densities = ad.calculate_density(heights)
    assert np.all(np.diff(densities) < 0)  # 고도가 증가할수록 밀도는 감소해야 함
    
    # 밀도는 항상 양수여야 함
    assert np.all(densities > 0)

def test_calculate_density_profile():
    """공기 밀도 프로파일 계산 테스트"""
    ad = AirDensity()
    heights = np.linspace(0, 10000, 100)
    profile = ad.calculate_density_profile(heights)
    
    assert len(profile) == len(heights)
    assert np.all(profile > 0)  # 모든 밀도가 양수여야 함
    assert np.all(np.diff(profile) < 0)  # 고도가 증가할수록 밀도는 감소해야 함 