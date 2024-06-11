from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Job, Task
from .serializers import StartScrapingSerializer
from .tasks import scrape_coin_data

class StartScrapingView(APIView):
    def post(self, request):
        serializer = StartScrapingSerializer(data=request.data)
        if serializer.is_valid():
            coins = serializer.validated_data['coins']
            job = Job.objects.create()
            for coin in coins:
                Task.objects.create(job=job, coin=coin)
                scrape_coin_data.delay(job.id, coin)
            return Response({'job_id': job.id}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ScrapingStatusView(APIView):
    def get(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)
        
        tasks = job.tasks.all()
        response_data = {
            'job_id': job.id,
            'tasks': [
                {
                    'coin': task.coin,
                    'status': task.status,
                    'result': task.result
                }
                for task in tasks
            ]
        }
        return Response(response_data, status=status.HTTP_200_OK)
