from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from solidPayApp.models import paymentRequest

class NewPayRequestTestCase(TestCase):
    def test_new_pay_request_with_valid_data(self):
        # Create a test payload with valid data
        payload = {
            "amount": "10",
            "recipient": "0x1234567890abcdef",
        }

        # Send a POST request to the API endpoint
        response = self.client.post(reverse("new-pay-request"), data=payload)

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert the response data contains the expected fields
        self.assertIn("privateKey", response.data)
        self.assertIn("createdAddress", response.data)
        self.assertIn("pendingAmount", response.data)
        self.assertIn("destinationAddress", response.data)
        self.assertIn("fullfilled", response.data)
        self.assertIn("requestDate", response.data)

        # Assert that the payment request object is saved to the database
        self.assertEqual(paymentRequest.objects.count(), 1)

        # Assert the WebSocket communication
        # Simulate socket connection and send test messages
        # Verify that the consumer receives the expected responses

        # Assert other scenarios and edge cases as needed

    def test_new_pay_request_with_missing_amount(self):
        # Create a test payload with missing 'amount' field
        payload = {
            "recipient": "0x1234567890abcdef",
        }

        # Send a POST request to the API endpoint
        response = self.client.post(reverse("new-pay-request"), data=payload)

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert that the payment request object is not saved to the database
        self.assertEqual(paymentRequest.objects.count(), 0)

        # Assert other error response details as needed

    def test_new_pay_request_with_invalid_amount(self):
        # Create a test payload with an invalid 'amount' value
        payload = {
            "amount": "invalid",
            "recipient": "0x1234567890abcdef",
        }

        # Send a POST request to the API endpoint
        response = self.client.post(reverse("new-pay-request"), data=payload)

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert that the payment request object is not saved to the database
        self.assertEqual(paymentRequest.objects.count(), 0)

        # Assert other error response details as needed

    def test_new_pay_request_with_missing_recipient(self):
        # Create a test payload with missing 'recipient' field
        payload = {
            "amount": "10",
        }

        # Send a POST request to the API endpoint
        response = self.client.post(reverse("new-pay-request"), data=payload)

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert that the payment request object is not saved to the database
        self.assertEqual(paymentRequest.objects.count(), 0)

        # Assert other error response details as needed

    def test_new_pay_request_with_additional_fields(self):
        # Create a test payload with additional fields
        payload = {
            "amount": "10",
            "recipient": "0x1234567890abcdef",
            "extraField": "value",
        }

        # Send a POST request to the API endpoint
        response = self.client.post(reverse("new-pay-request"), data=payload)

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert the response data contains the expected fields
        self.assertIn("privateKey", response.data)
        self.assertIn("createdAddress", response.data)
        self.assertIn("pendingAmount", response.data)
        self.assertIn("destinationAddress", response.data)
        self.assertIn("fullfilled", response.data)
        self.assertIn("requestDate", response.data)

        # Assert that the payment request object is saved to the database
        self.assertEqual(paymentRequest.objects.count(), 1)

        # Assert other scenarios and edge cases as needed

    # Add more test cases to cover other scenarios and edge cases

