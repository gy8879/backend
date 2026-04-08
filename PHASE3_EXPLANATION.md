# Phase 3 설명

## 구현 목표

- 게시글에 이미지 첨부 기능 추가
- Supabase Storage 업로드/삭제 연동
- 게시글 상세 응답에 이미지 목록 포함

## DB 변경 사항

### post_image (신규)

- 컬럼: `id`, `post_id`, `image_url`, `created_at`
- 게시글 1개에 이미지 N개(1:N) 구조
- 현재 프로젝트는 단수 테이블명 기준이라 FK는 `post(id)`를 참조

```sql
CREATE TABLE post_image (
    id SERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL REFERENCES post(id) ON DELETE CASCADE,
    image_url TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);
```

## 핵심 로직

### 1) 이미지 업로드

- 엔드포인트: `POST /api/v1/posts/{post_id}/images`
- 요청 형식: `multipart/form-data` (`image` 파일)
- 처리 순서:
  1. 게시글 존재/작성자 권한 확인
  2. Supabase Storage 버킷(`post-images`)에 업로드
  3. 공개 URL 생성
  4. `post_image` 테이블에 URL 저장

### 2) 이미지 삭제

- 엔드포인트: `DELETE /api/v1/posts/{post_id}/images/{image_id}`
- 처리 순서:
  1. 게시글/이미지 존재 및 작성자 권한 확인
  2. Storage 객체 삭제
  3. `post_image` 레코드 삭제

### 3) 게시글 상세 응답 확장

- `GET /api/v1/posts/{post_id}` 응답에 `images` 배열 포함
- 각 이미지 항목: `id`, `image_url`, `created_at`
- 기존 `comments` 필드와 함께 `images`가 같이 내려가도록 확장

## 환경변수

`.env`에 아래 값이 필요함:

```env
SUPABASE_URL=https://<project-ref>.supabase.co
SUPABASE_SERVICE_ROLE_KEY=<service-role-key>
```

## 의존성

- `python-multipart` 추가 (파일 업로드 처리용)

## 제출 시 설명 포인트 (권장)

- DB에는 파일 자체가 아니라 URL을 저장한다는 점
- JSON 요청과 multipart/form-data 요청 차이
- 작성자 권한 체크 후 업로드/삭제 처리 방식
