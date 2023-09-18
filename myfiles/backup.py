
# Handle final blog
# @cache_page(60 * 1)
# def final_blog(request, lang, slug):
language = check_language(lang)
if language != None:
    category = language.category.split(',')
    if 'Blog' in category or 'blog' in category:
        blog = Blog.objects.get(language=lang, slug=slug)
         comment = Comment.objects.filter(blog=blog, reply=None)
          rating = 0

           if request.user.is_authenticated:
                if blog_rating.objects.filter(blog=blog, user=request.user).exists():
                    rating_obj = blog_rating.objects.get(
                        blog=blog, user=request.user)
                    blog.rating = rating_obj.rating
                else:
                    blog.rating = 0

            if blog.like.filter(id=request.user.id).exists():
                blog.liked = True
            else:
                blog.liked = False
            # prism language
            prism = prism_name[blog.language]
            blog.content = blog.content.replace(
                '<code>', f'<body class="line-numbers"><pre class="code" > <code class="language-{prism}">')
            blog.content = blog.content.replace(
                '</code>', f'</code></pre></body>')

            meta = Meta(
                title="ARCODERS BLOG:- " + blog.title,
                description=blog.title,
                keywords=meta_data + [blog.title, blog.language],
                extra_props={
                    'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'},
                extra_custom_props=[('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
                                    ]
            )

            params = {'cat': cat, 'blog': blog, 'meta': meta,
                      'comments': comment, 'rating': True}
            return render(request, 'blog/final.html', params)

















    id = []
    like = []
    rating = []
    total_rating = []

    title = program_title.objects.filter(slug = slug)
    if title.exists():
        exists = True
        programs = Program.objects.filter(title=title[0])
        if request.user.is_authenticated:
            # for authentication
            auth = True
            for program in programs:
                # id
                id.append(program.id)

                # like_data
                if program.like.filter(id=request.user.id).exists():
                    like_data = True
                else:
                    like_data = False
                like_count = program.like_count()
                like.append([like_data, like_count])

                # rating
                rating_obj = program_rating.objects.filter(program=program, user=request.user)
                if rating_obj.exists():
                    rating_data = float(rating_obj[0].rating)
                else:
                    rating_data = 0
                rating.append(rating_data)

                # total rating
                total_rating.append(program.total_rating())
                

        else:
            auth = False
            for program in programs:
                id.append(program.id)
                like.append(False)
                rating.append(0)
                total_rating.append(program.total_rating())

    else:
        exists = False

    params = {'exists':exists, 'auth':auth, 'id':id, 'like':like, 'rating':rating, 'total_rating':total_rating}
    return JsonResponse(params)





















                var rating_data = `<div class="mb-3" style=" justify-content: center;">

                        <p style="font-family: cursive;color:dodgerblue;font-size: 1.4rem;margin-bottom:0;">Rate </p>
                        <div id="halfstarsReview${response.id}" style="color: dodgerblue; animation: animate 2s linear infinite"></div>

                        </div>

                        <input type="text" readonly id="halfstarsInput${response.id}" class="form-control form-control-sm" hidden
                            value=${response.rating}>


                    <br>
                    <br>

                `
                element.innerHTML += rating_data














                                            < script >
                            \$("#halfstarsReview${response.id}").rating({
                                "half": true,
                                "click": function (e) {
                                    console.log(e);
                                    \$("#halfstarsInput${response.id}").val(e.stars);
                                    var code_id = ${response.id}

                        \$.ajax({
                                url: '/program/rating/',
                                type: 'POST',
                                data: {
                                    id: code_id,
                                    rate: \$("#halfstarsInput${response.id}").val()
                                }
                            }).done(function (response) {
                                if (response == "True") {
                                    console.log("True")
                                }
                                else {

                                    console.log("false")

                                }
                            })
                                    .fail(function () {
                                        console.log("failed");
                                    })
                        }
                });




                var rate${response.id} = \$('#halfstarsInput${response.id}').val()
                for (var i = 1; i <= rate${response.id}; i++) {
            var str1 = "#halfstarsReview${response.id} i:nth-child(".concat(i)
            var str = str1.concat(')')
            \$(str).removeClass('fa-star-o')
            \$(str).addClass('fa-star')

        }
        if (rate{ { code.id } } -(i - 1) == 0.5) {
                                        var str1 = "#halfstarsReview${response.id} i:nth-child(".concat(i)
                                        var str = str1.concat(')')
                                        \$(str).removeClass('fa-star-o')
                                        \$(str).addClass('fa-star-half-o')

                                    }

                                            </script>







# for user image
            # for adding the profile
            print('\n\n\nnot a default image')
            username = request.user.username
            end = request.FILES['image'].name.split('.')[1]
            profile_image = Image.open(request.FILES['image'])
            # return_data = profile_imgae.save(f'media/files/image/user/{username}.{end}')
            profile_image.filename = request.user.username + '.' + end
            extension_name = user_data.image.name.split('.')[1]
            os.remove(f'media/files/image/user/{username}.{extension_name}')
            user_data.image = profile_image
            user_data.save()













                var rate${ response.programs.id[i] } = $('#halfstarsInput${response.programs.id[i]}').val()
                var j = i
                for (var i = 1; i <= rate${response.programs.id[j]}; i++) {
                var str1 = "#halfstarsReview${response.programs.id[j]} i:nth-child(".concat(j)
                var str = str1.concat(')')
                $(str).removeClass('fa-star-o')
                $(str).addClass('fa-star')

        }
        if (rate${response.programs.id[j]} -(i - 1) == 0.5) {
                                    var str1 = "#halfstarsReview${response.programs.id[j]} i:nth-child(".concat(i)
                                    var str = str1.concat(')')
                                    $(str).removeClass('fa-star-o')
                                    $(str).addClass('fa-star-half-o')

                                }
