from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text # Import necessary SQLAlchemy types for defining database models
from sqlalchemy.orm import Mapped, mapped_column, relationship # Import necessary classes and functions from SQLAlchemy for defining database models and relationships

from database import Base   # Import Base class from database.py to use as a base for SQLAlchemy models
 

class User(Base):  # Define User model that inherits from Base, representing the users table in the database
    __tablename__ = "users"     # Specify the name of the database table for this model

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True) # Define id column as an integer primary key with indexing for faster queries
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(200), nullable=False)
    image_file: Mapped[str | None] = mapped_column( # Define image_file column as a string that can be null, used to store the filename of the user's profile picture
        String(200),
        nullable=True,
        default=None,
    )
    # Define a relationship to the Post model, allowing access to the posts created by the user through the posts attribute. The back_populates parameter establishes a bidirectional relationship with the author attribute in the Post model. The cascade option ensures that when a user is deleted, all their associated posts are also deleted.
    posts: Mapped[list[Post]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
    )
    # Define a relationship to the PasswordResetToken model, allowing access to the password reset tokens associated with the user through the reset_tokens attribute. The back_populates parameter establishes a bidirectional relationship with the user attribute in the PasswordResetToken model. The cascade option ensures that when a user is deleted, all their associated password reset tokens are also deleted.
    reset_tokens: Mapped[list[PasswordResetToken]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    @property  # Define a property method to generate the image path for the user's profile picture based on the image_file field
    def image_path(self) -> str:
        if self.image_file:
            return f"/media/profile_pics/{self.image_file}"
        return "/static/profile_pics/default.jpg"


class Post(Base): # Define Post model that inherits from Base, representing the posts table in the database
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column( # Define user_id column as an integer foreign key that references the id column in the users table, used to establish a relationship between posts and users
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    date_posted: Mapped[datetime] = mapped_column( # Define date_posted column as a DateTime with timezone support, used to store the date and time when the post was created
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )

    author: Mapped[User] = relationship(back_populates="posts") # Define a relationship to the User model, allowing access to the author of the post through the author attribute
    
    
class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )

    user: Mapped[User] = relationship(back_populates="reset_tokens")