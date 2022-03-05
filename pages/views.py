import datetime
import time
import json

from django.contrib import messages
from django.db.models import *
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
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

    # Prepare Sections List
    section_list = Section.objects.values_list('section', flat=True)

    # Prepare Sections & Questions
    questions_dict = {}
    for i in section_list:
        this_section = list(Question.objects.filter(section__section=i).values_list('id', flat=True))
        questions_dict[i] = this_section
    print('Sections with their Questions: ', questions_dict)  # For debugging purposes

    # --- Create Session variables with new values --- #
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

    if request.method == 'POST':

        # --- Retrieve variables from Session --- #
        session_id = request.session.get('session_id')
        questions_dict = request.session.get('questions_dict')
        print('Session is: ', session_id)  # For debugging purposes
        print('questions_dict: ', questions_dict)  # For debugging purposes

        questions = Question.objects.count()
        # --- Avoid test when no questions are available --- #
        if questions == 0:
            html = "<html><body><h1>No Questions in Database!!!</h1>Go back to <a href='/dashboard'>Dashboard </a>" \
                   "and add some entries! </body></html> "
            return HttpResponse(html)

        # --- Check if it's the first POST --- #
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
                this_key = next(iter(questions_dict.keys()))  # Get the first key in dictionary
                this_section_values = questions_dict[this_key]  # Get the value of above key

                if this_section_values:
                    this_question_id = this_section_values[0]  # Get the first item in list
                    this_section_values.pop(0)  # Remove the above item

                    # --- Get values from Database --- #
                    this_question = Question.objects.get(id=this_question_id)

                    # --- Create Session variables with new values --- #
                    request.session['this_question_id'] = this_question_id

                    context = {  # Variables for Template
                        'this_question': this_question,
                        'section': this_key,
                        'team': team
                    }

                    return render(request, 'pages/frontend/home.html', context)

        if 'next' == request.POST['Post_name']:
            timestamp = int(time.time())  # Get timestamp in Epoch (seconds)
            selection = request.POST.get('selection')

            # --- Retrieve variables from Session --- #
            session_id = request.session.get('session_id')
            team = request.session.get('team')
            this_question_id = request.session.get('this_question_id')

            # # Saving data to the Database (Models.Data)
            nex = Data(session=session_id, status='next', timestamp=timestamp, question=this_question_id,
                       selection=selection, team=team)
            nex.save()
            print("Next record saved to the database!")
            print("----------- NEXT -----------")  # For debugging purposes

            # --- Calculate variables to send to template --- #
            print('questions_dict before: ', questions_dict)
            if questions_dict:
                this_key = next(iter(questions_dict.keys()))  # Get the first key in dictionary
                this_section_values = questions_dict[this_key]

                check_for_brake = Section.objects.get(section=this_key).answer_category
                if check_for_brake == 'brake':
                    print('Eimai sto brake')
                    context = {
                        'team': team
                    }
                    return render(request, 'pages/frontend/brake.html', context)

                if this_section_values:
                    this_question_id = this_section_values[0]  # Get the first item in list
                    this_section_values.pop(0)  # Remove the above item

                    # --- Get values from Database --- #
                    this_question = Question.objects.get(id=this_question_id)

                    # --- Delete & Update Session variables with new values --- #
                    del request.session['questions_dict']
                    del request.session['this_question_id']
                    request.session['questions_dict'] = questions_dict
                    request.session['this_question_id'] = this_question_id
                    print('New questions_dict: ', request.session.get('questions_dict'))
                    print('New this_question_id: ', request.session.get('this_question_id'))

                    context = {
                        # Variables for Template
                        'this_question': this_question,
                        'section': this_key,
                        'team': team
                    }

                    return render(request, 'pages/frontend/home.html', context)
                else:
                    questions_dict.pop(this_key)
                    print('Section ', this_key, ' is deleted!')

                    this_key = next(iter(questions_dict.keys()))  # Get the first key in dictionary
                    this_section_values = questions_dict[this_key]

                    check_for_brake = Section.objects.get(section=this_key).answer_category
                    if check_for_brake == 'brake':
                        print('Eimai sto brake2')
                        context = {
                            'team': team
                        }
                        return render(request, 'pages/frontend/brake.html', context)

                    if this_section_values:
                        this_question_id = this_section_values[0]  # Get the first item in list
                        this_section_values.pop(0)  # Remove the above item

                        # --- Get values from Database --- #
                        this_question = Question.objects.get(id=this_question_id)

                        # --- Delete & Update Session variables with new values --- #
                        del request.session['questions_dict']
                        del request.session['this_question_id']
                        request.session['questions_dict'] = questions_dict
                        request.session['this_question_id'] = this_question_id
                        print('New questions_dict: ', request.session.get('questions_dict'))
                        print('New this_question_id: ', request.session.get('this_question_id'))

                        context = {
                            # Variables for Template
                            'this_question': this_question,
                            'section': this_key,
                            'team': team
                        }

                        return render(request, 'pages/frontend/home.html', context)
            else:
                html = "<html><body><h1>END!!!</h1> </body></html> "
                return HttpResponse(html)

        # elif 'next-image' == request.POST['Post_name']:
        #
        #     # # --- Timestamp for Next or Start --- #
        #     next_time = request.POST['t']
        #
        #     # --- Check if all Images are done --- #
        #     if len(pairs_remaining) == 0:
        #
        #         # --- Retrieve variables from Session --- #
        #         flag = request.session.get('flag')
        #         logo = request.session.get('logo')
        #         footer = request.session.get('footer')
        #
        #         # --- Saving FINISHED entry to the Database --- #
        #         fin = Data(session=session_id, timestamp=next_time, status='finish', score=None,
        #                    countdown_per_pic=countdown_per_pic)
        #         fin.save()
        #         # For debugging purposes
        #         print('----------- FINISHED -----------')
        #
        #         # --- Data for the END page --- #
        #
        #         # Calculate Total time
        #         # --- Queries that get START and FINISH timestamps from Database --- #
        #         sta = int(Data.objects.get(session=session_id, status='start').timestamp)
        #         fin = int(Data.objects.get(session=session_id, status='finish').timestamp)
        #
        #         t_t = round((fin - sta) / 1000, 0)  # Total time converted in seconds and round (1 decimal)
        #         total_time = str(datetime.timedelta(seconds=t_t))
        #         print('Total time: ', total_time, 'hrs:min:sec')  # For debugging purposes.
        #
        #         # Calculate Average Search Time
        #         sum_dt = 0
        #         for i in pairs_done:
        #             st = Data.objects.filter(session=session_id, pair_id=i, status='start')
        #             nx = Data.objects.filter(session=session_id, pair_id=i, status='next')
        #
        #             if st.count() == 1 and nx.count() == 0:
        #                 t0 = int(st[0].timestamp)
        #             elif nx.count() == 1 and st.count() == 0:
        #                 t0 = int(nx[0].timestamp)
        #             else:
        #                 t0 = None
        #
        #             tr = Data.objects.filter(session=session_id, pair_id=i, status='True')
        #             fl = Data.objects.filter(session=session_id, pair_id=i, status='False')
        #             ex = Data.objects.filter(session=session_id, pair_id=i, status='Expire')
        #
        #             if tr.count() == 1:
        #                 t1 = int(tr[0].timestamp)
        #                 dt = t1 - t0
        #             elif fl.count() == 1:
        #                 t1 = int(fl[0].timestamp)
        #                 dt = t1 - t0
        #             elif ex.count() == 1:
        #                 t1 = int(ex[0].timestamp)
        #                 dt = t1 - t0
        #             else:
        #                 dt = None
        #
        #             sum_dt = sum_dt + dt
        #
        #         aver_st = sum_dt / len(pairs_done)
        #         aver_search_time = str(datetime.timedelta(seconds=round(aver_st / 1000, 0)))
        #         print('Average search time: ', aver_search_time, 'hrs:min:sec')  # For debugging purposes.
        #
        #         # Calculate Percent completed
        #         # --- Queries that get Accurate (yes) and Missed (no) Targets from Database --- #
        #         yes = Data.objects.filter(session=session_id, status=True).count()
        #
        #         percent_complete = round(yes / count_starting_pairs * 100)
        #         print('Percentage completed: ', percent_complete, '%')  # For debugging purposes.
        #
        #         context = {
        #             'flag': flag,
        #             'logo': logo,
        #             'footer': footer,
        #             'total_time': total_time,
        #             'aver_search_time': aver_search_time,
        #             'percent_complete': percent_complete,
        #         }
        #
        #         return render(request, 'pages/frontend/end.html', context)


# def end(request):
#
#     return render(request, 'pages/frontend/end.html')


@login_required
def brake(request):
    user = get_user(request)

    if user.username == 'user':
        return redirect('/')

    context = {
        # 'countdown': countdown,
    }

    return render(request, 'frontend/home.html', context)


# -------------------------------------------------------------------------------------------------------------------- #
#   BACK-END
# -------------------------------------------------------------------------------------------------------------------- #

@login_required
def dashboard(request):
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
    return render(request, 'pages/backend/dashboard.html', context)


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

    user = get_user(request)
    if user.username == 'user':
        return redirect('/')

    context = {
        'this_question': this_question,
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
            return redirect('/dashboard')
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
        return redirect('/dashboard')
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
            return redirect('/dashboard')
    context = {
        'this_option': this_option,
        'form': form
    }
    return render(request, 'pages/backend/options.html', context)

# @login_required
# def rankings(request):
#     user = get_user(request)
#     if user.username == 'user':
#         return redirect('/')
#
#     # --- Retrieve Session from Database --- #
#     last_session_in_data = Data.objects.aggregate(Max('session'))['session__max']
#     last_session_in_rank = Rank.objects.aggregate(Max('session'))['session__max']
#
#     if last_session_in_data is None:
#         print('No results to show.')
#         return render(request, 'pages/backend/rankings.html')
#
#     if last_session_in_rank is None:
#         print('No results to show.')
#         last_session_in_rank = 0
#
#     if last_session_in_rank < last_session_in_data:
#
#         # --- RANKING CALCULATIONS --- #
#         # --- Calculate average accuracy score for each pair --- #
#         pair_list = Data.objects.values_list('pair', flat=True).exclude(pair=None).distinct()
#
#         success = {}
#         failure = {}
#         accuracy = {}
#
#         for i in pair_list:
#
#             success[i] = Data.objects.filter(status='True', pair=i).count()
#             failure[i] = Data.objects.filter(Q(pair=i) & (Q(status='False') | Q(status='Expire'))).count()
#
#             avg_pair = Data.objects.filter(Q(pair=i) & (Q(status='True') | Q(status='False') | Q(status='Expire'))
#                                            ).aggregate(Avg('score'))['score__avg']
#             if avg_pair is None:
#                 avg_pair = 0
#
#             accuracy[i] = round(avg_pair, 2)
#
#             # --- Saving Success, Failures & Accuracy entry to the Database --- #
#             find_pair = Rank.objects.filter(pair=i)
#             if find_pair.exists():
#                 ac = Rank.objects.get(pair=i)
#                 ac.session = last_session_in_data
#                 ac.success = success[i]
#                 ac.failure = failure[i]
#                 ac.accuracy = accuracy[i]
#                 ac.save()
#                 print('Accuracy -------------- updated')
#             else:
#                 ac = Rank(pair=i, session=last_session_in_data, success=success[i], failure=failure[i],
#                           accuracy=accuracy[i])
#                 ac.save()
#                 print('Accuracy -------------- created')
#
#         # --- Calculate average time score for each pair --- #
#         session_list = Data.objects.values_list('session', flat=True).distinct()
#
#         time_dict = {}
#         for i in pair_list:
#             time_dict[i] = []  # Each dict value is an array of each pair time differences (milliseconds)
#
#         for i in session_list:
#             for j in pair_list:
#                 a1 = Data.objects.filter(Q(session=i) & Q(pair=j) & (Q(status='start') | Q(status='next')))
#                 if a1:
#                     a = a1[0].timestamp
#                 else:
#                     a = 0
#
#                 b1 = Data.objects.filter(
#                     Q(session=i) & Q(pair=j) & (Q(status='True') | Q(status='False') | Q(status='Expire')))
#                 if b1:
#                     b = b1[0].timestamp
#                     diff = int(b) - int(a)
#                     time_dict[j].append(diff)
#
#         response = {}
#         for i in pair_list:
#             #  Calculate the average time difference, convert in seconds.
#             x = sum(time_dict[i]) / len(time_dict[i]) / 1000
#             response[i] = round(x, 2)
#
#             # --- Saving Response entry to the Database --- #
#             find_pair = Rank.objects.filter(pair=i)
#             if find_pair.exists():
#                 re = Rank.objects.get(pair=i)
#                 re.response = response[i]
#                 re.save()
#                 print('Response -------------- updated')
#             else:
#                 re = Rank(response=response[i])
#                 re.save()
#                 print('Response -------------- created')
#
#         print('SUCCESS', success)
#         print('FAILURE', failure)
#         print('ACCURACY', accuracy)
#         print('RESPONSE', response)
#
#         rank = Rank.objects.all()
#         print('RANK', rank)
#         context = {'rank': rank}
#
#         return render(request, 'pages/backend/rankings.html', context)
#
#     rank = Rank.objects.all()
#     context = {'rank': rank}
#
#     return render(request, 'pages/backend/rankings.html', context)
