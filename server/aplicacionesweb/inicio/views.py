from django.shortcuts import render_to_response, HttpResponse
from models import Anuncio

def inicio(request,protegido=False):
    anuncios=Anuncio.objects.all()
    if protegido:
        return render_to_response('inicio.html', {
            'protegido':True,
            'texto':'Navegacion protegida por kerberus',
            'anuncios':anuncios,
            })
    else:
        return render_to_response('inicio.html', {
            'protegido':False,
            'texto':'No esta protegido',
            'anuncios':anuncios,
            })

def sitioDenegado(request,url=""):
    url="http://www.google2.com"
    return render_to_response('sitioDenegado.html', locals())

def hello(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))
