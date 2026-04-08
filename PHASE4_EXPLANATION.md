# Phase 4 설명

## 구현 목표

- JWT 기반 인증으로 전환
- `GET /auth/me`로 토큰 사용자 정보 조회
- 관리자 전용 룸 설정(운영시간/슬롯) API 추가
- 예약 생성 시 운영시간/슬롯 단위 검증 추가

## DB 변경 사항

### room_setting (신규)

```sql
CREATE TABLE room_setting (
    id SERIAL PRIMARY KEY,
    room_id INTEGER NOT NULL UNIQUE REFERENCES studyroom(id) ON DELETE CASCADE,
    open_time TIME NOT NULL DEFAULT '09:00',
    close_time TIME NOT NULL DEFAULT '22:00',
    slot_duration INTEGER NOT NULL DEFAULT 60,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);
```

## 인증 방식 (JWT)

1. `POST /api/v1/auth/login` 성공 시 access token 발급
2. 이후 보호된 API 호출 시 헤더 사용
   - `Authorization: Bearer <token>`
3. 서버에서 토큰 검증 후 사용자 식별/권한 검사

## 추가/변경 API

- `GET /api/v1/auth/me` : 내 정보 조회 (토큰 필요)
- `GET /api/v1/rooms/{room_id}/settings` : 룸 설정 조회 (admin)
- `PATCH /api/v1/rooms/{room_id}/settings` : 룸 설정 수정 (admin)

기존 `user_id` 쿼리 기반 보호 API들은 JWT 의존성으로 변경됨:
- posts 작성/수정/삭제/좋아요/이미지 업로드·삭제
- comments 작성/삭제
- reservations 내 예약 조회/생성/취소
- rooms 생성/수정/삭제

## 예약 검증 로직 강화

- 운영시간 검증:
  - `start_time >= open_time`
  - `end_time <= close_time`
- 슬롯 검증:
  - 예약 길이(분) % `slot_duration` == 0 이어야 허용

## 환경변수

`.env`에 JWT 설정(옵션, 미설정 시 기본값 사용):

```env
JWT_SECRET_KEY=change-this-secret-in-env
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=120
```
