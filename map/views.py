import os
import csv
import folium
import pandas as pd

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import redirect

from .forms import CountriesForm

def index(request):
    countries = CountriesForm() 
    context = {'countries': countries}
    return render(request, 'map/index.html', context)


def submit(request):
    if request.method != 'POST':
        #No data submitted; create a blank form
        countries = CountriesForm()
    else:
        #POST data submitted; process data
        form = CountriesForm(data=request.POST)
        if form.is_valid():
            countries_string = form.cleaned_data['countries']

            # Create a list of countries based separated by commas
            countries_list = countries_string.split(',')

            # Clean up whitespace
            countries = []
            for country in countries_list:
                countries.append(country.strip())

            header = ['Countries', 'Traveled']

            #Write to file
            tmp_path = os.path.join(settings.MEDIA_ROOT, 'tmp/countries.txt')
            with open(tmp_path, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                for country in countries:
                    row = [country, '1']
                    writer.writerow(row)

            return redirect('process')

def process(request):

    countries_traveled = pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'tmp/countries.txt'))

    political_countries_url = (
        "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
    )

    m = folium.Map(location=(30, 10), zoom_start=3, tiles="cartodb positron")

    folium.Choropleth(
        geo_data=political_countries_url,
        data=countries_traveled,
        columns=["Countries", "Traveled"],
        key_on="feature.properties.name",
        fill_color="RdYlGn",
        fill_opacity=0.8,
        line_opacity=0.3,
        nan_fill_color="white",
    ).add_to(m)

    m.save("tmp/traveled.html")
    path = "tmp/traveled.html"
    new_path = os.path.join(settings.MEDIA_ROOT, path)
    
    if os.path.exists(new_path):
        with open(new_path, 'rb') as f:
            try:
                response = HttpResponse(f)
                response['content_type'] = "application/octet-stream"
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(new_path)
                return response
            except Exception:
                raise Http404

    return redirect('index')