# Phase 6 — 그룹 예약: "혼자 말고 같이"

> 난이도: ★★★★☆ | 핵심: 모임 단위 예약, 다중 테이블 검증, 트랜잭션

---

## 목표

- 모집 완료된 스터디 그룹이 스터디룸을 예약
- 그룹 인원 ≤ 룸 capacity 검증
- 개인 예약과 그룹 예약 공존

---

## DB 변경사항

### reservations — 컬럼 추가

| 컬럼 | 타입 | 제약조건 | 설명 |
|---|---|---|---|
| group_id | INTEGER | FK → study_groups, NULLABLE | 그룹 예약인 경우 그룹 ID |

```sql
ALTER TABLE reservations ADD COLUMN group_id INTEGER REFERENCES study_groups(id) ON DELETE SET NULL;
```

> group_id가 NULL이면 개인 예약, 값이 있으면 그룹 예약

---

## 비즈니스 로직

### 그룹 예약 조건

```python
# 1. 그룹이 모집완료 상태여야 함
if group.status != '모집완료':
    raise 400("모집이 완료된 그룹만 예약할 수 있습니다")

# 2. 예약자가 조장이어야 함
if user.id != group.leader_id:
    raise 403("조장만 그룹 예약을 할 수 있습니다")

# 3. 그룹 인원이 룸 수용인원 이하여야 함
if group.current_members > room.capacity:
    raise 400("그룹 인원이 수용 인원을 초과합니다")

# 4. 시간 겹침 방지 (기존 로직 동일)
# 5. 운영시간 내 확인 (Phase 4 로직)
```

### 예약 시 capacity 계산 변경

```python
# 겹치는 시간대의 총 인원 계산
# 개인 예약 = 1명, 그룹 예약 = group.current_members명
total_occupancy = sum(
    1 if r.group_id is None else r.group.current_members
    for r in overlapping_reservations
)
if total_occupancy + new_reservation_members > room.capacity:
    raise 400("수용 인원을 초과합니다")
```

---

## API 변경

### 예약 생성 확장
| Method | Endpoint | 설명 | 권한 |
|---|---|---|---|
| POST | /reservations | group_id 필드 추가 (선택) | 로그인 / 조장 |

### 요청 예시

```json
// 개인 예약 (기존과 동일)
{
  "room_id": 1,
  "start_time": "2026-04-01T14:00:00",
  "end_time": "2026-04-01T16:00:00"
}

// 그룹 예약 (group_id 추가)
{
  "room_id": 1,
  "start_time": "2026-04-01T14:00:00",
  "end_time": "2026-04-01T16:00:00",
  "group_id": 3
}
```

---

## 학습 포인트

1. nullable FK의 의미 — 하나의 테이블이 두 가지 사용 패턴을 지원
2. 다중 테이블 조인 검증 — reservations + study_groups + study_rooms
3. 트랜잭션의 중요성 — 예약 생성 + occupancy 체크가 원자적으로 이루어져야 함
4. 복잡한 비즈니스 로직의 단계적 검증 — 상태 체크 → 권한 체크 → 인원 체크 → 겹침 체크
