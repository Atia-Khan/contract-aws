import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from .models import UserProfile  # Import your UserProfile model


@csrf_exempt
def upload_profile_image(request):
    if request.method == 'POST':
        # Assuming your frontend sends the base64-encoded image and filename
        encoded_image_data = request.POST.get('profile_image', '')
        image_filename = request.POST.get('filename', 'your_image.png')  # Default filename if not provided

        try:
            # Remove the data:image/png;base64, prefix
            encoded_image_data = encoded_image_data.split(',')[1]

            # Decode Base64 data
            decoded_image_data = base64.b64decode(encoded_image_data)

            # Create a ContentFile object
            image_file = ContentFile(decoded_image_data, name=image_filename)

            # Save the image to your model's ImageField
            # For example, if you have a UserProfile model with an ImageField named 'profile_image':
            user_profile = UserProfile.objects.get(user=request.user)  # Assuming you have a user associated with the profile
            user_profile.profile_image.save(image_filename, image_file, save=True)

            return JsonResponse({'message': 'Image uploaded successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

