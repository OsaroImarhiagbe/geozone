from datetime import timedelta

from fastapi import status
from passlib.context import CryptContext

from app.core.config import settings
from app.modules.auth.infrastructure.auth_dal.auth_dal import AuthRepositories
from app.modules.auth.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    Token,
    TokenResponse,
    UserAuthenticationData,
)

from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

from jose import jwt

from app.core.config import settings

class AuthService:
    """ Serivce handles the authentication and autherization within the backend application"""
    
    def __init__(self, repo:AuthRepositories, pwd_context=CryptContext(schemes=["bcrypt"]),token=settings.access_token_expire_minutes):
        self.__pwd_context = pwd_context
        self.__repo = repo
        self.__token_expire_minutes = token

    
    async def login_user(self,request: LoginRequest) -> TokenResponse:
        """
        Service Layer function to check user credentials against the database
        """
        # Query database for email and password
        user  = await self.__repo.grab_user_by_email(email=request.email)

        # verify password
        if not self._verify_password(request.password.get_secret_value(), user.hashed_password):
            raise ValueError("Incorrect email or password")
                
        ## if we have a user and user is a current active user (ex. not deleted account we will issue new access_token upon login)
        access_token_expires = timedelta(minutes=self.__token_expire_minutes) #ex. 15 minutes

        # Signing and Createing access token
        access_token = self.create_access_token(
            subject=user.id,
            role=user.role,
            email_verified=user.email_verified,
            expires_delta=access_token_expires
        )
        # Creating refresh token
        # first version of the
        refresh_token = self.create_refresh_token(subject=user.id,ver=1) # id coming from database, look into the versioning for refresh token

        return TokenResponse(
            status=status.HTTP_200_OK,
            error="",
            data=Token(
                access_token=access_token,
                refresh_token=refresh_token,
                user= UserAuthenticationData(
                    user_id=user.user_id,
                    authenticated=user.is_authenticated
                )
            )
            )
    
    async def register_user(self,request:RegisterRequest) -> TokenResponse:
        """
        Service layer for user registration
        """
        print('Checking if user exists')
        # Step 1: verify if email exists in database
        exisiting_user = await self.__repo.grab_user_by_email(email=request.email)
        if exisiting_user:
            raise ValueError('Email already exists')
        
        # hashed user password if email doesn't exists
        hashed_password = self._get_password(request.password.get_secret_value())

        # create the user within the db,.
        user = await self.__repo.create_user(request.email,hashed_password)

        print('Creating jwt......')
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes) #ex. 15 minutes

        # Signing and Createing access token
        access_token = create_access_token(
            subject=user.user_id,
            role=user.role,
            email_verified=user.email_verified,
            expires_delta=access_token_expires
        )
        # Creating refresh token
        # Create first version of refresh token for new user
        version = 1
        refresh_token = create_refresh_token(subject=user.user_id,ver=version) # id coming from database

        print('JWT has been created returning to the client......')
        return TokenResponse(
            status=status.HTTP_200_OK,
            error="",
            data=Token(
                access_token=access_token,
                refresh_token=refresh_token,
                user= UserAuthenticationData(
                    user_id=user.user_id,
                    email=user.email
                )
            )
            )
    


    def _verify_password(self,plain_password:str, hash_password:str) -> bool:
        """ Verifying plain password against hashed password"""
        return self.__pwd_context.verify(plain_password, hash_password)
    

    def _get_password(self,password:str) -> str:  
        return self.__pwd_context.hash(password)

    def create_access_token(self,subject: str,role:str,email_verified:bool,expires_delta: timedelta | None = None) -> str:
        """Creates JWT Access Token."""
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)

        to_encode = {
            "sub":str(subject),
            "email_verified":email_verified,
            "iss":"https://yourdomain.com", # We will figure out how to add the iss later and aud
            "role":role,
            "iat":datetime.now(UTC),
            "exp":expire,
        }

        ## Creating and Signing access token
        encode_jwt = jwt.encode(
            to_encode,
            settings.secret_key.get_secret_value(), 
            algorithm=settings.algorithm.get_secret_value()
        )

        return encode_jwt

    def create_refresh_token(self,subject:str,ver:int) -> str:
        """ Create JWT refresh token"""

        expire = datetime.now(UTC) + timedelta(days=settings.refresh_token_expire_days)

        to_encode = {
            "sub":str(subject),
            "ver":ver,
            "jti":str(uuid4()),
            "iss":"https://yourdomain.com",
            "iat":datetime.now(UTC),
            "exp":expire,
        }

        encode_jwt = jwt.encode(
            to_encode, 
            settings.secret_key.get_secret_value(), 
            algorithm=settings.algorithm.get_secret_value()
        )

        return encode_jwt
    

    def decode_token(token:str) -> dict[str,Any]:
        """ Decode JWT token to verify it"""
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        if not payload:
            raise ValueError("Invalid token!")
            
        return payload