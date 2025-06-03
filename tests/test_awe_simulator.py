import pytest
import numpy as np
from simulators.awe_simulator import AWESimulator

@pytest.fixture
def config():
    """테스트용 설정 데이터"""
    return {
        'simulation': {
            'duration': 24,  # 24시간
            'time_step': 1   # 1분 간격
        },
        'wind_profile': {
            'reference_height': 10,
            'reference_speed': 5.0,
            'power_law_exponent': 0.14
        },
        'air_density': {
            'sea_level_density': 1.225,
            'temperature_lapse_rate': 0.0065,
            'sea_level_temperature': 288.15
        },
        'awe_system': {
            'operating_height': 300,
            'tether_length': 350,
            'rated_power': 100,
            'min_wind_speed': 3.0,
            'max_wind_speed': 20.0
        }
    }

def test_awe_simulator_initialization(config):
    """AWESimulator 클래스 초기화 테스트"""
    simulator = AWESimulator(config)
    
    assert simulator.operating_height == 300
    assert simulator.tether_length == 350
    assert simulator.rated_power == 100
    assert simulator.min_wind_speed == 3.0
    assert simulator.max_wind_speed == 20.0
    assert simulator.duration == 24
    assert simulator.time_step == 1

def test_generate_wind_speeds(config):
    """풍속 데이터 생성 테스트"""
    simulator = AWESimulator(config)
    wind_speeds = simulator.generate_wind_speeds()
    
    # 시간 포인트 수 검증
    expected_points = int(config['simulation']['duration'] * 60 / config['simulation']['time_step'])
    assert len(wind_speeds) == expected_points
    
    # 풍속 범위 검증
    assert np.all(wind_speeds >= 0)
    assert np.all(wind_speeds < config['wind_profile']['reference_speed'] * 3)  # 3배 이상은 없어야 함

def test_run_simulation(config):
    """시뮬레이션 실행 테스트"""
    simulator = AWESimulator(config)
    results = simulator.run_simulation()
    
    # 결과 키 검증
    expected_keys = ['time', 'wind_speed', 'operating_wind_speed', 'air_density', 'power']
    assert all(key in results for key in expected_keys)
    
    # 데이터 길이 검증
    expected_length = int(config['simulation']['duration'] * 60 / config['simulation']['time_step'])
    assert len(results['time']) == expected_length
    assert len(results['wind_speed']) == expected_length
    assert len(results['power']) == expected_length
    
    # 데이터 범위 검증
    assert np.all(results['power'] >= 0)
    assert np.all(results['power'] <= config['awe_system']['rated_power'])
    assert np.all(results['wind_speed'] >= 0)
    assert np.all(results['air_density'] > 0)

def test_calculate_statistics(config):
    """통계 계산 테스트"""
    simulator = AWESimulator(config)
    results = simulator.run_simulation()
    stats = simulator.calculate_statistics(results)
    
    # 통계 키 검증
    expected_keys = [
        'total_energy', 'average_power', 'max_power',
        'capacity_factor', 'average_wind_speed', 'max_wind_speed'
    ]
    assert all(key in stats for key in expected_keys)
    
    # 통계 값 범위 검증
    assert stats['total_energy'] >= 0
    assert stats['average_power'] >= 0
    assert stats['max_power'] >= 0
    assert 0 <= stats['capacity_factor'] <= 1
    assert stats['average_wind_speed'] >= 0
    assert stats['max_wind_speed'] >= 0
    
    # 통계 값 관계 검증
    assert stats['max_power'] >= stats['average_power']
    assert stats['max_wind_speed'] >= stats['average_wind_speed'] 