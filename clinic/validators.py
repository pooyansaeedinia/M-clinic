from django.core.validators import FileExtensionValidator

ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'webp', 'gif']
ALLOWED_IMAGE_ACCEPT = '.jpg,.jpeg,.png,.webp,.gif,image/jpeg,image/png,image/webp,image/gif'

validate_image_upload = FileExtensionValidator(allowed_extensions=ALLOWED_IMAGE_EXTENSIONS)
