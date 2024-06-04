# users/pipeline.py

def save_mobile_number(backend, user, response, *args, **kwargs):
    request = kwargs.get('request')
    if request and 'mobile_number' in request.session:
        user.phone_number = request.session['mobile_number']
        user.save()
        del request.session['mobile_number']
