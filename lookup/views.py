from django.shortcuts import render

# Create your views here.
def method(request):
    import json
    import requests

    if request.method=='POST':
        zipcode=request.POST['zipcode']
        api_request=requests.get("https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode="+zipcode+"&distance=25&API_KEY=A8CBE33D-12E2-4D5B-8910-FD6F1CB94AC1")

        try:
            api=json.loads(api_request.content)


            if api[0]['Category']['Name'] == 'Good':
                cat_desc='Air quality is satisfactory, and air pollution poses little or no risk.'
                cat_col='green'

            elif api[0]['Category']['Name'] == 'Moderate':
                cat_desc='Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution.'
                cat_col='yellow'

            elif api[0]['Category']['Name'] == 'Unhealthy for Sensitive Groups' :
                cat_desc='Members of sensitive groups may experience health effects. The general public is less likely to be affected.'
                cat_col='orange'

            elif api[0]['Category']['Name'] == 'Unhealthy':
                cat_desc='Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects.'
                cat_col='red'

            elif api[0]['Category']['Name'] == 'Very Unhealthy' :
                cat_desc='Health alert: The risk of health effects is increased for everyone.'
                cat_col='violet'

            elif api[0]['Category']['Name'] == 'Hazardous' :
                cat_desc='Health warning of emergency conditions: everyone is more likely to be affected.'
                cat_col='maroon'

        except Exception as E:
            api="error..."
            cat_desc='none'
            cat_col='none'
        
        return render(request, 'lookup/basic.html', {'api':api, 'cat_desc':cat_desc, 'cat_col':cat_col})
    else:
        return render(request, 'lookup/basic.html')


def about(request):
    import json
    from geopy.geocoders import Nominatim
    from urllib.request import urlopen
    
    weather_api_key="a87fe8c39cbf4632490fdaa7e66cf6ca"

    address="vellore"
    
    geoloc=Nominatim(user_agent='phk16weather')

    location=geoloc.geocode("poigai vellore")

    
    try:
        api=location.raw
        lat=location.latitude
        lon=location.longitude
        url1="https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(lat, lon, weather_api_key)
        
        respons=urlopen(url1)
        seq=json.load(respons)
    except Exception as E:
        seq=E
    return render(request, 'lookup/about.html', {'api':seq})