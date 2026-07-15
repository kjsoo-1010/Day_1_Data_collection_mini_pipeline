# 코드 분석 보고서 (ruff check)

`ruff` 실행 결과([reports/ruff_result.txt](reports/ruff_result_2.txt))에 대한 항목별 분석

**요약: 총 11개 오류, 이 중 7개는 `--fix` 옵션으로 자동 수정 가능**

| 규칙 | 의미 | 발생 수 | 자동 수정 |
| --- | --- | --- | --- |
| I001 | import 블록이 정렬/포맷되지 않음 | 6 | 가능 |
| E401 | 한 줄에 여러 import | 1 | 불가 (수동) |
| E501 | 줄 길이 100자 초과 | 4 | 불가 (수동) |

---

## 1. I001 — Import block is un-sorted or un-formatted

isort 스타일로 import를 정렬/그룹화하지 않은 경우 발생. 발생 위치:

- [main.py:11](main.py#L11)
- [pipeline/benchmark.py:10](pipeline/benchmark.py#L10)
- [pipeline/fetch.py:11](pipeline/fetch.py#L11)
- [pipeline/schemas.py:10](pipeline/schemas.py#L10)
- [pipeline/storage.py:10](pipeline/storage.py#L10)
- [pipeline/transform.py:11](pipeline/transform.py#L11)

**수정 방법**: 자동 수정 가능하므로 아래 명령 한 번이면 6개 모두 해결됨.

```bash
uv run ruff check --fix .
```

---

## 2. E401 — Multiple imports on one line

- 위치: [pipeline/fetch.py:11](pipeline/fetch.py#L11)
- 현재 코드:
  ```python
  import asyncio, httpx
  ```

**수정 방법**: ruff가 자동으로 고쳐주지 않으므로 두 줄로 직접 분리해야 함.

```python
import asyncio

import httpx
```

---

## 3. E501 — Line too long (> 100자)

전부 긴 한글 주석/설명 문구가 원인이며, 자동 수정 불가하므로 줄바꿈 필요.

| 위치 | 길이 | 원인 |
| --- | --- | --- |
| [pipeline/schemas.py:7](pipeline/schemas.py#L7) | 158자 | 파일 상단 설명 주석이 한 줄에 이어짐 |
| [pipeline/schemas.py:36](pipeline/schemas.py#L36) | 103자 | `as_number` 필드 뒤 인라인 주석이 김 |
| [pipeline/transform.py:2](pipeline/transform.py#L2) | 107자 | 파일 상단 "작성목적" 주석이 김 |
| [pipeline/transform.py:7](pipeline/transform.py#L7) | 158자 | 파일 상단 설명 주석이 한 줄에 이어짐 |

**수정 방법 예시** (`pipeline/schemas.py:36`):

```python
# 변경 전
as_number: str | None = Field(default=None, alias="as")  # as는 파이썬 예약어이므로 as_number로 변경

# 변경 후
as_number: str | None = Field(default=None, alias="as")  # as는 예약어라 as_number로 대체
```

`schemas.py:7`, `transform.py:2`, `transform.py:7`처럼 파일 상단 설명 주석이 긴 경우는 여러 줄로 나누면 됨:

```python
# 변경 전
# 3. Countries API (한국 국가 정보)에서 필요한 필드 추출하여 Pydantic 모델 정의 (tests/fixtures 의 {API}_sample.json 참고)

# 변경 후
# 3. Countries API (한국 국가 정보)에서 필요한 필드 추출하여
#    Pydantic 모델 정의 (tests/fixtures 의 {API}_sample.json 참고)
```

---

## 진행 순서 제안

1. `uv run ruff check --fix .` 로 I001(import 정렬) 6건 자동 해결
2. `pipeline/fetch.py`의 E401 수동 수정 (import 2줄 분리)
3. `schemas.py`, `transform.py`의 E501 4건 — 긴 주석/인라인 코멘트 줄바꿈
4. `uv run ruff check . > reports/ruff_result_2.txt` 재실행하여 0 errors 확인 후 보고서 갱신
