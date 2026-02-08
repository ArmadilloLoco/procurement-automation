from rest_framework import generics, permissions
from .models import Product
from .serializers import ProductSerializer

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.select_related('supplier').prefetch_related('attributes')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.select_related('supplier').prefetch_related('attributes')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]