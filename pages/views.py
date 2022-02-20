import datetime
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

    # --- Check the language from url  --- #
    # choices = {'el': ('flag_el.png', 'logo_el.png', 'caption_pri_el', 'caption_sec_el', 'description_el', 'headline_el',
    #                   'instructions_el', 'footer_el'),
    #            'en': ('flag_en.png', 'logo.png', 'caption_pri_en', 'caption_sec_en', 'description_en', 'headline_en',
    #                   'instructions_en', 'footer_en')}
    # (flag, logo, caption_pri, caption_sec, description, headline, instructions, footer) = \
    #     choices.get(lang, (
    #         'flag_el.png', 'logo_el.png', 'caption_pri_el', 'caption_sec_el', 'description_el', 'headline_el',
    #         'instructions_el', 'footer_el'))
    # print('Language: is set to ', lang)  # For debugging purposes

    # --- Fetch headline, instructions & footer from Database Options  --- #
    headline = Option.objects.get(id=1).headline
    instructions = Option.objects.get(id=1).instructions
    footer = Option.objects.get(id=1).footer
    logo = 'logo.png'

    # --- Query to get all Pairs --- #
    # pairs = Pair.objects.values_list('id', flat=True)  # Get all Pairs id's as a list
    # print('All possible pairs are: ', pairs)  # For debugging purposes

    # --- Get countdown time that is set from Database Options  --- #
    # countdown_per_pic = Option.objects.get(id=1).countdown_per_pic

    # --- Get n pairs randomly --- #
    # n = Option.objects.get(id=1).sample_count  # Get value from Database (Option)
    # if n <= len(pairs):
    #     pairs_remaining = random.sample(list(pairs), n)
    #     print("Random sample", n, "out of ", len(pairs), "pairs of pictures")
    # else:
    #     pairs_remaining = random.sample(list(pairs), len(pairs))
    #     print("Not enough pictures for", n, "samples. Test will proceed with the maximum",
    #           len(pairs), "pairs of pictures")
    #
    # print('Available pairs: ', pairs_remaining)  # For debugging purposes
    # pairs_done = []  # Create an empty pictures done list

    # --- Get correct session from Database --- #
    max_session = Data.objects.aggregate(Max('session'))  # Query that gets maximum value of all sessions
    last_session = max_session['session__max']  # Clear the value to be an integer
    # Avoid error if database is empty
    if last_session is None:
        last_session = 0
    session_id = last_session + 1  # Next session value
    print('Session is: ', session_id)  # For debugging purposes

    # --- Create Session variables with new values --- #
    request.session['session_id'] = session_id

    # request.session['flag'] = flag
    request.session['logo'] = logo
    request.session['footer'] = footer

    # request.session['countdown_per_pic'] = countdown_per_pic
    # request.session['pairs_remaining'] = pairs_remaining
    # request.session['pairs_done'] = pairs_done
    # request.session['count_starting_pairs'] = len(pairs_remaining)
    #
    # request.session['caption_pri'] = caption_pri
    # request.session['caption_sec'] = caption_sec
    # request.session['description'] = description

    form = UserForm()

    context = {
        # 'flag': flag,
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
        countdown_per_pic = request.session.get('countdown_per_pic')
        pairs_remaining = request.session.get('pairs_remaining')
        pairs_done = request.session.get('pairs_done')
        count_starting_pairs = request.session.get('count_starting_pairs')
        random_pick = request.session.get('random_pick')
        caption_pri = request.session.get('caption_pri')
        caption_sec = request.session.get('caption_sec')
        description = request.session.get('description')

        # --- Avoid test when no pairs are available --- #
        if count_starting_pairs <= 0:
            html = "<html><body><h1>Database is empty!!!</h1>Go back to <a href='/dashboard'>Dashboard </a>" \
                   "and add some entries! </body></html> "
            return HttpResponse(html)

        print('Session is: ', session_id)  # For debugging purposes
        print('Remaining pairs: ', pairs_remaining)  # For debugging purposes
        print('Pairs done: ', pairs_done)  # For debugging purposes

        if 'commit-target' == request.POST['Post_name']:
            # --- Timestamp for Commit --- #
            commit_time = request.POST['t']  # Get time in Epoch (milliseconds)

            # --- Retrieve current targets from Session --- #
            pair_obj = Pair.objects.get(id=random_pick)
            target_obj = pair_obj.pair_target

            # --- Get filenames of pictures --- #
            filename_pri = pair_obj.image_pri.name
            filename_sec = pair_obj.image_sec.name

            # # --- Retrieve values from Primary target (px) --- #
            x_p = float(request.POST['x_p'])
            y_p = float(request.POST['y_p'])
            w_p = float(request.POST['w_p'])
            h_p = float(request.POST['h_p'])

            # --- Convert values to percentages (%) --- #
            xtl_pri = x_p / pair_obj.width_pri * 100
            ytl_pri = y_p / pair_obj.height_pri * 100
            w_pri = w_p / pair_obj.width_pri * 100
            h_pri = h_p / pair_obj.height_pri * 100

            # --- Calculate to bottom-right end of the selected box (%) --- #
            xbr_pri = xtl_pri + w_pri
            ybr_pri = ytl_pri + h_pri

            # --- Convert Database values (x, y, width, height) to percentages (%) --- #
            x0tl_pri = target_obj.x_pri / pair_obj.width_pri * 100
            y0tl_pri = target_obj.y_pri / pair_obj.height_pri * 100
            w0_pri = target_obj.w_pri / pair_obj.width_pri * 100
            h0_pri = target_obj.h_pri / pair_obj.height_pri * 100

            # --- Calculate to bottom-right end of Database box (%) --- #
            x0br_pri = x0tl_pri + w0_pri
            y0br_pri = y0tl_pri + h0_pri

            # --- Calculate the area of Intersection (Overlap) (%) --- #
            x1 = max(xtl_pri, x0tl_pri)
            x2 = min(xbr_pri, x0br_pri)
            y1 = max(ytl_pri, y0tl_pri)
            y2 = min(ybr_pri, y0br_pri)

            if x1 < x2 and y1 < y2:
                intersection_pri = (x2 - x1) * (y2 - y1)
            else:
                intersection_pri = 0

            # --- Calculate the area of Union (Overlap) (%) --- #
            union_pri = (w_pri * h_pri) + (w0_pri * h0_pri) - intersection_pri

            print(intersection_pri, union_pri)

            ratio = intersection_pri / union_pri
            score_pri = ratio * 100
            score = round(score_pri, 1)

            status: bool
            if int(round(score)) > 70:
                status = True
            elif int(round(score)) == 0:
                status = False
            else:
                status = False

            obj = {
                'xtl_pri': xtl_pri,
                'ytl_pri': ytl_pri,
                'xbr_pri': xbr_pri,
                'ybr_pri': ybr_pri,
                'total_score': score,
                'status': status
            }

            if target_obj.x_sec and target_obj.y_sec and target_obj.w_sec and target_obj.h_sec:
                # --- Retrieve values from Secondary target --- #
                x_s = float(request.POST['x_s'])
                y_s = float(request.POST['y_s'])
                w_s = float(request.POST['w_s'])
                h_s = float(request.POST['h_s'])

                # --- Convert values to percentages (%) --- #
                xtl_sec = x_s / pair_obj.width_sec * 100
                ytl_sec = y_s / pair_obj.height_sec * 100
                w_sec = w_s / pair_obj.width_sec * 100
                h_sec = h_s / pair_obj.height_sec * 100

                # --- Calculate to bottom-right end of the selected box (%) --- #
                xbr_sec = xtl_sec + w_sec
                ybr_sec = ytl_sec + h_sec

                # --- Convert Database values (x, y, width, height) to percentages (%) --- #
                x0tl_sec = target_obj.x_sec / pair_obj.width_sec * 100
                y0tl_sec = target_obj.y_sec / pair_obj.height_sec * 100
                w0_sec = target_obj.w_sec / pair_obj.width_sec * 100
                h0_sec = target_obj.h_sec / pair_obj.height_sec * 100

                # --- Calculate to bottom-right end of Database box (%) --- #
                x0br_sec = x0tl_sec + w0_sec
                y0br_sec = y0tl_sec + h0_sec

                # --- Calculate the area of Intersection (Overlap) (%) --- #
                x1 = max(xtl_sec, x0tl_sec)
                x2 = min(xbr_sec, x0br_sec)
                y1 = max(ytl_sec, y0tl_sec)
                y2 = min(ybr_sec, y0br_sec)

                if x1 < x2 and y1 < y2:
                    intersection_sec = (x2 - x1) * (y2 - y1)
                else:
                    intersection_sec = 0

                # --- Calculate the area of Union (Overlap) (%) --- #
                union_sec = (w_sec * h_sec) + (w0_sec * h0_sec) - intersection_sec

                print(intersection_sec, union_sec)

                ratio_sec = intersection_sec / union_sec
                score_sec = ratio_sec * 100

                score = round((score_pri + score_sec) / 2, 1)

                status: bool
                if int(round(score)) > 70:
                    status = True
                elif int(round(score)) == 0:
                    status = False
                else:
                    status = False

                obj.update({
                    'xtl_sec': xtl_sec,
                    'ytl_sec': ytl_sec,
                    'xbr_sec': xbr_sec,
                    'ybr_sec': ybr_sec,
                    'total_score': score,
                    'status': status
                })

                # For debugging purposes
                print('Score:', score)

                status: bool
                if int(round(score)) > 70:
                    status = True
                elif int(round(score)) == 0:
                    status = False
                else:
                    status = False

                # # Saving Click values to the Database (Models.Data)
                cli = Data(session=session_id, timestamp=commit_time, status=status, score=score,
                           pair_id=random_pick, filename_pri=filename_pri, filename_sec=filename_sec,
                           xtl_pri=xtl_pri, ytl_pri=ytl_pri, xbr_pri=xbr_pri, ybr_pri=ybr_pri,
                           xtl_sec=xtl_sec, ytl_sec=ytl_sec, xbr_sec=xbr_sec, ybr_sec=ybr_sec,
                           countdown_per_pic=countdown_per_pic)
                cli.save()
                print("Successfully added to the database!")

                # --- Clear pair in Session --- #
                del (request.session['random_pick'])

                return JsonResponse(obj, safe=True)

            # For debugging purposes
            print('Score:', score)

            # # Saving Click values to the Database (Models.Data)
            cli = Data(session=session_id, timestamp=commit_time, status=status, score=score,
                       pair_id=random_pick, filename_pri=filename_pri, filename_sec=filename_sec,
                       xtl_pri=xtl_pri, ytl_pri=ytl_pri, xbr_pri=xbr_pri, ybr_pri=ybr_pri,
                       countdown_per_pic=countdown_per_pic)
            cli.save()
            print("Successfully added to the database!")

            # --- Clear pair in Session --- #
            del (request.session['random_pick'])

            return JsonResponse(obj, safe=True)

        elif 'expired-target' == request.POST['Post_name']:
            # --- Timestamp for Expired --- #
            expired_time = int(Data.objects.last().timestamp) + (countdown_per_pic * 1000)

            # --- Retrieve current targets from Session --- #
            pair_obj = Pair.objects.get(id=random_pick)

            # --- Get filenames of pictures --- #
            filename_pri = pair_obj.image_pri.name
            filename_sec = pair_obj.image_sec.name

            # --- Saving EXPIRED values to the Database (Models.Data)--- #
            exp = Data(session=session_id, timestamp=expired_time, status='Expire', score=0,
                       pair_id=random_pick, filename_pri=filename_pri, filename_sec=filename_sec,
                       countdown_per_pic=countdown_per_pic)
            exp.save()
            print("Expired entry saved to the database!")  # For debugging purposes

        elif 'next-image' == request.POST['Post_name']:

            # # --- Timestamp for Next or Start --- #
            next_time = request.POST['t']

            # --- Check if all Images are done --- #
            if len(pairs_remaining) == 0:

                # --- Retrieve variables from Session --- #
                flag = request.session.get('flag')
                logo = request.session.get('logo')
                footer = request.session.get('footer')

                # --- Saving FINISHED entry to the Database --- #
                fin = Data(session=session_id, timestamp=next_time, status='finish', score=None,
                           countdown_per_pic=countdown_per_pic)
                fin.save()
                # For debugging purposes
                print('----------- FINISHED -----------')

                # --- Data for the END page --- #

                # Calculate Total time
                # --- Queries that get START and FINISH timestamps from Database --- #
                sta = int(Data.objects.get(session=session_id, status='start').timestamp)
                fin = int(Data.objects.get(session=session_id, status='finish').timestamp)

                t_t = round((fin - sta) / 1000, 0)  # Total time converted in seconds and round (1 decimal)
                total_time = str(datetime.timedelta(seconds=t_t))
                print('Total time: ', total_time, 'hrs:min:sec')  # For debugging purposes.

                # Calculate Average Search Time
                sum_dt = 0
                for i in pairs_done:
                    st = Data.objects.filter(session=session_id, pair_id=i, status='start')
                    nx = Data.objects.filter(session=session_id, pair_id=i, status='next')

                    if st.count() == 1 and nx.count() == 0:
                        t0 = int(st[0].timestamp)
                    elif nx.count() == 1 and st.count() == 0:
                        t0 = int(nx[0].timestamp)
                    else:
                        t0 = None

                    tr = Data.objects.filter(session=session_id, pair_id=i, status='True')
                    fl = Data.objects.filter(session=session_id, pair_id=i, status='False')
                    ex = Data.objects.filter(session=session_id, pair_id=i, status='Expire')

                    if tr.count() == 1:
                        t1 = int(tr[0].timestamp)
                        dt = t1 - t0
                    elif fl.count() == 1:
                        t1 = int(fl[0].timestamp)
                        dt = t1 - t0
                    elif ex.count() == 1:
                        t1 = int(ex[0].timestamp)
                        dt = t1 - t0
                    else:
                        dt = None

                    sum_dt = sum_dt + dt

                aver_st = sum_dt / len(pairs_done)
                aver_search_time = str(datetime.timedelta(seconds=round(aver_st / 1000, 0)))
                print('Average search time: ', aver_search_time, 'hrs:min:sec')  # For debugging purposes.

                # Calculate Percent completed
                # --- Queries that get Accurate (yes) and Missed (no) Targets from Database --- #
                yes = Data.objects.filter(session=session_id, status=True).count()

                percent_complete = round(yes / count_starting_pairs * 100)
                print('Percentage completed: ', percent_complete, '%')  # For debugging purposes.

                context = {
                    'flag': flag,
                    'logo': logo,
                    'footer': footer,
                    'total_time': total_time,
                    'aver_search_time': aver_search_time,
                    'percent_complete': percent_complete,
                }

                return render(request, 'pages/frontend/end.html', context)

            else:

                # --- Pair selection random generator --- #
                # random_pick = random.choice(pairs_remaining)  # Random choice from pairs list
                random_pick = min(pairs_remaining)  # minimum from pairs list

                # --- Remove/Add selected pair from pairs list --- #
                pairs_remaining.remove(random_pick)
                pairs_done.append(random_pick)

                # # --- Calculate completion percentage for progress bar --- #
                progress_bar = round(len(pairs_done) / count_starting_pairs * 100)

                # --- Update Session with new values --- #
                request.session['session_id'] = session_id
                request.session['pairs_remaining'] = pairs_remaining
                request.session['pairs_done'] = pairs_done
                request.session['random_pick'] = random_pick

                # Set an object variable for current pair
                pair_obj = Pair.objects.get(id=random_pick)
                print('Pair selected:', random_pick)  # For debugging purposes

                # --- Get filename of Primary and Secondary picture from Database --- #
                filename_pri = pair_obj.image_pri.name
                filename_sec = pair_obj.image_sec.name
                print('Filename of Primary picture:', filename_pri)
                print('Filename of Secondary picture:', filename_sec)

                # --- Get Captions and Description from Database --- #
                caption_primary = getattr(pair_obj, caption_pri)
                caption_secondary = getattr(pair_obj, caption_sec)
                description = getattr(pair_obj, description)

                # --- Create Target boxes from Database --- #

                # Get the target object of this pair
                target_obj = Target.objects.get(pair=random_pick)

                # Convert targets positions to percentages
                left_pri = target_obj.x_pri / pair_obj.width_pri * 100
                top_pri = target_obj.y_pri / pair_obj.height_pri * 100
                width_pri = target_obj.w_pri / pair_obj.width_pri * 100
                height_pri = target_obj.h_pri / pair_obj.height_pri * 100

                # Put them in array
                spot_pri = [left_pri, top_pri, width_pri, height_pri]

                # Check if secondary target exist
                if target_obj.x_sec and target_obj.y_sec and target_obj.w_sec and target_obj.h_sec:
                    left_sec = target_obj.x_sec / pair_obj.width_sec * 100
                    top_sec = target_obj.y_sec / pair_obj.height_sec * 100
                    width_sec = target_obj.w_sec / pair_obj.width_sec * 100
                    height_sec = target_obj.h_sec / pair_obj.height_sec * 100

                    # Put them in array
                    spot_sec = [left_sec, top_sec, width_sec, height_sec]
                    print('This pair has 2 targets')  # For debugging purposes

                else:
                    spot_sec = json.dumps(None)  # Convert python None to JavaScript null
                    print('This pair has 1 target')  # For debugging purposes

            # --- Put current pick to Session --- #
            request.session['random_pick'] = random_pick

            # --- Check if it's the first POST --- #
            if len(pairs_done) == 1:
                session_p = request.POST['session']
                start_time = next_time
                gender_p = request.POST['gender']
                age_p = request.POST['age']
                education_p = request.POST['education']
                sector_p = request.POST['sector']
                knowledge_p = request.POST['knowledge']

                # --- Saving User to the Database (Models.User)--- #
                user = User(session=session_p, gender=gender_p, age=age_p, education=education_p,
                            sector=sector_p, knowledge=knowledge_p)
                user.save()
                print("User entry saved to the database!")  # For debugging purposes

                # --- Saving Click of START to the Database (Models.Data)--- #
                sta = Data(session=session_id, timestamp=start_time, status='start', score=None,
                           pair_id=random_pick, filename_pri=filename_pri, filename_sec=filename_sec,
                           countdown_per_pic=countdown_per_pic)
                sta.save()
                print("----------- START -----------")  # For debugging purposes

                context = {
                    # Variables for Template
                    'pair_object': pair_obj,
                    'caption_primary': caption_primary,
                    'caption_secondary': caption_secondary,
                    'description': description,
                    'progress_bar': progress_bar,
                    'len_pairs_done': len(pairs_done),
                    'count_starting_pairs': count_starting_pairs,
                    # Variables for JavaScript
                    'filename_pri': filename_pri,
                    'filename_sec': filename_sec,
                    'countdown_per_pic': countdown_per_pic,
                    'spot_pri': spot_pri,
                    'spot_sec': spot_sec
                }

                return render(request, 'pages/frontend/home.html', context)

            # --- Saving Click of NEXT to the Database (Models.Data)--- #
            nex = Data(session=session_id, timestamp=next_time, status='next', score=None,
                       pair_id=random_pick, filename_pri=filename_pri, filename_sec=filename_sec,
                       countdown_per_pic=countdown_per_pic)
            nex.save()
            print("Next entry saved to the database!")  # For debugging purposes

            print('----------- NEXT -----------')

            context = {
                # Variables for Template
                'pair_object': pair_obj,
                'caption_primary': caption_primary,
                'caption_secondary': caption_secondary,
                'description': description,
                'progress_bar': progress_bar,
                'len_pairs_done': len(pairs_done),
                'count_starting_pairs': count_starting_pairs,
                # Variables for JavaScript
                'filename_pri': filename_pri,
                'filename_sec': filename_sec,
                'countdown_per_pic': countdown_per_pic,
                'spot_pri': spot_pri,
                'spot_sec': spot_sec
            }

            return render(request, 'pages/frontend/home.html', context)

        return render(request, 'pages/frontend/home.html')


# def end(request):
#
#     return render(request, 'pages/frontend/end.html')


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


@login_required
def rankings(request):
    user = get_user(request)
    if user.username == 'user':
        return redirect('/')

    # --- Retrieve Session from Database --- #
    last_session_in_data = Data.objects.aggregate(Max('session'))['session__max']
    last_session_in_rank = Rank.objects.aggregate(Max('session'))['session__max']

    if last_session_in_data is None:
        print('No results to show.')
        return render(request, 'pages/backend/rankings.html')

    if last_session_in_rank is None:
        print('No results to show.')
        last_session_in_rank = 0

    if last_session_in_rank < last_session_in_data:

        # --- RANKING CALCULATIONS --- #
        # --- Calculate average accuracy score for each pair --- #
        pair_list = Data.objects.values_list('pair', flat=True).exclude(pair=None).distinct()

        success = {}
        failure = {}
        accuracy = {}

        for i in pair_list:

            success[i] = Data.objects.filter(status='True', pair=i).count()
            failure[i] = Data.objects.filter(Q(pair=i) & (Q(status='False') | Q(status='Expire'))).count()

            avg_pair = Data.objects.filter(Q(pair=i) & (Q(status='True') | Q(status='False') | Q(status='Expire'))
                                           ).aggregate(Avg('score'))['score__avg']
            if avg_pair is None:
                avg_pair = 0

            accuracy[i] = round(avg_pair, 2)

            # --- Saving Success, Failures & Accuracy entry to the Database --- #
            find_pair = Rank.objects.filter(pair=i)
            if find_pair.exists():
                ac = Rank.objects.get(pair=i)
                ac.session = last_session_in_data
                ac.success = success[i]
                ac.failure = failure[i]
                ac.accuracy = accuracy[i]
                ac.save()
                print('Accuracy -------------- updated')
            else:
                ac = Rank(pair=i, session=last_session_in_data, success=success[i], failure=failure[i],
                          accuracy=accuracy[i])
                ac.save()
                print('Accuracy -------------- created')

        # --- Calculate average time score for each pair --- #
        session_list = Data.objects.values_list('session', flat=True).distinct()

        time_dict = {}
        for i in pair_list:
            time_dict[i] = []  # Each dict value is an array of each pair time differences (milliseconds)

        for i in session_list:
            for j in pair_list:
                a1 = Data.objects.filter(Q(session=i) & Q(pair=j) & (Q(status='start') | Q(status='next')))
                if a1:
                    a = a1[0].timestamp
                else:
                    a = 0

                b1 = Data.objects.filter(
                    Q(session=i) & Q(pair=j) & (Q(status='True') | Q(status='False') | Q(status='Expire')))
                if b1:
                    b = b1[0].timestamp
                    diff = int(b) - int(a)
                    time_dict[j].append(diff)

        response = {}
        for i in pair_list:
            #  Calculate the average time difference, convert in seconds.
            x = sum(time_dict[i]) / len(time_dict[i]) / 1000
            response[i] = round(x, 2)

            # --- Saving Response entry to the Database --- #
            find_pair = Rank.objects.filter(pair=i)
            if find_pair.exists():
                re = Rank.objects.get(pair=i)
                re.response = response[i]
                re.save()
                print('Response -------------- updated')
            else:
                re = Rank(response=response[i])
                re.save()
                print('Response -------------- created')

        print('SUCCESS', success)
        print('FAILURE', failure)
        print('ACCURACY', accuracy)
        print('RESPONSE', response)

        rank = Rank.objects.all()
        print('RANK', rank)
        context = {'rank': rank}

        return render(request, 'pages/backend/rankings.html', context)

    rank = Rank.objects.all()
    context = {'rank': rank}

    return render(request, 'pages/backend/rankings.html', context)
