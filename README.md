# AWE 시뮬레이션 프로젝트

이 프로젝트는 지상 기반 풍력 터빈과 공중 풍력 에너지(AWE) 시스템의 에너지 생산 효율성을 비교하는 시뮬레이션을 구현합니다.

## 주요 기능

- 고도에 따른 풍속 변화 모델링
- 고도에 따른 공기 밀도 변화 계산
- 지상 기반 시스템의 마찰 손실 계산
- AWE 장치 주변의 흐름 안정성 분석
- 배터리 충전 시뮬레이션

## 설치 방법

1. 저장소 클론:
```bash
git clone [repository-url]
cd awe_simulation_project
```

2. 가상환경 생성 및 활성화:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 의존성 설치:
```bash
pip install -r requirements.txt
```

## 사용 방법

1. `config.yaml`에서 시뮬레이션 파라미터 설정
2. 메인 시뮬레이션 실행:
```bash
python main.py
```

## 프로젝트 구조

- `data/`: 실험 및 시뮬레이션 데이터
- `models/`: 물리적/수학적 모델
- `simulators/`: 시스템 시뮬레이션 엔진
- `utils/`: 유틸리티 모듈
- `notebooks/`: 분석용 주피터 노트북
- `tests/`: 단위 테스트
- `results/`: 시뮬레이션 결과

## 라이선스

MIT License
