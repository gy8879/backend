"""
models 패키지의 __init__.py

여기서 모든 모델을 import 해두면, 다른 곳에서 짧게 쓸 수 있다:

  # 이렇게 길게 안 써도 되고
  from app.models.user import User
  from app.models.post import Post

  # 이렇게 짧게 쓸 수 있다
  from app.models import User, Post
"""

from app.models.user import User
from app.models.study_room import StudyRoom
from app.models.reservation import Reservation
from app.models.post import Post
from app.models.comment import Comment
from app.models.like import Like
