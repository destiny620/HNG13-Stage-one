from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import StringAnalysis
from .serializers import StringAnalysisSerializer
from django.db import IntegrityError
from django.core.exceptions import ValidationError

@api_view(['POST'])
def create_string_analysis(request):
    try:
        # Check if value field exists
        if 'value' not in request.data:
            return Response(
                {"error": "Missing required field 'value'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate data type
        if not isinstance(request.data['value'], str):
            return Response(
                {"error": "Invalid data type - value must be string"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Process the string analysis
        string_value = request.data['value']
        
        # Check for duplicate
        try:
            existing = StringAnalysis.objects.get(string_value=string_value)
            return Response(
                {"error": "String already analyzed"},
                status=status.HTTP_409_CONFLICT
            )
        except StringAnalysis.DoesNotExist:
            analysis = StringAnalysis.analyze_string(string_value)
            serializer = StringAnalysisSerializer(analysis)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    except ValidationError as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_string_analysis(request, string_value=None):
    try:
        if string_value:
            # Get specific string analysis
            try:
                analysis = StringAnalysis.objects.get(string_value=string_value)
                serializer = StringAnalysisSerializer(analysis)
                return Response(serializer.data)
            except StringAnalysis.DoesNotExist:
                return Response(
                    {"error": "String not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        # Handle filters for GET all
        filters = {}
        
        # Natural language filter support
        if 'length' in request.query_params:
            filters['length'] = request.query_params['length']
        if 'palindrome' in request.query_params:
            filters['is_palindrome'] = request.query_params['palindrome'].lower() == 'true'
        if 'word_count' in request.query_params:
            filters['word_count'] = request.query_params['word_count']

        analyses = StringAnalysis.objects.filter(**filters)
        serializer = StringAnalysisSerializer(analyses, many=True)
        return Response(serializer.data)

    except ValidationError as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['DELETE'])
def delete_string_analysis(request, string_value):
    try:
        analysis = StringAnalysis.objects.get(string_value=string_value)
        analysis.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except StringAnalysis.DoesNotExist:
        return Response(
            {"error": "String not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )