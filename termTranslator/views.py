__author__ = 'alex'
from forms import *
from django.template import RequestContext
from django.shortcuts import render_to_response
import langid
import wikipedia_updated as wk

supported_prefixes = [prefix[0] for prefix in SUPPORTED_PREFIXES]
print 'supported_prefixes: ' + str(supported_prefixes)
langid.set_languages(supported_prefixes)

def searchView(request):
    if ('search_query' in request.GET) and request.GET['search_query'].strip():
        search_query = request.GET['search_query']
        if ('prefix' in request.GET) and request.GET['prefix'].strip():
            prefix = request.GET['prefix']

            print(search_query)
            detected_langid = langid.classify(search_query)[0]
            print "Detected Lang: %s" % detected_langid
            wk.set_lang(detected_langid)

            print "Translate To: %s" % prefix
            try:
                page = wk.page(search_query)

                answer = page.lang_title(prefix)
                print("Answer: %s" % answer)
            except:
                print "term was not found"
                answer = "term was not found"

            form = searchForm(initial={'answer': answer})
    else:
        form = searchForm()


    return render_to_response('search.html',
                              {'form':form},
        context_instance=RequestContext(request))