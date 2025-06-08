from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import *

@api_view(['GET'])
def coche_list(request):
    coche = Coche.objects.all()
    serializer = CocheSerializer(coche, many=True)
    return Response(serializer.data)
