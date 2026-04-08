# Phase 5 설명

## 구현 내용

Phase 5에서는 커뮤니티(posts)와 별개의 "스터디 모집 시스템"을 구축했습니다. 모집글 생성, 스터디 신청, 신청 내역 수락/거절/대기 등의 상태 머신 패턴 로직이 도입되었습니다.

## 핵심 분리 테이블

### 1. study_group
- **용도**: 조장이 스터디원을 모집하기 위한 게시글
- **특징**: 커뮤니티(`posts`) 테이블에 모집 기능용 추가 컬럼(최대 인원 등)을 붙이는 대신, 별도의 테이블로 완전히 수평 분리(Normalization)하였습니다. 이렇게 함으로써 `posts` 테이블의 모호함을 줄였습니다.
- **주요 필드**: `max_members`, `current_members`, `status` (`모집중` / `모집완료`)

### 2. application
- **용도**: 일반 유저가 스터디에 신청한 내역
- **특징**: `group_id`와 `applicant_id` 복합 유니크 제약조건을 통해 한 명이 같은 스터디에 여러 번 중복 신청하는 것을 DB 레벨에서 방지하였습니다.
- **상태 관리**: `pending`(대기), `accepted`(수락), `rejected`(거절), `canceled`(취소)

## 비즈니스 및 상태 전이 로직

- **신청 (Apply)**: `student_group`의 상태가 `"모집중"`이면서, `current_members < max_members` 일 때만 신청이 가능토록 보장합니다. 동일인 중복 신청도 방지됩니다.
- **수락 (Accept)**: 조장이 신청을 수락(`accepted`로 상태 변경)하면 자동으로 모집글의 `current_members`가 1 증가합니다. 만약 수락으로 인해 `current_members`가 `max_members`에 도달하면 `study_group`의 상태가 `"모집완료"`로 자동 변경됩니다.
- **거절 및 수락 취소**: 이미 수락했던 신청을 거절(`rejected`)하거나 대기 상태(`pending`)로 복원할 경우, 다시 `current_members`가 1 감소하고 필요 시 모집글의 상태가 `"모집완료"`에서 `"모집중"`으로 자동으로 롤백됩니다.
- 이 모든 과정은 DB 서비스 레이어에서 트랜잭션의 컨텍스트를 활용해 오작동(인원 초과 버그 등)을 방지하도록 작성되었습니다.

## 추가된 API 엔드포인트

| Method | Endpoint | 설명 | 권한 |
|---|---|---|---|
| GET | `/api/v1/groups` | 전체 모집글 목록 조회 | 전체 허용 |
| GET | `/api/v1/groups/{id}` | 모집 상세 조회 | 전체 허용 |
| POST | `/api/v1/groups` | 신규 스터디 그룹 모집글 생성 | 로그인 유저 |
| PATCH | `/api/v1/groups/{id}` | 모집글 수정 (정원 등) | 작성자(조장) |
| DELETE | `/api/v1/groups/{id}` | 모집글 삭제 | 작성자(조장) |
| POST | `/api/v1/groups/{id}/apply` | 스터디에 신청 | 로그인 유저 |
| GET | `/api/v1/groups/{id}/applications` | 특정 모집글의 신청 내역 조회 | 작성자(조장) |
| PATCH | `/api/v1/applications/{id}` | 신청 건에 대한 상태 업데이트 (수락/거절 등) | 조장 |

## 학습 포인트 구현 확인

- [x] 테이블 분리의 이유를 몸소 체감 (`study_group`과 `post`의 차이 구축)
- [x] 상태 머신 패턴(`pending` → `accepted` / `rejected`) 적용 및 `increment/decrement` 부수 효과 트리거 구현
- [x] `current_members` 정합성 보장 (동시성 처리의 기초 뼈대 구축)
