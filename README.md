# 데이터 수집 미니 파이프라인

외부 API 3종(Open-Meteo, IP-API, Countries)에서 데이터를 비동기로 수집하고, pydantic으로 검증한 뒤 CSV/Parquet 두 형식으로 저장하며 두 형식의 읽기/쓰기 성능을 비교하는 데이터 수집 미니 파이프라인입니다.

## 실행 방법

```bash
pip install -r requirements.txt
python main.py
```

실행하면 3개 API를 동시에 호출해 데이터를 수집·검증하고, `data/processed/`에 CSV/Parquet 파일을 저장한 뒤 벤치마크 결과를 출력하고 `reports/benchmark_result.txt`에 저장합니다.

## 프로젝트 구조

```
pipeline/
├── config.py      # API URL, TIMEOUT, 데이터/리포트 저장 경로 등 설정값
├── fetch.py       # httpx + asyncio로 3개 API를 동시에 호출해 raw json 수집
├── schemas.py     # 수집 데이터가 유효한지 검증하는 pydantic 모델 정의
├── transform.py   # raw json을 pydantic 모델에 맞게 변환·검증
├── storage.py     # 검증된 데이터를 csv, parquet 두 형식으로 저장/로드
└── benchmark.py   # csv, parquet 형식의 읽기/쓰기 시간 측정 및 비교

tests/
├── fixtures/          # API에서 최초로 받아온 응답을 테스트용으로 저장한 샘플 json
└── test_schemas.py    # 저장해둔 샘플 데이터에 대한 스키마 검증 테스트

reports/
├── benchmark_result.txt  # benchmark.py 실행 결과 (csv/parquet 읽기·쓰기 시간)
├── pytest_result.txt     # pytest 스키마 검증 테스트 결과
└── ruff_result.txt       # ruff 코드 스타일 검사 결과

main.py   # 파이프라인 전체(수집 → 변환 → 저장 → 벤치마크)를 실행하는 진입점
```

## 수집 대상 API

| API | 용도 |
| --- | --- |
| [Open-Meteo](https://open-meteo.com/) | 서울 3일 시간대별 기온·강수확률 |
| [IP-API](https://ip-api.com/) | IP 기반 지역 정보 |
| [Countries](https://countries.dev/) | 한국 국가 정보 |

## 테스트 및 코드 검사

```bash
pytest > reports/pytest_result.txt           # 스키마 검증 테스트
ruff check . > reports/ruff_result.txt         # 코드 스타일 검사
```
