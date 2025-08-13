import boto3
from botocore.exceptions import ClientError
from app.core.config import get_settings
from app.core.logger import logger

settings = get_settings()

class NotificationService:
    def __init__(self):
        self.sns_client = boto3.client(
            "sns",
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region
        )

    def send_email(self, email: str, subject: str, message: str):
        try:
            topic_arn = self._get_or_create_topic("EmailNotifications")
            
            self._subscribe_email(topic_arn, email)

            response = self.sns_client.publish(
                TopicArn=topic_arn,
                Subject=subject,
                Message=message
            )
            logger.info(f"Email notification sent to {email}: {response}")
            return True
        except ClientError as e:
            logger.error(f"Error sending email: {e}")
            return False

    def send_sms(self, phone_number: str, message: str):
        try:
            response = self.sns_client.publish(
                PhoneNumber=phone_number,
                Message=message
            )
            logger.info(f"SMS notification sent to {phone_number}: {response}")
            return True
        except ClientError as e:
            logger.error(f"Error sending SMS: {e}")
            return False

    def _get_or_create_topic(self, topic_name: str):
        topic = self.sns_client.create_topic(Name=topic_name)
        return topic["TopicArn"]

    def _subscribe_email(self, topic_arn: str, email: str):
        self.sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol="email",
            Endpoint=email
        )
