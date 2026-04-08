import json
from datetime import datetime, timedelta
from pathlib import Path

from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

PROJECT_ROOT = Path(settings.BASE_DIR).parent
TEMPLATES_DIR = Path(settings.BASE_DIR) / 'templates'
DATA_DIR = Path(settings.BASE_DIR) / 'data'
USERS_FILE = DATA_DIR / 'users.txt'
USERS_JSON_FILE = DATA_DIR / 'users.json'
PRODUCTS_FILE = DATA_DIR / 'products.json'
PRODUCT_LOG_FILE = DATA_DIR / 'products.txt'
COMPARE_LOG_FILE = DATA_DIR / 'compare_logs.txt'
ORDERS_FILE = DATA_DIR / 'orders.json'
SECURITY_FILE = DATA_DIR / 'security.json'
SECURITY_LOG_FILE = DATA_DIR / 'security_events.txt'
ADMIN_EMAIL = 'ozodbek201024@gmail.com'
ADMIN_PASSWORD_HASH = (
    'pbkdf2_sha256$1200000$XlZdjzCykKKEBIZjiFNnFv$4/po+SIkpTCHEv4z0ga/fWCHX/gEAz+2ZrGwx9scOy4='
)
ADMIN_SESSION_KEY = 'marketly_admin'
ADMIN_SESSION_TIMEOUT_MINUTES = 30
MAX_ADMIN_LOGIN_ATTEMPTS = 5
ADMIN_LOGIN_LOCKOUT_MINUTES = 15
ADMIN_TEMPLATES = {'admin-panel.html', 'admin-security.html', 'manager-panel.html'}
ADMIN_SECURITY_TOPICS = [
    {
        'title': 'Dasturlash',
        'items': ['Python', 'C++', 'JavaScript'],
        'summary': "Backend servislar, avtomatlashtirish va audit skriptlarini yozish uchun asosiy tillar.",
    },
    {
        'title': 'Tarmoq asoslari',
        'items': ['TCP/IP', 'Firewalls', 'VPN'],
        'summary': "So'rovlar oqimini boshqarish, kirishni filtrlash va himoyalangan ulanish qurish uchun kerak.",
    },
    {
        'title': 'Operatsion tizimlar',
        'items': ['Linux', 'Windows Server'],
        'summary': "Server sozlamalari, servislar va loglarni nazorat qilishning tayanch muhiti.",
    },
    {
        'title': 'Kriptografiya',
        'items': ["Ma'lumotlarni shifrlash", 'Hashlash', 'Token himoyasi'],
        'summary': "Parollar, sessiyalar va maxfiy ma'lumotlarni xavfsiz saqlash uchun ishlatiladi.",
    },
    {
        'title': 'Xavfsizlik vositalari',
        'items': ['IDS/IPS', 'SIEM', 'Antivirus', 'Penetration testing'],
        'summary': "Tahdidlarni erta aniqlash, hodisalarni tahlil qilish va zaif joylarni topishga yordam beradi.",
    },
]
ADMIN_LOGIN_ATTEMPTS = {}


def page_view(request, template_name):
    if template_name in ADMIN_TEMPLATES and not _is_admin(request):
        return redirect('login')

    template_path = TEMPLATES_DIR / template_name
    if not template_path.exists():
        raise Http404(f'{template_name} topilmadi')
    return render(request, template_name)


def _now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def _append_text(file_path, content):
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open('a', encoding='utf-8') as file_obj:
        file_obj.write(content)


def _load_json_body(request):
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return {}


def _read_products():
    if not PRODUCTS_FILE.exists() or PRODUCTS_FILE.stat().st_size == 0:
        return []
    try:
        return json.loads(PRODUCTS_FILE.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return []


def _safe_int(value):
    try:
        digits = ''.join(ch for ch in str(value) if ch.isdigit())
        return int(digits) if digits else 0
    except (TypeError, ValueError):
        return 0


def _parse_product_datetime(value):
    try:
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    except (TypeError, ValueError):
        return None


def _write_products(products):
    PRODUCTS_FILE.write_text(
        json.dumps(products, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )


def _read_orders():
    if not ORDERS_FILE.exists() or ORDERS_FILE.stat().st_size == 0:
        return []
    try:
        data = json.loads(ORDERS_FILE.read_text(encoding='utf-8'))
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def _write_orders(orders):
    ORDERS_FILE.write_text(
        json.dumps(orders, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )


def _read_users():
    if USERS_JSON_FILE.exists() and USERS_JSON_FILE.stat().st_size > 0:
        try:
            data = json.loads(USERS_JSON_FILE.read_text(encoding='utf-8'))
            if isinstance(data, list):
                return data
        except json.JSONDecodeError:
            pass
    return []


def _write_users(users):
    USERS_JSON_FILE.write_text(
        json.dumps(users, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )


def _read_security_settings():
    if SECURITY_FILE.exists() and SECURITY_FILE.stat().st_size > 0:
        try:
            data = json.loads(SECURITY_FILE.read_text(encoding='utf-8'))
            return {
                'enabled': bool(data.get('enabled', True)),
                'updatedAt': data.get('updatedAt', ''),
                'updatedBy': data.get('updatedBy', 'Admin'),
            }
        except json.JSONDecodeError:
            pass

    return {
        'enabled': True,
        'updatedAt': '',
        'updatedBy': 'Admin',
    }


def _write_security_settings(enabled, updated_by='Admin'):
    SECURITY_FILE.write_text(
        json.dumps(
            {
                'enabled': bool(enabled),
                'updatedAt': _now(),
                'updatedBy': updated_by,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding='utf-8',
    )


def _read_security_events(limit=20):
    if not SECURITY_LOG_FILE.exists() or SECURITY_LOG_FILE.stat().st_size == 0:
        return []

    lines = [line.strip() for line in SECURITY_LOG_FILE.read_text(encoding='utf-8').splitlines() if line.strip()]
    return list(reversed(lines[-limit:]))


def _log_security_event(event_type, message, actor='System'):
    _append_text(SECURITY_LOG_FILE, f'[{_now()}] [{event_type}] [{actor}] {message}\n')


def _upsert_user(user_data):
    users = _read_users()
    email = user_data.get('email', '').strip().lower()
    if not email:
        return

    existing_index = next(
        (index for index, user in enumerate(users) if user.get('email', '').strip().lower() == email),
        None,
    )

    if existing_index is None:
        users.append(user_data)
    else:
        users[existing_index] = {**users[existing_index], **user_data}

    _write_users(users)


def _serialize_user(data):
    return {
        'firstname': data.get('firstname', ''),
        'lastname': data.get('lastname', ''),
        'age': data.get('age', ''),
        'birthYear': data.get('birthYear', ''),
        'phone': data.get('phone', ''),
        'email': data.get('email', ''),
        'role': data.get('role', ''),
        'isRegistered': bool(data.get('isRegistered', False)),
        'savedAt': _now(),
    }


def _client_ip(request):
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', 'unknown')


def _is_admin(request):
    admin_session = request.session.get(ADMIN_SESSION_KEY, {})
    if admin_session.get('email') != ADMIN_EMAIL:
        return False

    logged_in_at = admin_session.get('loggedInAt', '')
    try:
        logged_in_time = datetime.strptime(logged_in_at, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        request.session.pop(ADMIN_SESSION_KEY, None)
        return False

    if datetime.now() - logged_in_time > timedelta(minutes=ADMIN_SESSION_TIMEOUT_MINUTES):
        request.session.pop(ADMIN_SESSION_KEY, None)
        return False

    return True


def _cleanup_login_attempts():
    cutoff = datetime.now() - timedelta(minutes=ADMIN_LOGIN_LOCKOUT_MINUTES)
    expired_keys = []
    for key, value in ADMIN_LOGIN_ATTEMPTS.items():
        if value.get('last_attempt') and value['last_attempt'] < cutoff:
            expired_keys.append(key)

    for key in expired_keys:
        ADMIN_LOGIN_ATTEMPTS.pop(key, None)


def _track_login_failure(key):
    _cleanup_login_attempts()
    record = ADMIN_LOGIN_ATTEMPTS.get(key, {'count': 0})
    record['count'] += 1
    record['last_attempt'] = datetime.now()
    ADMIN_LOGIN_ATTEMPTS[key] = record
    return record


def _clear_login_failures(key):
    ADMIN_LOGIN_ATTEMPTS.pop(key, None)


def _remaining_lockout_minutes(record):
    last_attempt = record.get('last_attempt')
    if not last_attempt:
        return 0

    unlock_time = last_attempt + timedelta(minutes=ADMIN_LOGIN_LOCKOUT_MINUTES)
    delta = unlock_time - datetime.now()
    if delta.total_seconds() <= 0:
        return 0

    full_minutes = int(delta.total_seconds() // 60)
    return full_minutes if delta.total_seconds() % 60 == 0 else full_minutes + 1


def _get_admin_security_payload():
    security = _read_security_settings()
    return {
        'security': {
            **security,
            'protections': [
                'Xavfsizlik headerlari',
                'Iframe bloklash',
                "Shubhali so'rovlarni filtrlash",
                'Cookie himoyasi',
                'Admin login rate limit',
                'Session timeout',
            ],
        },
        'securityTopics': ADMIN_SECURITY_TOPICS,
        'recentEvents': _read_security_events(),
        'recommendations': [
            'Admin parolini muntazam yangilang va brauzerda saqlamang.',
            'VPN yoki ishonchli tarmoq orqali admin panelga kiring.',
            'IDS/IPS va SIEM loglarini haftalik tekshirib boring.',
            'Penetration testing hamda dependency audit ni reja asosida bajaring.',
        ],
    }


def _serialize_manager_product(product):
    sold_count = _safe_int(product.get('soldCount', 0))
    price_value = _safe_int(product.get('price', 0))
    return {
        'id': product.get('id'),
        'name': product.get('title') or product.get('productName') or '-',
        'price': product.get('price', '0'),
        'priceValue': price_value,
        'category': product.get('category') or 'Boshqa',
        'soldCount': sold_count,
        'uploadedAt': product.get('createdAt', '-'),
        'revenueValue': sold_count * price_value,
    }


def _get_manager_payload(search_query=''):
    now = datetime.now()
    normalized_query = search_query.strip().lower()
    raw_products = _read_products()
    raw_orders = _read_orders()
    sold_by_product = {}

    for order in raw_orders:
        product_id = order.get('productId')
        sold_by_product[product_id] = sold_by_product.get(product_id, 0) + _safe_int(order.get('quantity', 1))

    products = []
    for product in raw_products:
        serialized = _serialize_manager_product(product)
        serialized['soldCount'] = sold_by_product.get(product.get('id'), 0)
        serialized['revenueValue'] = serialized['soldCount'] * serialized['priceValue']
        products.append(serialized)

    if normalized_query:
        filtered_products = [
            product
            for product in products
            if normalized_query in product['name'].lower() or normalized_query in product['category'].lower()
        ]
    else:
        filtered_products = products

    monthly_uploaded = 0
    monthly_sold = 0
    monthly_revenue = 0

    for raw_product in raw_products:
        product_time = _parse_product_datetime(raw_product.get('createdAt'))
        if product_time and product_time.year == now.year and product_time.month == now.month:
            monthly_uploaded += 1

    for order in raw_orders:
        order_time = _parse_product_datetime(order.get('createdAt'))
        if order_time and order_time.year == now.year and order_time.month == now.month:
            quantity = _safe_int(order.get('quantity', 1))
            monthly_sold += quantity
            monthly_revenue += quantity * _safe_int(order.get('price', 0))

    total_inventory = len(products)
    total_sold = sum(product['soldCount'] for product in products)
    top_product = max(products, key=lambda item: item['soldCount'], default=None)

    return {
        'summary': {
            'monthLabel': now.strftime('%Y-%m'),
            'monthlyUploaded': monthly_uploaded,
            'monthlySold': monthly_sold,
            'monthlyRevenue': monthly_revenue,
            'totalInventory': total_inventory,
            'totalSold': total_sold,
            'topProductName': top_product['name'] if top_product else '-',
        },
        'products': filtered_products,
        'query': search_query,
    }


@csrf_exempt
def save_data(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'Method not allowed'}, status=405)

    data = _load_json_body(request)
    email = data.get('email', '')
    role = data.get('role', '')
    log_entry = f"[BOSHLANG'ICH] | Vaqt: {_now()} | Email: {email} | Rol: {role}\n"
    _append_text(USERS_FILE, log_entry)
    _upsert_user(
        {
            'email': email,
            'role': role,
            'savedAt': _now(),
        }
    )
    return JsonResponse({'status': "Muvaffaqiyatli saqlandi"})


@csrf_exempt
def save_profile(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'Method not allowed'}, status=405)

    data = _load_json_body(request)
    log_entry = (
        f"[PROFIL] | Ism: {data.get('firstname', '')} {data.get('lastname', '')} "
        f"| Yosh: {data.get('age', '')} | Tel: {data.get('phone', '')} "
        f"| Email: {data.get('email', '')} | Rol: {data.get('role', '')}\n"
    )
    _append_text(USERS_FILE, log_entry)
    _upsert_user(_serialize_user(data))
    return JsonResponse({'status': 'Success'})


@csrf_exempt
def save_final_user(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'Method not allowed'}, status=405)

    data = _load_json_body(request)
    log_entry = (
        f"[YAKUNIY QAYD] | Rol: {data.get('role', '')} | "
        f"Ism: {data.get('firstname', '')} {data.get('lastname', '')} | "
        f"Tel: {data.get('phone', '')} | Vaqt: {_now()}\n"
    )
    _append_text(USERS_FILE, log_entry)
    final_user = _serialize_user({**data, 'isRegistered': True})
    _upsert_user(final_user)

    redirect_url = '/xaridor.html'
    if data.get('role') == 'Tadbirkor':
        redirect_url = '/tadbirkor.html'

    return JsonResponse({'status': 'OK', 'redirectUrl': redirect_url})


@csrf_exempt
def add_product(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'Method not allowed'}, status=405)

    data = _load_json_body(request)
    category = data.get('category') or 'Boshqa'
    product_log = (
        f"[YANGI MAHSULOT] | Nomi: {data.get('productName', '')} | "
        f"Narxi: {data.get('price', '')} UZS | "
        f"Kategoriya: {category} | Tavsif: {data.get('description', '')} | Vaqt: {_now()}\n"
    )
    _append_text(PRODUCT_LOG_FILE, product_log)

    products = _read_products()
    products.append(
        {
            'id': len(products) + 1,
            'productName': data.get('productName', ''),
            'title': data.get('productName', ''),
            'price': data.get('price', ''),
            'description': data.get('description', ''),
            'category': category,
            'img': data.get('img', ''),
            'soldCount': _safe_int(data.get('soldCount', 0)),
            'createdAt': _now(),
        }
    )
    _write_products(products)
    return JsonResponse({'status': 'OK'})


def get_products(request):
    return JsonResponse(_read_products(), safe=False)


@csrf_exempt
def create_order(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'Method not allowed'}, status=405)

    data = _load_json_body(request)
    product_id = _safe_int(data.get('productId'))
    quantity = max(1, _safe_int(data.get('quantity', 1)))
    buyer_email = data.get('buyerEmail', '').strip().lower()

    products = _read_products()
    product = next((item for item in products if _safe_int(item.get('id')) == product_id), None)
    if not product:
        return JsonResponse({'status': 'error', 'message': 'Mahsulot topilmadi'}, status=404)

    orders = _read_orders()
    order = {
        'id': len(orders) + 1,
        'productId': product_id,
        'productName': product.get('title') or product.get('productName') or '-',
        'price': _safe_int(product.get('price', 0)),
        'quantity': quantity,
        'buyerEmail': buyer_email,
        'category': product.get('category') or 'Boshqa',
        'createdAt': _now(),
    }
    orders.append(order)
    _write_orders(orders)

    return JsonResponse({'status': 'ok', 'order': order})


def user_orders(request):
    buyer_email = request.GET.get('email', '').strip().lower()
    orders = _read_orders()

    if buyer_email:
        orders = [order for order in orders if order.get('buyerEmail', '').strip().lower() == buyer_email]

    serialized = [
        {
            'id': order.get('id'),
            'productName': order.get('productName'),
            'date': order.get('createdAt'),
            'quantity': order.get('quantity', 1),
            'total': f"{_safe_int(order.get('price', 0)) * _safe_int(order.get('quantity', 1))} UZS",
            'status': 'Qabul qilindi',
        }
        for order in reversed(orders)
    ]

    return JsonResponse(serialized, safe=False)


@csrf_exempt
def save_compare(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'Method not allowed'}, status=405)

    data = _load_json_body(request)
    _append_text(COMPARE_LOG_FILE, f"Solishtirildi: {json.dumps(data, ensure_ascii=False)}\n")
    return JsonResponse({'status': 'OK'})


def admin_login(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'Method not allowed'}, status=405)

    data = _load_json_body(request)
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    attempt_key = f'{email}:{_client_ip(request)}'
    _cleanup_login_attempts()
    attempt_record = ADMIN_LOGIN_ATTEMPTS.get(attempt_key, {})

    if attempt_record.get('count', 0) >= MAX_ADMIN_LOGIN_ATTEMPTS:
        return JsonResponse(
            {
                'status': 'locked',
                'message': f"Juda ko'p urinish bo'ldi. {_remaining_lockout_minutes(attempt_record)} daqiqadan keyin qayta urinib ko'ring.",
            },
            status=429,
        )

    if email != ADMIN_EMAIL or not check_password(password, ADMIN_PASSWORD_HASH):
        updated_record = _track_login_failure(attempt_key)
        _log_security_event(
            'FAILED_LOGIN',
            f"Admin login muvaffaqiyatsiz. Email: {email or '-'} | IP: {_client_ip(request)} | Uruinish: {updated_record['count']}",
            actor='Anonymous',
        )
        return JsonResponse({'status': 'error', 'message': "Login yoki parol noto'g'ri"}, status=401)

    _clear_login_failures(attempt_key)
    request.session[ADMIN_SESSION_KEY] = {'email': ADMIN_EMAIL, 'loggedInAt': _now()}
    request.session.set_expiry(ADMIN_SESSION_TIMEOUT_MINUTES * 60)
    _log_security_event(
        'LOGIN_SUCCESS',
        f"Admin tizimga kirdi. IP: {_client_ip(request)}",
        actor='Ozodbek Admin',
    )
    return JsonResponse(
        {
            'status': 'ok',
            'admin': {
                'email': ADMIN_EMAIL,
                'name': 'Ozodbek Admin',
            },
        }
    )


def admin_session(request):
    if not _is_admin(request):
        return JsonResponse({'authenticated': False})

    return JsonResponse(
        {
            'authenticated': True,
            'admin': {
                'email': ADMIN_EMAIL,
                'name': 'Ozodbek Admin',
            },
        }
    )


def admin_logout(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'Method not allowed'}, status=405)

    if _is_admin(request):
        _log_security_event(
            'LOGOUT',
            f"Admin tizimdan chiqdi. IP: {_client_ip(request)}",
            actor='Ozodbek Admin',
        )

    request.session.pop(ADMIN_SESSION_KEY, None)
    return JsonResponse({'status': 'ok'})


def admin_dashboard(request):
    if not _is_admin(request):
        return JsonResponse({'status': 'forbidden'}, status=403)

    users = list(reversed(_read_users()))
    products = list(reversed(_read_products()))
    categories = {}

    for product in products:
        category = product.get('category') or 'Boshqa'
        categories[category] = categories.get(category, 0) + 1

    return JsonResponse(
        {
            'users': users,
            'products': products,
            'categories': [
                {'name': name, 'count': count}
                for name, count in sorted(categories.items(), key=lambda item: item[0].lower())
            ],
            **_get_admin_security_payload(),
        }
    )


def admin_security_toggle(request):
    if not _is_admin(request):
        return JsonResponse({'status': 'forbidden'}, status=403)

    if request.method != 'POST':
        return JsonResponse({'status': 'Method not allowed'}, status=405)

    data = _load_json_body(request)
    enabled = bool(data.get('enabled', True))
    _write_security_settings(enabled, updated_by='Ozodbek Admin')
    _log_security_event(
        'SECURITY_TOGGLE',
        f"Xavfsizlik rejimi {'yoqildi' if enabled else 'o‘chirildi'}.",
        actor='Ozodbek Admin',
    )
    return JsonResponse({'status': 'ok', **_get_admin_security_payload()})


def admin_security_overview(request):
    if not _is_admin(request):
        return JsonResponse({'status': 'forbidden'}, status=403)

    return JsonResponse(_get_admin_security_payload())


def manager_dashboard(request):
    if not _is_admin(request):
        return JsonResponse({'status': 'forbidden'}, status=403)

    query = request.GET.get('q', '')
    return JsonResponse(_get_manager_payload(query))
