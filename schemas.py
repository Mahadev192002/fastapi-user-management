from datetime import datetime   # Import datetime for handling date and time fields in the PostResponse model
 
from pydantic import BaseModel, ConfigDict, EmailStr, Field  # Import necessary classes and functions from Pydantic for data validation and modeling


class UserBase(BaseModel): # Base Pydantic model for user data, used as a base for creating and responding with user information
    username: str = Field(min_length=1, max_length=50) # Username field with validation for minimum and maximum length
    email: EmailStr = Field(max_length=120) # Email field with validation to ensure it's a valid email address and has a maximum length
    


class UserCreate(UserBase):  # Pydantic model for creating a new user, inherits from UserBase and can be extended with additional fields if needed
    pass 


class UserResponse(UserBase): # Pydantic model for responding with user information, inherits from UserBase and includes additional fields for the response
    model_config = ConfigDict(from_attributes=True) # Configuration to allow creating a UserResponse model instance from an ORM model (like SQLAlchemy models)

    id: int     # ID field for the user, included in the response
    image_file: str | None  # Image file field for the user's profile picture, can be None if the user has not uploaded a profile picture
    image_path: str # Image path field for the user's profile picture, included in the response and generated from the image_file field
    
    
      
class UserUpdate(BaseModel): # Pydantic model for updating user information, used for validating data when updating a user's profile, with all fields optional to allow partial updates
    username: str | None = Field(default=None, min_length=1, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=120)
    image_file: str | None = Field(default=None, min_length=1, max_length=200)


class PostBase(BaseModel):  # Base Pydantic model for post data, used as a base for creating and responding with post information
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)


class PostCreate(PostBase): # Pydantic model for creating a new post, inherits from PostBase and can be extended with additional fields if needed
    user_id: int  # TEMPORARY

class PostUpdate(BaseModel): # Pydantic model for updating post information, used for validating data when updating a post, with all fields optional to allow partial updates
    title: str | None = Field(default=None, min_length=1, max_length=100)
    content: str | None = Field(default=None, min_length=1)

class PostResponse(PostBase): # Pydantic model for responding with post information, inherits from PostBase and includes additional fields for the response
    model_config = ConfigDict(from_attributes=True) # Configuration to allow creating a PostResponse model instance from an ORM model (like SQLAlchemy models)

    id: int   # ID field for the post, included in the response
    user_id: int # User ID field for the post, included in the response to indicate which user created the post
    date_posted: datetime # Date posted field for the post, included in the response to indicate when the post was created
    author: UserResponse    # Author field for the post, included in the response and represented as a nested UserResponse model to provide information about the author of the post