from django.db.models import query
from django.db.models.fields import CommaSeparatedIntegerField
from program.views import like
from .models import Language, user_detail 
from .language_name import alphaname, prism_name
from django.core import serializers

# for user caching
from django.core.cache import cache, caches
from cache_key_generator import get_cache_key
from django.http import JsonResponse
from program.models import Program, program_title, program_rating
from querybook.models import Solutions, Query, solution_rating


def get_languages(request):
    languages = Language.objects.all()
    for language in languages:
        language.about = language.about.replace('-', '&#8209;')
        try:
            language.alphaname = alphaname[language.name]
            language.prism_name = prism_name[language.name]
        except:
            language.alphaname = 'testing'
            language.prism_name = 'testing'

    # saving user data 
    if request.user.is_authenticated:
        user_key = 'user/' + str(request.user.username) + '/'
        user_cache_value = caches['user'].get(user_key)
        if user_cache_value is not None:
            params = user_cache_value

        else:
            # Handle liking
            programs = Program.objects.filter(like = request.user)
            solutions = Solutions.objects.filter(like = request.user)
        
            program_like_id = list()
            solution_like_id = list()


            for program in programs:
                program_like_id.append(program.id)

            for solution in solutions:
                solution_like_id.append(solution.id)


            # handle rating
            program_ratings = program_rating.objects.filter(user = request.user)
            program_rating_data = dict()
            sum_program_rating = 0
            program_rating_count = 0
            for rating in program_ratings:
                program_rating_data[rating.program.id] = rating.rating
                sum_program_rating += rating.rating
                program_rating_count += 1
            if program_rating_count == 0:
                program_rating_count = 1

            solution_ratings = solution_rating.objects.filter(user = request.user)
            solution_rating_data = dict()
            sum_query_rating = 0
            query_rating_count = 0
            for rating in solution_ratings:
                solution_rating_data[rating.solution.id] = rating.rating
                sum_query_rating += rating.rating
                query_rating_count += 1
            if query_rating_count == 0:
                query_rating_count = 1



            user_data_obj = user_detail.objects.filter(user = request.user)

            
            program = {
                'like' : program_like_id,
                'rating' : program_rating_data
            }

            querybook = {
                'like' : solution_like_id,
                'rating' : solution_rating_data 
            }

            if not user_data_obj.exists():
            
                user_data = {
                    'dob': "N/A",
                    'gender': "Male",
                    'about': "-",
                    'privacy': False,
                    'image' : "",
                    'program_rating' : round((sum_query_rating * 20)/query_rating_count, 2),
                    'solution_rating' : round((sum_program_rating * 20)/program_rating_count, 2)
                    
                }
            else:
                user_data_obj = user_data_obj.first()
                user_data = {
                    'dob': user_data_obj.dob,
                    'gender': user_data_obj.gender,
                    'about': user_data_obj.about,
                    'privacy': user_data_obj.privacy,
                    'image' : user_data_obj.image,
                    'program_rating' : round((sum_query_rating * 20)/query_rating_count, 2),
                    'solution_rating' : round((sum_program_rating * 20)/program_rating_count, 2)
                    
                }

            user = {
                'username': request.user.username,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'id': request.user.id,
                'email': request.user.email
            }

            params = {
                'user' : user,
                'user_data' : user_data,
                # 'program_like_id' : program_like_id,
                # 'solution_like_id' : solution_like_id,
                # 'program_rating' : program_rating_data,
                'program' : program,
                'querybook' : querybook
                       }
            caches['user'].set(user_key, params, 60*60)
    else:
        user_key = 'user/' + str(request.user.username) + '/'
        user_cache_value = caches['user'].get(user_key)
        if user_cache_value is not None:
            params = user_cache_value

        else:
            # Handle liking
            program_like_id = list()
            solution_like_id = list()


            # handle rating
            program_rating_data = dict()
            solution_rating_data = dict()



            program = {
                'like' : program_like_id,
                'rating' : program_rating_data
            }

            querybook = {
                'like' : solution_like_id,
                'rating' : solution_rating_data   

            }

            user_data = {
                
            }

            user = {
            }

            params = {
                'user' : user,
                'user_data' : user_data,
                # 'program_like_id' : program_like_id,
                # 'solution_like_id' : solution_like_id,
                # 'program_rating' : program_rating_data,
                'program' : program,
                'querybook' : querybook
                       }
            caches['user'].set(user_key, params, 10*60)

    language_json = serializers.serialize('json', languages)
    return {'languages':languages, 'language_serialized':language_json}





