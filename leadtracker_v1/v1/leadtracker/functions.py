from . import models as lead_model
from django.db.models import Count, Sum, F


def get_dashboard():
    """
    Contain data about lead and their possibility to win.
    """
    lead_total = lead_model.Lead.objects.all().count()
    lead_won = lead_model.Lead.objects.filter(status=2).count()
    lead_lost = lead_model.Lead.objects.filter(status=3).count()
    lead_stage = (lead_model.Lead.objects.values(
        stage=F("current_stage__name"))
        .annotate(count=Count("current_stage"))
        .order_by("-count")
    )
    all_stages = (lead_model.Stage.objects.values("name"))
            
    possibility = lead_model.StageAnswer.objects.annotate(
            points_secured=Sum(
                F('option_id__points') * F('question_id__credit')),
            credit_registerd=Count('question_id') * 5, 
            possibility=F('points_secured') / F('credit_registerd')
            ).order_by('lead_id').values('lead_id__name','possibility')
        
    return {
            "lead_total": lead_total,
            "lead_won": lead_won,
            "lead_lost": lead_lost,
            "lead_stage": lead_stage,
            "stages": all_stages,
            "possibility":possibility,
    }
    