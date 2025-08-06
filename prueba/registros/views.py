from django.shortcuts import render, redirect

from .forms import ComentarioContactoForm, FormArchivos
from .models import Alumnos, ComentarioContacto, Archivos
from django.shortcuts import get_object_or_404
from django.contrib import messages
import datetime

# Create your views here.
#Accedemos al modelo Alumnos que contiene la estructura de la tabla.
def registros(request):
    alumnos=Alumnos.objects.all()
#all recupera todos los objetos del modelo (registros de la tabla alumnos)
    return render(request,"registros/principal.html",{'alumnos':alumnos})
#Indicamos el lugar donde se renderizará el resultado de esta vista y enviamos la lista de alumnos recuparados

def registrar(request):
    if request.method == 'POST':
        form = ComentarioContactoForm(request.POST)
        if form.is_valid(): #Si los datos recibidos son correctos

            form.save() #inserta
            return redirect('Comentarios')

    form = ComentarioContactoForm()
    #Si algo sale mal se reenvian al formulario los datos ingresados
    return render(request,'registros/contacto.html',{'form': form})

def contacto(request):
    return render(request,"registros/contacto.html")
#Indicamos el lugar donde se renderizará el resultado de esta vista

#Accedemos al modelo Comentarios que contiene la estructura de la tabla.
def comentarios(request):
    comentarios=ComentarioContacto.objects.all()
#all recupera todos los objetos del modelo (registros de la tabla alumnos)
    return render(request,"registros/comentarios.html",{'comentarios':comentarios})
#Indicamos el lugar donde se renderizará el resultado de esta vista y enviamos la lista de alumnos recuparados

def eliminarComentarioContacto(request, id, confirmacion='registros/confirmarEliminacion.html'):
    comentario = get_object_or_404(ComentarioContacto, id=id)
    if request.method=='POST':
        comentario.delete()
        comentarios=ComentarioContacto.objects.all()
        return render(request,"registros/comentarios.html",{'comentarios':comentarios})

    return render(request, confirmacion, {'object':comentario})

def consultarComentarioIndividual(request, id):
    comentario=ComentarioContacto.objects.get(id=id)
    #get permite establecer una condicionante a la consulta y recupera el objetos
    #del modelo que cumple la condición (registro de la tabla ComentariosContacto.
    #get se emplea cuando se sabe que solo hay un objeto que coincide con su
    #consulta.
    return render(request,"registros/formEditarComentario.html",{'comentario':comentario})
    #Indicamos el lugar donde se renderizará el resultado de esta vista
    # y enviamos la lista de alumnos recuparados.
    
def editarComentarioContacto(request, id):
    comentario = get_object_or_404(ComentarioContacto, id=id)
    form = ComentarioContactoForm(request.POST, instance=comentario)
    #Referenciamos que el elemento del formulario pertenece al comentario
    # ya existente
    if form.is_valid():
        form.save() #si el registro ya existe, se modifica.
        comentarios=ComentarioContacto.objects.all()
        return render(request,"registros/comentarios.html",{'comentarios':comentarios})
    #Si el formulario no es valido nos regresa al formulario para verificar
    #datos
    return render(request,"registros/formEditarComentario.html",{'comentario':comentario})

#filter nos retornara los registros que coinciden con los parametros de #busqueda de datos
def consultas1(request):
    #Con una sola condicion
    alumnos=Alumnos.objects.filter(carrera="TI")
    return render(request, "registros/consultas.html", {'alumnos':alumnos})

def consultas2(request):
    #Con Dos sola condicion
    alumnos=Alumnos.objects.filter(carrera="TI").filter(turno="Matutino")
    return render(request, "registros/consultas.html", {'alumnos':alumnos})

def consultas3(request):
    #Si solo deseamos recuperar ciertos datos agregamos la funcion only,
    #listando los campos que queremos de la consulta emplear filter() o en el ejemplo all()
    alumnos=Alumnos.objects.all().only("matricula", "nombre", "carrera", "turno", "imagen")
    return render(request, "registros/consultas.html", {'alumnos':alumnos})

def consultas4(request):
    #Con una sola condicion
    alumnos=Alumnos.objects.filter(turno__contains="Vesp")
    return render(request, "registros/consultas.html", {'alumnos':alumnos})

def consultas5(request):
    #Con una sola condicion
    alumnos=Alumnos.objects.filter(nombre__in=["Juan", "Ana"])
    return render(request, "registros/consultas.html", {'alumnos':alumnos})

def consultas6(request):
    #Con una sola condicion
    fechaInicio = datetime.date(2025,6,20)
    fechaFin = datetime.date(2025,7,10)
    alumnos=Alumnos.objects.filter(created__range=(fechaInicio, fechaFin))
    return render(request, "registros/consultas.html", {'alumnos':alumnos})

def consultas7(request):
    #Con una sola condicion
    fechaInicio = datetime.date(2025,7,8)
    fechaFin = datetime.date(2025,7,9)
    comentarios=ComentarioContacto.objects.filter(created__range=(fechaInicio, fechaFin))
    return render(request, "registros/comentarios.html", {'comentarios':comentarios})

def consultas8(request):
    #Con una sola condicion
    comentarios=ComentarioContacto.objects.filter(mensaje__startswith=("as"))
    return render(request, "registros/comentarios.html", {'comentarios':comentarios})

def consultas9(request):
    #Con una sola condicion
    comentarios=ComentarioContacto.objects.filter(usuario__exact=("PACO"))
    return render(request, "registros/comentarios.html", {'comentarios':comentarios})

def consultas10(request):
    #Con una sola condicion
    comentarios=ComentarioContacto.objects.only("mensaje")
    return render(request, "registros/comentarios.html", {'comentarios':comentarios})

def consultas11(request):
    #Con una sola condicion
    comentarios=ComentarioContacto.objects.filter(mensaje__endswith=("MAN"))
    return render(request, "registros/comentarios.html", {'comentarios':comentarios})

def archivos(request):
    if request.method == 'POST':
        form = FormArchivos(request.POST, request.FILES)
        if form.is_valid():
            titulo = request.POST['titulo']
            descripcion = request.POST['descripcion']
            archivo = request.FILES['archivo']
            insert = Archivos(titulo=titulo, descripcion=descripcion,
            archivo=archivo)
            insert.save()
            return render(request,"registros/archivos.html")
        else:

            messages.error(request, "Error al procesar el formulario")

    else:
        return render(request,"registros/archivos.html",{'archivo':Archivos})
def consultasSQL(request):
    alumnos=Alumnos.objects.raw('SELECT id, matricula,nombre, carrera, turno, imagen FROM registros_alumnos WHERE carrera="TI" ORDER BY turno DESC')
    return render(request,"registros/consultas.html", {'alumnos':alumnos})