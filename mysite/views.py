import subprocess
from django.http import HttpResponse
from .forms import GoogleSheetForm
import os
from django.http import HttpResponseRedirect
from django_q.tasks import async_task
from .models import ScriptTask
from django.http import JsonResponse
from django.utils import timezone
import uuid
from django.shortcuts import redirect, render, get_object_or_404
import signal
from django_q.models import Task
from .models import ScheduledScriptTask
from .forms import PasswordForm
from .forms import ScheduledScriptTaskForm
from .models import validate_script_path




#########################



import mysql.connector
from mysql.connector import Error
from django.shortcuts import render
from datetime import datetime, timedelta
import re

# MySQL Configuration for script logs
MYSQL_LOG_CONFIG = {
    'host': 'Karmel.mysql.pythonanywhere-services.com',
    'user': 'Karmel',
    'password': 'Aporia123456789',  # TODO: Replace with your actual password
    'database': 'Karmel$default'  # TODO: Replace with your actual database name
}


def get_mysql_log_connection():
    """Create and return a MySQL database connection for script logs."""
    try:
        connection = mysql.connector.connect(**MYSQL_LOG_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None


def _is_generic_failure_message(message: str) -> bool:
    if not message:
        return True
    normalized = message.strip().lower()
    return bool(
        re.search(r"failed\s+after\s+\d+\s+attempt", normalized)
        or normalized in {"failed", "error", "unknown error"}
    )


def _extract_failure_reason(result_message: str, script_output: str) -> str:
    """Extract the most useful failure line for detailed hover tooltip."""
    base_message = (result_message or "").strip()
    if base_message and not _is_generic_failure_message(base_message):
        return base_message

    output = script_output or ""
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    if not lines:
        return base_message or "Failed"

    priority_markers = (
        "Traceback",
        "Exception",
        "Error:",
        "Timeout",
        "HTTPError",
        "ConnectionError",
        "KeyError",
        "ValueError",
        "TypeError",
    )
    for line in reversed(lines):
        if any(marker in line for marker in priority_markers):
            return line

    return lines[-1]


def script_logs_page(request):
    """Display script run logs from MySQL database with two view modes."""
    connection = None
    cursor = None

    # Get filter parameters
    view_mode = request.GET.get('view_mode', 'grouped')  # 'grouped' or 'individual'
    date_filter = request.GET.get('date', '')
    if not date_filter:
        date_filter = datetime.now().strftime('%Y-%m-%d')
    general_label_filter = request.GET.get('general_label', '')
    label_filter = request.GET.get('label', '')
    script_filter = request.GET.get('script', '')
    status_filter = request.GET.get('status', '')

    grouped_data = []
    individual_data = []
    all_general_labels = []
    all_labels = []
    all_scripts = []

    try:
        connection = get_mysql_log_connection()
        if connection is None:
            return render(request, 'script_logs_page.html', {
                'error': 'Could not connect to MySQL database',
                'view_mode': view_mode,
                'filters': {'date': '', 'general_label': '', 'label': '', 'script': '', 'status': ''}
            })

        cursor = connection.cursor(dictionary=True)

        # Get distinct values for filter dropdowns
        cursor.execute("SELECT DISTINCT general_label FROM script_run_logs ORDER BY general_label")
        all_general_labels = [row['general_label'] for row in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT label FROM script_run_logs ORDER BY label")
        all_labels = [row['label'] for row in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT script_path FROM script_run_logs ORDER BY script_path")
        all_scripts = [row['script_path'] for row in cursor.fetchall()]

        if view_mode == 'grouped':
            # GROUPED VIEW: Get last 20 unique run batches grouped by batch_id

            query = """
                SELECT
                    id, run_timestamp, script_path, general_label, label,
                    status, result_message, script_output, execution_mode, batch_id
                FROM script_run_logs
                WHERE 1=1
            """
            params = []

            if date_filter:
                query += " AND DATE(run_timestamp) = %s"
                params.append(date_filter)

            if general_label_filter:
                query += " AND general_label = %s"
                params.append(general_label_filter)

            if status_filter:
                query += " AND status = %s"
                params.append(status_filter)

            query += " ORDER BY run_timestamp DESC LIMIT 500"

            cursor.execute(query, params)
            all_logs = cursor.fetchall()
            for log in all_logs:
                if log.get('status') != 'Success':
                    log['detailed_error_message'] = _extract_failure_reason(
                        log.get('result_message'),
                        log.get('script_output'),
                    )
                    log['display_message'] = log.get('result_message') or ''
                else:
                    log['display_message'] = log.get('result_message') or ''
                    log['detailed_error_message'] = ''

            # Group logs by batch_id (or fall back to time-based for old data without batch_id)
            groups = {}
            for log in all_logs:
                # Use batch_id if available, otherwise fall back to time-based grouping for legacy data
                batch_id = log.get('batch_id')
                if batch_id:
                    group_key = batch_id
                else:
                    # Fallback for old records without batch_id
                    timestamp = log['run_timestamp']
                    rounded_time = timestamp.replace(minute=(timestamp.minute // 10) * 10, second=0, microsecond=0)
                    group_key = f"legacy_{log['general_label']}_{rounded_time.strftime('%Y-%m-%d %H:%M')}"

                if group_key not in groups:
                    groups[group_key] = {
                        'general_label': log['general_label'],
                        'run_timestamp': log['run_timestamp'],
                        'execution_mode': log['execution_mode'],
                        'batch_id': batch_id or '',
                        'scripts': [],
                        'total': 0,
                        'success': 0,
                        'failed': 0
                    }

                groups[group_key]['scripts'].append(log)
                groups[group_key]['total'] += 1
                if log['status'] == 'Success':
                    groups[group_key]['success'] += 1
                else:
                    groups[group_key]['failed'] += 1

            # Calculate overall status for each group
            for group_key, group in groups.items():
                if group['failed'] == 0:
                    group['overall_status'] = 'Success'
                    group['status_class'] = 'success'
                    group['status_emoji'] = '✅'
                elif group['success'] == 0:
                    group['overall_status'] = 'Failed'
                    group['status_class'] = 'danger'
                    group['status_emoji'] = '❌'
                else:
                    group['overall_status'] = 'Partial'
                    group['status_class'] = 'warning'
                    group['status_emoji'] = '⚠️'

            # Sort by timestamp and limit to 20 groups
            grouped_data = sorted(groups.values(), key=lambda x: x['run_timestamp'], reverse=True)[:20]

        else:
            # INDIVIDUAL VIEW: Get last 100 individual script runs
            query = """
                SELECT
                    id, run_timestamp, script_path, general_label, label,
                    status, result_message, script_output, execution_mode, batch_id
                FROM script_run_logs
                WHERE 1=1
            """
            params = []

            if date_filter:
                query += " AND DATE(run_timestamp) = %s"
                params.append(date_filter)

            if general_label_filter:
                query += " AND general_label = %s"
                params.append(general_label_filter)

            if label_filter:
                query += " AND label LIKE %s"
                params.append(f"%{label_filter}%")

            if script_filter:
                query += " AND script_path LIKE %s"
                params.append(f"%{script_filter}%")

            if status_filter:
                query += " AND status = %s"
                params.append(status_filter)

            query += " ORDER BY run_timestamp DESC LIMIT 100"

            cursor.execute(query, params)
            individual_data = cursor.fetchall()
            for log in individual_data:
                if log.get('status') != 'Success':
                    log['detailed_error_message'] = _extract_failure_reason(
                        log.get('result_message'),
                        log.get('script_output'),
                    )
                    log['display_message'] = log.get('result_message') or ''
                else:
                    log['display_message'] = log.get('result_message') or ''
                    log['detailed_error_message'] = ''

    except Error as e:
        return render(request, 'script_logs_page.html', {
            'error': f'Database error: {str(e)}',
            'view_mode': view_mode,
            'filters': {'date': '', 'general_label': '', 'label': '', 'script': '', 'status': ''}
        })
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

    context = {
        'view_mode': view_mode,
        'grouped_data': grouped_data,
        'individual_data': individual_data,
        'all_general_labels': all_general_labels,
        'all_labels': all_labels,
        'all_scripts': all_scripts,
        'filters': {
            'date': date_filter,
            'general_label': general_label_filter,
            'label': label_filter,
            'script': script_filter,
            'status': status_filter,
        }
    }

    return render(request, 'script_logs_page.html', context)

















##############################################



import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Create and cache the client once at import time (faster than doing it per-request)
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]
CREDS_PATH = r"/home/Karmel/Amit/smart-surf-295322-88ad90affe77.json"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ikl6H8wvTmM-ZcTNordTV2up9dpeiJj6DPKwOP8bAC4/edit?gid=0#gid=0"
TAB_NAME = "Sheet1"  # or use the tab you want

_creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_PATH, SCOPE)
_gc = gspread.authorize(_creds)

def run_reports(request):
    try:
        sh = _gc.open_by_url(SHEET_URL)
        ws = sh.worksheet(TAB_NAME)  # or: ws = next(w for w in sh.worksheets() if w.id == 0)  # gid=0
        data = ws.get_all_values()   # or ws.get("A1:H50") to limit
        tab_title = ws.title
    except Exception as e:
        # Fall back to an empty table on error; you can also log e
        data = []
        tab_title = TAB_NAME

    return render(request, "run_scripts.html", {
        "sheet_data": data,
        "GOOGLE_SHEET_TAB": tab_title,  # optional: use in your template header
    })





##############################################



from django_q.models import Schedule
from .models import ScheduledScriptTask
from django.shortcuts import render

def list_scheduled_tasks(request):
    # Fetch tasks from both models
    custom_tasks = ScheduledScriptTask.objects.filter(is_active=True)
    django_q_tasks = Schedule.objects.all()

    return render(request, 'scheduled_tasks_list.html', {
        'custom_tasks': custom_tasks,
        'django_q_tasks': django_q_tasks,
    })

def scheduled_tasks_list(request):
    tasks = ScheduledScriptTask.objects.filter(is_active=True)

    return render(request, 'scheduled_tasks_list.html', {
        'tasks': tasks,
    })



# Add a new scheduled task
def add_scheduled_task(request):
    if request.method == 'POST':
        form = ScheduledScriptTaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_scheduled_tasks')
    else:
        form = ScheduledScriptTaskForm()
    return render(request, 'scheduled_task_form.html', {'form': form, 'action': 'Add'})

# Edit an existing scheduled task
def edit_scheduled_task(request, task_id):
    task = get_object_or_404(ScheduledScriptTask, id=task_id)
    if request.method == 'POST':
        form = ScheduledScriptTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('list_scheduled_tasks')
    else:
        form = ScheduledScriptTaskForm(instance=task)
    return render(request, 'scheduled_task_form.html', {'form': form, 'action': 'Edit'})

# Delete a scheduled task
def delete_scheduled_task(request, task_id):
    task = get_object_or_404(ScheduledScriptTask, id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('list_scheduled_tasks')
    return render(request, 'confirm_delete.html', {'task': task})







########################################





def execute_script(request, script_path):
    """
    Create a new task entry and execute the script with a unique execution code.
    Prevent running the same script if it's already running.
    """
    # Check if the script is already running
    existing_task = ScriptTask.objects.filter(
        script_name=script_path,
        status__in=['PENDING', 'RUNNING']
    ).first()

    if existing_task:
        # Render a custom error page
        return render(request, 'script_already_running.html', {
            'script_name': script_path,
            'task_id': existing_task.id
        })

    # Create a new task entry in the database
    task = ScriptTask.objects.create(
        script_name=script_path,
        status='PENDING',
        unique_code=uuid.uuid4(),
        created_at=timezone.now()
    )

    # Ensure task ID is passed correctly
    async_task(
        'mysite.tasks.run_script_task',
        script_path,
        str(task.unique_code),  # Ensure unique_code is passed correctly
        #hook='mysite.tasks.task_completion_hook'  # Optional: Hook for cleanup
    )

    # Redirect to the task status page
    return redirect('task_status', task_id=task.id)





def task_status(request, task_id):
    task = get_object_or_404(ScriptTask, id=task_id)
    return render(request, 'task_status.html', {
        'task_id': task.id,
        'script_name': task.script_name,
        'status': task.status,
        'output': task.output,
        'error': task.error,
        'created_at': task.created_at,
        'updated_at': task.updated_at,
    })




def running_tasks(request):
    # Get all running tasks
    running_tasks = ScriptTask.objects.filter(status='RUNNING').order_by('-created_at')

    # Get the last 10 tasks (any status)
    recent_tasks = ScriptTask.objects.all().order_by('-created_at')[:700]

    return render(request, 'running_tasks.html', {

        'recent_tasks': recent_tasks
    })




def _is_pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        # safer to assume alive
        return True


def _is_pgid_alive(pgid: int) -> bool:
    """
    The important check for your case:
    wrapper PID may die, while child processes in the same group still run.
    """
    try:
        os.killpg(pgid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def _kill_process_tree(pid: int, pgid: int = None, timeout_seconds: float = 8.0):
    import time

    # ✅ If PGID missing/looks wrong, try to derive real PGID from PID
    if pgid is None:
        try:
            pgid = os.getpgid(pid)
        except Exception:
            pgid = pid
    else:
        # If provided PGID is already "dead" but PID is alive,
        # it probably means the stored PGID is wrong -> recompute from PID.
        if _is_pid_alive(pid) and (not _is_pgid_alive(pgid)):
            try:
                pgid = os.getpgid(pid)
            except Exception:
                pass

    # ✅ Only "already not running" if BOTH are gone with the (possibly recomputed) PGID
    if (not _is_pid_alive(pid)) and (not _is_pgid_alive(pgid)):
        return True, "PID and PGID are already not running."

    def _signal_group(sig, wait_seconds):
        try:
            os.killpg(pgid, sig)
        except ProcessLookupError:
            return True, f"PGID {pgid} not found after sending {sig}."
        except PermissionError as e:
            return False, f"PermissionError sending {sig} to PGID {pgid}: {e}"
        except OSError as e:
            return False, f"OSError sending {sig} to PGID {pgid}: {e}"

        # ✅ Verify GROUP (PGID), not PID
        end = time.time() + wait_seconds
        while time.time() < end:
            if not _is_pgid_alive(pgid):
                return True, f"Stopped process group with signal {sig}."
            time.sleep(0.2)

        return False, f"PGID {pgid} still alive after signal {sig}."

    # 1) SIGINT
    ok, msg1 = _signal_group(signal.SIGINT, wait_seconds=min(2.5, timeout_seconds))
    if ok:
        return True, msg1

    # 2) SIGTERM
    ok, msg2 = _signal_group(signal.SIGTERM, wait_seconds=min(2.5, max(1.0, timeout_seconds - 2.5)))
    if ok:
        return True, msg2

    # 3) SIGKILL
    ok, msg3 = _signal_group(signal.SIGKILL, wait_seconds=2.0)
    if ok:
        return True, msg3

    # Final verification
    if _is_pgid_alive(pgid):
        return False, f"Kill failed: PGID {pgid} still alive. SIGINT={msg1} SIGTERM={msg2} SIGKILL={msg3}"

    return True, "Group is gone after signals."



def stop_task(request, unique_code):
    """
    Request stopping a task.
    IMPORTANT: Do NOT kill from the web process (different PID namespace on PythonAnywhere).
    A separate always-on "killer_daemon" should perform the kill.
    """
    task = get_object_or_404(ScriptTask, unique_code=unique_code)

    # Allow stopping RUNNING or PENDING
    if task.status in ("RUNNING", "PENDING"):
        task.status = "STOP_REQUESTED"
        task.error = None
        task.output = (task.output or "") + "\n🛑 Stop requested from web UI. Waiting for killer_daemon..."
        task.save()

    return redirect('task_status', task_id=task.id)




#######################################################



#######################################################




def kill_task_view(request):
    """
    Request killing a task by ID.
    IMPORTANT: Do NOT kill from the web process (different PID namespace on PythonAnywhere).
    A separate always-on "killer_daemon" should perform the kill.
    """
    message = None
    message_type = "success"

    if request.method == "POST":
        task_id = request.POST.get("task_id", "").strip()

        if not task_id.isdigit():
            return render(request, "kill_task.html", {
                "message": "Invalid Task ID.",
                "message_type": "error"
            })

        task = get_object_or_404(ScriptTask, id=int(task_id))

        if task.status not in ("RUNNING", "PENDING"):
            return render(request, "kill_task.html", {
                "message": f"Task {task_id} is not RUNNING/PENDING (current status: {task.status}). No stop requested.",
                "message_type": "error"
            })

        task.status = "STOP_REQ"
        task.error = None
        task.output = (task.output or "") + "\n🛑 Stop requested from web. Waiting for wrapper to terminate child..."
        task.save()

        message = f"Stop requested for task {task_id}. It will be terminated by killer_daemon."
        message_type = "success"

    return render(request, "kill_task.html", {
        "message": message,
        "message_type": message_type
    })





def Kill_Task_page(request):
    return render(request, "kill_task.html")


#######################################################




############## Karmel ##############

def run_facebook_script(request):
    script_path = "/home/Karmel/Karmel/Daily_reports/Facebook V3.py"
    return execute_script(request, script_path)

def run_google_script(request):
    script_path = "/home/Karmel/Karmel/Daily_reports/Google V3.py"
    return execute_script(request, script_path)

def run_tiktok_script(request):
    script_path = "/home/Karmel/Karmel/Daily_reports/Tiktok V3.py"
    return execute_script(request, script_path)

def run_outbrain_script(request):
    script_path = "/home/Karmel/Karmel/Daily_reports/Google V3.py"
    return execute_script(request, script_path)





############## Amit ##############


def run_newtabyes3_script(request):
    script_path = "/home/Karmel/Amit/newtabyes_test.py"
    return execute_script(request, script_path)

def run_backupmaintonic_script(request):
    script_path = "/home/Karmel/Amit/backupmaintonic.py"
    return execute_script(request, script_path)

def run_obyesforreport_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/obyesforreport 4.py"
    return execute_script(request, script_path)

def run_topofferskeywordstonicnew2025_script(request):
    script_path = "/home/Karmel/Amit/Amit/topofferskeywordstonicnew2025.py"
    return execute_script(request, script_path)

def run_tonicrsocchannelscreator_script(request):
    script_path = "/home/Karmel/Amit/Amit/tonicrsocchannelscreator.py"
    return execute_script(request, script_path)

def run_tonicrsocchannelspixels_script(request):
    script_path = "/home/Karmel/Amit/Amit/tonicrsocchannelspixels.py"
    return execute_script(request, script_path)

def run_inuvoyesallyesterdaydata2025_script(request):
    script_path = "/home/Karmel/Amit/Amit/inuvoyesallyesterdaydata2025.py"
    return execute_script(request, script_path)

def run_palaceupdate_script(request):
    script_path = "/home/Karmel/Amit/Amit/palaceupdate.py"
    return execute_script(request, script_path)

def run_Run_SistersDB_script(request):
    script_path = "/home/Karmel/Amit/Amit/SistersDB/Run_SistersDB.py"
    return execute_script(request, script_path)

def run_compliance_siteids_script(request):
    script_path = "/home/Karmel/Amit/Amit/compliance_siteids.py"
    return execute_script(request, script_path)

def run_sisterscompliancepj_script(request):
    script_path = "/home/Karmel/Amit/Amit/sisterscompliancepj.py"
    return execute_script(request, script_path)

def run_systemnewreport_mobile_script(request):
    script_path = "/home/Karmel/Amit/Taboola/systemnewreport_mobile.py"
    return execute_script(request, script_path)

def run_getkeywordsdata_script(request):
    script_path = "/home/Karmel/Amit/Amit/getkeywordsdata.py"
    return execute_script(request, script_path)

def run_Main_N2S_Today_script(request):
    script_path = "/home/Karmel/Amit/Auto_Runs/Run_Main_N2S_Today.py"
    return execute_script(request, script_path)



#def run_newtabyes3_script(request):
    #return HttpResponseRedirect('https://www.pythonanywhere.com/user/Karmel/files/home/Karmel/Amit/newtabyes3.py?edit')




def run_obyesforreport_final_script(request):
    script_path = "/home/Karmel/Amit/Amit/final_update/obyesforreport_final.py"
    return execute_script(request, script_path)

def run_backupmaintonic_final_script(request):
    script_path = "/home/Karmel/Amit/Amit/final_update/backupmaintonic_final.py"
    return execute_script(request, script_path)

def run_newtabyes_final_script(request):
    script_path = "/home/Karmel/Amit/Amit/final_update/newtabyes_final.py"
    return execute_script(request, script_path)

def run_trafficclubyesdata_script(request):
    script_path = "/home/Karmel/Amit/Amit/trafficclubyesdata.py"
    return execute_script(request, script_path)

def run_tcyes_2Days_script(request):
    script_path = "/home/Karmel/Amit/Traffic_Club/tcyes_2Days.py"
    return execute_script(request, script_path)



    # Creatives Scripts


#def run_allfbcreatives_script(request):
#   script_path = "/home/Karmel/Amit/Facebook/allfbcreatives.py"
#   return execute_script(request, script_path)


def run_allcreativestab_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative/allcreativestab 1.py"
    return execute_script(request, script_path)


def run_allobcreatives_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative/allobcreatives 1.py"
    return execute_script(request, script_path)


def run_allmediagocreatives_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative/allmediagocreatives 1.py"
    return execute_script(request, script_path)


def run_zemantacreativesall_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative/zemantacreativesall 1.py"
    return execute_script(request, script_path)


def run_poppincreatives_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative/poppincreatives 1.py"
    return execute_script(request, script_path)



    # WTHIW Scripts


def run_WTHIW_script(request):
    script_path = "/home/Karmel/Amit/Amit/WTHIW.py"
    return execute_script(request, script_path)


def run_WTHIW_Copysheets_script(request):
    script_path = "/home/Karmel/Amit/Amit/WTHIW-Copysheets.py"
    return execute_script(request, script_path)



    # Policy Scripts


def run_copyarticlesdata_script(request):
    script_path = "/home/Karmel/Amit/Amit/copyarticlesdata.py"
    return execute_script(request, script_path)


def run_newpolicycheckforall_running_script(request):
    script_path = "/home/Karmel/Amit/Amit/newpolicycheckforall_running.py"
    return execute_script(request, script_path)


def run_gen_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Amit/gen_newpolicycheckforall.py"
    return execute_script(request, script_path)



    # Oz


def run_copyarticlesdata_script(request):
    script_path = "/home/Karmel/Amit/Amit/copyarticlesdata.py"
    return execute_script(request, script_path)


def run_copyarticlesdataexcs_script(request):
    script_path = "/home/Karmel/Amit/Amit/copyarticlesdataexcs1-new.py"
    return execute_script(request, script_path)



    # Karmel tests


def run_tcyes_history_script(request):
    script_path = "/home/Karmel/Amit/Traffic_Club/tcyes_history.py"
    return execute_script(request, script_path)


def run_dailyfb_test_2_script(request):
    script_path = "/home/Karmel/Amit/Facebook/dailyfb_test_2.py"
    return execute_script(request, script_path)




############## Amir ##############




def run_MJ_Stock_Generator_V1_script(request):
    script_path = "/home/Karmel/Amir/creative/MJ_Stock_Generator_V1 2.py"
    return execute_script(request, script_path)



############## Sharon ##############




def run_allweeklyupdate_script(request):
    script_path = "/home/Karmel/Amit/Sharon/allweeklyupdate.py"
    return execute_script(request, script_path)



############## MGID ##############




def run_mgidrsoctoniccreate_link_callback_script(request):
    script_path = "/home/Karmel/Amit/MGID/mgidrsoctoniccreate_link_callback.py"
    return execute_script(request, script_path)



def run_mgid_active_tonic_campaigns_script(request):
    script_path = "/home/Karmel/Amit/MGID/mgid_active_tonic_campaigns.py"
    return execute_script(request, script_path)




############## Zemanta ##############



def run_toniczemanta_2_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/toniczemanta 2.py"
    return execute_script(request, script_path)

def run_toniczemanta2_2_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/toniczemanta2 2.py"
    return execute_script(request, script_path)

def run_zemantayes_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/zemantayes.py"
    return execute_script(request, script_path)

def run_zemanta2D_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/zemanta2D.py"
    return execute_script(request, script_path)

def run_invuozemantayes_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/invuozemantayes.py"
    return execute_script(request, script_path)

def run_zemantainuvoleads_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/zemantainuvoleads.py"
    return execute_script(request, script_path)





def run_imagescutob_zemanta_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/imagescutob-zemanta.py"
    return execute_script(request, script_path)

def run_newuploader_imagescutob_zemanta_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/imagescutob-zemanta-newuploader.py"
    return execute_script(request, script_path)





def run_zemanta3finals_andrea(request):
    script_path = "/home/Karmel/Amit/Zemanta/zemanta3finals-andrea.py"
    return execute_script(request, script_path)

def run_zemanta3finals_tonic_andrea(request):
    script_path = "/home/Karmel/Amit/Zemanta/zemanta3finals-tonic-andrea.py"
    return execute_script(request, script_path)

def run_zemantacreatives7days_andrea_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/zemantacreatives7days-andrea.py"
    return execute_script(request, script_path)




def run_zemantaNeedToArchive_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/zemantaNeedToArchive.py"
    return execute_script(request, script_path)

def run_zemantaarchived_1_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/zemantaarchived 1.py"
    return execute_script(request, script_path)

def run_zemantadataforupload_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/zemantadataforupload.py"
    return execute_script(request, script_path)

def run_Zemanta_L14_script(request):
    script_path = "/home/Karmel/Karmel/0Spend_Reports/Zemanta_L14_X.py"
    return execute_script(request, script_path)

def run_zemanta_whitelists_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/zemanta-whitelists.py"
    return execute_script(request, script_path)





def run_zemanta_publishers_merged_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/zemanta_publishers_merged.py"
    return execute_script(request, script_path)

def run_publishers_opt_BLACKLISTED_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/zemanta_run_publishers_opt_BLACKLISTED.py"
    return execute_script(request, script_path)

def run_publishers_opt_ENABLED_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/zemanta_run_publishers_opt_ENABLED.py"
    return execute_script(request, script_path)

def run_zemanta_publishers_merged_SOURCES_EXP_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/publishers_merged_SOURCES_EXP/zemanta_publishers_merged_SOURCES_EXP.py"
    return execute_script(request, script_path)




def run_zemantaccmps05112024_CcmpsOB_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/zemantaccmps05112024_CcmpsOB.py"
    return execute_script(request, script_path)

def run_zemantaccmps05112024_CcmpsOB2_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/zemantaccmps05112024_CcmpsOB2.py"
    return execute_script(request, script_path)

def run_zemantaccmps05112024_Ccmps_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/zemantaccmps05112024_Ccmps.py"
    return execute_script(request, script_path)

def run_zemantaccmps05112024_CcmpsM_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/zemantaccmps05112024_CcmpsM.py"
    return execute_script(request, script_path)




def run_zemantacads_Cadg_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/Multiple sheet scripts/zemantacads-Cadg.py"
    return execute_script(request, script_path)

def run_zemantacadg05112024_Cadg_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/Multiple sheet scripts/zemantacadg05112024-Cadg.py"
    return execute_script(request, script_path)

def run_zemantaopt_update_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/Multiple sheet scripts/zemantaopt_update.py"
    return execute_script(request, script_path)





def run_zemantacads_Cadg2_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/Multiple sheet scripts/zemantacads-Cadg2.py"
    return execute_script(request, script_path)

def run_zemantacadg05112024_Cadg2_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/Multiple sheet scripts/zemantacadg05112024-Cadg2.py"
    return execute_script(request, script_path)

def run_zemantaopt_update2_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/Multiple sheet scripts/zemantaopt_update2.py"
    return execute_script(request, script_path)

def run_zemantaopt_update3_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/Multiple sheet scripts/zemantaopt_update3.py"
    return execute_script(request, script_path)

def run_zemantaopt_update4_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/Multiple sheet scripts/zemantaopt_update4.py"
    return execute_script(request, script_path)





def run_zemantaopt_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/zemantaopt.py"
    return execute_script(request, script_path)



############## Taboola




def run_wandkeywords_script(request):
    script_path = "/home/Karmel/Amit/wandkeywords 1.py"
    return execute_script(request, script_path)

def run_SYSTEM_report_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Taboola/SYSTEM report 1.py"
    return execute_script(request, script_path)

def run_all_taboola_budgets_bids_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Taboola/all-taboola-budgets-bids 1.py"
    return execute_script(request, script_path)

def run_all_taboola_ids_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Taboola/all-taboola-ids.py"
    return execute_script(request, script_path)


def run_autogpt_tabooladesc_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Taboola/autogpt-tabooladesc.py"
    return execute_script(request, script_path)

def run_morning_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Taboola/morning.py"
    return execute_script(request, script_path)


def run_newtabyes_max_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Taboola/newtabyes-max.py"
    return execute_script(request, script_path)

def run_newtabyess1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Taboola/newtabyess1 1.py"
    return execute_script(request, script_path)


def run_tabautooptcr_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Taboola/tabautooptcr.py"
    return execute_script(request, script_path)




def run_tabcreatives3_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Taboola/tabcreatives3.py"
    return execute_script(request, script_path)

def run_tabcreatives4_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Taboola/tabcreatives4.py"
    return execute_script(request, script_path)

def run_tabcreatives2_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Taboola/tabcreatives2.py"
    return execute_script(request, script_path)





def run_tabcreativesforall_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Taboola/tabcreativesforall.py"
    return execute_script(request, script_path)

def run_tabooladatabreakdown_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Taboola/tabooladatabreakdown 1 1.py"
    return execute_script(request, script_path)

def run_tabupdatemaxcpcbid_auto_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Taboola/tabupdatemaxcpcbid-auto.py"
    return execute_script(request, script_path)


def run_tonicdavid_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Taboola/tonicdavid.py"
    return execute_script(request, script_path)

def run_tabsitescr_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Taboola/tabsitescr.py"
    return execute_script(request, script_path)

def run_newtabyess1_new_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Taboola/newtabyess1_new.py"
    return execute_script(request, script_path)

def run_taboola_allaccounts_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Taboola/taboola-allaccounts 1.py"
    return execute_script(request, script_path)


def run_tabupdatemaxcpcbid_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Taboola/tabupdatemaxcpcbid.py"
    return execute_script(request, script_path)


def run_maxcpaandcpcbidstaboolaopt_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Taboola/maxcpaandcpcbidstaboolaopt.py"
    return execute_script(request, script_path)


def run_pausetaboolal7nospend_script(request):
    script_path = "/home/Karmel/Amit/Taboola/pausetaboolal7nospend.py"
    return execute_script(request, script_path)



# Opt


def run_tabopt2026_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Taboola/tabopt2026 1.py"
    return execute_script(request, script_path)


# Taboola page - Wanduum



def run_T2tonicrsocwanduumnew3finals_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Wanduum/T2tonicrsocwanduumnew3finals.py"
    return execute_script(request, script_path)

def run_T3wandrsoccreatives_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Wanduum/T3wandrsoccreatives.py"
    return execute_script(request, script_path)

def run_T4wandtonicrsoctab3days_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Wanduum/T4wandtonicrsoctab3days.py"
    return execute_script(request, script_path)

def run_T5wandtonicrsoctabyes_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Wanduum/T5wandtonicrsoctabyes.py"
    return execute_script(request, script_path)


def run_T6wanduumrsoctonicoffers_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Wanduum/T6wanduumrsoctonicoffers.py"
    return execute_script(request, script_path)


def run_newtabyes2wand_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Wanduum/newtabyes2wand 1.py"
    return execute_script(request, script_path)


def run_newtabyeswandnewfull_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Wanduum/newtabyeswandnewfull 1.py"
    return execute_script(request, script_path)


def run_newtabyeswandnewfull_3click_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Wanduum/newtabyeswandnewfull-3click 1.py"
    return execute_script(request, script_path)


def run_tonic_wanduum_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Wanduum/tonic-wanduum 1.py"
    return execute_script(request, script_path)


def run_tonic_wanduum_3click_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Wanduum/tonic-wanduum-3click.py"
    return execute_script(request, script_path)


def run_tonicEPCtrackingWand_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Wanduum/tonicEPCtrackingWand.py"
    return execute_script(request, script_path)


def run_tonicwandforopt_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Wanduum/tonicwandforopt 1.py"
    return execute_script(request, script_path)


def run_systemnewreport_script(request):
    script_path = "/home/Karmel/Amit/Taboola/systemnewreport 2.py"
    return execute_script(request, script_path)


def run_tonicwanduumnew3finals_new_script(request):
    script_path = "/home/Karmel/Amit/tonicwanduumnew3finals_new.py"
    return execute_script(request, script_path)


def run_Wanduum_Rsoc_copy_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Wanduum/Wanduum_Rsoc_copy/Run_copy.py"
    return execute_script(request, script_path)




# Taboola page - Tonic Rsoc





def run_newtabyesrsoctonic_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Tonic_Rsoc/newtabyesrsoctonic.py"
    return execute_script(request, script_path)

def run_rsoctonicapple_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Tonic_Rsoc/rsoctonicapple.py"
    return execute_script(request, script_path)




# Taboola page - Inuvo





def run_inuvonewtabyes_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Inuvo/inuvonewtabyes 1.py"
    return execute_script(request, script_path)

def run_inuvoyes_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Inuvo/inuvoyes 1.py"
    return execute_script(request, script_path)




# Taboola page - Explore





def run_newtabyesexp_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Explore/newtabyesexp.py"
    return execute_script(request, script_path)

def run_texplore1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Explore/texplore1.py"
    return execute_script(request, script_path)







    # Compliance




def run_gettingtaboolarsocids_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Compliance/gettingtaboolarsocids.py"
    return execute_script(request, script_path)


def run_taboola_appealcompliancetonic_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Compliance/taboola-appealcompliancetonic.py"
    return execute_script(request, script_path)


def run_taboola_getcomplianceidsfromtonic_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Compliance/taboola-getcomplianceidsfromtonic.py"
    return execute_script(request, script_path)


def run_taboolacomplianceupdater2025_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Compliance/taboolacomplianceupdater2025.py"
    return execute_script(request, script_path)








    # Inuvo Compliance




def run_gettingtaboolainuvoids_2025_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Compliance/gettingtaboolainuvoids_2025.py"
    return execute_script(request, script_path)


def run_taboolacomplianceupdater_inuvo_2025_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Compliance/taboolacomplianceupdater_inuvo_2025.py"
    return execute_script(request, script_path)


def run_taboola_getcomplianceidsfrominuvo_script(request):
    script_path = "/home/Karmel/Amit/Taboola/Compliance/taboola_getcomplianceidsfrominuvo.py"
    return execute_script(request, script_path)





############## Outbrain





def run_Outbrain_14_X_script(request):
    script_path = "/home/Karmel/Karmel/Daily_reports/Outbrain_14_X.py"
    return execute_script(request, script_path)


def run_inuvoyesob_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/inuvoyesob 1.py"
    return execute_script(request, script_path)


def run_obyesinuvo_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/obyesinuvo.py"
    return execute_script(request, script_path)


def run_obyes_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/obyes 1.py"
    return execute_script(request, script_path)


def run_obcreativesl14_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/obcreativesl14 1.py"
    return execute_script(request, script_path)


def run_outbrainNeedToArchive_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/Archived/Archived2.py"
    return execute_script(request, script_path)





    # Compliance




def run_outbrain_appealcompliancetonic_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/Compliance/outbrain-appealcompliancetonic.py"
    return execute_script(request, script_path)


def run_outbrain_appealcompliancetonic_NewStuff_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/Compliance/outbrain-appealcompliancetonic_NewStuff.py"
    return execute_script(request, script_path)


def run_outbrain_getcomplianceidsfromtonic_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/Compliance/outbrain-getcomplianceidsfromtonic.py"
    return execute_script(request, script_path)


def run_outbraincomplianceupdater2025_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/Compliance/outbraincomplianceupdater2025.py"
    return execute_script(request, script_path)





    # Opt




def run_outbrainopt2026_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/Opt/outbrainopt2026.py"
    return execute_script(request, script_path)




############## Facebook





def run_allfbcreatives_script(request):
    script_path = "/home/Karmel/Amit/Facebook/allfbcreatives.py"
    return execute_script(request, script_path)


def run_inuvoyes_newmobile2025api_script(request):
    script_path = "/home/Karmel/Amit/Facebook/inuvoyes-newmobile2025api 1.py"
    return execute_script(request, script_path)


def run_inuvoopt_script(request):
    script_path = "/home/Karmel/Amit/Facebook/inuvoopt 2.py"
    return execute_script(request, script_path)


def run_tonic_fboffers_script(request):
    script_path = "/home/Karmel/Amit/Facebook/tonic-fboffers.py"
    return execute_script(request, script_path)


def run_dailyfb_script(request):
    script_path = "/home/Karmel/Amit/Facebook/dailyfb_test_2.py"
    return execute_script(request, script_path)


def run_fbopt2026_script(request):
    script_path = "/home/Karmel/Amit/Facebook/Optimization/fbopt2026 1.py"
    return execute_script(request, script_path)




    # Compliance




def run_facebook_appealcompliancetonic_script(request):
    script_path = "/home/Karmel/Amit/Facebook/Compliance/facebook-appealcompliancetonic.py"
    return execute_script(request, script_path)


def run_facebook_getcomplianceidsfromtonic_script(request):
    script_path = "/home/Karmel/Amit/Facebook/Compliance/facebook-getcomplianceidsfromtonic.py"
    return execute_script(request, script_path)


def run_facebookcomplianceupdater2025_script(request):
    script_path = "/home/Karmel/Amit/Facebook/Compliance/facebookcomplianceupdater2025.py"
    return execute_script(request, script_path)


def run_facebookcomplianceupdater2025_v2_script(request):
    script_path = "/home/Karmel/Amit/Facebook/Compliance/facebookcomplianceupdater2025-v2.py"
    return execute_script(request, script_path)


def run_getfbtonicids_script(request):
    script_path = "/home/Karmel/Amit/Facebook/Compliance/getfbtonicids.py"
    return execute_script(request, script_path)


def run_facebookcomplianceupdater2025_v3_script(request):
    script_path = "/home/Karmel/Amit/Facebook/Compliance/facebookcomplianceupdater2025_v3.py"
    return execute_script(request, script_path)




    # Reports




def run_FB_GGSH_script(request):
    script_path = "/home/Karmel/Amit/Auto_Runs/Run_FB_GGSH.py"
    return execute_script(request, script_path)





############## Mediago scripts




def run_System_Report_MG_1_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/System Report MG 1.py"
    return execute_script(request, script_path)

def run_mediagocreatecmp_1_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/mediagocreatecmp 1.py"
    return execute_script(request, script_path)

def run_mediagogetallcampaigns_1_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/mediagogetallcampaigns 1.py"
    return execute_script(request, script_path)

def run_mediagoyes_1_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/mediagoyes 1.py"
    return execute_script(request, script_path)

def run_mediagocreatives_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/mediagocreatives.py"
    return execute_script(request, script_path)

def run_mediagoopt_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/mediagoopt 3.py"
    return execute_script(request, script_path)




def run_mediagoyesinuvo_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/mediagoyesinuvo.py"
    return execute_script(request, script_path)

def run_mediagogetallcampaignsinuvo_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/mediagogetallcampaignsinuvo.py"
    return execute_script(request, script_path)

def run_inuvoyes_mediago_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/inuvoyes-mediago 1.py"
    return execute_script(request, script_path)

def run_mediagooptinuvo_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/mediagooptinuvo.py"
    return execute_script(request, script_path)

def run_mediagoinuvocreatives_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/mediagoinuvocreatives.py"
    return execute_script(request, script_path)

def run_mediagocreatecmpnewinuvo_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/mediagocreatecmpnewinuvo.py"
    return execute_script(request, script_path)





    # Compliance




def run_gettingtaboolarsocidsformediago_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/Compliance/gettingtaboolarsocidsformediago.py"
    return execute_script(request, script_path)


def run_getcreativesfromtaboolatomediago_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/Compliance/getcreativesfromtaboolatomediago.py"
    return execute_script(request, script_path)


def run_mediago_getcomplianceidsfromtonic_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/Compliance/mediago-getcomplianceidsfromtonic.py"
    return execute_script(request, script_path)





def run_mediago_getcomplianceforbulkfile_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/Compliance/mediago-getcomplianceforbulkfile.py"
    return execute_script(request, script_path)


def run_uploadtabformediago_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/Compliance/uploadtabformediago.py"
    return execute_script(request, script_path)


def run_uploadtabitemsformediago_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/Compliance/uploadtabitemsformediago.py"
    return execute_script(request, script_path)







def run_MediaGo_Daily_Spend_PAW_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/Reports/MediaGo_Daily_Spend_PAW.py"
    return execute_script(request, script_path)


def run_MediaGo_Creative_PAW_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/Reports/MediaGo_Creative_PAW.py"
    return execute_script(request, script_path)


def run_MediaGo_All_Campaigns_PAW_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/Reports/MediaGo_All_Campaigns_PAW.py"
    return execute_script(request, script_path)


def run_MediaGo_Opt_PAW_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/MediaGo_Opt_PAW.py"
    return execute_script(request, script_path)





############## Poppin scripts





def run_poppintonic_script(request):
    script_path = "/home/Karmel/Amit/Poppin/poppintonic.py"
    return execute_script(request, script_path)

def run_poppinyes_script(request):
    script_path = "/home/Karmel/Amit/Poppin/poppinyes.py"
    return execute_script(request, script_path)

def run_tonic_poppinoffers_script(request):
    script_path = "/home/Karmel/Amit/Poppin/tonic-poppinoffers_new.py"
    return execute_script(request, script_path)

def run_poppintonic_L7_script(request):
    script_path = "/home/Karmel/Amit/Poppin/poppintonic_L7.py"
    return execute_script(request, script_path)

def run_poppincreatecmp2_script(request):
    script_path = "/home/Karmel/Amit/Poppin/poppincreatecmp2 1.py"
    return execute_script(request, script_path)

def run_rsoctoniccreateofferspoppin_script(request):
    script_path = "/home/Karmel/Amit/Poppin/rsoctoniccreateofferspoppin.py"
    return execute_script(request, script_path)




def run_Poppin_Opt_PAW_script(request):
    script_path = "/home/Karmel/Amit/Poppin/Poppin_Opt_PAW.py"
    return execute_script(request, script_path)

def run_Poppin_Upload_PAW_script(request):
    script_path = "/home/Karmel/Amit/Poppin/TeamSheets/Bulk/Poppin_Upload_PAW.py"
    return execute_script(request, script_path)

def run_Poppin_Daily_Spend_PAW_script(request):
    script_path = "/home/Karmel/Amit/Poppin/Reports/Poppin_Daily_Spend_PAW.py"
    return execute_script(request, script_path)


def run_Poppin_Creative_PAW_script(request):
    script_path = "/home/Karmel/Amit/Poppin/Reports/Poppin_Creative_PAW.py"
    return execute_script(request, script_path)



          ##### Poppin X scripts





def Poppin_X_page(request):
    return render(request, 'Poppin_X_page.html')


def run_set_poppinXoffers_callback_script(request):
    script_path = "/home/Karmel/Amit/Poppin/Xpoppin/set_callback.py"
    return execute_script(request, script_path)


def run_tonic_poppinXoffers_script(request):
    script_path = "/home/Karmel/Amit/Poppin/Xpoppin/tonic-poppinXoffers.py"
    return execute_script(request, script_path)


def run_rsoctoniccreateofferspoppinX_script(request):
    script_path = "/home/Karmel/Amit/Poppin/Xpoppin/rsoctoniccreateofferspoppinX.py"
    return execute_script(request, script_path)


def run_poppinX_tonic_daily_script(request):
    script_path = "/home/Karmel/Amit/Poppin/Xpoppin/tonic_daily.py"
    return execute_script(request, script_path)




############## Maximizer scripts





def run_maximizer_createoffer_script(request):
    script_path = "/home/Karmel/Amit/Maximizer/maximizer-createoffer 2.py"
    return execute_script(request, script_path)

def run_maximizer_offersandverticals_script(request):
    script_path = "/home/Karmel/Amit/Maximizer/maximizer-offersandverticals 1.py"
    return execute_script(request, script_path)

def run_maximizerrevsites30days_script(request):
    script_path = "/home/Karmel/Amit/Maximizer/maximizerrevsites30days 1.py"
    return execute_script(request, script_path)

def run_maximizerrevyes_script(request):
    script_path = "/home/Karmel/Amit/Maximizer/maximizerrevyes 1.py"
    return execute_script(request, script_path)

def run_newtabyesmaximizer_script(request):
    script_path = "/home/Karmel/Amit/Maximizer/newtabyesmaximizer 1.py"
    return execute_script(request, script_path)

def run_tabautoopt_maximizer_script(request):
    script_path = "/home/Karmel/Amit/Maximizer/tabautoopt-maximizer 1.py"
    return execute_script(request, script_path)






############## Google scripts






def run_googleadsyesspend_script(request):
    script_path = "/home/Karmel/Amit/Google/googleadsyesspend.py"
    return execute_script(request, script_path)

def run_googleadscomb2_script(request):
    script_path = "/home/Karmel/Amit/Google/googleadscomb2.py"
    return execute_script(request, script_path)


def run_googleurls_script(request):
    script_path = "/home/Karmel/Amit/Google/googleurls.py"
    return execute_script(request, script_path)


def run_rsoctonicoffersggl_script(request):
    script_path = "/home/Karmel/Amit/Google/rsoctonicoffersggl-new2024 2.py"
    return execute_script(request, script_path)


def run_gglpctsmax_script(request):
    script_path = "/home/Karmel/Amit/Google/gglpctsmax.py"
    return execute_script(request, script_path)


def run_gglpctsdemandgen_script(request):
    script_path = "/home/Karmel/Amit/Google/gglpctsdemandgen.py"
    return execute_script(request, script_path)









def run_allgoogleyes_v2_script(request):
    script_path = "/home/Karmel/Amit/Google/allgoogleyes-v2.py"
    return execute_script(request, script_path)


def run_googlenospendl7days_script(request):
    script_path = "/home/Karmel/Amit/Google/googlenospendl7days.py"
    return execute_script(request, script_path)


def run_allgoogleyes_v2_Shinez_script(request):
    script_path = "/home/Karmel/Amit/Google/allgoogleyes-v2-shinez.py"
    return execute_script(request, script_path)


def run_googlenospendl7days_Shinez_script(request):
    script_path = "/home/Karmel/Amit/Google/googlenospendl7days-shinez.py"
    return execute_script(request, script_path)


def run_googleopt2026_script(request):
    script_path = "/home/Karmel/Amit/Google/googleopt2026 1.py"
    return execute_script(request, script_path)











    # Compliance




def run_gettingtaboolarsocidsforgoogle_script(request):
    script_path = "/home/Karmel/Amit/Google/Compliance/gettingtaboolarsocidsforgoogle.py"
    return execute_script(request, script_path)


def run_google_getcomplianceidsfromtonic_script(request):
    script_path = "/home/Karmel/Amit/Google/Compliance/google-getcomplianceidsfromtonic.py"
    return execute_script(request, script_path)


def run_getcreativesfromtaboolatogoogle_script(request):
    script_path = "/home/Karmel/Amit/Google/Compliance/getcreativesfromtaboolatogoogle.py"
    return execute_script(request, script_path)




def run_blockplacementsonggl_script(request):
    script_path = "/home/Karmel/Amit/Google/blockplacementsonggl.py"
    return execute_script(request, script_path)





    # Send To Taboola




def run_uploadtabforgenfile_script(request):
    script_path = "/home/Karmel/Amit/Google/SendtoTaboola/uploadtabforgenfile.py"
    return execute_script(request, script_path)


def run_uploadtabitemsforgenfile_script(request):
    script_path = "/home/Karmel/Amit/Google/SendtoTaboola/uploadtabitemsforgenfile.py"
    return execute_script(request, script_path)


def run_genfile_getcomplianceresults_script(request):
    script_path = "/home/Karmel/Amit/Google/SendtoTaboola/genfile-getcomplianceresults.py"
    return execute_script(request, script_path)



############## Newsbreak scripts






def run_rsoctoniccreateofferesnewsbreak_script(request):
    script_path = "/home/Karmel/Amit/Newsbreak/rsoctoniccreateofferesnewsbreak.py"
    return execute_script(request, script_path)

def run_tonic_newsbreakoffers_script(request):
    script_path = "/home/Karmel/Amit/Newsbreak/tonic-newsbreakoffers.py"
    return execute_script(request, script_path)


def run_set_callback_script(request):
    script_path = "/home/Karmel/Amit/Newsbreak/set_callback.py"
    return execute_script(request, script_path)


def run_newsbreakopt1_script(request):
    script_path = "/home/Karmel/Amit/Newsbreak/newsbreakopt1.py"
    return execute_script(request, script_path)


def run_newsbreakuploader_script(request):
    script_path = "/home/Karmel/Amit/Newsbreak/newsbreakuploader.py"
    return execute_script(request, script_path)



def run_newsbreakadsetdaily_script(request):
    script_path = "/home/Karmel/Amit/Newsbreak/newsbreakadsetdaily.py"
    return execute_script(request, script_path)


def run_newsbreakadsetsdata_script(request):
    script_path = "/home/Karmel/Amit/Newsbreak/newsbreakadsetsdata.py"
    return execute_script(request, script_path)


def run_newsbreakdaily2_script(request):
    script_path = "/home/Karmel/Amit/Newsbreak/newsbreakdaily2.py"
    return execute_script(request, script_path)




############## Twitter






def run_inuvoyes_new2025api_script(request):
    script_path = "/home/Karmel/Amit/Twitter/inuvoyes-new2025api.py"
    return execute_script(request, script_path)

def run_twitter_createcmp2025_script(request):
    script_path = "/home/Karmel/Amit/Twitter/twitter-createcmp2025_new.py"
    return execute_script(request, script_path)


def run_twitteropt_script(request):
    script_path = "/home/Karmel/Amit/Twitter/twitteropt.py"
    return execute_script(request, script_path)


def run_twitterreports_script(request):
    script_path = "/home/Karmel/Amit/Twitter/twitterreports.py"
    return execute_script(request, script_path)


def run_twitteryes_script(request):
    script_path = "/home/Karmel/Amit/Twitter/twitteryes.py"
    return execute_script(request, script_path)





############## Bulk - Creative




def run_DescriptionGPT_script(request):
    script_path = "/home/Karmel/Amit/creative/DescriptionGPT.py"
    return execute_script(request, script_path)


def run_GoogleHeadlines3_script(request):
    script_path = "/home/Karmel/Amit/creative/GoogleHeadlines3.py"
    return execute_script(request, script_path)


def run_Google__ImagesCutHeadlines3_script(request):
    script_path = "/home/Karmel/Amit/creative/Google__ImagesCutHeadlines3.py"
    return execute_script(request, script_path)


def run_MediaGOAutoGPT_script(request):
    script_path = "/home/Karmel/Amit/creative/MediaGOAutoGPT.py"
    return execute_script(request, script_path)


def run_MediaGoCreateAndCutImg_script(request):
    script_path = "/home/Karmel/Amit/creative/MediaGoCreateAndCutImg 1.py"
    return execute_script(request, script_path)


def run_KWCityCheck_script(request):
    script_path = "/home/Karmel/Amit/creative/KWCityCheck.py"
    return execute_script(request, script_path)


def run_videotozapcap_script(request):
    script_path = "/home/Karmel/Amit/creative/videotozapcap2 2.py"
    return execute_script(request, script_path)


def run_Symphony_create_script(request):
    script_path = "/home/Karmel/Amit/creative/Symphony_create3 2.py"
    return execute_script(request, script_path)


def run_FKGCreateKW_script(request):
    script_path = "/home/Karmel/Amit/creative/FKGCreateKW.py"
    return execute_script(request, script_path)


def run_VertCertDB_script(request):
    script_path = "/home/Karmel/Amit/creative/VertCertDB.py"
    return execute_script(request, script_path)


def run_PolicyCheck_script(request):
    script_path = "/home/Karmel/Amit/creative/PolicyCheck 2.py"
    return execute_script(request, script_path)


def run_MediaGo_ShortHeadlines_script(request):
    script_path = "/home/Karmel/Amit/creative/MediaGo-ShortHeadlines.py"
    return execute_script(request, script_path)


def run_MatanKWdecoder_script(request):
    script_path = "/home/Karmel/Amit/creative/MatanKWdecoder.py"
    return execute_script(request, script_path)


def run_creative_bulk_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk/newpolicycheckforall.py"
    return execute_script(request, script_path)






def run_Jenia_creatives_builder_script(request):
    script_path = "/home/Karmel/Aporia_Networks/workflows/creative_builder_dev/remote/creatives_builder_Jenia_remote.py"
    return execute_script(request, script_path)

#def run_Jenia_creatives_builder_script(request):
#    script_path = "/home/Karmel/Aporia_Networks/workflows/creative_builder_dev/remote/creatives_builder_Jenia_remote.py"
#    return execute_script(request, script_path)

        ########




def run_AutoCreativesWArsocHeadlines_script(request):
    script_path = "/home/Karmel/Amit/creative/AutoCreativesWArsocHeadlines.py"
    return execute_script(request, script_path)


def run_WARSOC_Auto_Creative_Create_IMG_script(request):
    script_path = "/home/Karmel/Amit/creative/Auto_Creative_Create_IMG.py"
    return execute_script(request, script_path)


def run_WARSOC_Auto_Creative_Split_IMG_script(request):
    script_path = "/home/Karmel/Amit/creative/Auto_Creative_Split_IMG.py"
    return execute_script(request, script_path)




def run_AutoCreativesWARSOC1_script(request):
    script_path = "/home/Karmel/Amit/creative/AutoCreativesWARSOC1.py"
    return execute_script(request, script_path)

def run_AutoCreativesWARSOC2_script(request):
    script_path = "/home/Karmel/Amit/creative/AutoCreativesWARSOC2.py"
    return execute_script(request, script_path)

def run_AutoCreativesWARSOC3_script(request):
    script_path = "/home/Karmel/Amit/creative/AutoCreativesWARSOC3.py"
    return execute_script(request, script_path)



        ########




def run_Danilo_videotozapcap_script(request):
    script_path = "/home/Karmel/Amit/creative/videotozapcap2_Danilo.py"
    return execute_script(request, script_path)


def run_Danilo_Symphony_create_script(request):
    script_path = "/home/Karmel/Amit/creative/Symphony_create3_Danilo.py"
    return execute_script(request, script_path)



        ######## Policy




def run_Jenia_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/creative/Policy/newpolicycheckforall.py"
    return execute_script(request, script_path)


def run_Jenia_googlepolicychecker_script(request):
    script_path = "/home/Karmel/Amit/creative/Policy/googlepolicychecker.py"
    return execute_script(request, script_path)


def run_Jenia_gcpgetdataforjenia_script(request):
    script_path = "/home/Karmel/Amit/creative/Policy/gcpgetdataforjenia.py"
    return execute_script(request, script_path)



        ########




def run_Jenia_newautogptforpanglework_script(request):
    script_path = "/home/Karmel/Amit/creative/newautogptforpanglework.py"
    return execute_script(request, script_path)


def run_Jenia_keywordsitallpangle2025_script(request):
    script_path = "/home/Karmel/Amit/creative/keywordsitallpangle2025.py"
    return execute_script(request, script_path)




############## Tiktok





def run_TKTRSOCARTICLEUPDATE_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TKTRSOCARTICLEUPDATE.py"
    return execute_script(request, script_path)


def run_imagegenreationautotiktok_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/imagegenreationautotiktok.py"
    return execute_script(request, script_path)


def run_tonic_tiktokoffers_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/tonic-tiktokoffers.py"
    return execute_script(request, script_path)



     ####



def run_video_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/newpolicycheckforall.py"
    return execute_script(request, script_path)




     ####



def run_Danilo_tonic_tiktokoffers_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/tonic-tiktokoffers_Danilo.py"
    return execute_script(request, script_path)




     ####



def run_imagecreativesforvideo_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/imagecreativesforvideo.py"
    return execute_script(request, script_path)





    # Compliance




def run_tiktok_appealcompliancetonic_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/Compliance/tiktok-appealforcompliancetonic.py"
    return execute_script(request, script_path)


def run_tiktok_getcomplianceidsfromtonic_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/Compliance/tiktok-getcomplianceidsfromtonic.py"
    return execute_script(request, script_path)


def run_tkactivateads_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/Compliance/tkactivateads.py"
    return execute_script(request, script_path)


def run_tkpauseads_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/Compliance/tkpauseads.py"
    return execute_script(request, script_path)


def run_gettiktokids_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/Compliance/gettiktokids.py"
    return execute_script(request, script_path)


    # Opt data update




def run_pangeupdate_only4days_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/pangeupdate-only4days.py"
    return execute_script(request, script_path)


def run_updatepangleoptdata_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/updatepangleoptdata.py"
    return execute_script(request, script_path)



    # Opt data update




def run_gcptoawsvideoconvert_jenia_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/gcptoaws/gcptoawsvideoconvert_jenia.py"
    return execute_script(request, script_path)


def run_gcptoawsvideoconvert_maya_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/gcptoaws/gcptoawsvideoconvert_maya.py"
    return execute_script(request, script_path)


def run_gcptoawsvideoconvert_elran_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/gcptoaws/gcptoawsvideoconvert_elran.py"
    return execute_script(request, script_path)


def run_gcptoawsvideoconvert_Omer_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/gcptoaws/gcptoawsvideoconvert_Omer.py"
    return execute_script(request, script_path)


def run_gcptoawsvideoconvert_matan_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/gcptoaws/gcptoawsvideoconvert_matan.py"
    return execute_script(request, script_path)






############## Duplicator




    # Taboola Duplicator


def run_getalltaboolaidsfordup_script(request):
    script_path = "/home/Karmel/Amit/Amit/bulk_creative/getalltaboolaidsfordup.py"
    return execute_script(request, script_path)


def run_getallcreativesfortabooladup_script(request):
    script_path = "/home/Karmel/Amit/Amit/bulk_creative/getallcreativesfortabooladup.py"
    return execute_script(request, script_path)


def run_getallcampaignsdatafordup_script(request):
    script_path = "/home/Karmel/Amit/Amit/bulk_creative/getallcampaignsdatafordup.py"
    return execute_script(request, script_path)





    # Outbrain Duplicator


def run_getallcampaigndetailsforoutbraindup_script(request):
    script_path = "/home/Karmel/Amit/Amit/bulk_creative/getallcampaigndetailsforoutbraindup_test.py"
    return execute_script(request, script_path)


def run_getallcreativesforoutbraindup_script(request):
    script_path = "/home/Karmel/Amit/Amit/bulk_creative/getallcreativesforoutbraindup_test.py"
    return execute_script(request, script_path)





    # Facebook Duplicator


def run_getallfbcreativesfordup_script(request):
    script_path = "/home/Karmel/Amit/Amit/bulk_creative/getallfbcreativesfordup-feb26.py"
    return execute_script(request, script_path)


def run_getallfbdata_script(request):
    script_path = "/home/Karmel/Amit/Amit/bulk_creative/getallfbdata.py"
    return execute_script(request, script_path)


def run_tonicforfb_script(request):
    script_path = "/home/Karmel/Amit/Amit/bulk_creative/tonicforfb.py"
    return execute_script(request, script_path)




    # Mediago Duplicator


def run_copymediagodata_script(request):
    script_path = "/home/Karmel/Amit/Amit/bulk_creative/copymediagodata.py"
    return execute_script(request, script_path)





    # Poppin Duplicator


def run_copypoppindata_script(request):
    script_path = "/home/Karmel/Amit/Amit/bulk_creative/copypoppindata.py"
    return execute_script(request, script_path)





    # Google Duplicator


def run_l4daysgoogleduplicatordata_script(request):
    script_path = "/home/Karmel/Amit/Amit/bulk_creative/l4daysgoogleduplicatordata.py"
    return execute_script(request, script_path)





    # Wthmm completer


def run_wthmmduplicatorupdate_script(request):
    script_path = "/home/Karmel/Amit/Amit/bulk_creative/wthmmduplicatorupdate.py"
    return execute_script(request, script_path)


def run_wthmmcompleter_script(request):
    script_path = "/home/Karmel/Amit/Amit/bulk_creative/wthmmcompleter.py"
    return execute_script(request, script_path)








def run_wthmmduplicatorupdate_Google_script(request):
    script_path = "/home/Karmel/Amit/Amit/bulk_creative/wthmmduplicatorupdate/wthmmduplicatorupdate_Google.py"
    return execute_script(request, script_path)



def run_wthmmduplicatorupdate_FB_script(request):
    script_path = "/home/Karmel/Amit/Amit/bulk_creative/wthmmduplicatorupdate/wthmmduplicatorupdate_FB.py"
    return execute_script(request, script_path)



def run_wthmmduplicatorupdate_Taboola_script(request):
    script_path = "/home/Karmel/Amit/Amit/bulk_creative/wthmmduplicatorupdate/wthmmduplicatorupdate_Taboola.py"
    return execute_script(request, script_path)



def run_wthmmduplicatorupdate_Outbrain_script(request):
    script_path = "/home/Karmel/Amit/Amit/bulk_creative/wthmmduplicatorupdate/wthmmduplicatorupdate_Outbrain.py"
    return execute_script(request, script_path)



def run_wthmmduplicatorupdate_Poppin_script(request):
    script_path = "/home/Karmel/Amit/Amit/bulk_creative/wthmmduplicatorupdate/wthmmduplicatorupdate_Poppin.py"
    return execute_script(request, script_path)



def run_wthmmduplicatorupdate_MediaGo_script(request):
    script_path = "/home/Karmel/Amit/Amit/bulk_creative/wthmmduplicatorupdate/wthmmduplicatorupdate_MediaGo.py"
    return execute_script(request, script_path)



def run_wthmmduplicatorupdate_TikTok_script(request):
    script_path = "/home/Karmel/Amit/Amit/bulk_creative/wthmmduplicatorupdate/wthmmduplicatorupdate_TikTok.py"
    return execute_script(request, script_path)




















############## GPT scripts





# Store the process globally (or you can use sessions for user-specific control)
global process

process = None  # Initialize as None

# Views to start and stop the GPT executor script
def process_form_page(request):
    global process  # Global process variable to store the running process
    if request.method == 'POST':
        form = GoogleSheetForm(request.POST)
        if form.is_valid():
            # Get the form data
            sheet_id = form.cleaned_data['sheet_id']
            sheet_name = form.cleaned_data['sheet_name']
            import_number = form.cleaned_data['import_number']
            output_number = form.cleaned_data['output_number']
            model_name = form.cleaned_data['model_name']

            # Start the GPT executor script
            try:
                # Call the script using subprocess and pass in the arguments
                script_path = "/home/Karmel/Amit/GPT_executor.py"
                process = subprocess.Popen(
                    ['python3', script_path, sheet_id, sheet_name, str(import_number), str(output_number), model_name],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                return render(request, 'process_form_page.html', {'form': form, 'status': 'Script started!'})
            except Exception as e:
                return render(request, 'process_form_page.html', {'form': form, 'error': str(e)})
    else:
        form = GoogleSheetForm()

    return render(request, 'process_form_page.html', {'form': form})


def stop_script(request):
    global process
    if process:
        try:
            os.kill(process.pid, 9)  # Send the kill signal to stop the process
            process = None  # Reset process
            return render(request, 'process_form_page.html', {'status': 'Script stopped!'})
        except OSError as e:
            return render(request, 'process_form_page.html', {'error': f"Error stopping script: {e}"})
    else:
        return render(request, 'process_form_page.html', {'error': 'No script is running.'})




def run_gpt_executor(sheet_id, sheet_name, import_number, output_number, model_name):
    # This is where you will use subprocess to run the script with the input values
    # For now, I'll include an example subprocess call
    script_path = "/home/Karmel/Amit/GPT_executor.py"

    try:
        # Call the script using subprocess and pass in the arguments (from the form input)
        result = subprocess.run(
            ['python3', script_path, sheet_id, sheet_name, str(import_number), str(output_number), model_name],
            capture_output=True, text=True
        )
        return result.stdout  # Return the script output to be displayed
    except Exception as e:
        raise RuntimeError(f"Script failed to execute: {str(e)}")


# # Helper function to execute scripts
# def execute_script(request, script_path):
#     try:
#         # Run the script using subprocess
#         result = subprocess.run(["python3", script_path], capture_output=True, text=True)
#         output = result.stdout

#         return HttpResponse(f"Script executed successfully. Output: {output}")
#     except Exception as e:
#         return HttpResponse(f"An error occurred: {str(e)}")



# Global variables to hold process instances for each script
global process_part1
global process_part2

process_part1 = None  # Initialize as None
process_part2 = None  # Initialize as None


# View to render the Part 1 page
def gpt_part1_page(request):
    return render(request, 'gpt_part1_page.html')

# View to render the Part 2 page
def gpt_part2_page(request):
    return render(request, 'gpt_part2_page.html')

# Start script for Part 1
def run_gpt_part1_script(request):
    global process_part1
    script_path = "/home/Karmel/Amit/auto-gpt-articles-ed_Part_1.py"
    try:
        process_part1 = subprocess.Popen(['python3', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return render(request, 'gpt_executor_page.html', {'status': 'Script 1 started!'})
    except Exception as e:
        return render(request, 'gpt_executor_page.html', {'error': str(e)})

# Stop script for Part 1
def stop_gpt_part1_script(request):
    global process_part1
    if process_part1:
        try:
            os.kill(process_part1.pid, 9)  # Send kill signal
            process_part1 = None
            return render(request, 'gpt_executor_page.html', {'status': 'Script 1 stopped!'})
        except OSError as e:
            return render(request, 'gpt_executor_page.html', {'error': f"Error stopping script 1: {e}"})
    else:
        return render(request, 'gpt_executor_page.html', {'error': 'No script is running.'})

# Start script for Part 2
def run_gpt_part2_script(request):
    global process_part2
    script_path = "/home/Karmel/Amit/auto-gpt-articles-ed_Part_2.py"
    try:
        process_part2 = subprocess.Popen(['python3', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return render(request, 'gpt_executor_page.html', {'status': 'Script 2 started!'})
    except Exception as e:
        return render(request, 'gpt_executor_page.html', {'error': str(e)})

# Stop script for Part 2
def stop_gpt_part2_script(request):
    global process_part2
    if process_part2:
        try:
            os.kill(process_part2.pid, 9)  # Send kill signal
            process_part2 = None
            return render(request, 'gpt_executor_page.html', {'status': 'Script 2 stopped!'})
        except OSError as e:
            return render(request, 'gpt_executor_page.html', {'error': f"Error stopping script 2: {e}"})
    else:
        return render(request, 'gpt_executor_page.html', {'error': 'No script is running.'})






########################################################



def karmel_reports_page(request):
    return render(request, 'karmel_reports_page.html')

def amit_scripts_page(request):
    return render(request, 'amit_scripts_page.html')

def gpt_executor_page(request):
    return render(request, 'gpt_executor_page.html')

def mediago_page(request):
    return render(request, 'Mediago_page_2.html')

def run_scripts_page(request):
    return run_reports(request)

def outbrain_page(request):
    return render(request, "outbrain_page.html")

def zemanta_page(request):
    return render(request, "zemanta_page.html")

def taboola_page(request):
    return render(request, "taboola_page.html")

def poppin_page(request):
    return render(request, "Poppin_page.html")

def maximizer_page(request):
    return render(request, "maximizer_page.html")

def google_page(request):
    return render(request, "google_page.html")

def facebook_page(request):
    return render(request, "facebook_page.html")

def twitter_page(request):
    return render(request, "twitter_page.html")

def newsbreak_page(request):
    return render(request, "Newsbreak_page.html")

def creative_page(request):
    return render(request, "creative_page.html")

def tiktok_page(request):
    return render(request, "tiktok_page.html")

def amir_page(request):
    return render(request, "amir_page.html")

def duplicator_page(request):
    return render(request, "duplicator_page.html")

def sharon_page(request):
    return render(request, "sharon_page.html")

def mgid_page(request):
    return render(request, "mgid_page.html")

def sasha_page(request):
    return render(request, "sasha_page.html")

def rss_articles_db_page(request):
    return render(request, "rss_articles_db_page.html")

def run_fetch_all_articles_summaries_script(request):
    script_path = "/home/Karmel/Aporia_Networks/workflows/articles_db_fetcher/fetch_all_articles_summaries.py"
    return execute_script(request, script_path)

def run_fetch_specific_articles_with_content_script(request):
    script_path = "/home/Karmel/Aporia_Networks/workflows/articles_db_fetcher/fetch_specific_articles_with_content.py"
    return execute_script(request, script_path)

def run_articles_db_manager_script(request):
    script_path = "/home/Karmel/Aporia_Networks/workflows/articles_db_fetcher/articles_db_manager.py"
    return execute_script(request, script_path)

def media_buyers_scripts(request):
    return render(request, "media_buyers_scripts.html")



# Define your passwords
OUTBRAIN_PASSWORD = "outbrain_pass"
ZEMANTA_PASSWORD = "zemanta_pass"
TABOOLA_PASSWORD = "taboola_pass"
AMIT_SCRIPTS_PASSWORD = "amit_pass"
MEDIAGO_PASSWORD = "mediago_pass"
POPPIN_PASSWORD = "poppin_pass"


# Password prompt and validation views
def outbrain_password(request):
    if request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["password"] == OUTBRAIN_PASSWORD:
                return redirect('outbrain_page')
            else:
                return render(request, "password_prompt.html", {"form": form, "error": "Incorrect password."})
    else:
        form = PasswordForm()
    return render(request, "password_prompt.html", {"form": form})

def zemanta_password(request):
    if request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["password"] == ZEMANTA_PASSWORD:
                return redirect('zemanta_page')
            else:
                return render(request, "password_prompt.html", {"form": form, "error": "Incorrect password."})
    else:
        form = PasswordForm()
    return render(request, "password_prompt.html", {"form": form})

def taboola_password(request):
    if request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["password"] == TABOOLA_PASSWORD:
                return redirect('taboola_page')
            else:
                return render(request, "password_prompt.html", {"form": form, "error": "Incorrect password."})
    else:
        form = PasswordForm()
    return render(request, "password_prompt.html", {"form": form})




# Password prompt and validation views for Amit Scripts
def amit_scripts_password(request):
    if request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["password"] == AMIT_SCRIPTS_PASSWORD:
                return redirect('amit_scripts_page')
            else:
                return render(request, "password_prompt.html", {"form": form, "error": "Incorrect password."})
    else:
        form = PasswordForm()
    return render(request, "password_prompt.html", {"form": form})

# Password prompt and validation views for Mediago Page
def mediago_password(request):
    if request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["password"] == MEDIAGO_PASSWORD:
                return redirect('mediago_page')
            else:
                return render(request, "password_prompt.html", {"form": form, "error": "Incorrect password."})
    else:
        form = PasswordForm()
    return render(request, "password_prompt.html", {"form": form})

# Password prompt and validation views for Mediago Page
def poppin_password(request):
    if request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["password"] == POPPIN_PASSWORD:
                return redirect('poppin_page')
            else:
                return render(request, "password_prompt.html", {"form": form, "error": "Incorrect password."})
    else:
        form = PasswordForm()
    return render(request, "password_prompt.html", {"form": form})




############## Taboola  team



    # Taboola page - Bulk



def taboola_Bulk_page(request):
    return render(request, 'taboola_team/Bulk.html')


def run_bulk_tonic_taboolaoffers_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk/tonic-taboolaoffers.py"
    return execute_script(request, script_path)


def run_bulk_rsoctoniccreateofferestaboola_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk/rsoctoniccreateofferestaboola.py"
    return execute_script(request, script_path)


def run_bulk_maxbidstaboola_UPCPCS1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk/maxbidstaboola_UPCPCS1.py"
    return execute_script(request, script_path)


def run_bulk_maxbidstaboola_UPCPCRSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk/maxbidstaboola_UPCPCRSOC.py"
    return execute_script(request, script_path)


def run_bulk_maxbidstaboola_UPCPC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk/maxbidstaboola_UPCPC.py"
    return execute_script(request, script_path)


def run_bulk_maxbidstaboola_UPCPCINU_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk/maxbidstaboola_UPCPCINU.py"
    return execute_script(request, script_path)







def run_bulk_tabduplicatorfortest_s1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk/tabduplicatorfortest_s1.py"
    return execute_script(request, script_path)


def run_bulk_tabduplicatorfortest_Inuvo_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk/tabduplicatorfortest_Inuvo.py"
    return execute_script(request, script_path)


def run_bulk_tabduplicatorfortest_AFD_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk/tabduplicatorfortest_AFD.py"
    return execute_script(request, script_path)


def run_bulk_tabduplicatorfortest_RSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk/tabduplicatorfortest_RSOC.py"
    return execute_script(request, script_path)


def run_bulk_tabduplicatorfortest_TC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk/tabduplicatorfortest_TC.py"
    return execute_script(request, script_path)







def run_bulk_upload_taboola_creatives_S1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk/upload_taboola_creatives_S1.py"
    return execute_script(request, script_path)

def run_bulk_upload_taboola_creatives_TC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk/upload_taboola_creatives_TC.py"
    return execute_script(request, script_path)

def run_bulk_upload_taboola_creatives_RSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk/upload_taboola_creatives_RSOC.py"
    return execute_script(request, script_path)

def run_bulk_upload_taboola_creatives_Inuvo_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk/upload_taboola_creatives_Inuvo.py"
    return execute_script(request, script_path)




def run_taboola_bulk_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk/newpolicycheckforall.py"
    return execute_script(request, script_path)







def run_taboola_bulk__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_taboola_bulk__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk/tc_channelsdb.py"
    return execute_script(request, script_path)


    # Taboola page - Bulk2



def taboola_Bulk2_page(request):
    return render(request, 'taboola_team/Bulk2.html')


def run_bulk2_tonic_taboolaoffers_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk2/tonic-taboolaoffers.py"
    return execute_script(request, script_path)


def run_bulk2_rsoctoniccreateofferestaboola_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk2/rsoctoniccreateofferestaboola.py"
    return execute_script(request, script_path)


def run_bulk2_maxbidstaboola_UPCPCS1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk2/maxbidstaboola_UPCPCS1.py"
    return execute_script(request, script_path)


def run_bulk2_maxbidstaboola_UPCPCRSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk2/maxbidstaboola_UPCPCRSOC.py"
    return execute_script(request, script_path)


def run_bulk2_maxbidstaboola_UPCPC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk2/maxbidstaboola_UPCPC.py"
    return execute_script(request, script_path)


def run_bulk2_maxbidstaboola_UPCPCINU_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk2/maxbidstaboola_UPCPCINU.py"
    return execute_script(request, script_path)


def run_bulk2_FKG_R_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk2/FKG-R.py"
    return execute_script(request, script_path)


def run_bulk2_KWCity_R_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk2/KWCity-R.py"
    return execute_script(request, script_path)






def run_bulk2_tabduplicatorfortest_s1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk2/tabduplicatorfortest_s1.py"
    return execute_script(request, script_path)


def run_bulk2_tabduplicatorfortest_Inuvo_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk2/tabduplicatorfortest_Inuvo.py"
    return execute_script(request, script_path)


def run_bulk2_tabduplicatorfortest_AFD_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk2/tabduplicatorfortest_AFD.py"
    return execute_script(request, script_path)


def run_bulk2_tabduplicatorfortest_RSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk2/tabduplicatorfortest_RSOC.py"
    return execute_script(request, script_path)





    # Taboola page - Bulk_3



def taboola_Bulk_3_page(request):
    return render(request, 'taboola_team/Bulk_3.html')


def run_Bulk_3_tonic_taboolaoffers_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk_3/tonic-taboolaoffers.py"
    return execute_script(request, script_path)


def run_Bulk_3_rsoctoniccreateofferestaboola_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk_3/rsoctoniccreateofferestaboola.py"
    return execute_script(request, script_path)


def run_Bulk_3_maxbidstaboola_UPCPCS1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk_3/maxbidstaboola_UPCPCS1.py"
    return execute_script(request, script_path)


def run_Bulk_3_maxbidstaboola_UPCPCRSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk_3/maxbidstaboola_UPCPCRSOC.py"
    return execute_script(request, script_path)


def run_Bulk_3_maxbidstaboola_UPCPC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk_3/maxbidstaboola_UPCPC.py"
    return execute_script(request, script_path)


def run_Bulk_3_maxbidstaboola_UPCPCINU_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk_3/maxbidstaboola_UPCPCINU.py"
    return execute_script(request, script_path)







def run_Bulk_3_tabduplicatorfortest_s1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk_3/tabduplicatorfortest_s1.py"
    return execute_script(request, script_path)


def run_Bulk_3_tabduplicatorfortest_Inuvo_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk_3/tabduplicatorfortest_Inuvo.py"
    return execute_script(request, script_path)


def run_Bulk_3_tabduplicatorfortest_AFD_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk_3/tabduplicatorfortest_AFD.py"
    return execute_script(request, script_path)


def run_Bulk_3_tabduplicatorfortest_RSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk_3/tabduplicatorfortest_RSOC.py"
    return execute_script(request, script_path)


def run_Bulk_3_tabduplicatorfortest_TC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk_3/tabduplicatorfortest_TC.py"
    return execute_script(request, script_path)







def run_Bulk_3_upload_taboola_creatives_S1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk_3/upload_taboola_creatives_S1.py"
    return execute_script(request, script_path)


def run_Bulk_3_upload_taboola_creatives_TC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk_3/upload_taboola_creatives_TC.py"
    return execute_script(request, script_path)


def run_Bulk_3_upload_taboola_creatives_RSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk_3/upload_taboola_creatives_RSOC.py"
    return execute_script(request, script_path)


def run_Bulk_3_upload_taboola_creatives_Inuvo_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk_3/upload_taboola_creatives_Inuvo.py"
    return execute_script(request, script_path)






def run_taboola_Bulk_3_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk_3/newpolicycheckforall.py"
    return execute_script(request, script_path)







def run_taboola_Bulk_3__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk_3/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_taboola_Bulk_3__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Bulk_3/tc_channelsdb.py"
    return execute_script(request, script_path)








    # Taboola page - Matan



def taboola_Matan_page(request):
    return render(request, 'taboola_team/Matan.html')


def run_Matan_tonic_taboolaoffers_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Matan/tonic-taboolaoffers.py"
    return execute_script(request, script_path)


def run_Matan_rsoctoniccreateofferestaboola_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Matan/rsoctoniccreateofferestaboola.py"
    return execute_script(request, script_path)


def run_Matan_maxbidstaboola_UPCPCS1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Matan/maxbidstaboola_UPCPCS1.py"
    return execute_script(request, script_path)


def run_Matan_maxbidstaboola_UPCPCRSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Matan/maxbidstaboola_UPCPCRSOC.py"
    return execute_script(request, script_path)


def run_Matan_maxbidstaboola_UPCPC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Matan/maxbidstaboola_UPCPC.py"
    return execute_script(request, script_path)


def run_Matan_maxbidstaboola_UPCPCINU_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Matan/maxbidstaboola_UPCPCINU.py"
    return execute_script(request, script_path)






def run_Matan_tabduplicatorfortest_s1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Matan/tabduplicatorfortest_s1.py"
    return execute_script(request, script_path)


def run_Matan_tabduplicatorfortest_Inuvo_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Matan/tabduplicatorfortest_Inuvo.py"
    return execute_script(request, script_path)


def run_Matan_tabduplicatorfortest_AFD_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Matan/tabduplicatorfortest_AFD.py"
    return execute_script(request, script_path)


def run_Matan_tabduplicatorfortest_RSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Matan/tabduplicatorfortest_RSOC.py"
    return execute_script(request, script_path)


def run_Matan_tabduplicatorfortest_TC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Matan/tabduplicatorfortest_TC.py"
    return execute_script(request, script_path)





def run_taboola_Matan_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Matan/newpolicycheckforall.py"
    return execute_script(request, script_path)




def run_Matan_gcpgetdataforjenia_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Matan/gcpgetdataforjenia.py"
    return execute_script(request, script_path)







def run_taboola_Matan__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Matan/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_taboola_Matan__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Matan/tc_channelsdb.py"
    return execute_script(request, script_path)


    # Taboola page - Omer



def taboola_Omer_page(request):
    return render(request, 'taboola_team/Omer.html')


def run_Omer_tonic_taboolaoffers_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Omer/tonic-taboolaoffers.py"
    return execute_script(request, script_path)


def run_Omer_rsoctoniccreateofferestaboola_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Omer/rsoctoniccreateofferestaboola.py"
    return execute_script(request, script_path)


def run_Omer_maxbidstaboola_UPCPCS1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Omer/maxbidstaboola_UPCPCS1.py"
    return execute_script(request, script_path)


def run_Omer_maxbidstaboola_UPCPCRSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Omer/maxbidstaboola_UPCPCRSOC.py"
    return execute_script(request, script_path)


def run_Omer_maxbidstaboola_UPCPC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Omer/maxbidstaboola_UPCPC.py"
    return execute_script(request, script_path)


def run_Omer_maxbidstaboola_UPCPCINU_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Omer/maxbidstaboola_UPCPCINU.py"
    return execute_script(request, script_path)






def run_Omer_tabduplicatorfortest_s1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Omer/tabduplicatorfortest_s1.py"
    return execute_script(request, script_path)


def run_Omer_tabduplicatorfortest_Inuvo_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Omer/tabduplicatorfortest_Inuvo.py"
    return execute_script(request, script_path)


def run_Omer_tabduplicatorfortest_AFD_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Omer/tabduplicatorfortest_AFD.py"
    return execute_script(request, script_path)


def run_Omer_tabduplicatorfortest_RSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Omer/tabduplicatorfortest_RSOC.py"
    return execute_script(request, script_path)


def run_Omer_tabduplicatorfortest_TC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Omer/tabduplicatorfortest_TC.py"
    return execute_script(request, script_path)




def run_taboola_Omer_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Omer/newpolicycheckforall.py"
    return execute_script(request, script_path)




def run_Omer_gcpgetdataforjenia_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Omer/gcpgetdataforjenia.py"
    return execute_script(request, script_path)








def run_taboola_Omer__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Omer/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_taboola_Omer__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Omer/tc_channelsdb.py"
    return execute_script(request, script_path)


    # Taboola page - Elad



def taboola_Elad_page(request):
    return render(request, 'taboola_team/Elad.html')


def run_Elad_tonic_taboolaoffers_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elad/tonic-taboolaoffers.py"
    return execute_script(request, script_path)


def run_Elad_rsoctoniccreateofferestaboola_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elad/rsoctoniccreateofferestaboola.py"
    return execute_script(request, script_path)


def run_Elad_maxbidstaboola_UPCPCS1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elad/maxbidstaboola_UPCPCS1.py"
    return execute_script(request, script_path)


def run_Elad_maxbidstaboola_UPCPCRSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elad/maxbidstaboola_UPCPCRSOC.py"
    return execute_script(request, script_path)


def run_Elad_maxbidstaboola_UPCPC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elad/maxbidstaboola_UPCPC.py"
    return execute_script(request, script_path)


def run_Elad_maxbidstaboola_UPCPCINU_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elad/maxbidstaboola_UPCPCINU.py"
    return execute_script(request, script_path)






def run_Elad_tabduplicatorfortest_s1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elad/tabduplicatorfortest_s1.py"
    return execute_script(request, script_path)


def run_Elad_tabduplicatorfortest_Inuvo_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elad/tabduplicatorfortest_Inuvo.py"
    return execute_script(request, script_path)


def run_Elad_tabduplicatorfortest_AFD_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elad/tabduplicatorfortest_AFD.py"
    return execute_script(request, script_path)


def run_Elad_tabduplicatorfortest_RSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elad/tabduplicatorfortest_RSOC.py"
    return execute_script(request, script_path)


def run_Elad_tabduplicatorfortest_TC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elad/tabduplicatorfortest_TC.py"
    return execute_script(request, script_path)




def run_taboola_Elad_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elad/newpolicycheckforall.py"
    return execute_script(request, script_path)




def run_Elad_gcpgetdataforjenia_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elad/gcpgetdataforjenia.py"
    return execute_script(request, script_path)







def run_taboola_Elad__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elad/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_taboola_Elad__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elad/tc_channelsdb.py"
    return execute_script(request, script_path)







def run_Elad_upload_taboola_creatives_S1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elad/upload_taboola_creatives_S1.py"
    return execute_script(request, script_path)


def run_Elad_upload_taboola_creatives_TC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elad/upload_taboola_creatives_TC.py"
    return execute_script(request, script_path)


def run_Elad_upload_taboola_creatives_RSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elad/upload_taboola_creatives_RSOC.py"
    return execute_script(request, script_path)


def run_Elad_upload_taboola_creatives_Inuvo_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elad/upload_taboola_creatives_Inuvo.py"
    return execute_script(request, script_path)






    # Taboola page - Elran



def taboola_Elran_page(request):
    return render(request, 'taboola_team/Elran.html')


def run_Elran_tonic_taboolaoffers_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elran/tonic-taboolaoffers.py"
    return execute_script(request, script_path)


def run_Elran_rsoctoniccreateofferestaboola_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elran/rsoctoniccreateofferestaboola.py"
    return execute_script(request, script_path)


def run_Elran_maxbidstaboola_UPCPCS1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elran/maxbidstaboola_UPCPCS1.py"
    return execute_script(request, script_path)


def run_Elran_maxbidstaboola_UPCPCRSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elran/maxbidstaboola_UPCPCRSOC.py"
    return execute_script(request, script_path)


def run_Elran_maxbidstaboola_UPCPC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elran/maxbidstaboola_UPCPC.py"
    return execute_script(request, script_path)


def run_Elran_maxbidstaboola_UPCPCINU_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elran/maxbidstaboola_UPCPCINU.py"
    return execute_script(request, script_path)






def run_Elran_tabduplicatorfortest_s1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elran/tabduplicatorfortest_s1.py"
    return execute_script(request, script_path)


def run_Elran_tabduplicatorfortest_Inuvo_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elran/tabduplicatorfortest_Inuvo.py"
    return execute_script(request, script_path)


def run_Elran_tabduplicatorfortest_AFD_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elran/tabduplicatorfortest_AFD.py"
    return execute_script(request, script_path)


def run_Elran_tabduplicatorfortest_RSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elran/tabduplicatorfortest_RSOC.py"
    return execute_script(request, script_path)


def run_Elran_tabduplicatorfortest_TC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elran/tabduplicatorfortest_TC.py"
    return execute_script(request, script_path)




def run_taboola_Elran_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elran/newpolicycheckforall.py"
    return execute_script(request, script_path)








def run_taboola_Elran__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elran/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_taboola_Elran__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elran/tc_channelsdb.py"
    return execute_script(request, script_path)







def run_Elran_upload_taboola_creatives_S1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elran/upload_taboola_creatives_S1.py"
    return execute_script(request, script_path)


def run_Elran_upload_taboola_creatives_TC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elran/upload_taboola_creatives_TC.py"
    return execute_script(request, script_path)


def run_Elran_upload_taboola_creatives_RSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elran/upload_taboola_creatives_RSOC.py"
    return execute_script(request, script_path)


def run_Elran_upload_taboola_creatives_Inuvo_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Elran/upload_taboola_creatives_Inuvo.py"
    return execute_script(request, script_path)




    # Taboola page - Maya



def taboola_Maya_page(request):
    return render(request, 'taboola_team/Maya.html')


def run_Maya_tonic_taboolaoffers_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Maya/tonic-taboolaoffers.py"
    return execute_script(request, script_path)


def run_Maya_rsoctoniccreateofferestaboola_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Maya/rsoctoniccreateofferestaboola.py"
    return execute_script(request, script_path)


def run_Maya_maxbidstaboola_UPCPCS1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Maya/maxbidstaboola_UPCPCS1.py"
    return execute_script(request, script_path)


def run_Maya_maxbidstaboola_UPCPCRSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Maya/maxbidstaboola_UPCPCRSOC.py"
    return execute_script(request, script_path)


def run_Maya_maxbidstaboola_UPCPC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Maya/maxbidstaboola_UPCPC.py"
    return execute_script(request, script_path)


def run_Maya_maxbidstaboola_UPCPCINU_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Maya/maxbidstaboola_UPCPCINU.py"
    return execute_script(request, script_path)


def run_Maya_tabautooptshitty_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Maya/tabautooptshitty.py"
    return execute_script(request, script_path)


def run_Maya_tabautooptsourcestonic_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Maya/tabautooptsourcestonic.py"
    return execute_script(request, script_path)






def run_Maya_tabduplicatorfortest_s1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Maya/tabduplicatorfortest_s1.py"
    return execute_script(request, script_path)


def run_Maya_tabduplicatorfortest_Inuvo_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Maya/tabduplicatorfortest_Inuvo.py"
    return execute_script(request, script_path)


def run_Maya_tabduplicatorfortest_AFD_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Maya/tabduplicatorfortest_AFD.py"
    return execute_script(request, script_path)


def run_Maya_tabduplicatorfortest_RSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Maya/tabduplicatorfortest_RSOC.py"
    return execute_script(request, script_path)


def run_Maya_tabduplicatorfortest_TC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Maya/tabduplicatorfortest_TC.py"
    return execute_script(request, script_path)







def run_Maya_upload_taboola_creatives_S1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Maya/upload_taboola_creatives_S1.py"
    return execute_script(request, script_path)

def run_Maya_upload_taboola_creatives_TC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Maya/upload_taboola_creatives_TC.py"
    return execute_script(request, script_path)

def run_Maya_upload_taboola_creatives_RSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Maya/upload_taboola_creatives_RSOC.py"
    return execute_script(request, script_path)

def run_Maya_upload_taboola_creatives_Inuvo_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Maya/upload_taboola_creatives_Inuvo.py"
    return execute_script(request, script_path)




def run_taboola_Maya_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Maya/newpolicycheckforall.py"
    return execute_script(request, script_path)








def run_taboola_Maya__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Maya/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_taboola_Maya__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Maya/tc_channelsdb.py"
    return execute_script(request, script_path)



    # Taboola page - Dina



def taboola_Dina_page(request):
    return render(request, 'taboola_team/Dina.html')


def run_Dina_tonic_taboolaoffers_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Dina/tonic-taboolaoffers.py"
    return execute_script(request, script_path)


def run_Dina_rsoctoniccreateofferestaboola_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Dina/rsoctoniccreateofferestaboola.py"
    return execute_script(request, script_path)


def run_Dina_maxbidstaboola_UPCPCS1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Dina/maxbidstaboola_UPCPCS1.py"
    return execute_script(request, script_path)


def run_Dina_maxbidstaboola_UPCPCRSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Dina/maxbidstaboola_UPCPCRSOC.py"
    return execute_script(request, script_path)


def run_Dina_maxbidstaboola_UPCPC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Dina/maxbidstaboola_UPCPC.py"
    return execute_script(request, script_path)


def run_Dina_maxbidstaboola_UPCPCINU_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Dina/maxbidstaboola_UPCPCINU.py"
    return execute_script(request, script_path)






def run_Dina_tabduplicatorfortest_s1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Dina/tabduplicatorfortest_s1.py"
    return execute_script(request, script_path)


def run_Dina_tabduplicatorfortest_Inuvo_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Dina/tabduplicatorfortest_Inuvo.py"
    return execute_script(request, script_path)


def run_Dina_tabduplicatorfortest_AFD_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Dina/tabduplicatorfortest_AFD.py"
    return execute_script(request, script_path)


def run_Dina_tabduplicatorfortest_RSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Dina/tabduplicatorfortest_RSOC.py"
    return execute_script(request, script_path)


def run_Dina_tabduplicatorfortest_TC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Dina/tabduplicatorfortest_TC.py"
    return execute_script(request, script_path)




def run_taboola_Dina_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Dina/newpolicycheckforall.py"
    return execute_script(request, script_path)








def run_taboola_Dina__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Dina/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_taboola_Dina__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Dina/tc_channelsdb.py"
    return execute_script(request, script_path)







def run_Dina_upload_taboola_creatives_S1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Dina/upload_taboola_creatives_S1.py"
    return execute_script(request, script_path)


def run_Dina_upload_taboola_creatives_TC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Dina/upload_taboola_creatives_TC.py"
    return execute_script(request, script_path)


def run_Dina_upload_taboola_creatives_RSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Dina/upload_taboola_creatives_RSOC.py"
    return execute_script(request, script_path)


def run_Dina_upload_taboola_creatives_Inuvo_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Dina/upload_taboola_creatives_Inuvo.py"
    return execute_script(request, script_path)




    # Taboola page - Or



def taboola_Or_page(request):
    return render(request, 'taboola_team/Or.html')


def run_Or_tonic_taboolaoffers_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Or/tonic-taboolaoffers.py"
    return execute_script(request, script_path)


def run_Or_rsoctoniccreateofferestaboola_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Or/rsoctoniccreateofferestaboola.py"
    return execute_script(request, script_path)


def run_Or_maxbidstaboola_UPCPCS1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Or/maxbidstaboola_UPCPCS1.py"
    return execute_script(request, script_path)


def run_Or_maxbidstaboola_UPCPCRSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Or/maxbidstaboola_UPCPCRSOC.py"
    return execute_script(request, script_path)


def run_Or_maxbidstaboola_UPCPC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Or/maxbidstaboola_UPCPC.py"
    return execute_script(request, script_path)


def run_Or_maxbidstaboola_UPCPCINU_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Or/maxbidstaboola_UPCPCINU.py"
    return execute_script(request, script_path)








def run_Or_tabduplicatorfortest_s1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Or/tabduplicatorfortest_s1.py"
    return execute_script(request, script_path)


def run_Or_tabduplicatorfortest_Inuvo_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Or/tabduplicatorfortest_Inuvo.py"
    return execute_script(request, script_path)


def run_Or_tabduplicatorfortest_AFD_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Or/tabduplicatorfortest_AFD.py"
    return execute_script(request, script_path)


def run_Or_tabduplicatorfortest_RSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Or/tabduplicatorfortest_RSOC.py"
    return execute_script(request, script_path)


def run_Or_tabduplicatorfortest_TC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Or/tabduplicatorfortest_TC.py"
    return execute_script(request, script_path)





def run_taboola_Or_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Or/newpolicycheckforall.py"
    return execute_script(request, script_path)









def run_taboola_Or__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Or/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_taboola_Or__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Or/tc_channelsdb.py"
    return execute_script(request, script_path)







def run_Or_upload_taboola_creatives_S1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Or/upload_taboola_creatives_S1.py"
    return execute_script(request, script_path)


def run_Or_upload_taboola_creatives_TC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Or/upload_taboola_creatives_TC.py"
    return execute_script(request, script_path)


def run_Or_upload_taboola_creatives_RSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Or/upload_taboola_creatives_RSOC.py"
    return execute_script(request, script_path)


def run_Or_upload_taboola_creatives_Inuvo_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Or/upload_taboola_creatives_Inuvo.py"
    return execute_script(request, script_path)




    # Taboola page - Yoav



def taboola_Yoav_page(request):
    return render(request, 'taboola_team/Yoav.html')


def run_Yoav_tonic_taboolaoffers_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Yoav/tonic-taboolaoffers.py"
    return execute_script(request, script_path)


def run_Yoav_rsoctoniccreateofferestaboola_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Yoav/rsoctoniccreateofferestaboola.py"
    return execute_script(request, script_path)


def run_Yoav_maxbidstaboola_UPCPCS1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Yoav/maxbidstaboola_UPCPCS1.py"
    return execute_script(request, script_path)


def run_Yoav_maxbidstaboola_UPCPCRSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Yoav/maxbidstaboola_UPCPCRSOC.py"
    return execute_script(request, script_path)


def run_Yoav_maxbidstaboola_UPCPC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Yoav/maxbidstaboola_UPCPC.py"
    return execute_script(request, script_path)


def run_Yoav_maxbidstaboola_UPCPCINU_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Yoav/maxbidstaboola_UPCPCINU.py"
    return execute_script(request, script_path)






def run_Yoav_tabduplicatorfortest_s1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Yoav/tabduplicatorfortest_s1.py"
    return execute_script(request, script_path)


def run_Yoav_tabduplicatorfortest_Inuvo_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Yoav/tabduplicatorfortest_Inuvo.py"
    return execute_script(request, script_path)


def run_Yoav_tabduplicatorfortest_AFD_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Yoav/tabduplicatorfortest_AFD.py"
    return execute_script(request, script_path)


def run_Yoav_tabduplicatorfortest_RSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Yoav/tabduplicatorfortest_RSOC.py"
    return execute_script(request, script_path)


def run_Yoav_tabduplicatorfortest_TC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Yoav/tabduplicatorfortest_TC.py"
    return execute_script(request, script_path)




def run_taboola_Yoav_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Yoav/newpolicycheckforall.py"
    return execute_script(request, script_path)


def run_Yoav_gcpgetdataforjenia_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Yoav/gcpgetdataforjenia.py"
    return execute_script(request, script_path)







def run_taboola_Yoav__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Yoav/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_taboola_Yoav__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Yoav/tc_channelsdb.py"
    return execute_script(request, script_path)







def run_Yoav_upload_taboola_creatives_S1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Yoav/upload_taboola_creatives_S1.py"
    return execute_script(request, script_path)


def run_Yoav_upload_taboola_creatives_TC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Yoav/upload_taboola_creatives_TC.py"
    return execute_script(request, script_path)


def run_Yoav_upload_taboola_creatives_RSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Yoav/upload_taboola_creatives_RSOC.py"
    return execute_script(request, script_path)


def run_Yoav_upload_taboola_creatives_Inuvo_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Yoav/upload_taboola_creatives_Inuvo.py"
    return execute_script(request, script_path)








    # Taboola page - Ilana



def taboola_Ilana_page(request):
    return render(request, 'taboola_team/Ilana.html')


def run_Ilana_tonic_taboolaoffers_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Ilana/tonic-taboolaoffers.py"
    return execute_script(request, script_path)


def run_Ilana_rsoctoniccreateofferestaboola_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Ilana/rsoctoniccreateofferestaboola.py"
    return execute_script(request, script_path)


def run_Ilana_maxbidstaboola_UPCPCS1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Ilana/maxbidstaboola_UPCPCS1.py"
    return execute_script(request, script_path)


def run_Ilana_maxbidstaboola_UPCPCRSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Ilana/maxbidstaboola_UPCPCRSOC.py"
    return execute_script(request, script_path)


def run_Ilana_maxbidstaboola_UPCPC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Ilana/maxbidstaboola_UPCPC.py"
    return execute_script(request, script_path)


def run_Ilana_maxbidstaboola_UPCPCINU_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Ilana/maxbidstaboola_UPCPCINU.py"
    return execute_script(request, script_path)


    # Taboola page - Dor



def taboola_Dor_page(request):
    return render(request, 'taboola_team/Dor.html')


def run_Dor_tonic_taboolaoffers_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Dor/tonic-taboolaoffers.py"
    return execute_script(request, script_path)


def run_Dor_rsoctoniccreateofferestaboola_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Dor/rsoctoniccreateofferestaboola.py"
    return execute_script(request, script_path)


def run_Dor_maxbidstaboola_UPCPCS1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Dor/maxbidstaboola_UPCPCS1.py"
    return execute_script(request, script_path)


def run_Dor_maxbidstaboola_UPCPCRSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Dor/maxbidstaboola_UPCPCRSOC.py"
    return execute_script(request, script_path)


def run_Dor_maxbidstaboola_UPCPC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Dor/maxbidstaboola_UPCPC.py"
    return execute_script(request, script_path)


def run_Dor_maxbidstaboola_UPCPCINU_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Dor/maxbidstaboola_UPCPCINU.py"
    return execute_script(request, script_path)




    # Taboola page - Batel



def taboola_Batel_page(request):
    return render(request, 'taboola_team/Batel.html')


def run_Batel_tonic_taboolaoffers_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Batel/tonic-taboolaoffers.py"
    return execute_script(request, script_path)


def run_Batel_rsoctoniccreateofferestaboola_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Batel/rsoctoniccreateofferestaboola.py"
    return execute_script(request, script_path)


def run_Batel_maxbidstaboola_UPCPCS1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Batel/maxbidstaboola_UPCPCS1.py"
    return execute_script(request, script_path)


def run_Batel_maxbidstaboola_UPCPCRSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Batel/maxbidstaboola_UPCPCRSOC.py"
    return execute_script(request, script_path)


def run_Batel_maxbidstaboola_UPCPC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Batel/maxbidstaboola_UPCPC.py"
    return execute_script(request, script_path)


def run_Batel_maxbidstaboola_UPCPCINU_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Batel/maxbidstaboola_UPCPCINU.py"
    return execute_script(request, script_path)




    # Taboola page - Nofar



def taboola_Nofar_page(request):
    return render(request, 'taboola_team/Nofar.html')


def run_Nofar_tonic_taboolaoffers_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Nofar/tonic-taboolaoffers.py"
    return execute_script(request, script_path)


def run_Nofar_rsoctoniccreateofferestaboola_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Nofar/rsoctoniccreateofferestaboola.py"
    return execute_script(request, script_path)


def run_Nofar_maxbidstaboola_UPCPCS1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Nofar/maxbidstaboola_UPCPCS1.py"
    return execute_script(request, script_path)


def run_Nofar_maxbidstaboola_UPCPCRSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Nofar/maxbidstaboola_UPCPCRSOC.py"
    return execute_script(request, script_path)


def run_Nofar_maxbidstaboola_UPCPC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Nofar/maxbidstaboola_UPCPC.py"
    return execute_script(request, script_path)


def run_Nofar_maxbidstaboola_UPCPCINU_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Nofar/maxbidstaboola_UPCPCINU.py"
    return execute_script(request, script_path)






############## Outbrain team











    # Outbrain page - Bulk



def outbrain_Bulk_page(request):
    return render(request, 'outbrain_team/Bulk.html')


def run_Bulk_rsoctoniccreateofferesoutbrain_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Bulk/rsoctoniccreateofferesoutbrain.py"
    return execute_script(request, script_path)


def run_Bulk_tonic_outbrainoffers_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Bulk/tonic_outbrainoffers.py"
    return execute_script(request, script_path)





def run_KWCityCheckL_script(request):
    script_path = "/home/Karmel/Amit/creative/KWCityCheckL.py"
    return execute_script(request, script_path)


def run_ShortenHeadlinesL_script(request):
    script_path = "/home/Karmel/Amit/creative/ShortenHeadlinesL.py"
    return execute_script(request, script_path)


def run_FKGOz2_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Bulk/FKGOz2.py"
    return execute_script(request, script_path)




def run_outbrain_bulk_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Bulk/newpolicycheckforall.py"
    return execute_script(request, script_path)


def run_outbrain_bulk_gcpgetdataforjenia_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Bulk/gcpgetdataforjenia.py"
    return execute_script(request, script_path)



def run_outbrain_bulk__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Bulk/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_outbrain_bulk__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Bulk/tc_channelsdb.py"
    return execute_script(request, script_path)




def run_bulk_outbrain_uploader_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Bulk/outbrain_uploader.py"
    return execute_script(request, script_path)





    # Outbrain page - Slavo



def outbrain_Slavo_page(request):
    return render(request, 'outbrain_team/Slavo.html')


def run_Slavo_rsoctoniccreateofferesoutbrain_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Slavo/rsoctoniccreateofferesoutbrain.py"
    return execute_script(request, script_path)


def run_Slavo_tonic_outbrainoffers_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Slavo/tonic_outbrainoffers.py"
    return execute_script(request, script_path)



def run_outbrain_Slavo_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Slavo/newpolicycheckforall.py"
    return execute_script(request, script_path)


def run_Slavo_gcpgetdataforjenia_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Slavo/gcpgetdataforjenia.py"
    return execute_script(request, script_path)





def run_outbrain_Slavo__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Slavo/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_outbrain_Slavo__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Slavo/tc_channelsdb.py"
    return execute_script(request, script_path)


    # Outbrain page - Jelena



def outbrain_Jelena_page(request):
    return render(request, 'outbrain_team/Jelena.html')


def run_Jelena_rsoctoniccreateofferesoutbrain_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Jelena/rsoctoniccreateofferesoutbrain.py"
    return execute_script(request, script_path)


def run_Jelena_tonic_outbrainoffers_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Jelena/tonic_outbrainoffers.py"
    return execute_script(request, script_path)



def run_outbrain_Jelena_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Jelena/newpolicycheckforall.py"
    return execute_script(request, script_path)


def run_Jelena_gcpgetdataforjenia_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Jelena/gcpgetdataforjenia.py"
    return execute_script(request, script_path)








def run_outbrain_Jelena__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Jelena/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_outbrain_Jelena__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Jelena/tc_channelsdb.py"
    return execute_script(request, script_path)


    # Outbrain page - Dimitrije



def outbrain_Dimitrije_page(request):
    return render(request, 'outbrain_team/Dimitrije.html')


def run_Dimitrije_rsoctoniccreateofferesoutbrain_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Dimitrije/rsoctoniccreateofferesoutbrain.py"
    return execute_script(request, script_path)


def run_Dimitrije_tonic_outbrainoffers_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Dimitrije/tonic_outbrainoffers.py"
    return execute_script(request, script_path)



def run_outbrain_Dimitrije_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Dimitrije/newpolicycheckforall.py"
    return execute_script(request, script_path)


def run_Dimitrije_gcpgetdataforjenia_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Dimitrije/gcpgetdataforjenia.py"
    return execute_script(request, script_path)






def run_outbrain_Dimitrije__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Dimitrije/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_outbrain_Dimitrije__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Dimitrije/tc_channelsdb.py"
    return execute_script(request, script_path)








    # Outbrain page - Ivana_K



def outbrain_Ivana_K_page(request):
    return render(request, 'outbrain_team/Ivana_K.html')


def run_Ivana_K_rsoctoniccreateofferesoutbrain_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Ivana K/rsoctoniccreateofferesoutbrain.py"
    return execute_script(request, script_path)


def run_Ivana_K_tonic_outbrainoffers_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Ivana K/tonic_outbrainoffers.py"
    return execute_script(request, script_path)



def run_outbrain_Ivana_K_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Ivana K/newpolicycheckforall.py"
    return execute_script(request, script_path)


def run_Ivana_K_gcpgetdataforjenia_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Ivana K/gcpgetdataforjenia.py"
    return execute_script(request, script_path)






def run_outbrain_Ivana_K__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Ivana K/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_outbrain_Ivana_K__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Ivana K/tc_channelsdb.py"
    return execute_script(request, script_path)






    # Outbrain page - Nemanja


def outbrain_Nemanja_page(request):
    return render(request, 'outbrain_team/Nemanja.html')


def run_Nemanja_rsoctoniccreateofferesoutbrain_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Nemanja/rsoctoniccreateofferesoutbrain.py"
    return execute_script(request, script_path)


def run_Nemanja_tonic_outbrainoffers_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Nemanja/tonic_outbrainoffers.py"
    return execute_script(request, script_path)



def run_outbrain_Nemanja_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Nemanja/newpolicycheckforall.py"
    return execute_script(request, script_path)


def run_Nemanja_gcpgetdataforjenia_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Nemanja/gcpgetdataforjenia.py"
    return execute_script(request, script_path)






def run_outbrain_Nemanja__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Nemanja/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_outbrain_Nemanja__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Nemanja/tc_channelsdb.py"
    return execute_script(request, script_path)










    # Outbrain page - Nadja


def outbrain_Nadja_page(request):
    return render(request, 'outbrain_team/Nadja.html')


def run_Nadja_rsoctoniccreateofferesoutbrain_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Nadja/rsoctoniccreateofferesoutbrain.py"
    return execute_script(request, script_path)


def run_Nadja_tonic_outbrainoffers_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Nadja/tonic_outbrainoffers.py"
    return execute_script(request, script_path)


    # Outbrain page - Bartek



def outbrain_Bartek_page(request):
    return render(request, 'outbrain_team/Bartek.html')


def run_Bartek_rsoctoniccreateofferesoutbrain_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Bartek/rsoctoniccreateofferesoutbrain.py"
    return execute_script(request, script_path)


def run_Bartek_tonic_outbrainoffers_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Bartek/tonic_outbrainoffers.py"
    return execute_script(request, script_path)





    # Outbrain page - Ivana_Z



def outbrain_Ivana_Z_page(request):
    return render(request, 'outbrain_team/Ivana_Z.html')


def run_Ivana_Z_rsoctoniccreateofferesoutbrain_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Ivana Z/rsoctoniccreateofferesoutbrain.py"
    return execute_script(request, script_path)


def run_Ivana_Z_tonic_outbrainoffers_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Ivana Z/tonic_outbrainoffers.py"
    return execute_script(request, script_path)










############## Zemanta team






    # Zemanta page - Bulk



def zemanta_Bulk_page(request):
    return render(request, 'zemanta_team/Bulk.html')


def run_Bulk_rsoctoniccreateoffereszemanta_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Bulk/rsoctoniccreateoffereszemanta.py"
    return execute_script(request, script_path)


def run_Bulk_tonic_zemantaoffers_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Bulk/tonic-zemantaoffers.py"
    return execute_script(request, script_path)


    ## image_cut


def run_Bulk_imagescutob_dup22_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Bulk/imagescutob_dup22.py"
    return execute_script(request, script_path)


def run_Bulk_imagescutob_dupinuvo_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Bulk/imagescutob_dupinuvo.py"
    return execute_script(request, script_path)


def run_Bulk_imagescutob_duprsoc_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Bulk/imagescutob_duprsoc.py"
    return execute_script(request, script_path)


def run_Bulk_imagescutob_dups1_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Bulk/imagescutob_dups1.py"
    return execute_script(request, script_path)



    ##



def run_Bulk_ZemantaDescrip_script(request):
    script_path = "/home/Karmel/Amit/creative/ZemantaDescrip.py"
    return execute_script(request, script_path)


def run_Bulk_ZemantaShorthead_script(request):
    script_path = "/home/Karmel/Amit/creative/ZemantaShorthead.py"
    return execute_script(request, script_path)



    # Zemanta page - Bartek



def zemanta_Bartek_page(request):
    return render(request, 'zemanta_team/Bartek.html')


def run_Bartek_rsoctoniccreateoffereszemanta_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Bartek/rsoctoniccreateoffereszemanta.py"
    return execute_script(request, script_path)


def run_Bartek_tonic_zemantaoffers_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Bartek/tonic-zemantaoffers.py"
    return execute_script(request, script_path)



    ##image_cut


def run_Bartek_imagescutob_dup22_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Bartek/imagescutob_dup22.py"
    return execute_script(request, script_path)


def run_Bartek_imagescutob_dupinuvo_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Bartek/imagescutob_dupinuvo.py"
    return execute_script(request, script_path)


def run_Bartek_imagescutob_duprsoc_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Bartek/imagescutob_duprsoc.py"
    return execute_script(request, script_path)


def run_Bartek_imagescutob_dups1_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Bartek/imagescutob_dups1.py"
    return execute_script(request, script_path)



    # Zemanta page - Nemanja



def zemanta_Nemanja_page(request):
    return render(request, 'zemanta_team/Nemanja.html')


def run_Nemanja_rsoctoniccreateoffereszemanta_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Nemanja/rsoctoniccreateoffereszemanta.py"
    return execute_script(request, script_path)


def run_Nemanja_tonic_zemantaoffers_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Nemanja/tonic-zemantaoffers.py"
    return execute_script(request, script_path)



    ##image_cut


def run_Nemanja_imagescutob_dup22_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Nemanja/imagescutob_dup22.py"
    return execute_script(request, script_path)


def run_Nemanja_imagescutob_dupinuvo_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Nemanja/imagescutob_dupinuvo.py"
    return execute_script(request, script_path)


def run_Nemanja_imagescutob_duprsoc_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Nemanja/imagescutob_duprsoc.py"
    return execute_script(request, script_path)


def run_Nemanja_imagescutob_dups1_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Nemanja/imagescutob_dups1.py"
    return execute_script(request, script_path)



    # Zemanta page - Petar



def zemanta_Petar_page(request):
    return render(request, 'zemanta_team/Petar.html')


def run_Petar_rsoctoniccreateoffereszemanta_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Petar/rsoctoniccreateoffereszemanta.py"
    return execute_script(request, script_path)


def run_Petar_tonic_zemantaoffers_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Petar/tonic-zemantaoffers.py"
    return execute_script(request, script_path)



    ##image_cut


def run_Petar_imagescutob_dup22_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Petar/imagescutob_dup22.py"
    return execute_script(request, script_path)


def run_Petar_imagescutob_dupinuvo_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Petar/imagescutob_dupinuvo.py"
    return execute_script(request, script_path)


def run_Petar_imagescutob_duprsoc_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Petar/imagescutob_duprsoc.py"
    return execute_script(request, script_path)


def run_Petar_imagescutob_dups1_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Petar/imagescutob_dups1.py"
    return execute_script(request, script_path)



    # Zemanta page - Dimitrije



def zemanta_Dimitrije_page(request):
    return render(request, 'zemanta_team/Dimitrije.html')


def run_Dimitrije_rsoctoniccreateoffereszemanta_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Dimitrije/rsoctoniccreateoffereszemanta.py"
    return execute_script(request, script_path)


def run_Dimitrije_tonic_zemantaoffers_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Dimitrije/tonic-zemantaoffers.py"
    return execute_script(request, script_path)




    ##image_cut


def run_Dimitrije_imagescutob_dup22_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Dimitrije/imagescutob_dup22.py"
    return execute_script(request, script_path)


def run_Dimitrije_imagescutob_dupinuvo_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Dimitrije/imagescutob_dupinuvo.py"
    return execute_script(request, script_path)


def run_Dimitrije_imagescutob_duprsoc_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Dimitrije/imagescutob_duprsoc.py"
    return execute_script(request, script_path)


def run_Dimitrije_imagescutob_dups1_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Dimitrije/imagescutob_dups1.py"
    return execute_script(request, script_path)



    # Zemanta page - Nadja



def zemanta_Nadja_page(request):
    return render(request, 'zemanta_team/Nadja.html')


def run_Nadja_rsoctoniccreateoffereszemanta_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Nadja/rsoctoniccreateoffereszemanta.py"
    return execute_script(request, script_path)


def run_Nadja_tonic_zemantaoffers_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Nadja/tonic-zemantaoffers.py"
    return execute_script(request, script_path)


    ##image_cut


def run_Nadja_imagescutob_dup22_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Nadja/imagescutob_dup22.py"
    return execute_script(request, script_path)


def run_Nadja_imagescutob_dupinuvo_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Nadja/imagescutob_dupinuvo.py"
    return execute_script(request, script_path)


def run_Nadja_imagescutob_duprsoc_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Nadja/imagescutob_duprsoc.py"
    return execute_script(request, script_path)


def run_Nadja_imagescutob_dups1_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Nadja/imagescutob_dups1.py"
    return execute_script(request, script_path)



    # Zemanta page - Slavo



def zemanta_Slavo_page(request):
    return render(request, 'zemanta_team/Slavo.html')


def run_Slavo_rsoctoniccreateoffereszemanta_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Slavo/rsoctoniccreateoffereszemanta.py"
    return execute_script(request, script_path)


def run_Slavo_tonic_zemantaoffers_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Slavo/tonic-zemantaoffers.py"
    return execute_script(request, script_path)


    ##image_cut


def run_Slavo_imagescutob_dup22_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Slavo/imagescutob_dup22.py"
    return execute_script(request, script_path)


def run_Slavo_imagescutob_dupinuvo_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Slavo/imagescutob_dupinuvo.py"
    return execute_script(request, script_path)


def run_Slavo_imagescutob_duprsoc_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Slavo/imagescutob_duprsoc.py"
    return execute_script(request, script_path)


def run_Slavo_imagescutob_dups1_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Slavo/imagescutob_dups1.py"
    return execute_script(request, script_path)



    # Zemanta page - Ivana Z



def zemanta_Ivana_Z_page(request):
    return render(request, 'zemanta_team/Ivana_Z.html')


def run_Ivana_Z_rsoctoniccreateoffereszemanta_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Ivana Z/rsoctoniccreateoffereszemanta.py"
    return execute_script(request, script_path)


def run_Ivana_Z_tonic_zemantaoffers_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Ivana Z/tonic-zemantaoffers.py"
    return execute_script(request, script_path)


    ##image_cut


def run_Ivana_Z_imagescutob_dup22_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Ivana Z/imagescutob_dup22.py"
    return execute_script(request, script_path)


def run_Ivana_Z_imagescutob_dupinuvo_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Ivana Z/imagescutob_dupinuvo.py"
    return execute_script(request, script_path)


def run_Ivana_Z_imagescutob_duprsoc_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Ivana Z/imagescutob_duprsoc.py"
    return execute_script(request, script_path)


def run_Ivana_Z_imagescutob_dups1_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Ivana Z/imagescutob_dups1.py"
    return execute_script(request, script_path)



    # Zemanta page - Jelena



def zemanta_Jelena_page(request):
    return render(request, 'zemanta_team/Jelena.html')


def run_Jelena_rsoctoniccreateoffereszemanta_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Jelena/rsoctoniccreateoffereszemanta.py"
    return execute_script(request, script_path)


def run_Jelena_tonic_zemantaoffers_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Jelena/tonic-zemantaoffers.py"
    return execute_script(request, script_path)


    ##image_cut


def run_Jelena_imagescutob_dup22_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Jelena/imagescutob_dup22.py"
    return execute_script(request, script_path)


def run_Jelena_imagescutob_dupinuvo_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Jelena/imagescutob_dupinuvo.py"
    return execute_script(request, script_path)


def run_Jelena_imagescutob_duprsoc_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Jelena/imagescutob_duprsoc.py"
    return execute_script(request, script_path)


def run_Jelena_imagescutob_dups1_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Jelena/imagescutob_dups1.py"
    return execute_script(request, script_path)





    # Zemanta page - Ivana K



def zemanta_Ivana_K_page(request):
    return render(request, 'zemanta_team/Ivana_K.html')


def run_Ivana_K_rsoctoniccreateoffereszemanta_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Ivana K/rsoctoniccreateoffereszemanta.py"
    return execute_script(request, script_path)


def run_Ivana_K_tonic_zemantaoffers_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Ivana K/tonic-zemantaoffers.py"
    return execute_script(request, script_path)


    ##image_cut


def run_Ivana_K_imagescutob_dup22_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Ivana K/imagescutob_dup22.py"
    return execute_script(request, script_path)


def run_Ivana_K_imagescutob_dupinuvo_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Ivana K/imagescutob_dupinuvo.py"
    return execute_script(request, script_path)


def run_Ivana_K_imagescutob_duprsoc_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Ivana K/imagescutob_duprsoc.py"
    return execute_script(request, script_path)


def run_Ivana_K_imagescutob_dups1_script(request):
    script_path = "/home/Karmel/Amit/Zemanta/TeamSheets/Ivana K/imagescutob_dups1.py"
    return execute_script(request, script_path)





############## Google team






    # Google page - Bulk



def google_Bulk_page(request):
    return render(request, 'google_team/Bulk.html')


def run_Bulk_Manual_imagescut_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Bulk/Manual_imagescut.py"
    return execute_script(request, script_path)


def run_Bulk_GoogleCreateve_IMG_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Bulk/GoogleCreateve_IMG.py"
    return execute_script(request, script_path)

def run_Bulk_GoogleCreateve_IMG_Split_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Bulk/GoogleCreateve_IMG_Split.py"
    return execute_script(request, script_path)



def run_Bulk_GoogleGPTCreative_step1_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Bulk/GoogleGPTCreative_step1.py"
    return execute_script(request, script_path)


def run_Bulk_GoogleGPTCreative_step2_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Bulk/GoogleGPTCreative_step2.py"
    return execute_script(request, script_path)





def run_Bulk_GoogleRSoCTonicActiveLinks_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Bulk/GoogleRSoCTonicActiveLinks.py"
    return execute_script(request, script_path)


def run_Bulk_GoogleRSoCTonicCreatLinks_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Bulk/GoogleRSoCTonicCreatLinks.py"
    return execute_script(request, script_path)





def run_google_bulk__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Bulk/tc_channelsdb.py"
    return execute_script(request, script_path)


def run_google_bulk__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Bulk/tc_channels_createnew.py"
    return execute_script(request, script_path)





def run_google_bulk_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Bulk/googlepolicychecker.py"
    return execute_script(request, script_path)





def run_Bulk_google_uploader_v3_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Bulk/google_uploader_v3.py"
    return execute_script(request, script_path)



def run_Bulk_google_uploader_v3_image_test_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Bulk/google_uploader_v3_image_test.py"
    return execute_script(request, script_path)


    # Google page - Maya



def google_Maya_page(request):
    return render(request, 'google_team/Maya.html')


def run_Maya_Manual_imagescut_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Maya/Manual_imagescut.py"
    return execute_script(request, script_path)


def run_Maya_GoogleCreateve_IMG_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Maya/GoogleCreateve_IMG.py"
    return execute_script(request, script_path)

def run_Maya_GoogleCreateve_IMG_Split_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Maya/GoogleCreateve_IMG_Split.py"
    return execute_script(request, script_path)



def run_Maya_GoogleGPTCreative_step1_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Maya/GoogleGPTCreative_step1.py"
    return execute_script(request, script_path)


def run_Maya_GoogleGPTCreative_step2_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Maya/GoogleGPTCreative_step2.py"
    return execute_script(request, script_path)



def run_Maya_GoogleRSoCTonicActiveLinks_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Maya/GoogleRSoCTonicActiveLinks.py"
    return execute_script(request, script_path)


def run_Maya_GoogleRSoCTonicCreatLinks_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Maya/GoogleRSoCTonicCreatLinks.py"
    return execute_script(request, script_path)





def run_google_Maya_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Maya/googlepolicychecker.py"
    return execute_script(request, script_path)



def run_Maya_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Maya/newpolicycheckforall.py"
    return execute_script(request, script_path)


def run_Maya_gcpgetdataforjenia_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Maya/gcpgetdataforjenia.py"
    return execute_script(request, script_path)





def run_google_Maya__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Maya/tc_channelsdb.py"
    return execute_script(request, script_path)


def run_google_Maya__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Maya/tc_channels_createnew.py"
    return execute_script(request, script_path)







def run_Maya_google_uploader_v3_image_test_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Maya/google_uploader_v3_image_test.py"
    return execute_script(request, script_path)




    # Google page - Or



def google_Or_page(request):
    return render(request, 'google_team/Or.html')


def run_Or_Manual_imagescut_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Or/Manual_imagescut.py"
    return execute_script(request, script_path)


def run_Or_Creative_imagescut_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Or/Creative_imagescut.py"
    return execute_script(request, script_path)




def run_Or_google_uploader_v3_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Or/google_uploader_v3_image_test.py"
    return execute_script(request, script_path)





def run_Or_GoogleRSoCTonicActiveLinks_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Or/GoogleRSoCTonicActiveLinks.py"
    return execute_script(request, script_path)


def run_Or_GoogleRSoCTonicCreatLinks_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Or/GoogleRSoCTonicCreatLinks.py"
    return execute_script(request, script_path)





def run_google_Or_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Or/googlepolicychecker.py"
    return execute_script(request, script_path)


def run_Or_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Or/newpolicycheckforall.py"
    return execute_script(request, script_path)


def run_Or_gcpgetdataforjenia_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Or/gcpgetdataforjenia.py"
    return execute_script(request, script_path)





def run_google_Or__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Or/tc_channelsdb.py"
    return execute_script(request, script_path)


def run_google_Or__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Or/tc_channels_createnew.py"
    return execute_script(request, script_path)




    # Google page - Dina



def google_Dina_page(request):
    return render(request, 'google_team/Dina.html')


def run_Dina_Manual_imagescut_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Dina/Manual_imagescut.py"
    return execute_script(request, script_path)


def run_Dina_Creative_imagescut_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Dina/Creative_imagescut.py"
    return execute_script(request, script_path)




def run_Dina_google_uploader_v3_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Dina/google_uploader_v3_image_test.py"
    return execute_script(request, script_path)





def run_Dina_GoogleRSoCTonicActiveLinks_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Dina/GoogleRSoCTonicActiveLinks.py"
    return execute_script(request, script_path)


def run_Dina_GoogleRSoCTonicCreatLinks_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Dina/GoogleRSoCTonicCreatLinks.py"
    return execute_script(request, script_path)







def run_google_Dina_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Dina/googlepolicychecker.py"
    return execute_script(request, script_path)


def run_Dina_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Dina/newpolicycheckforall.py"
    return execute_script(request, script_path)


def run_Dina_gcpgetdataforjenia_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Dina/gcpgetdataforjenia.py"
    return execute_script(request, script_path)





def run_google_Dina__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Dina/tc_channelsdb.py"
    return execute_script(request, script_path)


def run_google_Dina__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Dina/tc_channels_createnew.py"
    return execute_script(request, script_path)




    # Google page - Yoav



def google_Yoav_page(request):
    return render(request, 'google_team/Yoav.html')


def run_Yoav_Manual_imagescut_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Yoav/Manual_imagescut.py"
    return execute_script(request, script_path)


def run_Yoav_Creative_imagescut_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Yoav/Creative_imagescut.py"
    return execute_script(request, script_path)



def run_Yoav_google_uploader_v3_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Yoav/google_uploader_v3_image_test.py.py"
    return execute_script(request, script_path)




def run_Yoav_GoogleRSoCTonicActiveLinks_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Yoav/GoogleRSoCTonicActiveLinks.py"
    return execute_script(request, script_path)


def run_Yoav_GoogleRSoCTonicCreatLinks_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Yoav/GoogleRSoCTonicCreatLinks.py"
    return execute_script(request, script_path)





def run_google_Yoav_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Yoav/googlepolicychecker.py"
    return execute_script(request, script_path)


def run_Yoav_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Yoav/newpolicycheckforall.py"
    return execute_script(request, script_path)


def run_Yoav_gcpgetdataforjenia_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Yoav/gcpgetdataforjenia.py"
    return execute_script(request, script_path)





def run_google_Yoav__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Yoav/tc_channelsdb.py"
    return execute_script(request, script_path)


def run_google_Yoav__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Yoav/tc_channels_createnew.py"
    return execute_script(request, script_path)




    # Google page - Elad



def google_Elad_page(request):
    return render(request, 'google_team/Elad.html')


def run_Elad_Manual_imagescut_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Elad/Manual_imagescut.py"
    return execute_script(request, script_path)


def run_Elad_Creative_imagescut_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Elad/Creative_imagescut.py"
    return execute_script(request, script_path)




def run_Elad_google_uploader_v3_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Elad/google_uploader_v3_image_test.py"
    return execute_script(request, script_path)




def run_Elad_GoogleRSoCTonicActiveLinks_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Elad/GoogleRSoCTonicActiveLinks.py"
    return execute_script(request, script_path)


def run_Elad_GoogleRSoCTonicCreatLinks_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Elad/GoogleRSoCTonicCreatLinks.py"
    return execute_script(request, script_path)





def run_google_Elad_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Elad/googlepolicychecker.py"
    return execute_script(request, script_path)


def run_Elad_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Elad/newpolicycheckforall.py"
    return execute_script(request, script_path)


def run_Elad_gcpgetdataforjenia_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Elad/gcpgetdataforjenia.py"
    return execute_script(request, script_path)





def run_google_Elad__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Elad/tc_channelsdb.py"
    return execute_script(request, script_path)


def run_google_Elad__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Elad/tc_channels_createnew.py"
    return execute_script(request, script_path)










    # Google page - Elran



def google_Elran_page(request):
    return render(request, 'google_team/Elran.html')


def run_Elran_Manual_imagescut_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Elran/Manual_imagescut.py"
    return execute_script(request, script_path)


def run_Elran_Creative_imagescut_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Elran/Creative_imagescut.py"
    return execute_script(request, script_path)




def run_Elran_google_uploader_v3_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Elran/google_uploader_v3_image_test.py"
    return execute_script(request, script_path)





def run_Elran_GoogleRSoCTonicActiveLinks_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Elran/GoogleRSoCTonicActiveLinks.py"
    return execute_script(request, script_path)


def run_Elran_GoogleRSoCTonicCreatLinks_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Elran/GoogleRSoCTonicCreatLinks.py"
    return execute_script(request, script_path)






def run_google_Elran_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Elran/googlepolicychecker.py"
    return execute_script(request, script_path)



def run_Elran_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Elran/newpolicycheckforall.py"
    return execute_script(request, script_path)


def run_Elran_gcpgetdataforjenia_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Elran/gcpgetdataforjenia.py"
    return execute_script(request, script_path)





def run_google_Elran__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Elran/tc_channelsdb.py"
    return execute_script(request, script_path)


def run_google_Elran__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Elran/tc_channels_createnew.py"
    return execute_script(request, script_path)




    # Google page - Omer



def google_Omer_page(request):
    return render(request, 'google_team/Omer.html')


def run_Omer_Manual_imagescut_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Omer/Manual_imagescut.py"
    return execute_script(request, script_path)


def run_Omer_Creative_imagescut_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Omer/Creative_imagescut.py"
    return execute_script(request, script_path)




def run_Omer_GoogleRSoCTonicActiveLinks_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Omer/GoogleRSoCTonicActiveLinks.py"
    return execute_script(request, script_path)


def run_Omer_GoogleRSoCTonicCreatLinks_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Omer/GoogleRSoCTonicCreatLinks.py"
    return execute_script(request, script_path)





def run_google_Omer_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Omer/googlepolicychecker.py"
    return execute_script(request, script_path)



def run_Omer_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Omer/newpolicycheckforall.py"
    return execute_script(request, script_path)




def run_google_Omer__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Omer/tc_channelsdb.py"
    return execute_script(request, script_path)


def run_google_Omer__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Google/TeamSheets/Omer/tc_channels_createnew.py"
    return execute_script(request, script_path)





############## Poppin team


    # Poppin page - Bulk






def run_Poppin_bulk__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Poppin/TeamSheets/Bulk/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_Poppin_bulk__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Poppin/TeamSheets/Bulk/tc_channelsdb.py"
    return execute_script(request, script_path)




    # Poppin page - Elad



def poppin_Elad_page(request):
    return render(request, 'poppin_team/Elad.html')


def run_Elad_rsoctoniccreateofferspoppin_script(request):
    script_path = "/home/Karmel/Amit/Poppin/TeamSheets/Elad/rsoctoniccreateofferspoppin.py"
    return execute_script(request, script_path)


def run_Elad_tonic_poppinoffers_script(request):
    script_path = "/home/Karmel/Amit/Poppin/TeamSheets/Elad/tonic-poppinoffers.py"
    return execute_script(request, script_path)






def run_Poppin_Elad__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Poppin/TeamSheets/Elad/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_Poppin_Elad__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Poppin/TeamSheets/Elad/tc_channelsdb.py"
    return execute_script(request, script_path)



    # Poppin page - Matan



def poppin_Matan_page(request):
    return render(request, 'poppin_team/Matan.html')


def run_Matan_rsoctoniccreateofferspoppin_script(request):
    script_path = "/home/Karmel/Amit/Poppin/TeamSheets/Matan/rsoctoniccreateofferspoppin.py"
    return execute_script(request, script_path)


def run_Matan_tonic_poppinoffers_script(request):
    script_path = "/home/Karmel/Amit/Poppin/TeamSheets/Matan/tonic-poppinoffers.py"
    return execute_script(request, script_path)






def run_Poppin_Matan__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Poppin/TeamSheets/Matan/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_Poppin_Matan__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Poppin/TeamSheets/Matan/tc_channelsdb.py"
    return execute_script(request, script_path)






############## Facebook team






    # Facebook page - Bulk



def facebook_Bulk_page(request):
    return render(request, 'facebook_team/Bulk.html')


def run_Bulk_FBRSoCTonicCreatLinks_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Bulk/FBRSoCTonicCreatLinks.py"
    return execute_script(request, script_path)


def run_Bulk_tonic_FBoffers_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Bulk/tonic-fboffers.py"
    return execute_script(request, script_path)


def run_Bulk_FBRSoCTonicCreatpixel_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Bulk/FBRSoCTonicCreatpixel.py"
    return execute_script(request, script_path)


def run_Bulk_FBRSoCTonicCreat_link_pixel_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Bulk/FBRSoCTonicCreat_link_pixel.py"
    return execute_script(request, script_path)




def run_Bulk_predictochannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Bulk/predictochannels-createnew.py"
    return execute_script(request, script_path)


def run_Bulk_predictochannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Bulk/predictochannelsdb.py"
    return execute_script(request, script_path)


def run_Bulk_Compadochannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Bulk/compadochannels-createnew.py"
    return execute_script(request, script_path)






def run_facebook_Bulk_tc_channels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Bulk/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_facebook_Bulk_tc_channelsdb_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Bulk/tc_channelsdb.py"
    return execute_script(request, script_path)








def run_facebook_Bulk_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Bulk/newpolicycheckforall.py"
    return execute_script(request, script_path)





def run_facebook_Bulk_Extract_TXT_IMG_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Bulk/Extract_TXT_IMG.py"
    return execute_script(request, script_path)





def run_Bulk_fb_uploader_v26_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Bulk/fb_uploader_v26.py"
    return execute_script(request, script_path)


    # Facebook page - Andrea



def facebook_Andrea_page(request):
    return render(request, 'facebook_team/Andrea.html')


def run_Andrea_FBRSoCTonicCreatLinks_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Andrea/FBRSoCTonicCreatLinks.py"
    return execute_script(request, script_path)


def run_Andrea_tonic_FBoffers_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Andrea/tonic-fboffers.py"
    return execute_script(request, script_path)


def run_Andrea_FBRSoCTonicCreatpixel_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Andrea/FBRSoCTonicCreatpixel.py"
    return execute_script(request, script_path)


def run_Andrea_FBRSoCTonicCreat_link_pixel_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Andrea/FBRSoCTonicCreat_link_pixel.py"
    return execute_script(request, script_path)




def run_Andrea_predictochannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Andrea/predictochannels-createnew.py"
    return execute_script(request, script_path)


def run_Andrea_Compadochannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Andrea/compadochannels-createnew.py"
    return execute_script(request, script_path)


def run_Andrea_predictochannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Andrea/predictochannelsdb.py"
    return execute_script(request, script_path)





def run_facebook_Andrea_Extract_TXT_IMG_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Andrea/Extract_TXT_IMG.py"
    return execute_script(request, script_path)



    # Facebook page - Slavo



def facebook_Slavo_page(request):
    return render(request, 'facebook_team/Slavo.html')


def run_Slavo_FBRSoCTonicCreatLinks_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Slavo/FBRSoCTonicCreatLinks.py"
    return execute_script(request, script_path)


def run_Slavo_tonic_FBoffers_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Slavo/tonic-fboffers.py"
    return execute_script(request, script_path)


def run_Slavo_FBRSoCTonicCreatpixel_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Slavo/FBRSoCTonicCreatpixel.py"
    return execute_script(request, script_path)


def run_Slavo_FBRSoCTonicCreat_link_pixel_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Slavo/FBRSoCTonicCreat_link_pixel.py"
    return execute_script(request, script_path)




def run_Slavo_predictochannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Slavo/predictochannels-createnew.py"
    return execute_script(request, script_path)


def run_Slavo_Compadochannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Slavo/compadochannels-createnew.py"
    return execute_script(request, script_path)


def run_Slavo_predictochannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Slavo/predictochannelsdb.py"
    return execute_script(request, script_path)





def run_facebook_Slavo_Extract_TXT_IMG_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Slavo/Extract_TXT_IMG.py"
    return execute_script(request, script_path)



    # Facebook page - Jelena



def facebook_Jelena_page(request):
    return render(request, 'facebook_team/Jelena.html')


def run_Jelena_FBRSoCTonicCreatLinks_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Jelena/FBRSoCTonicCreatLinks.py"
    return execute_script(request, script_path)


def run_Jelena_tonic_FBoffers_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Jelena/tonic-fboffers.py"
    return execute_script(request, script_path)


def run_Jelena_FBRSoCTonicCreatpixel_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Jelena/FBRSoCTonicCreatpixel.py"
    return execute_script(request, script_path)


def run_Jelena_FBRSoCTonicCreat_link_pixel_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Jelena/FBRSoCTonicCreat_link_pixel.py"
    return execute_script(request, script_path)




def run_Jelena_predictochannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Jelena/predictochannels-createnew.py"
    return execute_script(request, script_path)


def run_Jelena_Compadochannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Jelena/compadochannels-createnew.py"
    return execute_script(request, script_path)


def run_Jelena_predictochannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Jelena/predictochannelsdb.py"
    return execute_script(request, script_path)





def run_facebook_Jelena_Extract_TXT_IMG_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Jelena/Extract_TXT_IMG.py"
    return execute_script(request, script_path)



    # Facebook page - Dimitrije



def facebook_Dimitrije_page(request):
    return render(request, 'facebook_team/Dimitrije.html')


def run_Dimitrije_FBRSoCTonicCreatLinks_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Dimitrije/FBRSoCTonicCreatLinks.py"
    return execute_script(request, script_path)


def run_Dimitrije_tonic_FBoffers_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Dimitrije/tonic-fboffers.py"
    return execute_script(request, script_path)


def run_Dimitrije_FBRSoCTonicCreatpixel_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Dimitrije/FBRSoCTonicCreatpixel.py"
    return execute_script(request, script_path)


def run_Dimitrije_FBRSoCTonicCreat_link_pixel_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Dimitrije/FBRSoCTonicCreat_link_pixel.py"
    return execute_script(request, script_path)




def run_Dimitrije_predictochannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Dimitrije/predictochannels-createnew.py"
    return execute_script(request, script_path)


def run_Dimitrije_Compadochannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Dimitrije/compadochannels-createnew.py"
    return execute_script(request, script_path)


def run_Dimitrije_predictochannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Dimitrije/predictochannelsdb.py"
    return execute_script(request, script_path)





def run_facebook_Dimitrije_Extract_TXT_IMG_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Dimitrije/Extract_TXT_IMG.py"
    return execute_script(request, script_path)



    # Facebook page - Ivana_K



def facebook_Ivana_K_page(request):
    return render(request, 'facebook_team/Ivana_K.html')


def run_Ivana_K_FBRSoCTonicCreatLinks_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Ivana K/FBRSoCTonicCreatLinks.py"
    return execute_script(request, script_path)


def run_Ivana_K_tonic_FBoffers_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Ivana K/tonic-fboffers.py"
    return execute_script(request, script_path)


def run_Ivana_K_FBRSoCTonicCreatpixel_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Ivana K/FBRSoCTonicCreatpixel.py"
    return execute_script(request, script_path)


def run_Ivana_K_FBRSoCTonicCreat_link_pixel_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Ivana K/FBRSoCTonicCreat_link_pixel.py"
    return execute_script(request, script_path)




def run_Ivana_K_predictochannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Ivana K/predictochannels-createnew.py"
    return execute_script(request, script_path)


def run_Ivana_K_Compadochannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Ivana K/compadochannels-createnew.py"
    return execute_script(request, script_path)


def run_Ivana_K_predictochannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Ivana K/predictochannelsdb.py"
    return execute_script(request, script_path)





def run_facebook_Ivana_K_Extract_TXT_IMG_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Ivana K/Extract_TXT_IMG.py"
    return execute_script(request, script_path)



    # Facebook page - Nemanja



def facebook_Nemanja_page(request):
    return render(request, 'facebook_team/Nemanja.html')


def run_Nemanja_FBRSoCTonicCreatLinks_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Nemanja/FBRSoCTonicCreatLinks.py"
    return execute_script(request, script_path)


def run_Nemanja_tonic_FBoffers_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Nemanja/tonic-fboffers.py"
    return execute_script(request, script_path)


def run_Nemanja_FBRSoCTonicCreatpixel_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Nemanja/FBRSoCTonicCreatpixel.py"
    return execute_script(request, script_path)


def run_Nemanja_FBRSoCTonicCreat_link_pixel_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Nemanja/FBRSoCTonicCreat_link_pixel.py"
    return execute_script(request, script_path)




def run_Nemanja_predictochannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Nemanja/predictochannels-createnew.py"
    return execute_script(request, script_path)


def run_Nemanja_Compadochannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Nemanja/compadochannels-createnew.py"
    return execute_script(request, script_path)


def run_Nemanja_predictochannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Nemanja/predictochannelsdb.py"
    return execute_script(request, script_path)





def run_facebook_Nemanja_Extract_TXT_IMG_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Nemanja/Extract_TXT_IMG.py"
    return execute_script(request, script_path)













############## MediaGo  team






    # MediaGo page - 2025


def run_rsoccreatetonicoffersmediago_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/TeamSheets/2025/rsoccreatetonicoffersmediago 1.py"
    return execute_script(request, script_path)

def run_tonic_mediagooffers_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/TeamSheets/2025/tonic-mediagooffers 1.py"
    return execute_script(request, script_path)






    # MediaGo page - Bulk



def mediago_Bulk_page(request):
    return render(request, 'mediago_team/Bulk.html')

def run_Bulk_rsoccreatetonicoffersmediago_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/TeamSheets/Bulk/rsoccreatetonicoffersmediago.py"
    return execute_script(request, script_path)

def run_Bulk_tonic_mediagooffers_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/TeamSheets/Bulk/tonic_mediagooffers.py"
    return execute_script(request, script_path)

def run_bulk_MediaGoShortneHeadlines_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/TeamSheets/Bulk/MediaGoShortneHeadlines.py"
    return execute_script(request, script_path)



###


def run_MediaGo_bulk__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/TeamSheets/Bulk/tc_channels_createnew.py"
    return execute_script(request, script_path)

def run_MediaGo_bulk__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/TeamSheets/Bulk/tc_channelsdb.py"
    return execute_script(request, script_path)



###


def run_MediaGo_Upload_PAW_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/TeamSheets/Bulk/MediaGo_Upload_PAW.py"
    return execute_script(request, script_path)



    # MediaGo page - Or



def mediago_Or_page(request):
    return render(request, 'mediago_team/Or.html')

def run_Or_rsoccreatetonicoffersmediago_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/TeamSheets/Or/rsoccreatetonicoffersmediago 1.py"
    return execute_script(request, script_path)

def run_Or_tonic_mediagooffers_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/TeamSheets/Or/tonic-mediagooffers 1.py"
    return execute_script(request, script_path)



###


def run_MediaGo_Or__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/TeamSheets/Or/tc_channels_createnew.py"
    return execute_script(request, script_path)

def run_MediaGo_Or__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/TeamSheets/Or/tc_channelsdb.py"
    return execute_script(request, script_path)






    # MediaGo page - Yoav



def mediago_Yoav_page(request):
    return render(request, 'mediago_team/Yoav.html')

def run_Yoav_rsoccreatetonicoffersmediago_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/TeamSheets/Yoav/rsoccreatetonicoffersmediago 1.py"
    return execute_script(request, script_path)

def run_Yoav_tonic_mediagooffers_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/TeamSheets/Yoav/tonic-mediagooffers 1.py"
    return execute_script(request, script_path)



###


def run_MediaGo_Yoav__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/TeamSheets/Yoav/tc_channels_createnew.py"
    return execute_script(request, script_path)

def run_MediaGo_Yoav__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/TeamSheets/Yoav/tc_channelsdb.py"
    return execute_script(request, script_path)






    # MediaGo page - Omer



def mediago_Omer_page(request):
    return render(request, 'mediago_team/Omer.html')

def run_Omer_rsoccreatetonicoffersmediago_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/TeamSheets/Omer/rsoccreatetonicoffersmediago 1.py"
    return execute_script(request, script_path)

def run_Omer_tonic_mediagooffers_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/TeamSheets/Omer/tonic-mediagooffers 1.py"
    return execute_script(request, script_path)



###


def run_MediaGo_Omer__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/TeamSheets/Omer/tc_channels_createnew.py"
    return execute_script(request, script_path)

def run_MediaGo_Omer__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/TeamSheets/Omer/tc_channelsdb.py"
    return execute_script(request, script_path)






    # MediaGo page - Maya


def mediago_Maya_page(request):
    return render(request, 'mediago_team/Maya.html')

def run_Maya_rsoccreatetonicoffersmediago_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/TeamSheets/Maya/rsoccreatetonicoffersmediago 1.py"
    return execute_script(request, script_path)

def run_Maya_tonic_mediagooffers_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/TeamSheets/Maya/tonic-mediagooffers 1.py"
    return execute_script(request, script_path)



###


def run_MediaGo_Maya__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/TeamSheets/Maya/tc_channels_createnew.py"
    return execute_script(request, script_path)

def run_MediaGo_Maya__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/MediaGo/TeamSheets/Maya/tc_channelsdb.py"
    return execute_script(request, script_path)







############## Tiktok team






    # Tiktok page - Bulk



def tiktok_Bulk_page(request):
    return render(request, 'tiktok_team/Bulk.html')


def run_Bulk_TKRSoCTonicCreat_link_pixel_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Bulk/TKRSoCTonicCreat_link_pixel.py"
    return execute_script(request, script_path)


def run_Bulk_tonic_TKoffers_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Bulk/tonic-tkoffers.py"
    return execute_script(request, script_path)


def run_Bulk_TKRSoCTonicCreatpixel_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Bulk/TKRSoCTonicCreatpixel.py"
    return execute_script(request, script_path)


def run_Bulk_TKRSoCTonicCreatLinks_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Bulk/TKRSoCTonicCreatLinks.py"
    return execute_script(request, script_path)


###


def run_Tiktok_bulk__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Bulk/tc_channels_createnew.py"
    return execute_script(request, script_path)

def run_Tiktok_bulk__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Bulk/tc_channelsdb.py"
    return execute_script(request, script_path)


###


def run_Bulk_TKRSoCTonicCreat_link_pixel_Dup_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Bulk/TKRSoCTonicCreat_link_pixel_Dup.py"
    return execute_script(request, script_path)

def run_Bulk_TKRSoCTonicCreatpixel_Dup_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Bulk/TKRSoCTonicCreatpixel_Dup.py"
    return execute_script(request, script_path)


###


def run_Tiktok_Bulk_Manual_imagescut_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Bulk/Manual_imagescut.py"
    return execute_script(request, script_path)


def run_TikTokCreateScript_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Bulk/TikTokCreateScript.py"
    return execute_script(request, script_path)


###


def run_Bulk_tiktok_ads_uploader_v5_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Bulk/tiktok_ads_uploader_v5.py"
    return execute_script(request, script_path)


def run_Bulk_tiktok_duplicator_2026_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Bulk/tiktok_duplicator_2026.py"
    return execute_script(request, script_path)



    # Tiktok page - Omer



def tiktok_Omer_page(request):
    return render(request, 'tiktok_team/Omer.html')


def run_Omer_TKRSoCTonicCreat_link_pixel_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Omer/TKRSoCTonicCreat_link_pixel.py"
    return execute_script(request, script_path)


def run_Omer_tonic_TKoffers_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Omer/tonic-tkoffers.py"
    return execute_script(request, script_path)


def run_Omer_TKRSoCTonicCreatpixel_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Omer/TKRSoCTonicCreatpixel.py"
    return execute_script(request, script_path)


def run_Omer_TKRSoCTonicCreatLinks_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Omer/TKRSoCTonicCreatLinks.py"
    return execute_script(request, script_path)


###


def run_Tiktok_Omer__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Omer/tc_channels_createnew.py"
    return execute_script(request, script_path)

def run_Tiktok_Omer__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Omer/tc_channelsdb.py"
    return execute_script(request, script_path)






    # Tiktok page - Maya



def tiktok_Maya_page(request):
    return render(request, 'tiktok_team/Maya.html')


def run_Maya_TKRSoCTonicCreat_link_pixel_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Maya/TKRSoCTonicCreat_link_pixel.py"
    return execute_script(request, script_path)


def run_Maya_tonic_TKoffers_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Maya/tonic-tkoffers.py"
    return execute_script(request, script_path)


def run_Maya_TKRSoCTonicCreatpixel_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Maya/TKRSoCTonicCreatpixel.py"
    return execute_script(request, script_path)


def run_Maya_TKRSoCTonicCreatLinks_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Maya/TKRSoCTonicCreatLinks.py"
    return execute_script(request, script_path)


###


def run_Tiktok_Maya__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Maya/tc_channels_createnew.py"
    return execute_script(request, script_path)

def run_Tiktok_Maya__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Maya/tc_channelsdb.py"
    return execute_script(request, script_path)






    # Tiktok page - Matan



def tiktok_Matan_page(request):
    return render(request, 'tiktok_team/Matan.html')


def run_Matan_TKRSoCTonicCreat_link_pixel_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Matan/TKRSoCTonicCreat_link_pixel.py"
    return execute_script(request, script_path)


def run_Matan_tonic_TKoffers_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Matan/tonic-tkoffers.py"
    return execute_script(request, script_path)


def run_Matan_TKRSoCTonicCreatpixel_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Matan/TKRSoCTonicCreatpixel.py"
    return execute_script(request, script_path)


def run_Matan_TKRSoCTonicCreatLinks_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Matan/TKRSoCTonicCreatLinks.py"
    return execute_script(request, script_path)


###


def run_Tiktok_Matan__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Matan/tc_channels_createnew.py"
    return execute_script(request, script_path)

def run_Tiktok_Matan__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Matan/tc_channelsdb.py"
    return execute_script(request, script_path)






    # Tiktok page - Elran



def tiktok_Elran_page(request):
    return render(request, 'tiktok_team/Elran.html')


def run_Elran_TKRSoCTonicCreat_link_pixel_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Elran/TKRSoCTonicCreat_link_pixel.py"
    return execute_script(request, script_path)


def run_Elran_tonic_TKoffers_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Elran/tonic-tkoffers.py"
    return execute_script(request, script_path)


def run_Elran_TKRSoCTonicCreatpixel_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Elran/TKRSoCTonicCreatpixel.py"
    return execute_script(request, script_path)


def run_Elran_TKRSoCTonicCreatLinks_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Elran/TKRSoCTonicCreatLinks.py"
    return execute_script(request, script_path)


###


def run_Tiktok_Elran__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Elran/tc_channels_createnew.py"
    return execute_script(request, script_path)

def run_Tiktok_Elran__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Tiktok/TeamSheets/Elran/tc_channelsdb.py"
    return execute_script(request, script_path)




############## WTHMM team




    # Dimitrije


def run_Dimitrije_keywordsanalyze_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative_2/KW_scripts/Dimitrije/keywordsanalyze.py"
    return execute_script(request, script_path)


def run_Dimitrije_keywordstokeywords_v3_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative_2/KW_scripts/Dimitrije/keywordstokeywords_v3.py"
    return execute_script(request, script_path)




    # Slavo


def run_Slavo_keywordsanalyze_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative_2/KW_scripts/Slavo/keywordsanalyze.py"
    return execute_script(request, script_path)


def run_Slavo_keywordstokeywords_v3_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative_2/KW_scripts/Slavo/keywordstokeywords_v3.py"
    return execute_script(request, script_path)




    # Ivana_K


def run_Ivana_K_keywordsanalyze_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative_2/KW_scripts/Ivana_K/keywordsanalyze.py"
    return execute_script(request, script_path)


def run_Ivana_K_keywordstokeywords_v3_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative_2/KW_scripts/Ivana_K/keywordstokeywords_v3.py"
    return execute_script(request, script_path)




    # Jelena


def run_Jelena_keywordsanalyze_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative_2/KW_scripts/Jelena/keywordsanalyze.py"
    return execute_script(request, script_path)


def run_Jelena_keywordstokeywords_v3_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative_2/KW_scripts/Jelena/keywordstokeywords_v3.py"
    return execute_script(request, script_path)




    # Nemanja


def run_Nemanja_keywordsanalyze_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative_2/KW_scripts/Nemanja/keywordsanalyze.py"
    return execute_script(request, script_path)


def run_Nemanja_keywordstokeywords_v3_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative_2/KW_scripts/Nemanja/keywordstokeywords_v3.py"
    return execute_script(request, script_path)




    # Elad


def run_Elad_keywordsanalyze_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative_2/KW_scripts/Elad/keywordsanalyze.py"
    return execute_script(request, script_path)


def run_Elad_keywordstokeywords_v3_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative_2/KW_scripts/Elad/keywordstokeywords_v3.py"
    return execute_script(request, script_path)


def run_Elad_creatives_builder_script(request):
    script_path = "/home/Karmel/Aporia_Networks/workflows/creative_builder_dev/remote/creatives_builder_Elad_remote.py"
    return execute_script(request, script_path)



    # Elran


def run_Elran_keywordsanalyze_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative_2/KW_scripts/Elran/keywordsanalyze.py"
    return execute_script(request, script_path)


def run_Elran_keywordstokeywords_v3_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative_2/KW_scripts/Elran/keywordstokeywords_v3.py"
    return execute_script(request, script_path)


def run_Elran_creatives_builder_script(request):
    script_path = "/home/Karmel/Aporia_Networks/workflows/creative_builder_dev/remote/creatives_builder_Elran_remote.py"
    return execute_script(request, script_path)



    # Omer


def run_Omer_keywordsanalyze_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative_2/KW_scripts/Omer/keywordsanalyze.py"
    return execute_script(request, script_path)


def run_Omer_keywordstokeywords_v3_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative_2/KW_scripts/Omer/keywordstokeywords_v3.py"
    return execute_script(request, script_path)


def run_Omer_creatives_builder_script(request):
    script_path = "/home/Karmel/Aporia_Networks/workflows/creative_builder_dev/remote/creatives_builder_Omer_remote.py"
    return execute_script(request, script_path)



    # Dina


def run_Dina_keywordsanalyze_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative_2/KW_scripts/Dina/keywordsanalyze.py"
    return execute_script(request, script_path)


def run_Dina_keywordstokeywords_v3_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative_2/KW_scripts/Dina/keywordstokeywords_v3.py"
    return execute_script(request, script_path)


def run_Dina_creatives_builder_script(request):
    script_path = "/home/Karmel/Aporia_Networks/workflows/creative_builder_dev/remote/creatives_builder_Dina_remote.py"
    return execute_script(request, script_path)



    # Yoav


def run_Yoav_keywordsanalyze_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative_2/KW_scripts/Yoav/keywordsanalyze.py"
    return execute_script(request, script_path)


def run_Yoav_keywordstokeywords_v3_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative_2/KW_scripts/Yoav/keywordstokeywords_v3.py"
    return execute_script(request, script_path)


def run_Yoav_creatives_builder_script(request):
    script_path = "/home/Karmel/Aporia_Networks/workflows/creative_builder_dev/remote/creatives_builder_Yoav_remote.py"
    return execute_script(request, script_path)



    # Matan


def run_Matan_keywordsanalyze_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative_2/KW_scripts/Matan/keywordsanalyze.py"
    return execute_script(request, script_path)


def run_Matan_keywordstokeywords_v3_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative_2/KW_scripts/Matan/keywordstokeywords_v3.py"
    return execute_script(request, script_path)




    # Or


def run_Or_keywordsanalyze_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative_2/KW_scripts/Or/keywordsanalyze.py"
    return execute_script(request, script_path)


def run_Or_keywordstokeywords_v3_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative_2/KW_scripts/Or/keywordstokeywords_v3.py"
    return execute_script(request, script_path)


def run_Or_creatives_builder_script(request):
    script_path = "/home/Karmel/Aporia_Networks/workflows/creative_builder_dev/remote/creatives_builder_Or_remote.py"
    return execute_script(request, script_path)

def run_Sasha_creatives_builder_script(request):
    script_path = "/home/Karmel/Aporia_Networks/workflows/creative_builder_dev/api_runners/creatives_builder_Sasha_api.py"
    return execute_script(request, script_path)



    # Maya


def run_Maya_keywordsanalyze_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative_2/KW_scripts/Maya/keywordsanalyze.py"
    return execute_script(request, script_path)


def run_Maya_keywordstokeywords_v3_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative_2/KW_scripts/Maya/keywordstokeywords_v3.py"
    return execute_script(request, script_path)


def run_Maya_creatives_builder_script(request):
    script_path = "/home/Karmel/Aporia_Networks/workflows/creative_builder_dev/remote/creatives_builder_Maya_remote.py"
    return execute_script(request, script_path)


























########################################################################




    #### Elad #####


def media_buyer_Elad_page(request):
    return render(request, 'media_buyers/Elad.html')


    #### Facebook



def run_Elad_FBRSoCTonicCreatLinks_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Elad/FBRSoCTonicCreatLinks.py"
    return execute_script(request, script_path)


def run_Elad_tonic_FBoffers_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Elad/tonic-fboffers.py"
    return execute_script(request, script_path)


def run_Elad_FBRSoCTonicCreatpixel_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Elad/FBRSoCTonicCreatpixel.py"
    return execute_script(request, script_path)


def run_Elad_FBRSoCTonicCreat_link_pixel_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Elad/FBRSoCTonicCreat_link_pixel.py"
    return execute_script(request, script_path)





def run_facebook_Elad_tc_channels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Elad/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_facebook_Elad_tc_channelsdb_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Elad/tc_channelsdb.py"
    return execute_script(request, script_path)


def run_facebook_Elad_Extract_TXT_IMG_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Elad/Extract_TXT_IMG.py"
    return execute_script(request, script_path)






def run_Elad_fb_uploader_v26_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Elad/fb_uploader_v26.py"
    return execute_script(request, script_path)








    #### Outbrain




def run_Elad_rsoctoniccreateofferesoutbrain_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Elad/rsoctoniccreateofferesoutbrain.py"
    return execute_script(request, script_path)


def run_Elad_tonic_outbrainoffers_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Elad/tonic_outbrainoffers.py"
    return execute_script(request, script_path)





def run_outbrain_Elad__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Elad/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_outbrain_Elad__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Elad/tc_channelsdb.py"
    return execute_script(request, script_path)





def run_Elad_outbrain_uploader_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Elad/outbrain_uploader.py"
    return execute_script(request, script_path)










    #### Or #####


def media_buyer_Or_page(request):
    return render(request, 'media_buyers/Or.html')


    #### Facebook



def run_Or_FBRSoCTonicCreatLinks_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Or/FBRSoCTonicCreatLinks.py"
    return execute_script(request, script_path)


def run_Or_tonic_FBoffers_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Or/tonic-fboffers.py"
    return execute_script(request, script_path)


def run_Or_FBRSoCTonicCreatpixel_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Or/FBRSoCTonicCreatpixel.py"
    return execute_script(request, script_path)


def run_Or_FBRSoCTonicCreat_link_pixel_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Or/FBRSoCTonicCreat_link_pixel.py"
    return execute_script(request, script_path)





def run_facebook_Or_tc_channels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Or/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_facebook_Or_tc_channelsdb_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Or/tc_channelsdb.py"
    return execute_script(request, script_path)


def run_facebook_Or_Extract_TXT_IMG_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Or/Extract_TXT_IMG.py"
    return execute_script(request, script_path)






def run_Or_fb_uploader_v26_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Or/fb_uploader_v26.py"
    return execute_script(request, script_path)








    #### Outbrain




def run_Or_rsoctoniccreateofferesoutbrain_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Or/rsoctoniccreateofferesoutbrain.py"
    return execute_script(request, script_path)


def run_Or_tonic_outbrainoffers_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Or/tonic_outbrainoffers.py"
    return execute_script(request, script_path)





def run_outbrain_Or__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Or/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_outbrain_Or__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Or/tc_channelsdb.py"
    return execute_script(request, script_path)





def run_Or_outbrain_uploader_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Or/outbrain_uploader.py"
    return execute_script(request, script_path)





    #### Yoav #####


def media_buyer_Yoav_page(request):
    return render(request, 'media_buyers/Yoav.html')


    #### Facebook



def run_Yoav_FBRSoCTonicCreatLinks_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Yoav/FBRSoCTonicCreatLinks.py"
    return execute_script(request, script_path)


def run_Yoav_tonic_FBoffers_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Yoav/tonic-fboffers.py"
    return execute_script(request, script_path)


def run_Yoav_FBRSoCTonicCreatpixel_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Yoav/FBRSoCTonicCreatpixel.py"
    return execute_script(request, script_path)


def run_Yoav_FBRSoCTonicCreat_link_pixel_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Yoav/FBRSoCTonicCreat_link_pixel.py"
    return execute_script(request, script_path)





def run_facebook_Yoav_tc_channels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Yoav/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_facebook_Yoav_tc_channelsdb_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Yoav/tc_channelsdb.py"
    return execute_script(request, script_path)


def run_facebook_Yoav_Extract_TXT_IMG_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Yoav/Extract_TXT_IMG.py"
    return execute_script(request, script_path)






def run_Yoav_fb_uploader_v26_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Yoav/fb_uploader_v26.py"
    return execute_script(request, script_path)








    #### Outbrain




def run_Yoav_rsoctoniccreateofferesoutbrain_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Yoav/rsoctoniccreateofferesoutbrain.py"
    return execute_script(request, script_path)


def run_Yoav_tonic_outbrainoffers_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Yoav/tonic_outbrainoffers.py"
    return execute_script(request, script_path)





def run_outbrain_Yoav__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Yoav/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_outbrain_Yoav__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Yoav/tc_channelsdb.py"
    return execute_script(request, script_path)





def run_Yoav_outbrain_uploader_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Yoav/outbrain_uploader.py"
    return execute_script(request, script_path)







    #### Dina #####


def media_buyer_Dina_page(request):
    return render(request, 'media_buyers/Dina.html')


    #### Facebook



def run_Dina_FBRSoCTonicCreatLinks_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Dina/FBRSoCTonicCreatLinks.py"
    return execute_script(request, script_path)


def run_Dina_tonic_FBoffers_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Dina/tonic-fboffers.py"
    return execute_script(request, script_path)


def run_Dina_FBRSoCTonicCreatpixel_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Dina/FBRSoCTonicCreatpixel.py"
    return execute_script(request, script_path)


def run_Dina_FBRSoCTonicCreat_link_pixel_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Dina/FBRSoCTonicCreat_link_pixel.py"
    return execute_script(request, script_path)





def run_facebook_Dina_tc_channels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Dina/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_facebook_Dina_tc_channelsdb_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Dina/tc_channelsdb.py"
    return execute_script(request, script_path)


def run_facebook_Dina_Extract_TXT_IMG_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Dina/Extract_TXT_IMG.py"
    return execute_script(request, script_path)






def run_Dina_fb_uploader_v26_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Dina/fb_uploader_v26.py"
    return execute_script(request, script_path)








    #### Outbrain




def run_Dina_rsoctoniccreateofferesoutbrain_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Dina/rsoctoniccreateofferesoutbrain.py"
    return execute_script(request, script_path)


def run_Dina_tonic_outbrainoffers_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Dina/tonic_outbrainoffers.py"
    return execute_script(request, script_path)





def run_outbrain_Dina__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Dina/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_outbrain_Dina__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Dina/tc_channelsdb.py"
    return execute_script(request, script_path)





def run_Dina_outbrain_uploader_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Dina/outbrain_uploader.py"
    return execute_script(request, script_path)





    #### Elran #####


def media_buyer_Elran_page(request):
    return render(request, 'media_buyers/Elran.html')


    #### Facebook



def run_Elran_FBRSoCTonicCreatLinks_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Elran/FBRSoCTonicCreatLinks.py"
    return execute_script(request, script_path)


def run_Elran_tonic_FBoffers_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Elran/tonic-fboffers.py"
    return execute_script(request, script_path)


def run_Elran_FBRSoCTonicCreatpixel_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Elran/FBRSoCTonicCreatpixel.py"
    return execute_script(request, script_path)


def run_Elran_FBRSoCTonicCreat_link_pixel_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Elran/FBRSoCTonicCreat_link_pixel.py"
    return execute_script(request, script_path)





def run_facebook_Elran_tc_channels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Elran/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_facebook_Elran_tc_channelsdb_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Elran/tc_channelsdb.py"
    return execute_script(request, script_path)


def run_facebook_Elran_Extract_TXT_IMG_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Elran/Extract_TXT_IMG.py"
    return execute_script(request, script_path)






def run_Elran_fb_uploader_v26_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Elran/fb_uploader_v26.py"
    return execute_script(request, script_path)








    #### Outbrain




def run_Elran_rsoctoniccreateofferesoutbrain_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Elran/rsoctoniccreateofferesoutbrain.py"
    return execute_script(request, script_path)


def run_Elran_tonic_outbrainoffers_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Elran/tonic_outbrainoffers.py"
    return execute_script(request, script_path)





def run_outbrain_Elran__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Elran/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_outbrain_Elran__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Elran/tc_channelsdb.py"
    return execute_script(request, script_path)





def run_Elran_outbrain_uploader_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Elran/outbrain_uploader.py"
    return execute_script(request, script_path)














    #### Guy #####


def media_buyer_Guy_page(request):
    return render(request, 'media_buyers/Guy.html')


    #### Facebook



def run_Guy_FBRSoCTonicCreatLinks_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Guy/FBRSoCTonicCreatLinks.py"
    return execute_script(request, script_path)


def run_Guy_tonic_FBoffers_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Guy/tonic-fboffers.py"
    return execute_script(request, script_path)


def run_Guy_FBRSoCTonicCreatpixel_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Guy/FBRSoCTonicCreatpixel.py"
    return execute_script(request, script_path)


def run_Guy_FBRSoCTonicCreat_link_pixel_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Guy/FBRSoCTonicCreat_link_pixel.py"
    return execute_script(request, script_path)





def run_facebook_Guy_tc_channels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Guy/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_facebook_Guy_tc_channelsdb_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Guy/tc_channelsdb.py"
    return execute_script(request, script_path)


def run_facebook_Guy_Extract_TXT_IMG_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Guy/Extract_TXT_IMG.py"
    return execute_script(request, script_path)






def run_Guy_fb_uploader_v26_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Guy/fb_uploader_v26.py"
    return execute_script(request, script_path)








    #### Outbrain




def run_Guy_rsoctoniccreateofferesoutbrain_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Guy/rsoctoniccreateofferesoutbrain.py"
    return execute_script(request, script_path)


def run_Guy_tonic_outbrainoffers_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Guy/tonic_outbrainoffers.py"
    return execute_script(request, script_path)





def run_outbrain_Guy__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Guy/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_outbrain_Guy__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Guy/tc_channelsdb.py"
    return execute_script(request, script_path)





def run_Guy_outbrain_uploader_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Guy/outbrain_uploader.py"
    return execute_script(request, script_path)








    #### Taboola



def run_Guy_tonic_taboolaoffers_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Guy/tonic-taboolaoffers.py"
    return execute_script(request, script_path)


def run_Guy_rsoctoniccreateofferestaboola_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Guy/rsoctoniccreateofferestaboola.py"
    return execute_script(request, script_path)







def run_Guy_tabduplicatorfortest_s1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Guy/tabduplicatorfortest_s1.py"
    return execute_script(request, script_path)


def run_Guy_tabduplicatorfortest_Inuvo_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Guy/tabduplicatorfortest_Inuvo.py"
    return execute_script(request, script_path)


def run_Guy_tabduplicatorfortest_AFD_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Guy/tabduplicatorfortest_AFD.py"
    return execute_script(request, script_path)


def run_Guy_tabduplicatorfortest_RSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Guy/tabduplicatorfortest_RSOC.py"
    return execute_script(request, script_path)


def run_Guy_tabduplicatorfortest_TC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Guy/tabduplicatorfortest_TC.py"
    return execute_script(request, script_path)





def run_taboola_Guy_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Guy/newpolicycheckforall.py"
    return execute_script(request, script_path)








def run_taboola_Guy__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Guy/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_taboola_Guy__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Guy/tc_channelsdb.py"
    return execute_script(request, script_path)







def run_Guy_upload_taboola_creatives_S1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Guy/upload_taboola_creatives_S1.py"
    return execute_script(request, script_path)


def run_Guy_upload_taboola_creatives_TC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Guy/upload_taboola_creatives_TC.py"
    return execute_script(request, script_path)


def run_Guy_upload_taboola_creatives_RSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Guy/upload_taboola_creatives_RSOC.py"
    return execute_script(request, script_path)


def run_Guy_upload_taboola_creatives_Inuvo_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Guy/upload_taboola_creatives_Inuvo.py"
    return execute_script(request, script_path)





    #### WTHMM




def run_Guy_keywordsanalyze_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative_2/KW_scripts/Guy/keywordsanalyze.py"
    return execute_script(request, script_path)


def run_Guy_keywordstokeywords_v3_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative_2/KW_scripts/Guy/keywordstokeywords_v3.py"
    return execute_script(request, script_path)


def run_Guy_creatives_builder_script(request):
    script_path = "/home/Karmel/Aporia_Networks/workflows/creative_builder_dev/remote/creatives_builder_Guy_remote.py"
    return execute_script(request, script_path)














    #### Sahar #####


def media_buyer_Sahar_page(request):
    return render(request, 'media_buyers/Sahar.html')


    #### Facebook



def run_Sahar_FBRSoCTonicCreatLinks_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Sahar/FBRSoCTonicCreatLinks.py"
    return execute_script(request, script_path)


def run_Sahar_tonic_FBoffers_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Sahar/tonic-fboffers.py"
    return execute_script(request, script_path)


def run_Sahar_FBRSoCTonicCreatpixel_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Sahar/FBRSoCTonicCreatpixel.py"
    return execute_script(request, script_path)


def run_Sahar_FBRSoCTonicCreat_link_pixel_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Sahar/FBRSoCTonicCreat_link_pixel.py"
    return execute_script(request, script_path)





def run_facebook_Sahar_tc_channels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Sahar/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_facebook_Sahar_tc_channelsdb_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Sahar/tc_channelsdb.py"
    return execute_script(request, script_path)


def run_facebook_Sahar_Extract_TXT_IMG_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Sahar/Extract_TXT_IMG.py"
    return execute_script(request, script_path)






def run_Sahar_fb_uploader_v26_script(request):
    script_path = "/home/Karmel/Amit/Facebook/TeamSheets/Sahar/fb_uploader_v26.py"
    return execute_script(request, script_path)








    #### Outbrain




def run_Sahar_rsoctoniccreateofferesoutbrain_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Sahar/rsoctoniccreateofferesoutbrain.py"
    return execute_script(request, script_path)


def run_Sahar_tonic_outbrainoffers_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Sahar/tonic_outbrainoffers.py"
    return execute_script(request, script_path)





def run_outbrain_Sahar__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Sahar/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_outbrain_Sahar__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Sahar/tc_channelsdb.py"
    return execute_script(request, script_path)





def run_Sahar_outbrain_uploader_script(request):
    script_path = "/home/Karmel/Amit/Outbrain/TeamSheets/Sahar/outbrain_uploader.py"
    return execute_script(request, script_path)








    #### Taboola



def run_Sahar_tonic_taboolaoffers_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Sahar/tonic-taboolaoffers.py"
    return execute_script(request, script_path)


def run_Sahar_rsoctoniccreateofferestaboola_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Sahar/rsoctoniccreateofferestaboola.py"
    return execute_script(request, script_path)







def run_Sahar_tabduplicatorfortest_s1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Sahar/tabduplicatorfortest_s1.py"
    return execute_script(request, script_path)


def run_Sahar_tabduplicatorfortest_Inuvo_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Sahar/tabduplicatorfortest_Inuvo.py"
    return execute_script(request, script_path)


def run_Sahar_tabduplicatorfortest_AFD_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Sahar/tabduplicatorfortest_AFD.py"
    return execute_script(request, script_path)


def run_Sahar_tabduplicatorfortest_RSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Sahar/tabduplicatorfortest_RSOC.py"
    return execute_script(request, script_path)


def run_Sahar_tabduplicatorfortest_TC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Sahar/tabduplicatorfortest_TC.py"
    return execute_script(request, script_path)





def run_taboola_Sahar_newpolicycheckforall_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Sahar/newpolicycheckforall.py"
    return execute_script(request, script_path)








def run_taboola_Sahar__tchannels_createnew_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Sahar/tc_channels_createnew.py"
    return execute_script(request, script_path)


def run_taboola_Sahar__tchannelsdb_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Sahar/tc_channelsdb.py"
    return execute_script(request, script_path)







def run_Sahar_upload_taboola_creatives_S1_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Sahar/upload_taboola_creatives_S1.py"
    return execute_script(request, script_path)


def run_Sahar_upload_taboola_creatives_TC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Sahar/upload_taboola_creatives_TC.py"
    return execute_script(request, script_path)


def run_Sahar_upload_taboola_creatives_RSOC_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Sahar/upload_taboola_creatives_RSOC.py"
    return execute_script(request, script_path)


def run_Sahar_upload_taboola_creatives_Inuvo_script(request):
    script_path = "/home/Karmel/Amit/Taboola/TeamSheets/Sahar/upload_taboola_creatives_Inuvo.py"
    return execute_script(request, script_path)





    #### WTHMM




def run_Sahar_keywordsanalyze_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative_2/KW_scripts/Sahar/keywordsanalyze.py"
    return execute_script(request, script_path)


def run_Sahar_keywordstokeywords_v3_script(request):
    script_path = "/home/Karmel/Amit/Amit/creative_2/KW_scripts/Sahar/keywordstokeywords_v3.py"
    return execute_script(request, script_path)


def run_Sahar_creatives_builder_script(request):
    script_path = "/home/Karmel/Aporia_Networks/workflows/creative_builder_dev/remote/creatives_builder_Sahar_remote.py"
    return execute_script(request, script_path)


def media_buyer_Jenia_page(request):
    return render(request, 'media_buyers/Jenia.html')
