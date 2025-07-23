from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
import datetime
import psutil
import platform
import socket
import subprocess
import os

from .models import Product, Stock
from emp.models import Outlet
from transaction.models import Transaction
from .serializers import ProductSerializer, StockSerializer
from emp.serializers import OutletSerializer
from transaction.serializers import TransactionSerializer
from rest_framework import status
# ------------------------------------------
# Product ViewSet with search on stock
# ------------------------------------------
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('search', '')
        stocks = Stock.objects.filter(
            Q(product__ItDesc__icontains=query) | Q(outlet__outletName__icontains=query)
        )
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='by-itcode/(?P<itcode>[^/.]+)')
    def get_by_itcode(self, request, itcode=None):
        try:
            product = Product.objects.get(Itcode=itcode)
            return Response({'id': product.id})
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

# ------------------------------------------
# Transaction ViewSet with search functionality
# ------------------------------------------
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('search', '')
        transactions = Transaction.objects.filter(
            Q(product__ItDesc__icontains=query) | Q(outlet__outletName__icontains=query)
        )
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

# ------------------------------------------
# Stock ViewSet
# ------------------------------------------
class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

# ------------------------------------------
# Outlet ViewSet
# ------------------------------------------
class OutletViewSet(viewsets.ModelViewSet):
    queryset = Outlet.objects.all()
    serializer_class = OutletSerializer

# ------------------------------------------
# Helper: Safely get CPU temperature (cross-platform safe)
# ------------------------------------------
def get_cpu_temperature():
    try:
        # Check if sensors_temperatures is available
        temps_func = getattr(psutil, "sensors_temperatures", None)
        if temps_func is None:
            return None

        temps = psutil.sensors_temperatures()
        if not temps:
            return None

        # Look for common CPU temperature labels
        for name, entries in temps.items():
            for entry in entries:
                label = entry.label.lower() if entry.label else ''
                if label.startswith('cpu') or 'core' in label:
                    return entry.current

        # Fallback: return first temperature available
        first_entry = next(iter(next(iter(temps.values()))), None)
        if first_entry:
            return first_entry.current

    except Exception:
        return None

# ------------------------------------------
# Helper: Check service status (Linux & Windows)
# ------------------------------------------
def check_service(name):
    try:
        system = platform.system()
        if system == 'Linux':
            # Using systemctl on Linux
            result = subprocess.run(['systemctl', 'is-active', name], capture_output=True, text=True)
            return result.stdout.strip()
        elif system == 'Windows':
            # Using 'sc query' on Windows
            result = subprocess.run(['sc', 'query', name], capture_output=True, text=True)
            if 'RUNNING' in result.stdout:
                return 'running'
            else:
                return 'stopped'
        else:
            return 'unknown'
    except Exception:
        return 'unknown'

# ------------------------------------------
# Health data API view
# ------------------------------------------
def health_data(request):
    # Collect system stats
    memory = psutil.virtual_memory()
    cpu_percent = psutil.cpu_percent(interval=1)
    disk = psutil.disk_usage('/')
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.datetime.now() - boot_time

    # Network usage counters
    net_io = psutil.net_io_counters()

    # Get top 5 processes by CPU usage
    processes = []
    for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
        try:
            info = proc.info
            # Some processes might not have cpu_percent immediately, so default to 0
            info['cpu_percent'] = info.get('cpu_percent', 0) or 0
            processes.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Sort descending by CPU usage
    processes = sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)[:5]

    # Get CPU temperature safely
    cpu_temp = get_cpu_temperature()


    # System info
    system_info = {
        'os': platform.platform(),
        'hostname': socket.gethostname(),
        'python_version': platform.python_version(),
    }

    # Error log reading
    error_logs = []
    # Choose log file based on OS
    if platform.system() == 'Linux':
        log_file_path = '/var/log/syslog'
    elif platform.system() == 'Windows':
        # You should specify your actual Windows log file path here
        log_file_path = r'C:\path\to\your\windows\logfile.log'
    else:
        log_file_path = None

    if log_file_path and os.path.exists(log_file_path):
        try:
            with open(log_file_path, 'r') as f:
                lines = f.readlines()
                filtered = [line.strip() for line in lines if 'ERROR' in line or 'WARN' in line]
                error_logs = filtered[-5:]  # last 5 error/warn lines
        except Exception:
            error_logs = ["Error reading logs or file not found."]
    else:
        error_logs = ["Log file path not configured or does not exist."]


    # Prepare JSON response
    data = {
        'status': 'OK',
        'server_time': datetime.datetime.now().isoformat(),
        'version': '1.0.0',
        'cpu_percent': cpu_percent,
        'memory': {
            'total': memory.total,
            'used': memory.used,
            'percent': memory.percent,
        },
        'disk': {
            'total': disk.total,
            'used': disk.used,
            'percent': disk.percent,
        },
        'uptime': str(uptime).split('.')[0],  # clean uptime string (remove microseconds)
        'network': {
            'sent': net_io.bytes_sent,
            'recv': net_io.bytes_recv,
        },
        'top_processes': processes,
        'temperature': {
            'cpu': cpu_temp,
        },
        'system': system_info,
        'errors': error_logs,
        
    }
    return JsonResponse(data)

# ------------------------------------------
# Render product dashboard HTML page
# ------------------------------------------
def product_dashboard(request):
    return render(request, 'index.html')
