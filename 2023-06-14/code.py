import requests
import logging
import qcloud_cos


class VideoPreview:
    def __init__(self, cos_client, material_api_url):
        self.cos_client = cos_client
        self.material_api_url = material_api_url

    def set_image_preview(self, image_id: str) -> str:
        try:
            preview_url = self._get_preview_url(image_id)
            cos_url = self._save_to_cos(preview_url)
            return cos_url
        except Exception as e:
            logging.error(f"Error occurred while setting image preview: {str(e)}")
            raise

    def get_image_preview(self, image_id: str) -> str:
        try:
            cos_url = self._get_cos_url(image_id)
            return cos_url
        except qcloud_cos.CosServiceError as e:
            if e.get_error_code() == "NoSuchKey":
                logging.error(f"COS object not found for image ID: {image_id}")
                raise ValueError(f"Invalid image ID: {image_id}")
            else:
                logging.error(f"Error occurred while getting image preview: {str(e)}")
                raise

    def _get_preview_url(self, image_id: str) -> str:
        response = requests.get(self.material_api_url)
        response.raise_for_status()
        data = response.json()
        preview_url = data.get(image_id)
        if not preview_url:
            raise ValueError(f"Preview URL not found for image ID: {image_id}")
        return preview_url

    def _save_to_cos(self, preview_url: str) -> str:
        # Save the preview image to COS bucket using the COS client
        # Replace the following code with the actual implementation for saving to COS
        cos_url = "cos://bucket/image.jpg"
        return cos_url

    def _get_cos_url(self, image_id: str) -> str:
        # Retrieve the COS URL for the image using the COS client
        # Replace the following code with the actual implementation for retrieving COS URL
        cos_url = "cos://bucket/image.jpg"
        return cos_url
