# Phase 4 — 토큰 + 설정: "토큰이 뭔데?"

> 난이도: ★★★☆ | 핵심: JWT 인증, 관리자 설정 페이지

---

## 목표

- 세션/쿠키 대신 JWT 토큰으로 인증 전환
- 관리자가 스터디룸 운영 설정을 관리할 수 있는 기능
- 룸별 운영시간, 타임슬롯 단위(1h/2h) 설정

---

## DB 변경사항

### room_settings — 신규 테이블

| 컬럼 | 타입 | 제약조건 | 설명 |
|---|---|---|---|
| id | SERIAL | PK | 설정 고유 번호 |
| room_id | INTEGER | FK → study_rooms, UNIQUE, NOT NULL | 룸 |
| open_time | TIME | NOT NULL, DEFAULT '09:00' | 운영 시작 시간 |
| close_time | TIME | NOT NULL, DEFAULT '22:00' | 운영 종료 시간 |
| slot_duration | INTEGER | NOT NULL, DEFAULT 60 | 타임슬롯 단위 (분) |
| created_at | TIMESTAMPTZ | DEFAULT now() | 생성일 |
| updated_at | TIMESTAMPTZ | DEFAULT now() | 수정일 |

```sql
CREATE TABLE room_settings (
    id SERIAL PRIMARY KEY,
    room_id INTEGER NOT NULL UNIQUE REFERENCES study_rooms(id) ON DELETE CASCADE,
    open_time TIME NOT NULL DEFAULT '09:00',
    close_time TIME NOT NULL DEFAULT '22:00',
    slot_duration INTEGER NOT NULL DEFAULT 60,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);
```

---

## JWT 인증 흐름

```
1. POST /auth/login → email + password 검증 → JWT 발급
2. 클라이언트: Authorization: Bearer {token} 헤더에 토큰 포함
3. 서버: 매 요청마다 토큰 검증 → user_id 추출
```

### 토큰 구조

```json
{
  "sub": 1,          // user_id
  "role": "admin",   // 역할
  "exp": 1234567890  // 만료 시간
}
```

---

## 비즈니스 로직 변경

### 예약 시 운영시간 검증

```python
# 예약 시간이 운영시간 내인지 체크
if reservation.start_time < room_settings.open_time:
    raise 400("운영 시간 이전에는 예약할 수 없습니다")
if reservation.end_time > room_settings.close_time:
    raise 400("운영 시간 이후에는 예약할 수 없습니다")
```

### 슬롯 단위 검증

```python
# 예약 시간이 슬롯 단위에 맞는지 체크
duration = (end_time - start_time).minutes
if duration % slot_duration != 0:
    raise 400("예약 시간은 슬롯 단위의 배수여야 합니다")
```

---

## 추가 API 엔드포인트

### Auth 변경
| Method | Endpoint | 설명 |
|---|---|---|
| POST | /auth/login | JWT 토큰 반환으로 변경 |
| GET | /auth/me | 토큰에서 user_id 추출하여 내 정보 반환 |

### 관리자 — 룸 설정
| Method | Endpoint | 설명 | 권한 |
|---|---|---|---|
| GET | /rooms/{id}/settings | 룸 설정 조회 | admin |
| PATCH | /rooms/{id}/settings | 룸 설정 수정 | admin |

---

## 학습 포인트

1. 세션 vs 토큰 인증의 차이 — 왜 API 서버에서 JWT가 많이 쓰이는지
2. JWT 구조 (header.payload.signature)
3. FastAPI의 Depends()를 활용한 인증 미들웨어
4. 설정 테이블 설계 — 하드코딩 vs DB 설정의 유연성
