import requests
import time
import json

BASE_URL = "http://127.0.0.1:8000"

test_receipts = [
    {
        "data": {
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
                {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
                {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
                {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
                {"shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": "12.00"}
            ],
            "total": "35.35"
        },
        "expected_points": 28
    },
    {
        "data": {
            "retailer": "M&M Corner Market",
            "purchaseDate": "2022-03-20",
            "purchaseTime": "14:33",
            "items": [
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"}
            ],
            "total": "9.00"
        },
        "expected_points": 109
    }
]

invalid_receipt = {
    "retailer": "123",  
    "purchaseDate": "2022-01-01",
    "purchaseTime": "13:01",
    "items": [{"shortDescription": "Item", "price": "5.00"}],
    "total": "4.99"  
}



def test_receipt_processing(receipt_data, expected_points):
    print(f"\nSubmitting receipt for retailer: {receipt_data['retailer']}...")

    response = requests.post(f"{BASE_URL}/receipts/process", json=receipt_data)
    if response.status_code != 200:
        print(f"Failed to submit receipt: {response.text}")
        return

    receipt_id = response.json().get("id")
    print(f"Receipt processed! ID: {receipt_id}")

    time.sleep(1)

    response = requests.get(f"{BASE_URL}/receipts/{receipt_id}/points")
    if response.status_code != 200:
        print(f"Failed to fetch points: {response.text}")
        return

    received_points = response.json().get("points")
    print(f"Points received: {received_points}")

    if received_points == expected_points:
        print("Test Passed! ")
    else:
        print(f"Test Failed! Expected {expected_points}, but got {received_points}.")


def test_invalid_receipt():
    print("\nTesting Invalid Receipt Submission...")
    print(f"Sending invalid receipt data: {json.dumps(invalid_receipt, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/receipts/process", json=invalid_receipt)
    print(f"Response status code: {response.status_code}")
    print(f"Response body: {response.text}")
    
    if response.status_code == 400:
        print("BadRequest (400) received as expected.")
    else:
        print(f"Expected 400 BadRequest, got {response.status_code}: {response.text}")


def test_non_existent_receipt():
    print("\nTesting Non-Existent Receipt...")
    fake_id = "non-existent-id"
    response = requests.get(f"{BASE_URL}/receipts/{fake_id}/points")

    if response.status_code == 404:
        print("NotFound (404) received as expected.")
    else:
        print(f"Expected 404 NotFound, got {response.status_code}: {response.text}")


if __name__ == "__main__":
    for test in test_receipts:
        test_receipt_processing(test["data"], test["expected_points"])
    test_invalid_receipt()
    test_non_existent_receipt()
