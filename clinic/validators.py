from django.core.validators import FileExtensionValidator

ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'webp', 'gif']
ALLOWED_IMAGE_ACCEPT = '.jpg,.jpeg,.png,.webp,.gif,image/jpeg,image/png,image/webp,image/gif'

validate_image_upload = FileExtensionValidator(allowed_extensions=ALLOWED_IMAGE_EXTENSIONS)

ALLOWED_LANGUAGE_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png']
ALLOWED_LANGUAGE_IMAGE_ACCEPT = '.jpg,.jpeg,.png,image/jpeg,image/png'
validate_language_image_upload = FileExtensionValidator(
    allowed_extensions=ALLOWED_LANGUAGE_IMAGE_EXTENSIONS
)
