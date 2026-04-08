# Phase 3 — 이미지 업로드: "글에 사진도 넣고 싶은데"

> 난이도: ★★★ | 핵심: Supabase Storage 연동, 파일 업로드/조회

---

## 목표

- 게시글에 이미지를 첨부할 수 있게 확장
- Supabase Storage로 파일 업로드/조회
- 게시글당 여러 이미지 지원 (post_images 테이블)

---

## DB 변경사항

### post_images — 신규 테이블

| 컬럼 | 타입 | 제약조건 | 설명 |
|---|---|---|---|
| id | SERIAL | PK | 이미지 고유 번호 |
| post_id | INTEGER | FK → posts, NOT NULL | 게시글 |
| image_url | TEXT | NOT NULL | 스토리지 URL |
| created_at | TIMESTAMPTZ | DEFAULT now() | 업로드일 |

```sql
CREATE TABLE post_images (
    id SERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    image_url TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);
```

---

## Supabase Storage 설정

1. Supabase 대시보드에서 `post-images` 버킷 생성
2. 공개 읽기 허용 (Public bucket)
3. 업로드는 인증된 유저만 가능

---

## API 변경

### 이미지 업로드
| Method | Endpoint | 설명 |
|---|---|---|
| POST | /posts/{post_id}/images | 이미지 업로드 (multipart/form-data) |
| DELETE | /posts/{post_id}/images/{image_id} | 이미지 삭제 (본인만) |

### 게시글 상세 응답에 이미지 포함

```json
{
  "id": 1,
  "title": "알고리즘 스터디 후기",
  "content": "...",
  "images": [
    { "id": 1, "image_url": "https://xxx.supabase.co/storage/v1/object/public/post-images/abc.png" }
  ]
}
```

---

## 학습 포인트

1. DB에 파일을 직접 저장하지 않는 이유 — URL만 저장, 파일은 스토리지에
2. multipart/form-data vs JSON 요청의 차이
3. 1:N 관계 테이블 추가 설계 (posts ↔ post_images)
4. 외부 스토리지 서비스 연동 경험
