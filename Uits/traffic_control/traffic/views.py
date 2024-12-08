from django.shortcuts import render
from .models import LicenceOwner, Fine, Expiry

from .forms import SearchForm

def home(request):
    return render(request, 'traffic/home.html')


def fine_details(request):
    dob = request.GET.get('dob')  # Get DOB from request
    nid = request.GET.get('nid')  # Get NID from request
    message = None

    if dob and nid:
        # Fetch licence owner by DOB and NID
        try:
            owner = LicenceOwner.objects.get(dob=dob, nid=nid)
            fines = Fine.objects.filter(licence_number=owner)  # Get fines for the owner
        except LicenceOwner.DoesNotExist:
            fines = []  # No owner found, so no fines
            message = "No matching owner found for the provided DOB and NID."
    else:
        fines = []  # Default to empty list if no search criteria
        message = "Please provide both DOB and NID."

    return render(request, 'traffic/fine_details.html', {'fine_details': fines, 'message': message})

def expiry_details(request):
    dob = request.GET.get('dob')  # Get DOB from request
    nid = request.GET.get('nid')  # Get NID from request
    message = None

    if dob and nid:
        # Fetch licence owner by DOB and NID
        try:
            owner = LicenceOwner.objects.get(dob=dob, nid=nid)
            expiry_records = Expiry.objects.filter(licence_number=owner)  # Get expiry records for the owner
        except LicenceOwner.DoesNotExist:
            expiry_records = []  # No owner found
            message = "No matching owner found for the provided DOB and NID."
    else:
        expiry_records = []  # Default to empty list if no search criteria
        message = "Please provide both DOB and NID."

    return render(request, 'traffic/expiry_details.html', {'expiry_details': expiry_records, 'message': message})

from django.core.mail import send_mail
from django.shortcuts import render
from django.conf import settings

def contact_us(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        try:
            # Compose email
            subject = "New Contact Us Message"
            body = f"""
            You have received a new message:
            Name: {name}
            Email: {email}
            Phone: {phone}
            Message: {message}
            """
            recipient = "mhb9323@gmail.com"
            sender = settings.DEFAULT_FROM_EMAIL

            # Send email
            send_mail(subject, body, sender, [recipient])

            return render(request, "traffic/contact_us.html", {"success": True})
        except Exception as e:
            error_message = f"Failed to send the message. Error: {str(e)}"
            return render(request, "traffic/contact_us.html", {"error": error_message})

    return render(request, "traffic/contact_us.html")


def search_license(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            licence_number = form.cleaned_data['licence_number']
            try:
                owner = LicenceOwner.objects.get(licence_number=licence_number)
                fine_details = Fine.objects.filter(licence_number=owner)
                expiry_details = Expiry.objects.get(licence_number=owner)
                
                return render(request, 'traffic/license_details.html', {
                    'owner': owner,
                    'fine_details': fine_details,
                    'expiry_details': expiry_details
                })
            except LicenceOwner.DoesNotExist:
                return render(request, 'error.html', {'message': 'Wrong Licence Number'})
        else:
            return render(request, 'error.html', {'message': 'Invalid Form Submission'})
    else:
        form = SearchForm()
    return render(request, 'traffic/search_license.html', {'form': form})

