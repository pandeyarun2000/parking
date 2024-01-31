from django.shortcuts import render
from django.http import HttpResponse
from django.utils.safestring import mark_safe
import PyPDF2

def home(request):
    return render(request, 'home.html')

import re

def search_pdf(request):
    if request.method == 'POST':
        # get the keywords from the form data
        keywords = request.POST['keywords'].split(",")

        # get the PDF files from the form data
        pdf_files = request.FILES.getlist('pdf_file')

        # initialize an empty dictionary to store the sections containing the keywords for each file
        results = {}

        # loop through each PDF file
        for pdf_file in pdf_files:
            # create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            # initialize an empty list to store the sections containing the keywords for the current file
            file_results = []

            # loop through each page in the PDF document
            for page_num in range(len(pdf_reader.pages)):
                # extract the text from the current page
                page = pdf_reader.pages[page_num]
                text = page.extract_text()

                # check if any of the keywords are in the text
                for keyword in keywords:
                    if keyword in text:
                        # if the keyword is found, extract the entire section containing it
                        section_start = text.find(keyword)
                        section_end = text.find(".", section_start)
                        
                        # extract the paragraph after the keyword if the keyword's first letter is capitalized
                        if keyword[0].isupper():
                            match = re.search(r'\n\s*[A-Z].*?(?=\n\s*[A-Z]|$)', text[section_end:])
                            if match:
                                section_end += match.end()
                            else:
                                section_end = len(text)
                        
                        while section_end != -1:
                            if section_end > section_start and text[section_end-1].islower():
                                # if the period is part of an abbreviation, keep searching
                                section_end = text.find(".", section_end+1)
                            else:
                                # otherwise, this is the end of the section
                                break
                        section = text[section_start:section_end]

                        # highlight the keyword in the section
                        highlighted_section = section.replace(keyword, f'<span style="background-color: yellow;">{keyword}</span>')

                        # add the section to the list of results for the current file
                        file_results.append(highlighted_section)

            # add the list of results for the current file to the dictionary of results, using the file name as the key
            results[pdf_file.name] = file_results

        # render the results page with the sections containing the keywords for each file
        return render(request, 'results.html', {'results': results, 'keywords': keywords})

    else:
        # render the search page
        return render(request, 'search.html')


    
    

