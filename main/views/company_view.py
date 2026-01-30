from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import OpenApiResponse, extend_schema

from main.models import Company
from main.serializers import CompanySerializer


class CompanyAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        return Company.objects.first()

    @extend_schema(
        tags=["Company"],
        description="Company ma'lumotini olish (singleton). Anonymous faqat ko'radi.",
        responses={200: CompanySerializer},
    )
    def get(self, request, *args, **kwargs):
        company = self.get_object()
        if not company:
            return Response(None, status=status.HTTP_200_OK)
        serializer = CompanySerializer(company)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Company"],
        description="Company yaratish (faqat bir marta).",
        request=CompanySerializer,
        responses={201: CompanySerializer, 400: OpenApiResponse(description="Company already exists.")},
    )
    def post(self, request, *args, **kwargs):
        if Company.objects.exists():
            return Response(
                {"detail": "Company already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = CompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        tags=["Company"],
        description="Company to'liq yangilash.",
        request=CompanySerializer,
        responses={200: CompanySerializer, 404: OpenApiResponse(description="Company not found.")},
    )
    def put(self, request, *args, **kwargs):
        company = self.get_object()
        if not company:
            return Response({"detail": "Company not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = CompanySerializer(company, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Company"],
        description="Company qisman yangilash.",
        request=CompanySerializer,
        responses={200: CompanySerializer, 404: OpenApiResponse(description="Company not found.")},
    )
    def patch(self, request, *args, **kwargs):
        company = self.get_object()
        if not company:
            return Response({"detail": "Company not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = CompanySerializer(company, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # @extend_schema(
    #     tags=["Company"],
    #     description="Company o'chirish.",
    #     responses={204: OpenApiResponse(description="Deleted.")},
    # )
    # def delete(self, request, *args, **kwargs):
    #     company = self.get_object()
    #     if not company:
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     company.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
