from arcoder.models import Language

# remove the quotation from the program title
def program_title_remove_quotations(program_data):
    for index,data in enumerate(program_data):
        title = data.title
        title = title.replace('\"', '&quot;')
        title = title.replace("\'", '&apos;')
        program_data[index].title = title
    return program_data


# remove the quotation from the query
def query_title_remove_quotations(query_data):
    for index, data in enumerate(query_data):
        title = data.query
        title = title.replace('\"', '&quot;')
        title = title.replace("\'", '&apos;')
        query_data[index].query = title
    return query_data



def check_language(lang):
    try:
        if lang == 'C  ':
            lang = 'C++'
        language = Language.objects.get(name=lang)
    except:
        language = None
    return language

