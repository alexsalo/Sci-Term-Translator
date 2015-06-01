__author__ = 'alex'
from forms import *
from django.template import RequestContext
from django.shortcuts import render_to_response
from bs4 import BeautifulSoup
import langid
import wikipedia_updated

supported_prefixes = [prefix[0] for prefix in SUPPORTED_PREFIXES]
print 'supported_prefixes: ' + str(supported_prefixes)
langid.set_languages(supported_prefixes)

def searchView(request):
    if ('search_query' in request.GET) and request.GET['search_query'].strip():
        search_query = request.GET['search_query']
        if ('prefix' in request.GET) and request.GET['prefix'].strip():
            prefix = request.GET['prefix']

            print BeautifulSoup(search_query,from_encoding="utf-8")

            detected_langid = langid.classify(search_query)[0]
            print "Detected Lang: %s" % detected_langid
            print "Translate To: %s" % prefix

            if prefix == 'en' and detected_langid == 'en':
                detected_langid = 'de'
            if prefix == 'de' and detected_langid == 'de':
                detected_langid = 'en'

            translationFound = False
            wikipedia_updated.set_lang(detected_langid)

            # Base case
            try:
                page = wikipedia_updated.page(search_query)
                answer = page.lang_title(prefix)
                print BeautifulSoup(answer, from_encoding="utf-8")
                translationFound = True
            except Exception as e:
                print e

            # Try other languages
            if not translationFound:
                lids = [p for p in supported_prefixes if p != detected_langid and p!= prefix]
                for lid in lids:
                    if not translationFound:
                        print "Translation was not found, trying to use page langs: %s" % lid
                        wikipedia_updated.set_lang(lid)
                        try:
                            page = wikipedia_updated.page(search_query)
                            answer = page.lang_title(prefix)
                            print BeautifulSoup(answer,from_encoding="utf-8")
                            translationFound = True
                        except:
                            pass

            if not translationFound:
                answer = "Term was not found"

            form = searchForm(initial={'answer': answer, 'prefix' : prefix, 'search_query' : search_query})
        else:
            form = searchForm() #initial={'prefix' : 'ru'})
    else:
        form = searchForm()


    return render_to_response('search.html',
                              {'form':form},
        context_instance=RequestContext(request))