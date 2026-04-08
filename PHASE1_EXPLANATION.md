# Phase 1 설명

## 구현 목표

- 회원가입/로그인: `email + password` 기반 인증
- 게시판: 게시글 CRUD, 댓글 작성/삭제, 좋아요 토글
- 스터디룸 예약: 예약 생성/조회/취소, 시간 겹침 방지

## 기술 스택

- FastAPI
- SQLAlchemy
- PostgreSQL(Supabase)

## 테이블 매핑 기준

- 현재 프로젝트는 단수 테이블명 기준으로 매핑함
- 사용 테이블: `user`, `post`, `comment`, `like`, `reservation`, `studyroom`, `post_image`

## 인증 방식 (Phase 1)

- JWT 없이 동작
- 인증이 필요한 API는 `user_id`를 쿼리 파라미터로 전달받아 처리
- 로그인 성공 시 `user_id` 반환

## 핵심 비즈니스 로직

### 1) 예약 시간 겹침 방지

- 같은 룸에서 아래 조건을 만족하는 예약이 있으면 생성 거절
- 조건: `existing.start_time < new_end_time` AND `existing.end_time > new_start_time`
- 겹침 존재 시 `400 Bad Request` 반환

### 2) 좋아요 토글

- `POST /posts/{post_id}/like`
- `(user_id, post_id)`가 이미 존재하면 좋아요 취소(DELETE)
- 없으면 좋아요 생성(INSERT)
- 최종 좋아요 수를 응답으로 반환
- 중복 좋아요 방지를 위해 `(user_id, post_id)` 유니크 제약 사용

### 3) 권한 체크

- 게시글 수정/삭제: 작성자 본인만 가능
- 댓글 삭제: 작성자 본인만 가능
- 예약 취소: 예약자 본인만 가능

## API 엔드포인트

### Auth

- `POST /api/v1/auth/signup` : 회원가입
- `POST /api/v1/auth/login` : 로그인

### Rooms / Reservations

- `GET /api/v1/rooms/` : 스터디룸 목록
- `POST /api/v1/reservations/` : 예약 생성 (겹침 체크)
- `GET /api/v1/reservations/me` : 내 예약 목록
- `DELETE /api/v1/reservations/{reservation_id}` : 예약 취소

### Posts / Comments / Likes

- `GET /api/v1/posts/` : 게시글 목록
- `POST /api/v1/posts/` : 게시글 작성
- `GET /api/v1/posts/{post_id}` : 게시글 상세(조회수 증가, 댓글 포함)
- `PATCH /api/v1/posts/{post_id}` : 게시글 수정
- `DELETE /api/v1/posts/{post_id}` : 게시글 삭제
- `POST /api/v1/posts/{post_id}/like` : 좋아요 토글
- `GET /api/v1/posts/{post_id}/comments/` : 댓글 목록
- `POST /api/v1/posts/{post_id}/comments/` : 댓글 작성
- `DELETE /api/v1/comments/{comment_id}` : 댓글 삭제

## 실행 방법

```bash
uvicorn main:app --reload
```

- Swagger: `http://127.0.0.1:8000/docs`

## 제출 시 첨부 권장 항목

- GitHub 레포 링크
- `/docs` 전체 캡처
- 주요 API 테스트 캡처(회원가입/로그인, 예약 생성, 좋아요 토글)
