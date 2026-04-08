# Phase 2 설명

## 구현 목표

- 비밀번호를 평문 저장에서 `bcrypt 해싱`으로 변경
- `users.role`(user/admin) 기반 권한 분리
- 스터디룸 `capacity` 기반 다인 예약 허용
- 관리자 전용 스터디룸 관리 API 추가

## DB 변경 사항

### user

- `role VARCHAR(20) NOT NULL DEFAULT 'user'` 컬럼 추가
- 회원가입 시 role 미지정이면 기본값 `user`

### studyroom

- `capacity INTEGER NOT NULL DEFAULT 1` 컬럼 추가
- `description TEXT` 컬럼 추가

> 현재 프로젝트는 단수 테이블명(`user`, `studyroom`) 기준으로 동작

## 핵심 비즈니스 로직

### 1) 비밀번호 해싱/검증

- 회원가입:
  - `passlib`의 `CryptContext`로 비밀번호 해싱 후 저장
- 로그인:
  - `verify(plain_password, hashed_password)`로 검증

## 2) role 기반 권한 분리

- 스터디룸 생성/수정/삭제는 관리자만 가능
- 서비스 계층에서 `user.role == 'admin'` 검사
- 일반 유저가 접근 시 `403 Forbidden` 반환

### 3) capacity 기반 예약 검증

- 기존 Phase 1: 겹치는 예약이 1건이라도 있으면 거절
- Phase 2:
  - 겹치는 예약 수(`COUNT`)를 조회
  - `COUNT < room.capacity`이면 예약 허용
  - `COUNT >= room.capacity`이면 예약 거절

## 추가/변경 API

### 관리자 전용 Rooms API

- `POST /api/v1/rooms/` : 스터디룸 생성 (admin)
- `PATCH /api/v1/rooms/{room_id}` : 스터디룸 수정 (admin)
- `DELETE /api/v1/rooms/{room_id}` : 스터디룸 삭제 (admin)

### 기존 API 유지 + 내부 로직 강화

- `POST /api/v1/auth/signup` : bcrypt 해싱 저장
- `POST /api/v1/auth/login` : bcrypt 검증
- `POST /api/v1/reservations/` : capacity 기준 예약 가능 여부 검증

## 실행 방법

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

- Swagger: `http://127.0.0.1:8000/docs`

## 제출 시 설명 포인트 (권장)

- 왜 평문 비밀번호 저장이 위험한지
- bcrypt 해싱 적용 방식(저장/검증 분리)
- role 기반 권한 체크 위치(서비스 계층)
- capacity 기반 예약 허용 조건(COUNT 비교)
