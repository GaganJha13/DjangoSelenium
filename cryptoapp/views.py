from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult
from .tasks import scrape_coin
from uuid import uuid4

class StartScrapingView(APIView):
    def post(self, request, *args, **kwargs):
        coins = request.data.get("coins", [])
        if not coins:
            return Response({"error": "No coins provided"}, status=status.HTTP_400_BAD_REQUEST)

        job_id = str(uuid4())
        task = scrape_coins.delay(coins)
        return Response({"job_id": task.id}, status=status.HTTP_202_ACCEPTED)

class ScrapingStatusView(APIView):
    def get(self, request, job_id, *args, **kwargs):
        task = AsyncResult(job_id)
        if task.state == 'PENDING':
            response = {
                "job_id": job_id,
                "status": "Pending...",
                "tasks": []
            }
        elif task.state == 'SUCCESS':
            results = task.result
            scraped_data = []
            for result in results:
                if 'output' in result:
                    scraped_data.append({
                        "coin": result['coin'],
                        "output": result['output']
                    })
                else:
                    scraped_data.append({
                        "coin": result['coin'],
                        "error": result['error']
                    })
            response = {
                "job_id": job_id,
                "status": "Completed",
                "tasks": scraped_data
            }
        else:
            response = {
                "job_id": job_id,
                "status": task.state,
                "tasks": []
            }

        return Response(response)
