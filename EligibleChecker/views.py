from django.shortcuts import render,redirect,get_object_or_404
from .models import University, Program, SavedProgram, ProgramType
from django.db.models import Q
from .form import CreateCustomUserForm, ContactForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from django.http import HttpResponse
import os

from reportlab.lib.pagesizes import letter
from PIL import Image  # For logo processing
import io  # To convert image formats


# Create your views here.


PROGRAM_CATEGORIES = {
             "Computer Science":  ["BSc in Computer Science", "BSc in Applied Computer Science", "Diploma in Computer Science","BSc in Computer Technology",
                              "BSc in Information Technology", "Diploma in Information Technology", "BSc in Information Systems", "Certificate in Information Technology",
                              "BSc in Business Computing", "Bachelor of Business Information Technology", "Diploma in Business Information Technology",
                              "BSc in Computer Networks & Cyber Security", "Certificate in CCNA",
                              "BSc in Software Engineering", "Diploma in Software Development", "CISCO Certfication", "Diploma in Information Science", "Bsc in Computer Technology"],

            "Architecture":     ["Bachelor of Architectural Studies/ Bachelor of Architecture"]                   

    }


def signUp_view(request):
    if request.method =='POST':
        form=CreateCustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect('login')

    else:
        form=CreateCustomUserForm()
    return render(request, 'EligibleChecker/signup.html', {'form': form})



def login_view(request):
    next_url = request.GET.get('next', 'home')  # Get 'next' parameter, default to home
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
           
            response = redirect(next_url)
            response.set_cookie('email', email, max_age=60*60*24*7) 
            return response

        else:
            return render(request, 'EligibleChecker/login.html', {'error': 'Invalid email or password', 'next': next_url})
        

    email = request.COOKIES.get('email', '')    
    return render(request, 'EligibleChecker/login.html', {'next': next_url, 'email': email})


    


def home_view(request):

    PROGRAM_CATEGORIES = {
        "Computer Science":  ["BSc in Computer Science", "BSc in Applied Computer Science", "Diploma in Computer Science","BSc in Computer Technology",
                              "BSc in Information Technology", "Diploma in Information Technology", "BSc in Information Systems", "Certificate in Information Technology",
                              "BSc in Business Computing", "Bachelor of Business Information Technology", "Diploma in Business Information Technology",
                              "BSc in Computer Networks & Cyber Security", "Certificate in CCNA",
                              "BSc in Software Engineering", "Diploma in Software Development", "CISCO Certfication", "Diploma in Information Science", "Bsc in Computer Technology"],

        "Architecture":     ["Bachelor of Architectural Studies/ Bachelor of Architecture"]                   

 
    }
    
  
    
    print(PROGRAM_CATEGORIES.keys())

    programs = University.objects.values_list('programs__name', flat=True).distinct()  
    return render(request, 'EligibleChecker/home.html', {'program_categories': PROGRAM_CATEGORIES,'programs': programs})

    


def universities(request):

    universities=University.objects.all()
    programs = University.objects.values_list('programs__name', flat=True).distinct() 
      
 

    search_query=request.GET.get('query', '').strip()
    if search_query:
        universities=universities.filter(name__icontains=search_query)
    
   

    selected_filter = request.GET.get('university_type', 'all')
     # Apply filter based on university type
    if selected_filter == 'Public':
        universities = universities.filter(type='Public')
    elif selected_filter == 'Private':
        universities = universities.filter(type='Private')

    context = {
        'universities': universities,
        'selected_filter': selected_filter,
        'programs':programs,
     
    }
    return render(request,"EligibleChecker/university_list.html" ,context)


def programs(request, university_id):
    
    university = get_object_or_404(University, id=university_id)
    print(university)
    
    query = request.GET.get('query', '').strip()
    selected_program_id = request.GET.get('selected_program')  # Fetch selected program ID
    category_param = request.GET.get("category")

    print(category_param)

    # Get all programs offered by this university
    all_programs = Program.objects.filter(university=university)
    programs= University.objects.values_list('programs__name', flat=True).distinct() 
    print("All Programs:", all_programs)


    
 

    related_programs=[]
    
    selected_program=None 

    selected_category = category_param 

    if selected_program_id:
        selected_program = get_object_or_404(Program, id=selected_program_id, university=university)
       
        selected_program.filtered_program_types = selected_program.program_types.filter(university=university)
       
    # If no program is selected, show searched program
    elif query:
        searched_program = all_programs.filter(name__icontains=query.strip())
           
        if searched_program.exists():
            selected_program = searched_program.first()  # Default to first found program
            print(f"DEBUG: Selected program -> {selected_program}")  

            selected_program.filtered_program_types = selected_program.program_types.filter(university=university)
            print(f"DEBUG: Program Types Found -> {selected_program.filtered_program_types}")  # Debugging
        else:
            selected_program = None

 

    if not selected_category and selected_program:
        for category, programs_list in PROGRAM_CATEGORIES.items():
            if selected_program.name in programs_list:
                selected_category = category
                break # Stop searching after finding the category

        # Fetch related programs in the same category
    if selected_category:
            related_query = Q()
            for program in PROGRAM_CATEGORIES[selected_category]:
                related_query |= Q(name__icontains=program)  # Use icontains for case-insensitive matching

            related_programs = all_programs.filter(related_query).exclude(id=selected_program.id)


    
    if request.user.is_authenticated:
        saved_programs = SavedProgram.objects.filter(user=request.user).values_list('program_id', flat=True)
    else:
        saved_programs = request.session.get('saved_programs', [])  # Get saved programs from session

    return render(request, 'EligibleChecker/programs.html', { 'university': university,
        'selected_program': selected_program,
        'related_programs': related_programs,
        'saved_programs': saved_programs,
        'query': query,
        'all_programs': all_programs,
        'programs':programs,
        'selected_category':selected_category,
        'PROGRAM_CATEGORIES':PROGRAM_CATEGORIES
        })


def saved_programs(request, program_id):

      program = get_object_or_404(Program, id=program_id)

      if request.user.is_authenticated:
        # Save for logged-in users
            saved_program, created = SavedProgram.objects.get_or_create(user=request.user, program=program)

      if not created:
            saved_program.delete()  # Unsave if already saved

      else:
        # Save temporarily in session for guests
        saved_programs = request.session.get('saved_programs', [])  # Get saved programs list
        if program_id in saved_programs:
            saved_programs.remove(program_id)  # Unsave
        else:
            saved_programs.append(program_id)  # Save

        request.session['saved_programs'] = saved_programs  # Update session
        messages.info(request, "You need to log in to permanently save programs.")  # Notify guest user

      return redirect('programs', university_id=program.university.id)  # Redirect back



def home_search_results(request):

    query = request.GET.get('query', '')
    print(query)  # Debugging: Check what query is being passed

    university_type = request.GET.get('university_type', 'all')
    all_programs = Program.objects.values_list('name', flat=True).distinct()
    category_selected = request.GET.get('category', '')
    universities = []
    programs = []
    program_types=[]


 

    
    if query:
        # Get programs matching the selected subprogram
        programs = Program.objects.filter(name__icontains=query)

      
        if programs.exists():
            # Get related program types for the selected subprogram
            program_types = ProgramType.objects.filter(program__in=programs).select_related('university')

            # Get universities offering the selected subprogram
            university_ids = program_types.values_list('university_id', flat=True).distinct()
            universities = University.objects.filter(id__in=university_ids)

            
            # Filter universities by type
            if university_type != 'all':
                universities = universities.filter(type=university_type)


        return render(request, 'EligibleChecker/home_search_results.html', {
        'query': query,
        'category_selected': category_selected,
        'universities': universities,
        'selected_filter': university_type,
        'programs': programs,
        'program_types': program_types,
        'program_categories': PROGRAM_CATEGORIES,  # Pass categories to template
    })


def download_program_pdf(request, program_id):
    
    if not request.user.is_authenticated:
        messages.warning(request, "Please login first to download the program info.")
        return redirect('login') 
    program = get_object_or_404(Program, id=program_id)

    program_type = ProgramType.objects.filter(program=program).first()
   
    university = program.university
    logo_path = university.university_logo.path 
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{program.name}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4  # Get A4 dimensions

    logo_width = 100
    logo_height = 100

    # **HEADER SECTION**
    # University Logo and Name (Inline with spacing)
    y_position = height - 100
    p.setFont("Helvetica-Bold", 16)
    
    # Logo at the top-left
    p.drawImage(logo_path, 50, y_position, logo_width, logo_height, mask="auto") 
    
    # University name next to the logo with spacing
    p.drawString(150, y_position + 40, university.name)  # Spacing between logo and name
    
    # **Contact Information (Left-aligned)**
    y_position -= 30  # Move down after university info
    p.setFont("Helvetica", 16)
    p.drawString(50, y_position, f"Department: {program_type.department}")
    y_position -= 20
    p.drawString(50, y_position, f"Name: {university.name}")
    y_position -= 20
    p.drawString(50, y_position, f"Phone: {university.main_phone_number}")
    y_position -= 20
    p.drawString(50, y_position, f"Email: {program_type.Email}")
    p.linkURL(f"mailto:{program_type.Email}", (50, y_position - 2, 300, y_position + 10))  # Clickable Email
    y_position -= 20
    p.drawString(50, y_position, f"Website: {university.main_website_link}")
    p.linkURL(university.main_website_link, (50, y_position - 2, 400, y_position + 10))  # Clickable Website

    # **Margin Before Program Name**
    y_position -= 60  # Add margin top before program name
    
    # **Program Name (Centered, Bold)**
    p.setFont("Helvetica-Bold", 18)
    p.drawString(width / 2 - 270, y_position, program.name)  # Centered program name with bold

    # **PROGRAM DETAILS (Left-aligned)**
    y_position -= 40  # Move down after program name
    p.setFont("Helvetica", 14)
    p.drawString(50, y_position, f"Course Type: {program_type.get_type_display()}")

    y_position -= 20
    p.drawString(50, y_position, "Entry Requirements:")

    y_position -= 20
    for req in program_type.get_requirements_list():
        p.drawString(70, y_position, f"- {req}")
        y_position -= 15

    y_position -= 10
    p.drawString(50, y_position, f"Duration: {program_type.duration}")

  
    p.showPage()
    p.save()

    return response

def AboutView(request):

    return render(request,"EligibleChecker/about.html")

def contact(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Send email
            send_mail(
                subject=f"New contact from {form.cleaned_data['name']}",
                message=form.cleaned_data['message'],
                from_email=form.cleaned_data['email'],
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
            )
            return redirect('contact_success')
    else:
        form = ContactForm()
    return render(request, 'EligibleChecker/contact.html', {'form': form})

def contact_success_view(request):
    return render(request, 'EligibleChecker/contact_success.html')