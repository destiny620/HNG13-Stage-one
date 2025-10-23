from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import hashlib
from collections import Counter
import re
from .models import StringAnalysis
from .serializers import StringAnalysisSerializer

class StringAnalyzerView(APIView):
    def calculate_string_properties(self, input_string):
        try:
            if not isinstance(input_string, str):
                raise ValueError("Input must be a string")
                
            # Calculate length
            length = len(input_string)
            
            # Check if palindrome
            is_palindrome = input_string.lower() == input_string.lower()[::-1]
            
            # Get unique characters count
            unique_characters = len(set(input_string))
            
            # Count words
            word_count = len(input_string.split())
            
            # Calculate SHA256 hash
            sha256_hash = hashlib.sha256(input_string.encode()).hexdigest()
            
            # Character frequency map
            character_frequency_map = dict(Counter(input_string))
            
            return {
                'string_value': input_string,
                'length': length,
                'is_palindrome': is_palindrome,
                'unique_characters': unique_characters,
                'word_count': word_count,
                'sha256_hash': sha256_hash,
                'character_frequency_map': character_frequency_map
            }
        except Exception as e:
            raise ValueError(str(e))

    def post(self, request):
        try:
            if 'string_value' not in request.data:
                return Response(
                    {'error': 'string_value field is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            input_string = request.data.get('string_value')
            
            # Check if string already exists
            if StringAnalysis.objects.filter(string_value=input_string).exists():
                return Response(
                    {'error': 'String already exists'}, 
                    status=status.HTTP_409_CONFLICT
                )

            try:
                properties = self.calculate_string_properties(input_string)
            except ValueError as e:
                return Response(
                    {'error': str(e)}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = StringAnalysisSerializer(data=properties)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(
                serializer.errors, 
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
            
        except Exception as e:
            return Response(
                {'error': 'Internal server error'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # ...existing code for get method...

    def delete(self, request, string_value):
        try:
            analysis = StringAnalysis.objects.get(string_value=string_value)
            analysis.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except StringAnalysis.DoesNotExist:
            return Response(
                {'error': 'String not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': 'Internal server error'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class NaturalLanguageFilterView(APIView):
    def get(self, request):
        try:
            query = request.query_params.get('query', '').lower()
            queryset = StringAnalysis.objects.all()

            if 'palindromic' in query:
                queryset = queryset.filter(is_palindrome=True)
            
            if 'single word' in query:
                queryset = queryset.filter(word_count=1)
                
            if 'longer than' in query:
                match = re.search(r'longer than (\d+)', query)
                if match:
                    length = int(match.group(1))
                    queryset = queryset.filter(length__gt=length)
                    
            if 'contains' in query:
                match = re.search(r'contains.*([a-z])', query)
                if match:
                    char = match.group(1)
                    queryset = queryset.filter(string_value__contains=char)
                    
            serializer = StringAnalysisSerializer(queryset, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
