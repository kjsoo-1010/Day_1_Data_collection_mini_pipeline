## 1. `pipeline/config.py` : API URL, 타임아웃, 저장 경로 상수.

## 2. `pipeline/schemas.py` : `WeatherHourlyRecord`, `IPInfo` pydantic 모델 정의.

## 3. `pipeline/fetch.py` : 

----

# 데이터 수집 미니 파이프라인
1. pipeline
- config.py 에서 불러올 api 데이터 정보값 저장
- schemas.py 에서 불러올 api 데이터가 유효한 지 pydantic model 정의
- transform.py 에서 api에서 받아온 raw json 을 미리 정의한 pydantic model schema에 맞게 변환하고 검증. 
- storage.py 에서 검증 통과한 데이터를 csv, parquet 두 형식으로 저장.
- benchmark.py 에서 생성된 csv, parquet 파일을 읽고 쓰기 시간 측정 및 비교


2. test
- test/fixtures 는 api 에서 최초로 받아온 데이터에 대해 테스트용으로 저장
- test_schemas.py 에서 로컬로 저장해둔 데이터에 대해 검증이 어떻게 이루어지는 지 테스트

3. reports
- benchmark_result.txt 는 pipeline/benchmark.py 파일을 실행했을 때 출력된 결과물을 저장한 파일
- pytest_result.txt 는 pytest 로 스키마 검증 테스트 했을 때 출력된 값을 txt로 저장
- ruff_result.txt 는 ruff 로 코드 스타일 검사 결과 출력된 값을 txt로 저장
