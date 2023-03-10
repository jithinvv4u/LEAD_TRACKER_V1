#!/usr/bin/env python
# coding=utf-8
"""Constants under the leadtracker section are stored here."""

from common.library import ChoiceAdapter
from django.db import models
from django.utils.translation import gettext_lazy as _

#Type of questions
class QuestionType(ChoiceAdapter):
    COMMON = 1,
    STAGE = 2,

#Lead source choice
class LeadSourceChoice(ChoiceAdapter):
    LINKEDIN = 1,

#Question field Type choice 
class QuestionTypeChoice(ChoiceAdapter):
    TEXT = 1, 
    RADIO = 2,
    CHECKBOX = 3,
    RANGE = 4,
    BOOL = 5,
    
#Question field Type choice 
class StatusChoice(ChoiceAdapter):
    ACTIVE = 1, 
    WON = 2, 
    LOST = 3, 
    
class RoleChoice(ChoiceAdapter):
    CEO = 1,
    PROJRCT_MANAGER = 2,
    SENIOR_BACKEND_DEVELOPER = 3,
    SENIOR_FRONTEND_DEVELOPER = 4,
    JUNIOR_BACKEND_DEVELOPER = 5,
    JUNIOR_FRONTEND_DEVELOPER = 6,
