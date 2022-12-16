from rest_framework import viewsets
from v1.leadtracker.models import Lead

class IdDecodeModelViewSet(viewsets.ModelViewSet):
    """
    Viewset to decode idencode to normal id
    """

    lookup_url_kwarg = 'idencode'

    def get_object(self):
        print(self.basename)
        return Lead.objects.get_by_encoded_id(self.kwargs['idencode'])
