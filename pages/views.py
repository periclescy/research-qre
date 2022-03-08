import datetime
import time
from django.contrib import messages
from django.db.models import *
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user
from .forms import *
from .models import *


# -------------------------------------------------------------------------------------------------------------------- #
#   REGISTRATION
# -------------------------------------------------------------------------------------------------------------------- #

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('/')
        else:
            # Return an 'invalid login' error message.
            messages.info(request, 'Username or Password is incorrect')

    logo = 'logo'
    footer = Option.objects.get(id=1).footer

    context = {
        'logo': logo,
        'footer': footer
    }

    return render(request, 'registration/login.html', context)


def logout_page(request):
    logout(request)
    return redirect('login')


# -------------------------------------------------------------------------------------------------------------------- #
#   FRONT-END
# -------------------------------------------------------------------------------------------------------------------- #
@login_required
def start(request):
    print('----------- WELCOME -----------')  # Welcome message

    # --- Fetch headline, instructions & footer from Database Options  --- #
    headline = Option.objects.get(id=1).headline
    instructions = Option.objects.get(id=1).instructions
    footer = Option.objects.get(id=1).footer
    logo = 'logo.png'

    # --- Get correct session from Database --- #
    max_session = Data.objects.aggregate(Max('session'))  # Query that gets maximum value of all sessions
    last_session = max_session['session__max']  # Clear the value to be an integer

    # Avoid error if database is empty
    if last_session is None:
        last_session = 0
    session_id = last_session + 1  # Next session value
    print('Session is: ', session_id)  # For debugging purposes

    # Get brake time from Database
    brake_time = Option.objects.get(id=1).brake_time

    # Prepare Sections List
    section_list = Section.objects.values_list('section', flat=True)

    # Prepare Sections & Questions
    questions_dict = {}
    for i in section_list:
        this_section = list(Question.objects.filter(section__section=i).values_list('id', flat=True))
        questions_dict[i] = this_section
    print('Sections with their Questions: ', questions_dict)  # For debugging purposes

    # --- Check if there are any empty Sections and set session flag. --- #
    for key in questions_dict:
        x = questions_dict[key]
        if x:
            request.session.pop('is_section_empty', None)
        else:
            request.session['is_section_empty'] = 'EMPTY-SECTION'
            print('At least one Section are empty!')
            break

    # --- Create Session variables with new values --- #
    request.session['brake_time'] = brake_time
    request.session['logo'] = logo
    request.session['footer'] = footer
    request.session['session_id'] = session_id
    request.session['questions_dict'] = questions_dict

    form = UserForm()

    context = {
        'logo': logo,
        'headline': headline,
        'instructions': instructions,
        'footer': footer,
        'session_id': session_id,
        'form': form
    }

    return render(request, 'pages/frontend/start.html', context)


@login_required
def home(request):
    user = get_user(request)

    if user.username == 'curator':
        return redirect('/')

    # --- Check if there are any empty Sections --- #
    if request.session.get('is_section_empty'):
        print('At least one Section is empty.')
        html = "<html><body><h1>Empty Section!!!</h1> <p>At least one Section is empty, without any questions/brakes.</p> Please go <a href='/start'>back</a>.</body></html> "
        return HttpResponse(html)

    if request.method == 'POST':
        # --- Retrieve variables from Session --- #
        session_id = request.session.get('session_id')
        brake_time = request.session.get('brake_time')
        questions_dict = request.session.get('questions_dict')

        print('Session is: ', session_id)  # For debugging purposes
        print('Brake time is: ', brake_time, 'min.')  # For debugging purposes
        print('questions_dict: ', questions_dict)  # For debugging purposes

        # --- Avoid test when no questions are available --- #
        questions = Question.objects.count()
        if questions == 0:
            html = "<html><body><h1>No Questions in Database!!!</h1>Go <a href='/start'>back </a>" \
                   "and add some entries! </body></html> "
            return HttpResponse(html)

        # --- FIRST POST --- #
        if 'start-post' == request.POST['Post_name']:
            start_time = int(time.time())
            session = request.POST['session']
            team = request.POST['team']
            gender = request.POST['gender']
            age = request.POST['age']
            education = request.POST['education']
            district = request.POST['district']
            residence = request.POST['residence']

            # --- Create Session variables with new values --- #
            request.session['team'] = team

            # --- Saving User to the Database (Models.User)--- #
            user = User(session=session, team=team, gender=gender, age=age, education=education,
                        district=district, residence=residence)
            user.save()
            print("User entry saved to the database!")  # For debugging purposes

            # --- Saving Click of START to the Database (Models.Data)--- #
            sta = Data(session=session_id, status='start', timestamp=start_time, question=None,
                       selection=None, team=team)
            sta.save()
            print("Start record saved to the database!")
            print("----------- START -----------")  # For debugging purposes

            # --- Calculate variables to send to template --- #
            if questions_dict:

                # Check if user is on B team to remove Section A
                if team == 'B':
                    questions_dict.pop("A")
                    print("Section A is removed from user member of Team B.")

                this_section = next(iter(questions_dict.keys()))  # Get the first key in dictionary
                this_section_values = questions_dict[this_section]  # Get the value of above key

                if this_section_values:
                    this_question_id = this_section_values[0]  # Get the first item in list
                    this_section_values.pop(0)  # Remove the above item

                    # --- Get values from Database --- #
                    this_question = Question.objects.get(id=this_question_id)

                    # --- Create Session variables with new values --- #
                    request.session['this_question_id'] = this_question_id
                    request.session['this_section'] = this_section

                    context = {  # Variables for Template
                        'this_question': this_question,
                        'section': this_section,
                        'team': team,
                        'brake_time': brake_time
                    }

                    return render(request, 'pages/frontend/home.html', context)

        # --- NEXT POST --- #
        if 'next' == request.POST['Post_name']:

            timestamp = int(time.time())  # Get timestamp in Epoch (seconds)
            selection = request.POST.get('selection')

            # --- Retrieve variables from Session --- #
            session_id = request.session.get('session_id')
            team = request.session.get('team')
            this_question_id = request.session.get('this_question_id')
            this_section = request.session.get('this_section')

            # --- FINISH POST --- #
            # --- Check if there are any questions left. --- #
            len_dict = len(questions_dict)
            if len_dict <= 1:
                last_section_key = next(iter(questions_dict.keys()))
                if not questions_dict[last_section_key]:
                    # # Saving data to the Database (Models.Data)
                    fin = Data(session=session_id, status='finish', timestamp=timestamp, section=this_section,
                               question=this_question_id, selection=selection, team=team)
                    fin.save()
                    print("End record saved to the database!")
                    print("----------- END -----------")  # For debugging purposes

                    # Calculate Total Time
                    # --- Queries that get START and FINISH timestamps from Database --- #
                    sta = int(Data.objects.get(session=session_id, status='start').timestamp)
                    fin = int(Data.objects.get(session=session_id, status='finish').timestamp)

                    time_diff = round(fin - sta)  # Total time converted in seconds and round.
                    total_time = str(datetime.timedelta(seconds=time_diff))
                    print('Total time: ', total_time, 'hrs:min:sec')  # For debugging purposes.

                    context = {
                        'total_time': total_time,
                        'footer': Option.objects.get(id=1).footer
                    }

                    return render(request, 'pages/frontend/end.html', context)

            # # Saving data to the Database (Models.Data)
            nex = Data(session=session_id, status='next', timestamp=timestamp, section=this_section,
                       question=this_question_id, selection=selection, team=team)
            nex.save()
            print("Next record saved to the database!")
            print("----------- NEXT -----------")  # For debugging purposes

            # --- Calculate variables to send to template --- #
            if questions_dict:
                this_section = next(iter(questions_dict.keys()))  # Get the first key in dictionary
                this_section_values = questions_dict[this_section]

                if this_section_values:
                    this_question_id = this_section_values[0]  # Get the first item in list
                    this_section_values.pop(0)  # Remove the above item

                    # --- Get values from Database --- #
                    this_question = Question.objects.get(id=this_question_id)

                    # --- Delete & Update Session variables with new values --- #
                    del request.session['questions_dict']
                    del request.session['this_question_id']
                    del request.session['this_section']
                    request.session['questions_dict'] = questions_dict
                    request.session['this_question_id'] = this_question_id
                    request.session['this_section'] = this_section

                    context = {
                        # Variables for Template
                        'this_question': this_question,
                        'section': this_section,
                        'team': team,
                        'brake_time': brake_time
                    }

                    return render(request, 'pages/frontend/home.html', context)
                else:
                    questions_dict.pop(this_section)
                    print('Section ', this_section, ' is deleted!')

                    this_section = next(iter(questions_dict.keys()))  # Get the first key in dictionary
                    this_section_values = questions_dict[this_section]

                    if this_section_values:
                        this_question_id = this_section_values[0]  # Get the first item in list
                        this_section_values.pop(0)  # Remove the above item

                        # --- Get values from Database --- #
                        this_question = Question.objects.get(id=this_question_id)

                        # --- Delete & Update Session variables with new values --- #
                        del request.session['questions_dict']
                        del request.session['this_question_id']
                        del request.session['this_section']
                        request.session['questions_dict'] = questions_dict
                        request.session['this_question_id'] = this_question_id
                        request.session['this_section'] = this_section

                        context = {
                            # Variables for Template
                            'this_question': this_question,
                            'section': this_section,
                            'team': team,
                            'brake_time': brake_time
                        }

                        return render(request, 'pages/frontend/home.html', context)


# -------------------------------------------------------------------------------------------------------------------- #
#   BACK-END
# -------------------------------------------------------------------------------------------------------------------- #

@login_required
def question(request):
    questions = Question.objects.all()
    total_questions = questions.count()
    total_tests = Data.objects.all().aggregate(Max('session'))['session__max']

    user = get_user(request)
    if user.username == 'user':
        return redirect('/')

    context = {
        'questions': questions,
        'total_questions': total_questions,
        'total_tests': total_tests
    }
    return render(request, 'pages/backend/question.html', context)


@login_required
def section(request):
    user = get_user(request)
    if user.username == 'user':
        return redirect('/')

    form = SectionForm()
    sections = Section.objects.all()
    total_sections = sections.count()
    total_tests = Data.objects.all().aggregate(Max('session'))['session__max']

    instance_list = []
    for z in sections:
        instance_list.append(SectionForm(instance=z))
    sections_instance_list = zip(sections, instance_list)

    if request.method == 'POST':
        print(request.POST.get("action_status"))

        if request.POST.get("action_status") == 'UPDATE':
            this_section = Section.objects.get(id=request.POST.get("section_id"))
            form = SectionForm(request.POST, request.FILES, instance=this_section)

            if form.is_valid():
                print('Form is valid.')
                model1 = form.save()
                messages.success(request, 'Your changes successfully applied!')
                success_url = f"/section"
                return redirect(success_url)
            else:
                print('Something wrong with form.')
                print(form.errors)
                form1 = SectionForm()
                messages.error(request, 'Error: Your changes are not valid!')
                # messages.error(request, )
                return redirect("/section")
                # return render(request, 'pages/backend/section.html', {'form': form})

        elif request.POST.get("action_status") == 'CREATE':
            form = SectionForm(request.POST)
            print(request.POST)

            if form.is_valid():
                print('Form is valid')
                model = form.save()
                messages.success(request, 'New Section successfully created!')
                return redirect('/section')
            else:
                print('Something wrong with the form')
                print(form.errors)
                form = SectionForm()
                messages.error(request, 'Error: Your entries are not valid!')
                return redirect("/section")
                # return render(request, 'pages/backend/section.html', {'form': form})

        elif request.POST.get("action_status") == 'DELETE':
            this_section = Section.objects.get(id=request.POST.get("section_id"))
            this_section.delete()
            messages.success(request, 'The question successfully deleted!')
            return redirect('/section')

    context = {
        'sections': sections,
        'total_sections': total_sections,
        'total_tests': total_tests,
        'sections_instance_list': sections_instance_list,
        'form': form
    }
    return render(request, 'pages/backend/section.html', context)


@login_required
def details(request, pk):
    questions = Question.objects.all()
    this_question = questions.get(id=pk)

    user = get_user(request)
    if user.username == 'user':
        return redirect('/')

    form = QuestionForm(instance=this_question)

    context = {
        'this_question': this_question,
        'form': form,
    }
    return render(request, 'pages/backend/details.html', context)


@login_required
def preview(request, pk):
    questions = Question.objects.all()
    this_question = questions.get(id=pk)
    section = this_question.section
    brake_time = Option.objects.get(id=1).brake_time

    user = get_user(request)
    if user.username == 'user':
        return redirect('/')

    context = {
        'this_question': this_question,
        'section': section,
        'brake_time': brake_time
    }
    return render(request, 'pages/backend/preview.html', context)


@login_required
def create(request):
    user = get_user(request)
    if user.username == 'user':
        return redirect('/')

    form = QuestionForm()
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        print(request.POST)

        if form.is_valid():
            print('All forms are valid')
            model1 = form.save()
            messages.success(request, 'New Question successfully created!')
            return redirect('/question')
        else:
            print('Something wrong with forms')
            form = QuestionForm()
            messages.error(request, 'Error: Your entries are not valid!')
            return render(request, 'pages/backend/create_update_form.html', {'form1': form})

    context = {
        'form': form
    }
    return render(request, 'pages/backend/create_update_form.html', context)


@login_required
def update(request, pk):
    user = get_user(request)
    if user.username == 'user':
        return redirect('/')

    this_question = Question.objects.get(id=pk)
    form = QuestionForm(instance=this_question)

    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES, instance=this_question)

        if form.is_valid():
            print('All forms are valid')
            model1 = form.save()
            messages.success(request, 'Your changes successfully applied!')
            success_url = f"/details/{this_question.id}"
            return redirect(success_url)
        else:
            print('Something wrong with forms')
            form1 = QuestionForm()
            messages.error(request, 'Error: Your changes are not valid!')
            return render(request, 'pages/backend/create_update_form.html', {'form': form})

    context = {
        'this_question': this_question,
        'form': form,
    }
    return render(request, 'pages/backend/create_update_form.html', context)


@login_required
def delete(request, pk):
    user = get_user(request)
    if user.username == 'user':
        return redirect('/')

    this_question = Question.objects.get(id=pk)
    if request.method == "POST":
        this_question.delete()
        messages.success(request, 'The question successfully deleted!')
        return redirect('/question')
    context = {
        'item': this_question
    }
    return render(request, 'pages/backend/delete.html', context)


@login_required
def options(request):
    user = get_user(request)
    if user.username == 'user':
        return redirect('/')

    this_option = Option.objects.get(id=1)
    form = OptionForm(instance=this_option)
    if request.method == 'POST':
        form = OptionForm(request.POST, instance=this_option)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your options successfully applied!!')
            return redirect('/start')
    context = {
        'this_option': this_option,
        'form': form
    }
    return render(request, 'pages/backend/options.html', context)
