from django.core.exceptions import ValidationError


def validate_file_size(value):
    print("salam manam validator")
    print(value.size)
    filesize = value.size

    if filesize > 10048576:
        raise ValidationError("The maximum file size that can be uploaded is 10MB")
    else:
        return value
