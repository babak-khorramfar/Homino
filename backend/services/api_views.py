from rest_framework.views import APIView
from rest_framework.response import Response
from services.models import ServiceCategory
from services.serializers import ServiceCategorySerializer


class CategoryListView(APIView):
    def get(self, request):
        parents = ServiceCategory.objects.filter(parent__isnull=True)
        serializer = ServiceCategorySerializer(parents, many=True)
        return Response(serializer.data)
