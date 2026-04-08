# Phase 1 — 뼈대: "일단 돌아가게"

> 난이도: ★★ | 테이블: 6개 | 핵심: 기본 CRUD + 시간 겹침 방지

---

## 목표

- email + password(평문)로 회원가입/로그인
- 텍스트 게시글, 댓글, 좋아요 (한 글에 한 번만)
- 스터디룸 1인 예약, 시간 겹침 방지

---

## DB 스키마

### users

| 컬럼 | 타입 | 제약조건 | 설명 |
|---|---|---|---|
| id | SERIAL | PK | 유저 고유 번호 |
| username | VARCHAR(50) | NOT NULL | 아이디 |
| password | VARCHAR(255) | NOT NULL | 비밀번호 (평문, Phase 2에서 해싱) |
| email | VARCHAR(255) | UNIQUE, NOT NULL | 이메일 |
| nickname | VARCHAR(50) | NOT NULL | 닉네임 |
| created_at | TIMESTAMPTZ | DEFAULT now() | 가입일 |

### study_rooms

| 컬럼 | 타입 | 제약조건 | 설명 |
|---|---|---|---|
| id | SERIAL | PK | 룸 고유 번호 |
| name | VARCHAR(100) | NOT NULL | 룸 이름 |
| created_at | TIMESTAMPTZ | DEFAULT now() | 생성일 |

> capacity, description은 Phase 2에서 추가

### reservations

| 컬럼 | 타입 | 제약조건 | 설명 |
|---|---|---|---|
| id | SERIAL | PK | 예약 고유 번호 |
| user_id | INTEGER | FK → users, NOT NULL | 예약자 |
| room_id | INTEGER | FK → study_rooms, NOT NULL | 예약 룸 |
| start_time | TIMESTAMPTZ | NOT NULL | 시작 시간 |
| end_time | TIMESTAMPTZ | NOT NULL | 종료 시간 |
| created_at | TIMESTAMPTZ | DEFAULT now() | 생성일 |

> 겹침 방지: `WHERE room_id = ? AND start_time < ? AND end_time > ?`

### posts

| 컬럼 | 타입 | 제약조건 | 설명 |
|---|---|---|---|
| id | SERIAL | PK | 게시글 고유 번호 |
| user_id | INTEGER | FK → users, NOT NULL | 작성자 |
| title | VARCHAR(200) | NOT NULL | 제목 |
| content | TEXT | NOT NULL | 내용 |
| view_count | INTEGER | DEFAULT 0 | 조회수 |
| created_at | TIMESTAMPTZ | DEFAULT now() | 작성일 |
| updated_at | TIMESTAMPTZ | DEFAULT now() | 수정일 |

### comments

| 컬럼 | 타입 | 제약조건 | 설명 |
|---|---|---|---|
| id | SERIAL | PK | 댓글 고유 번호 |
| post_id | INTEGER | FK → posts, NOT NULL | 게시글 |
| user_id | INTEGER | FK → users, NOT NULL | 작성자 |
| content | TEXT | NOT NULL | 내용 |
| created_at | TIMESTAMPTZ | DEFAULT now() | 작성일 |

### likes

| 컬럼 | 타입 | 제약조건 | 설명 |
|---|---|---|---|
| id | SERIAL | PK | 좋아요 고유 번호 |
| user_id | INTEGER | FK → users, NOT NULL | 유저 |
| post_id | INTEGER | FK → posts, NOT NULL | 게시글 |
| created_at | TIMESTAMPTZ | DEFAULT now() | 생성일 |

> UNIQUE(user_id, post_id) — 한 글에 한 번만 좋아요

---

## 비즈니스 로직

### 예약 겹침 방지

```sql
-- 같은 룸에서 시간이 겹치는 예약이 있으면 거절
SELECT COUNT(*) FROM reservations
WHERE room_id = :room_id
  AND start_time < :end_time
  AND end_time > :start_time;
-- COUNT > 0 이면 400 반환 (Phase 1에서는 1건이라도 있으면 거절)
```

### 좋아요 토글

```
POST /posts/{post_id}/like
→ likes에 (user_id, post_id) 존재하면 DELETE, 없으면 INSERT
```

---

## API 엔드포인트

### Auth
| Method | Endpoint | 설명 |
|---|---|---|
| POST | /auth/signup | 회원가입 |
| POST | /auth/login | 로그인 (email + password 비교) |

### 예약
| Method | Endpoint | 설명 |
|---|---|---|
| GET | /rooms | 전체 스터디룸 목록 |
| POST | /reservations | 예약 생성 (겹침 체크) |
| GET | /reservations/me | 내 예약 목록 |
| DELETE | /reservations/{id} | 예약 취소 (본인만) |

### 커뮤니티
| Method | Endpoint | 설명 |
|---|---|---|
| GET | /posts | 게시글 목록 |
| POST | /posts | 게시글 작성 |
| GET | /posts/{id} | 게시글 상세 (댓글 포함) |
| PATCH | /posts/{id} | 게시글 수정 (본인만) |
| DELETE | /posts/{id} | 게시글 삭제 (본인만) |
| POST | /posts/{id}/like | 좋아요 토글 |
| POST | /posts/{id}/comments | 댓글 작성 |
| DELETE | /comments/{id} | 댓글 삭제 (본인만) |

---

## 인증 방식

- 로그인 시 email + password를 DB에서 비교 (평문)
- 인증이 필요한 엔드포인트는 로그인 후 받은 user_id를 사용
- Phase 4에서 JWT로 전환 예정
