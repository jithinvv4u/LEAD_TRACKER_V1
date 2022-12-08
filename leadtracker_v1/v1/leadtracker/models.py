""" Models for leadtracker """

from django.db import models

from common.models import AbstractBaseModel
from common.library import get_file_path

from django.utils.translation import gettext_lazy as _
from v1.leadtracker import constants as lead_consts
# Create your models here.


class Tag(AbstractBaseModel):
    """
    Model to save lead tag details.

    Attribs:
        name(char)       : Lead tag name.
        
    Inherited Attribs:
        creator(obj): Creator user of the object.
        updater(obj): Updater of the object.
        created_on(datetime): Added date of the object.
        updated_on(datetime): Last updated date of the object.
    """
    name = models.CharField(
        max_length=100, verbose_name=_('Tag Name'))
    
    def __str__(self):
        """String format of model object"""
        return f'{self.name}'
    
class StagePreset(AbstractBaseModel):
    """
    Model to all stage presets.

    Attribs:
        name(char)    : Name of all presets.
        is_active(int): True if preset is active(default=True)
                
    Inherited Attribs:
        creator(obj): Creator user of the object.
        updater(obj): Updater of the object.
        created_on(datetime): Added date of the object.
        updated_on(datetime): Last updated date of the object.
    """
    name = models.CharField(
        max_length=100, verbose_name=_('Preset Name'))
    is_active = models.BooleanField(
        default=True, verbose_name=_('Is Active'))

    def __str__(self):
        """String format of model object"""
        return f'{self.name}'

class Lead(AbstractBaseModel):
    """
    Model to save Lead details.

    Attribs:
        name(char)       : Lead name.
        pipedrive(char   : Lead pipedrive link.
        team_size(int)   : current team size information.
        revenue(float)   : Revenue of Lead.
        lead_source(char): Source of lead.
        is_active(int)   : True if lead is active(default=True)

    Inherited Attribs:
        preset_id(obj): Lead current Stage Preset.
        current_stage(obj): The Lead Current stage.
        preset_id(obj): Creator user of the object.
        creator(obj): Creator user of the object.
        updater(obj): Updater of the object.
        created_on(datetime): Added date of the object.
        updated_on(datetime): Last updated date of the object.
    """
    preset_id = models.ForeignKey(
        'leadtracker.StagePreset', on_delete=models.CASCADE,
        related_name='leads', verbose_name=_('Preset ID'),
        blank=True, null=True, default=None)
    name = models.CharField(
        max_length=100, verbose_name=_('Lead Name'))
    pipedrive = models.URLField(
        max_length=1024, default='', blank=True, null=True,
        verbose_name=_('Pipedrive Link'))
    team_size = models.PositiveIntegerField(
        default=0, null=True, blank=True, verbose_name=_('Team Size'))
    revenue = models.FloatField(
        default=0, null=True, blank=True, verbose_name=_('Revenue'))
    lead_source = models.IntegerField(
        default=lead_consts.LeadSourceChoice.LINKEDIN,
        choices=lead_consts.LeadSourceChoice.choices(),
        verbose_name=_('Lead Source'))
    is_active = models.BooleanField(
        default=True, verbose_name=_('Is Active'))
    current_stage = models.ForeignKey(
        'leadtracker.Stage', on_delete=models.CASCADE,
        related_name='leads', verbose_name=_('Current Stage'),
        blank=True, null=True, default=None)
    
    def __str__(self):
        """String format of model object"""
        return f'{self.name}'
    
    
class Organization(AbstractBaseModel):
    """
    Model to save organization details.

    Attribs:
        name(char)  : Name of Organization.
        email(obj)  : Organization email.
        website(obj): Organization website.
        country(obj): Organization country.

    Inherited Attribs:
        lead_id(obj): Lead object of organization.
        creator(obj): Creator user of the object.
        updater(obj): Updater of the object.
        created_on(datetime): Added date of the object.
        updated_on(datetime): Last updated date of the object.
    """
    lead_id = models.ForeignKey(
        'leadtracker.Lead', on_delete=models.CASCADE, related_name='organizations',
        verbose_name=_('Lead ID'), blank=True, null=True, default=None)
    name = models.CharField(
        max_length=100, verbose_name=_('Organization Name'))
    email = models.EmailField(verbose_name=_('Organization Email'))
    website = models.CharField(
        max_length=500, default='', blank=True, null=True,
        verbose_name=_('organization website'))
    country = models.CharField(
        max_length=100, verbose_name=_('Organization Country'),
        default='', blank=True, null=True,
        
    )
    
    def __str__(self):
        """String format of model object"""
        return f'{self.name}'
    
    
class LeadTag(AbstractBaseModel):
    """
    Model to save lead tag details.
        
    Inherited Attribs:
        lead_id(obj): Lead object of lead tag.
        tag_id(obj) : Tag object of lead tag.
        creator(obj): Creator user of the object.
        updater(obj): Updater of the object.
        created_on(datetime): Added date of the object.
        updated_on(datetime): Last updated date of the object.
    """
    lead_id = models.ForeignKey(
        'leadtracker.Lead', on_delete=models.CASCADE, related_name='tags',
        verbose_name=_('Lead'), blank=True, null=True, default=None)
    tag_id = models.ForeignKey(
        'leadtracker.Tag', on_delete=models.CASCADE, related_name='tags',
        verbose_name=_('Tag'), blank=True, null=True, default=None)
    
    
class Stage(AbstractBaseModel):
    """
    Model to save Stage details.

    Attribs:
        name(char)    : Stage name.
        is_active(int): True if stage is active(default=True).
        default(bool) : Default stage for lead.
        weightage(int): Used for stage representation.
        credit(int)   : The value given to each stage.

    Inherited Attribs:
        preset_id(obj): Preset object of stage.
        creator(obj): Creator user of the object.
        updater(obj): Updater of the object.
        created_on(datetime): Added date of the object.
        updated_on(datetime): Last updated date of the object.
    """
    preset_id = models.ForeignKey(
        'leadtracker.StagePreset', on_delete=models.CASCADE,
        related_name='stages', verbose_name=_('Preset ID'), 
        blank=True, null=True, default=None)
    name = models.CharField(
        max_length=100, verbose_name=_('Stage Name'))
    is_active = models.BooleanField(
        default=True, verbose_name=_('Is Active'))
    default = models.BooleanField(
        default=False, verbose_name=_('Default Stage'))
    weightage = models.SmallIntegerField(default=0)
    credit = models.SmallIntegerField(default=1)

    def __str__(self):
        """String format of model object"""
        return f'{self.name}'
    
    
class Question(AbstractBaseModel):
    """
    Model to save Questions.

    Attribs:
        question(char): field to store questions.
        type(int)     : Common and lead journey questions.
        field_type(int):Question field type.
        weightage(int): Used to represetn questions.
        credit(int)   : Represent questions based on priority.

    Inherited Attribs:
        preset_id(obj): Preset object of stage.
        creator(obj): Creator user of the object.
        updater(obj): Updater of the object.
        created_on(datetime): Added date of the object.
        updated_on(datetime): Last updated date of the object.
    """
    preset_id = models.ForeignKey(
        'leadtracker.StagePreset', on_delete=models.CASCADE,
        related_name='questions', verbose_name=_('Preset ID'),
        blank=True, null=True, default=None)
    question = models.CharField(
        max_length=500, verbose_name=_('Question'))
    type = models.IntegerField(
        default=lead_consts.QuestionType.COMMON,
        choices=lead_consts.QuestionType.choices(),
        verbose_name=_('Question Type'))
    field_type = models.IntegerField(
        default=lead_consts.QuestionTypeChoice.TEXT,
        choices=lead_consts.QuestionTypeChoice.choices(),
        verbose_name=_('Question Field Type'))
    weightage = models.SmallIntegerField(default=0)
    credit = models.SmallIntegerField(default=1)

    def __str__(self):
        return f'{self.question}'

class Option(AbstractBaseModel):
    """
    Model to save options of each question.

    Attribs:
        option(char)  : options based on questions.
        points(int)   : points for each options.
        is_active : True if ansewr is active(default=True)

    Inherited Attribs:
        question_id(obj): Question object of option.
        creator(obj): Creator user of the object.
        updater(obj): Updater of the object.
        created_on(datetime): Added date of the object.
        updated_on(datetime): Last updated date of the object.
    """
    question_id = models.ForeignKey(
        'leadtracker.Question', on_delete=models.CASCADE,
        related_name='questions', verbose_name=_('Question'), 
        blank=True, null=True, default=None)
    option = models.CharField(
        max_length=500, verbose_name=_('Options'),
        default='', blank=True, null=True)
    points = models.SmallIntegerField(default=1)
    is_active = models.BooleanField(
        default=True, verbose_name=_('Is Active'))

    def __str__(self):
        return self.option


class StageAnswer(AbstractBaseModel):
    """
    Model to save Stage Answer.

    Attribs:
        is_active(int) : True if stage answer is active(default=True)
        score(int) : Add score to each answers.

    Inherited Attribs:
        option_id(obj): Option object of stage answer.
        lead_id(obj): Lead object of stage answer.
        stage_id(obj): stage object of stage answer.
        creator(obj): Creator user of the object.
        updater(obj): Updater of the object.
        created_on(datetime): Added date of the object.
        updated_on(datetime): Last updated date of the object.
    """
    option_id = models.ForeignKey(
        'leadtracker.Option', on_delete=models.CASCADE,
        related_name='stageanswers', verbose_name=_('Option'), 
        blank=True, null=True, default=None)
    question_id = models.ForeignKey(
        'leadtracker.Question', on_delete=models.CASCADE,
        related_name='stageanswers', verbose_name=_('Question'), 
        blank=True, null=True, default=None)
    lead_id = models.ForeignKey(
        'leadtracker.Lead', on_delete=models.CASCADE, related_name='answers',
        verbose_name=_('Lead'), blank=True, null=True, default=None)
    stage_id = models.ForeignKey(
        'leadtracker.Stage', on_delete=models.CASCADE,
        related_name='stageanswers', verbose_name=_('Stage'), 
        blank=True, null=True, default=None)
    is_active = models.BooleanField(
        default=True, verbose_name=_('Is Active'))
    score = models.IntegerField(default=0)
    

class GeneralAnswer(AbstractBaseModel):
    """
    Model to save General Answer.

    Attribs:
        is_active(int) : True if stage answer is active(default=True)
        score(int) : Add score to each answers.

    Inherited Attribs:
        answer_id(obj): Answer object of stage answer.
        lead_id(obj): Lead object of stage answer.
        creator(obj): Creator user of the object.
        updater(obj): Updater of the object.
        created_on(datetime): Added date of the object.
        updated_on(datetime): Last updated date of the object.
    """
    option_id = models.ForeignKey(
        'leadtracker.Option', on_delete=models.CASCADE,
        related_name='generalanswers', verbose_name=_('Option'), 
        blank=True, null=True, default=None)
    question_id = models.ForeignKey(
        'leadtracker.Question', on_delete=models.CASCADE,
        related_name='generalanswers', verbose_name=_('Question'), 
        blank=True, null=True, default=None)
    lead_id = models.ForeignKey(
        'leadtracker.Lead', on_delete=models.CASCADE, 
        related_name='generalanswers',verbose_name=_('Lead'), 
        blank=True, null=True, default=None)
    is_active = models.BooleanField(
        default=True, verbose_name=_('Is Active'))
    score = models.IntegerField(default=0)
    
    
class Contact(AbstractBaseModel):
    """
    Model to save Contact Details.

    Attribs:
        name(char)     : Name of lead
        email(email)   : email id of lead
        organization(char): name of organization
        role(char)     : role of person in that organization
        linkedin(char) : LinkedIn link.

    Inherited Attribs:
        creator(obj): Creator user of the object.
        updater(obj): Updater of the object.
        created_on(datetime): Added date of the object.
        updated_on(datetime): Last updated date of the object.
    """
    name = models.CharField(
        max_length=100,verbose_name=_('Name'))
    email = models.EmailField(verbose_name=_('Email'))
    organization = models.CharField(
        max_length=100, default='', blank=True, null=True,
        verbose_name=_('Organization Name'))
    role = models.CharField(
        max_length=100, default='', blank=True, null=True,
        verbose_name=_('Role'))
    linkedin = models.URLField(
        max_length=1024, default='', blank=True, null=True,
        verbose_name=_('LinkedIn'))
    
    def __str__(self):
        """String format of model object"""
        return f'{self.name}'
    
    
class LeadContact(AbstractBaseModel):
    """
    Model to save Lead Contact.

    Attribs:
        is_decision_maker(char): Lead is decision maker or not.
        is_board_member(email) : Lead is a board member or not.

    Inherited Attribs:
        contact_id(obj): contact object of lead contact.
        lead_id(obj): lead object of the lead contact.
        stage_id(obj): stage object of the lead contact.
        creator(obj): Creator user of the object.
        updater(obj): Updater of the object.
        created_on(datetime): Added date of the object.
        updated_on(datetime): Last updated date of the object.
    """
    contact_id = models.ForeignKey(
        'leadtracker.Contact', on_delete=models.CASCADE,
        related_name='contacts', verbose_name=_('Contact ID'), 
        blank=True, null=True, default=None)
    lead_id = models.ForeignKey(
        'leadtracker.Lead', on_delete=models.CASCADE, related_name='contacts',
        verbose_name=_('Lead ID'), blank=True, null=True, default=None)
    stage_id = models.ForeignKey(
        'leadtracker.Stage', on_delete=models.CASCADE,
        related_name='contacts', verbose_name=_('Stage ID'), 
        blank=True, null=True, default=None)
    is_decision_maker = models.BooleanField(
        default=False, verbose_name=_('Is Decision Maker'))
    is_board_member = models.BooleanField(
        default=False, verbose_name=_('Is Board Member'))