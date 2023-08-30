import requests
import logging
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .enum import *  

logger = logging.getLogger(__name__)

class MockItemViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        try:
            res_1 = requests.get(url=MockEndpointsEnum.mock1_url.value)
            res_2 = requests.get(url=MockEndpointsEnum.mock2_url.value)

            if res_1.status_code == 200:
                response_1 = res_1.json()
            else:
                logger.error(f"Mock1 API returned status code: {res_1.status_code}")
                return Response({"error": "Failed to fetch data from Mock1 API"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if res_2.status_code == 200:
                response_2 = res_2.json()
            else:
                logger.error(f"Mock2 API returned status code: {res_2.status_code}")
                return Response({"error": "Failed to fetch data from Mock2 API"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Create a dictionary to hold the merged data
            merged_data = {}

            # Merge data from input1 and input2 based on customer_id
            for entry1, entry2 in zip(response_1, response_2):
                customer_id = entry1["customer_id"]

                if customer_id not in merged_data:
                    merged_data[customer_id] = {
                        "id": entry1["id"],
                        "customer_id": customer_id,
                        "pack1": [
                            f"{pack_entry.get('ingredient', None)} {pack_entry.get('quantity', None)}{pack_entry.get('unit', None)}" for pack_entry in
                            entry1["pack_data"]
                        ],
                        "pack2": [
                            f"{pack_entry.get('ingredient', None)} {pack_entry.get('quantity', None)}{pack_entry.get('unit', None)}" for pack_entry in
                            entry2["pack_data"]
                        ]

                    }
            

            return Response(merged_data)

        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred while making API requests: {e}")
            return Response({"error": "Failed to fetch data from external APIs"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
