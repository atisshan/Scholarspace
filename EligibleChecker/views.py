from django.shortcuts import render,redirect,get_object_or_404
from .models import University, Program, SavedProgram, ProgramType
from django.db.models import Q
from .form import CreateCustomUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages

# Create your views here.


PROGRAM_CATEGORIES = {
        "Computer Science":  ["Bsc in Computer Science", "Bsc in Applied Computer Science", "Diploma in Computer Science",
                              "Bsc in IT", "Diploma in IT", "Bsc in Information Systems", "Certificate in IT",
                              "Bsc in Business Computing", "Bachelor of Business IT", "Diploma in Business IT",
                              "Bsc in Computer Networks & Cyber Security", "Certificate in CCNA",
                              "Bsc in Software Engineering", "Diploma in Software Development"]
    }


def home_view(request):
    PROGRAM_CATEGORIES = {
    "Computer Science":  ["Bsc in Computer Science", "Bsc in Applied Computer Science", "Diploma in Computer Science",
    "Bsc in IT", "Diploma in IT", "Bsc in Information Systems", "Certificate in IT",
    "Bsc in Business Computing", "Bachelor of Business IT", "Diploma in Business IT",
    "Bsc in Computer Networks & Cyber Security", "Certificate in CCNA",
    "Bsc in Software Engineering", "Diploma in Software Development"]
    }
    print(PROGRAM_CATEGORIES.keys())

    programs = University.objects.values_list('programs__name', flat=True).distinct()  
    return render(request, 'EligibleChecker/home.html', {'program_categories': PROGRAM_CATEGORIES,'programs': programs})

    


def universities(request):

    universities=University.objects.all()
    programs = University.objects.values_list('programs__name', flat=True).distinct() 


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

    # Get all programs offered by this university
    all_programs = Program.objects.filter(university=university)
    programs= University.objects.values_list('programs__name', flat=True).distinct() 
    print("All Programs:", all_programs)


    
 

    related_programs=[]
    # Define related programs manually
    related_keywords = {
        "computer science": ["IT", "CCNA", "Cisco", "ICT", "Cyber Security", "Computer Networks", 'Information Science', 'Information Systems'],
        "it": ["Computer Science", "CCNA", "Cisco", "ICT", "Cyber Security", "Computer Networks", 'Information Systems','Information Science'],
        "ccna": ["Cisco", "IT", "Computer Science", "Cyber Security", 'Information Systems','Information Science'],
        "cisco": ["CCNA", "IT", "Computer Networks",'Information Systems','Information Science'],
        "ict": ["IT", "Computer Science", "Cyber Security",'Information Systems','Information Science'],
        "cyber security": ["IT", "ICT", "Computer Networks",'Information Systems','Information Science'],
        "computer networks": ["IT", "CCNA", "Cisco", "Cyber Security",'Information Systems','Information Science'],
        "information science":["IT", "CCNA", "Cisco", "ICT", "Cyber Security",'Information Systems', "Computer Networks"],
        'Information Systems':["IT", "CCNA", "Cisco", "ICT", "Cyber Security",'Information Science', "Computer Networks"]
    }   
    selected_program=None   
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
            
    if selected_program:      # Fetch related programs
        related_program_names = related_keywords.get(selected_program.name.lower(), [])
        related_query = Q()
        for keyword in related_program_names:
                    related_query |= Q(name__icontains=keyword)

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
        'programs':programs})

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
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
           
            return redirect(next_url)

        else:
            return render(request, 'EligibleChecker/login.html', {'error': 'Invalid username or password', 'next': next_url})
    return render(request, 'EligibleChecker/login.html', {'next': next_url})


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