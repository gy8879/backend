# Phase 2 — 보안: "비번이 이래도 되나?"

> 난이도: ★★☆ | 핵심: bcrypt 해싱, role 기반 권한, capacity 도입

---

## 목표

- 비밀번호를 bcrypt로 해싱하여 저장
- users에 role(user/admin) 추가, 관리자 전용 엔드포인트 보호
- 스터디룸에 capacity(수용인원) 추가, 다인 예약 허용

---

## DB 변경사항

### users — 컬럼 추가

| 컬럼 | 타입 | 제약조건 | 설명 |
|---|---|---|---|
| role | VARCHAR(20) | DEFAULT 'user' | 역할 (user / admin) |

```sql
ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user' NOT NULL;
```

> password 컬럼은 그대로 사용하되, 저장하는 값이 평문 → bcrypt 해시로 변경

### study_rooms — 컬럼 추가

| 컬럼 | 타입 | 제약조건 | 설명 |
|---|---|---|---|
| capacity | INTEGER | NOT NULL, DEFAULT 1 | 수용 인원 |
| description | TEXT | | 룸 설명 |

```sql
ALTER TABLE study_rooms ADD COLUMN capacity INTEGER NOT NULL DEFAULT 1;
ALTER TABLE study_rooms ADD COLUMN description TEXT;
```

---

## 비즈니스 로직 변경

### 비밀번호 해싱

```python
# 회원가입 시
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"])
hashed = pwd_context.hash(password)

# 로그인 시
pwd_context.verify(plain_password, hashed_password)
```

### capacity 기반 예약 검증

```sql
-- 같은 룸, 겹치는 시간대의 예약 수가 capacity 미만이면 허용
SELECT COUNT(*) FROM reservations
WHERE room_id = :room_id
  AND start_time < :end_time
  AND end_time > :start_time;
-- COUNT < study_rooms.capacity 이면 허용
```

### 관리자 권한 체크

- 스터디룸 생성/수정/삭제는 admin만 가능
- role 검사: `if user.role != 'admin': raise 403`

---

## 추가 API 엔드포인트

### 관리자 — 스터디룸 관리
| Method | Endpoint | 설명 | 권한 |
|---|---|---|---|
| POST | /rooms | 스터디룸 생성 | admin |
| PATCH | /rooms/{id} | 스터디룸 수정 | admin |
| DELETE | /rooms/{id} | 스터디룸 삭제 | admin |

---

## 학습 포인트

1. "왜 비밀번호를 평문으로 저장하면 안 되는지" — DB 탈취 시 전체 계정 노출
2. bcrypt의 단방향 해싱 원리 — 같은 비밀번호도 매번 다른 해시값
3. role 기반 권한 분리의 기본 개념
4. COUNT 집계 쿼리로 비즈니스 로직 검증
