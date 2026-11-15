from datetime import timedelta

from fastapi import status
# from passlib.context import CryptContext

from app.core.config import settings


from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

import jwt


from app.core.config import settings

class AIService:
    """ Serivce handles calling Claude API for AI Analysis"""
    
    def __init__(self):
        pass

    async def get_parcel_analysis(self):
        """
        Service layer function makes external API call to Claude LLM API
        """
        pass