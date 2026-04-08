# Phase 5 — 모집 시스템: "같이 공부할 사람?"

> 난이도: ★★★★ | 핵심: study_groups 테이블 분리, 신청/수락/거절 상태 관리

---

## 목표

- 커뮤니티(posts)와 별도로 스터디 모집 시스템 구축
- 모집 → 신청 → 수락/거절 흐름 구현
- "왜 테이블을 분리해야 하는지" 체감

---

## DB 변경사항

### study_groups — 신규 테이블

| 컬럼 | 타입 | 제약조건 | 설명 |
|---|---|---|---|
| id | SERIAL | PK | 모집 고유 번호 |
| leader_id | INTEGER | FK → users, NOT NULL | 조장 (모집자) |
| title | VARCHAR(200) | NOT NULL | 모집 제목 |
| description | TEXT | | 모집 설명 |
| max_members | INTEGER | NOT NULL | 최대 인원 |
| current_members | INTEGER | DEFAULT 1 | 현재 인원 (조장 포함) |
| status | VARCHAR(20) | DEFAULT '모집중' | 모집중 / 모집완료 / 종료 |
| created_at | TIMESTAMPTZ | DEFAULT now() | 생성일 |

### applications — 신규 테이블

| 컬럼 | 타입 | 제약조건 | 설명 |
|---|---|---|---|
| id | SERIAL | PK | 신청 고유 번호 |
| group_id | INTEGER | FK → study_groups, NOT NULL | 모집글 |
| applicant_id | INTEGER | FK → users, NOT NULL | 신청자 |
| status | VARCHAR(20) | DEFAULT 'pending' | pending / accepted / rejected |
| message | TEXT | | 신청 메시지 |
| created_at | TIMESTAMPTZ | DEFAULT now() | 신청일 |

> UNIQUE(group_id, applicant_id) — 한 모집에 중복 신청 방지

```sql
CREATE TABLE study_groups (
    id SERIAL PRIMARY KEY,
    leader_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    max_members INTEGER NOT NULL,
    current_members INTEGER DEFAULT 1,
    status VARCHAR(20) DEFAULT '모집중' NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE applications (
    id SERIAL PRIMARY KEY,
    group_id INTEGER NOT NULL REFERENCES study_groups(id) ON DELETE CASCADE,
    applicant_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'pending' NOT NULL,
    message TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(group_id, applicant_id)
);
```

---

## 비즈니스 로직

### 신청 가능 조건

```python
# 모집이 열려있고, 인원이 안 찼을 때만 신청 가능
if group.status != '모집중':
    raise 400("모집이 마감되었습니다")
if group.current_members >= group.max_members:
    raise 400("인원이 가득 찼습니다")
```

### 수락 시 인원 증가

```python
# 수락하면 current_members += 1
# current_members >= max_members가 되면 자동으로 status = '모집완료'
```

### 거절/취소

```python
# 거절: application.status = 'rejected'
# 수락 취소: current_members -= 1, 모집완료 → 모집중으로 복원
```

---

## API 엔드포인트

### 스터디 모집
| Method | Endpoint | 설명 | 권한 |
|---|---|---|---|
| GET | /groups | 모집글 목록 | 전체 |
| POST | /groups | 모집글 작성 | 로그인 |
| GET | /groups/{id} | 모집 상세 (신청 목록 포함) | 전체 |
| PATCH | /groups/{id} | 모집글 수정 (조장만) | 조장 |
| DELETE | /groups/{id} | 모집글 삭제 (조장만) | 조장 |

### 신청
| Method | Endpoint | 설명 | 권한 |
|---|---|---|---|
| POST | /groups/{id}/apply | 스터디 신청 | 로그인 |
| GET | /groups/{id}/applications | 신청 목록 (조장만) | 조장 |
| PATCH | /applications/{id} | 신청 수락/거절 | 조장 |

---

## 학습 포인트

1. 테이블 분리의 이유 — posts에 모집 기능을 넣으면 nullable 컬럼이 많아지고 역할이 모호해짐
2. 상태 머신 패턴 — pending → accepted / rejected 전이
3. current_members 정합성 — 수락/거절/취소 시 정확한 증감
4. 트랜잭션의 필요성 — 수락 + 인원 증가가 동시에 일어나야 함
