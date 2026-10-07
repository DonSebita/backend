from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms

from courses.models import Course, Area
from enrollments.models import Order, Cart, CartItem
from users.models import User
from users.forms import UsuarioForm
from enrollments.models import Order

def error_404_view(request, exception=None):
    return render(request, '404.html', status=404)

# ─── Contexto compartido del footer ──────────────────────────────────────────
FOOTER = {
    'nombre': 'Sebastian Lucas Eduardo Sandoval',
    'seccion': 'Sección 1',
}


# ─── Formularios simples ──────────────────────────────────────────────────────

User = get_user_model()

class InstructorChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class CourseForm(forms.ModelForm):
    # 2. Clases de Tailwind inyectadas directamente al Select nativo
    instructor = InstructorChoiceField(
        queryset=User.objects.filter(role__in=['INSTRUCTOR', 'COORDINATOR']),
        empty_label="Seleccione un profesor...",
        label="Instructor asignado",
        widget=forms.Select(attrs={
            'class': 'w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2.5 text-white outline-none focus:border-indigo-500 cursor-pointer'
        })
    )

    class Meta:
        model = Course
        fields = ['title', 'description', 'instructor', 'enrollment_cost', 'start_date', 'end_date', 'max_capacity', 'area']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['name', 'description']

class InstructorForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False,
        label="Contraseña",
        help_text="Déjala vacía para mantener la contraseña actual."
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)

        # Siempre será instructor
        user.role = User.Role.INSTRUCTOR

        # Solo cambia la contraseña si se escribió una nueva
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user

# ─── PÚBLICAS ─────────────────────────────────────────────────────────────────

def index(request):
    """Página de inicio."""

    areas = Area.objects.all()

    # Curso destacado:
    # toma el último curso creado.
    curso_destacado = Course.objects.select_related(
        'instructor'
    ).order_by('-id').first()

    return render(request, 'index.html', {
        'areas': areas,
        'curso_destacado': curso_destacado,
        **FOOTER,
    })

def lista_cursos(request):

    courses = Course.objects.all()
    areas = Area.objects.all().order_by('name')

    # BUSCAR
    buscar = request.GET.get('buscar', '').strip()

    if buscar:
        courses = courses.filter(
            title__icontains=buscar
        )

    # FILTRAR POR ÁREA
    area = request.GET.get('area', '')

    if area:
        courses = courses.filter(
            area_id=area
        )

    # ORDENAR
    orden = request.GET.get('orden', '')

    if orden == 'precio_menor':
        courses = courses.order_by('enrollment_cost')

    elif orden == 'precio_mayor':
        courses = courses.order_by('-enrollment_cost')

    elif orden == 'recientes':
        courses = courses.order_by('-id')

    else:
        courses = courses.order_by('-id')

    return render(
        request,
        'cursos/lista.html',
        {
            'courses': courses,
            'areas': areas,
            'buscar': buscar,
        }
    )

    courses = Course.objects.all()
    areas = Area.objects.all().order_by('name')

    # Buscar
    buscar = request.GET.get('buscar', '').strip()

    if buscar:
        courses = courses.filter(
            title__icontains=buscar
        )

    # Área
    area = request.GET.get('area', '')

    if area:
        courses = courses.filter(
            area_id=area
        )

    area_seleccionada = int(area) if area.isdigit() else None

    # Orden
    orden = request.GET.get('orden', '')

    if orden == 'precio_menor':
        courses = courses.order_by('enrollment_cost')

    elif orden == 'precio_mayor':
        courses = courses.order_by('-enrollment_cost')

    elif orden == 'recientes':
        courses = courses.order_by('-id')

    else:
        courses = courses.order_by('-id')

    return render(
        request,
        'cursos/lista.html',
        {
            'courses': courses,
            'areas': areas,
            'area_seleccionada': area_seleccionada,
            'buscar': buscar,
            'orden_seleccionado': orden,
        }
    )

    courses = Course.objects.all()
    areas = Area.objects.all().order_by('name')

    # Buscar
    buscar = request.GET.get('buscar', '').strip()

    if buscar:
        courses = courses.filter(
            title__icontains=buscar
        )

    # Área
    area = request.GET.get('area', '')

    if area:
        courses = courses.filter(
            area_id=area
        )

    # Orden
    orden = request.GET.get('orden', '')

    if orden == 'precio_menor':
        courses = courses.order_by('enrollment_cost')

    elif orden == 'precio_mayor':
        courses = courses.order_by('-enrollment_cost')

    elif orden == 'recientes':
        courses = courses.order_by('-id')

    else:
        courses = courses.order_by('-id')

    return render(
        request,
        'cursos/lista.html',
        {
            'courses': courses,
            'areas': areas,
            'area_seleccionada': area,
            'buscar': buscar,
            'orden_seleccionado': orden,
        }
    )

    courses = Course.objects.all()
    areas = Area.objects.all().order_by('name')

    # -------------------------
    # BUSCAR
    # -------------------------

    buscar = request.GET.get('buscar', '').strip()

    if buscar:
        courses = courses.filter(
            title__icontains=buscar
        )


    # -------------------------
    # FILTRAR POR ÁREA
    # -------------------------

    area = request.GET.get('area', '')

    if area:
        courses = courses.filter(area_id=area)

    area_seleccionada = int(area) if area.isdigit() else None


    # -------------------------
    # ORDENAR
    # -------------------------

    orden = request.GET.get('orden', '')

    if orden == 'precio_menor':
        courses = courses.order_by('enrollment_cost')

    elif orden == 'precio_mayor':
        courses = courses.order_by('-enrollment_cost')

    else:
        # Últimos cursos agregados
        courses = courses.order_by('-id')


    return render(
        request,
        'cursos/lista.html',
        {
            'courses': courses,
            'areas': areas,
        }
    )

def login_view(request):
    """Inicio de sesión. Redirige al panel correspondiente según el rol."""
    if request.user.is_authenticated:
        return _redirect_by_role(request.user)

    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            return _redirect_by_role(user)
        messages.error(request, 'Credenciales inválidas')

    return render(request, 'login.html', FOOTER)


def register_view(request):
    """Registro de nuevos estudiantes."""
    if request.user.is_authenticated:
        return redirect('estudiante_dashboard')

    if request.method == 'POST':
        u = request.POST.get('username', '').strip()
        e = request.POST.get('email', '').strip()
        p = request.POST.get('password', '')

        if not u or not e or not p:
            messages.error(request, 'Completa todos los campos')
        elif User.objects.filter(username=u).exists():
            messages.error(request, 'El usuario ya existe')
        elif User.objects.filter(email=e).exists():
            messages.error(request, 'El correo ya está registrado')
        else:
            user = User.objects.create_user(username=u, email=e, password=p, role='STUDENT')
            login(request, user)
            return redirect('estudiante_dashboard')

    return render(request, 'register.html', FOOTER)


def logout_view(request):
    """Cierra sesión y redirige al home."""
    logout(request)
    return redirect('index')


def _redirect_by_role(user):
    """Helper: redirige al panel correcto según rol."""
    if user.is_staff or user.is_superuser or getattr(user, 'role', '') == 'COORDINATOR':
        return redirect('admin_dashboard')
    return redirect('estudiante_dashboard')


# ─── PANEL ESTUDIANTE ─────────────────────────────────────────────────────────

@login_required(login_url='/login/')
def estudiante_dashboard(request):
    """Panel principal del estudiante: muestra sus cursos pagados."""
    paid_orders = (
        Order.objects
        .filter(user=request.user, status='PAGADO')
        .prefetch_related('items__course')
    )
    # Deduplicar cursos conservando orden
    seen = set()
    courses = []
    for order in paid_orders:
        for item in order.items.all():
            if item.course.id not in seen:
                seen.add(item.course.id)
                courses.append(item.course)

    return render(request, 'estudiante/dashboard.html', {
        'courses': courses,
        **FOOTER,
    })


@login_required(login_url='/login/')
def estudiante_perfil(request):
    """Perfil del estudiante."""
    return render(request, 'estudiante/perfil.html', {
        'usuario': request.user,
        **FOOTER,
    })


@login_required(login_url='/login/')
def estudiante_carrito(request):
    """Carrito de compras del estudiante (vista HTML)."""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('course').all()
    total = sum(item.course.enrollment_cost for item in items)
    return render(request, 'estudiante/carrito.html', {
        'items': items,
        'total': total,
        **FOOTER,
    })


@login_required(login_url='/login/')
def carrito_agregar(request, course_id):
    """Agrega un curso al carrito desde la vista HTML."""
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        if not CartItem.objects.filter(cart=cart, course=course).exists():
            CartItem.objects.create(cart=cart, course=course)
            messages.success(request, f'"{course.title}" añadido al carrito.')
        else:
            messages.info(request, 'Ese curso ya está en tu carrito.')
    return redirect('index')


@login_required(login_url='/login/')
def carrito_eliminar(request, item_id):
    """Elimina un ítem del carrito (vista HTML)."""
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, 'Curso eliminado del carrito.')
    return redirect('estudiante_carrito')


@login_required(login_url='/login/')
def checkout_html(request):
    """Procesa el pago del carrito (lógica atómica delegada al API)."""
    import requests as http_requests
    from rest_framework_simplejwt.tokens import RefreshToken

    if request.method == 'POST':
        # Generamos un token JWT para llamar nuestra propia API
        token = RefreshToken.for_user(request.user).access_token
        resp = http_requests.post(
            request.build_absolute_uri('/api/ordenes/checkout/'),
            headers={'Authorization': f'Bearer {token}'},
        )
        if resp.status_code == 201:
            messages.success(request, '¡Pago realizado exitosamente!')
            return redirect('estudiante_dashboard')
        else:
            data = resp.json()
            messages.error(request, data.get('error', 'Error al procesar el pago.'))
    return redirect('estudiante_carrito')


# ─── PANEL ADMINISTRADOR ──────────────────────────────────────────────────────

def _require_coordinator(request):
    """Devuelve True si tiene acceso de coordinador/admin, False si debe ser rechazado."""
    return request.user.is_authenticated and (
        request.user.is_staff
        or request.user.is_superuser
        or getattr(request.user, 'role', '') == 'COORDINATOR'
    )


@login_required(login_url='/login/')
def admin_dashboard(request):
    """Panel principal del administrador/coordinador con estadísticas."""
    if not _require_coordinator(request):
        messages.error(request, 'Acceso denegado.')
        return redirect('estudiante_dashboard')

    from django.db.models import Sum
    total_sales = (
        Order.objects
        .filter(status='PAGADO')
        .aggregate(total=Sum('items__price_at_purchase'))['total'] or 0
    )

    return render(request, 'admin/dashboard.html', {
        'total_courses': Course.objects.count(),
        'total_users':   User.objects.count(),
        'total_orders':  Order.objects.count(),
        'total_sales':   total_sales,
        **FOOTER,
    })


@login_required(login_url='/login/')
def admin_cursos(request):
    """Lista de todos los cursos para el panel admin."""
    if not _require_coordinator(request):
        return redirect('index')

    courses = Course.objects.select_related('area').all()
    return render(request, 'admin/cursos.html', {'courses': courses, **FOOTER})


@login_required(login_url='/login/')
def admin_curso_nuevo(request):
    """Formulario para crear un curso nuevo."""
    if not _require_coordinator(request):
        return redirect('index')

    form = CourseForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Curso creado correctamente.')
        return redirect('admin_cursos')

    return render(request, 'admin/curso_form.html', {
        'form': form, 'accion': 'Crear curso', **FOOTER
    })


@login_required(login_url='/login/')
def admin_curso_editar(request, pk):
    """Formulario para editar un curso existente."""
    if not _require_coordinator(request):
        return redirect('index')

    course = get_object_or_404(Course, pk=pk)
    form = CourseForm(request.POST or None, instance=course)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Curso actualizado.')
        return redirect('admin_cursos')

    return render(request, 'admin/curso_form.html', {
        'form': form, 'accion': 'Editar curso', **FOOTER
    })


@login_required(login_url='/login/')
def admin_curso_eliminar(request, pk):
    """Elimina un curso (requiere confirmación POST)."""
    if not _require_coordinator(request):
        return redirect('index')

    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Curso eliminado.')
        return redirect('admin_cursos')

    return render(request, 'admin/curso_confirm_delete.html', {
        'course': course, **FOOTER
    })


@login_required(login_url='/login/')
def admin_areas(request):
    """Lista de áreas."""
    if not _require_coordinator(request):
        return redirect('index')

    areas = Area.objects.all()
    return render(request, 'admin/areas.html', {'areas': areas, **FOOTER})


@login_required(login_url='/login/')
def admin_area_nueva(request):
    """Crear un área nueva."""
    if not _require_coordinator(request):
        return redirect('index')

    form = AreaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Área creada.')
        return redirect('admin_areas')

    return render(request, 'admin/area_form.html', {
        'form': form, 'accion': 'Crear área', **FOOTER
    })


@login_required(login_url='/login/')
def admin_area_editar(request, pk):
    """Editar un área."""
    if not _require_coordinator(request):
        return redirect('index')

    area = get_object_or_404(Area, pk=pk)
    form = AreaForm(request.POST or None, instance=area)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Área actualizada.')
        return redirect('admin_areas')

    return render(request, 'admin/area_form.html', {
        'form': form, 'accion': 'Editar área', **FOOTER
    })


@login_required(login_url='/login/')
def admin_area_eliminar(request, pk):
    """Eliminar un área."""
    if not _require_coordinator(request):
        return redirect('index')

    area = get_object_or_404(Area, pk=pk)
    if request.method == 'POST':
        area.delete()
        messages.success(request, 'Área eliminada.')
        return redirect('admin_areas')

    return render(request, 'admin/area_confirm_delete.html', {
        'area': area, **FOOTER
    })


@login_required(login_url='/login/')
def admin_usuarios(request):
    """Lista de todos los usuarios."""
    if not _require_coordinator(request):
        return redirect('index')

    usuarios = User.objects.all().order_by('-date_joined')
    return render(request, 'admin/usuarios.html', {'usuarios': usuarios, **FOOTER})


@login_required(login_url='/login/')
def admin_ordenes(request):
    """Lista de todas las órdenes."""
    if not _require_coordinator(request):
        return redirect('index')

    ordenes = Order.objects.select_related('user').prefetch_related('items__course').order_by('-created_at')
    return render(request, 'admin/ordenes.html', {'ordenes': ordenes, **FOOTER})

@login_required(login_url='/login/')
def admin_instructores(request):
    """Lista de instructores filtrada por rol."""
    if not _require_coordinator(request):
        return redirect('index')

    instructores = User.objects.filter(role='INSTRUCTOR').order_by('-date_joined')
    return render(request, 'admin/instructores.html', {'instructores': instructores, **FOOTER})

@login_required(login_url='/login/')
def admin_instructor_nuevo(request):
    """Crea un instructor nuevo."""
    if not _require_coordinator(request):
        return redirect('index')

    form = InstructorForm(request.POST or None)
    form.fields['password'].required = True # La clave es obligatoria al crear
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Instructor creado correctamente.')
        return redirect('admin_instructores')

    return render(request, 'admin/instructor_form.html', {
        'form': form, 'accion': 'Añadir instructor', **FOOTER
    })

@login_required(login_url='/login/')
def admin_instructor_editar(request, pk):
    if not _require_coordinator(request):
        return redirect('index')

    instructor = get_object_or_404(
        User,
        pk=pk,
        role=User.Role.INSTRUCTOR
    )

    form = InstructorForm(
        request.POST or None,
        instance=instructor
    )

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(
            request,
            'Instructor actualizado correctamente.'
        )
        return redirect('admin_instructores')

    return render(request, 'admin/instructor_form.html', {
        'form': form,
        'accion': 'Editar instructor',
        **FOOTER
    })
@login_required(login_url='/login/')
def admin_instructor_eliminar(request, pk):
    if not _require_coordinator(request):
        return redirect('index')

    instructor = get_object_or_404(
        User,
        pk=pk,
        role=User.Role.INSTRUCTOR
    )

    if request.method == 'POST':
        instructor.delete()

        messages.success(
            request,
            'Instructor eliminado correctamente.'
        )

        return redirect('admin_instructores')

    return render(request, 'admin/instructor_eliminar.html', {
        'instructor': instructor,
        **FOOTER
    })

@login_required
def checkout_html(request):

    cart = Cart.objects.filter(
        user=request.user
    ).prefetch_related(
        'items__course'
    ).first()

    if not cart or not cart.items.exists():
        return redirect('estudiante_carrito')

    total = sum(
        item.course.enrollment_cost
        for item in cart.items.all()
    )

    context = {
        'cart': cart,
        'total': total,
    }

    return render(
        request,
        'estudiante/checkout.html',
        context
    )

@login_required
def admin_usuarios(request):

    usuarios = User.objects.all().order_by('-date_joined')

    return render(
        request,
        'admin/usuarios.html',
        {
            'usuarios': usuarios
        }
    )

@login_required
def admin_usuario_nuevo(request):

    if not request.user.is_superuser:
        return redirect('admin_dashboard')

    if request.method == 'POST':

        form = UsuarioForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('admin_usuarios')

    else:

        form = UsuarioForm()

    return render(
        request,
        'admin/usuario_form.html',
        {
            'form': form,
            'accion': 'Nuevo usuario'
        }
    )

@login_required
def admin_usuario_editar(request, pk):

    if not request.user.is_superuser:
        return redirect('admin_dashboard')

    usuario = get_object_or_404(User, pk=pk)

    if request.method == 'POST':

        form = UsuarioForm(
            request.POST,
            instance=usuario
        )

        if form.is_valid():

            form.save()

            return redirect('admin_usuarios')

    else:

        form = UsuarioForm(
            instance=usuario
        )

    return render(
        request,
        'admin/usuario_form.html',
        {
            'form': form,
            'accion': 'Editar usuario',
            'usuario': usuario
        }
    )

@login_required
def admin_usuario_eliminar(request, pk):

    if not request.user.is_superuser:
        return redirect('admin_dashboard')

    usuario = get_object_or_404(User, pk=pk)

    if usuario == request.user:
        return redirect('admin_usuarios')

    if request.method == 'POST':

        usuario.delete()

        return redirect('admin_usuarios')

    return render(
        request,
        'admin/usuarios_eliminar.html',
        {
            'usuario': usuario
        }
    )

@login_required
def estudiante_mis_cursos(request):

    ordenes = Order.objects.filter(
        user=request.user
    ).prefetch_related(
        'items__course'
    ).order_by('-created_at')

    return render(
        request,
        'estudiante/mis_cursos.html',
        {
            'ordenes': ordenes
        }
    )