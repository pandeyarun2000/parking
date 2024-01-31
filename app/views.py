from django.shortcuts import render, redirect
from django.http import HttpResponse
import PyPDF2
import re
import csv
from django.utils.html import strip_tags

def home(request):
    return render(request, 'home.html')

def search_pdf(request):
    if request.method == 'POST':
        keywords = request.POST['keywords'].split(",")
        pdf_files = request.FILES.getlist('pdf_file')
        results = {}

        for pdf_file in pdf_files:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            file_results = []

            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()

                for keyword in keywords:
                    if keyword in text:
                        section_start = text.find(keyword)
                        section_end = text.find(".", section_start)

                        if keyword[0].isupper():
                            match = re.search(r'\n\s*[A-Z].*?(?=\n\s*[A-Z]|$)', text[section_end:])
                            if match:
                                section_end += match.end()
                            else:
                                section_end = len(text)

                        while section_end != -1:
                            if section_end > section_start and text[section_end-1].islower():
                                section_end = text.find(".", section_end+1)
                            else:
                                break
                        section = text[section_start:section_end]

                        highlighted_section = section.replace(keyword, f'<span style="background-color: yellow;">{keyword}</span>')
                        file_results.append(highlighted_section)

            results[pdf_file.name] = file_results

        request.session['results'] = results
        request.session['keywords'] = keywords
        return redirect('results')

    else:
        return render(request, 'search.html')

def results(request):
    results = request.session.get('results', {})
    keywords = request.session.get('keywords', [])
    return render(request, 'results.html', {'results': results, 'keywords': keywords})

def download_csv(request):
    results = request.session.get('results', {})
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="search_results.csv"'

    writer = csv.writer(response)
    writer.writerow(['File Name', 'Section'])

    for file_name, file_results in results.items():
        for section in file_results:
            section = strip_tags(section)

            if file_name in section:
                section = section.replace(file_name, '-')

            writer.writerow([file_name, section.strip()])

    return response





    






    
    

