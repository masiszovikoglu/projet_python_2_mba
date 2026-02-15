# 🔍 How to Verify API is Running in Docker

Complete guide to confirm your Banking API is running inside a Docker container, not locally.

---

## ✅ Method 1: Check Docker Container Status

### Command:
```powershell
docker ps
```

### What to look for:
```
CONTAINER ID   IMAGE          COMMAND                  STATUS                    PORTS                    NAMES
abc123def456   banking-api    "uvicorn banking_api…"   Up 5 minutes (healthy)    0.0.0.0:8000->8000/tcp   banking-api
```

**Indicators:**
- ✅ **NAMES**: `banking-api` container is listed
- ✅ **STATUS**: Shows "Up X minutes (healthy)"
- ✅ **PORTS**: Shows `0.0.0.0:8000->8000/tcp` (Docker port mapping)

### If NOT in Docker:
```
# Empty output or no banking-api container listed
```

---

## ✅ Method 2: Check Container Hostname

### Command:
```powershell
# When running in Docker
docker compose exec api hostname

# When running locally
hostname
```

### Comparison:

**In Docker (returns container ID):**
```
abc123def456
```

**Running Locally (returns your computer name):**
```
DESKTOP-XYZ123
```

---

## ✅ Method 3: Check Container Logs

### Command:
```powershell
docker compose logs api
```

### What to look for:
```
banking-api  | INFO:     Started server process [1]
banking-api  | INFO:     Waiting for application startup.
banking-api  | INFO:     Application startup complete.
banking-api  | INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Indicators:**
- ✅ Log lines prefixed with `banking-api |`
- ✅ Server running on `0.0.0.0:8000` (Docker network)
- ✅ Process ID is usually `[1]` in container

### If NOT in Docker:
```
# Error: no container named "api"
# Or: logs appear in your terminal directly
```

---

## ✅ Method 4: Check Process Information Inside Container

### Command:
```powershell
docker compose exec api ps aux
```

### What to look for:
```
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0   2416  1428 ?        Ss   12:00   0:00 /bin/sh -c uvicorn banking_api.main:app --host 0.0.0.0 --port 8000
root         7  0.5  2.1 245680 86432 ?        S    12:00   0:03 python -m uvicorn banking_api.main:app --host 0.0.0.0 --port 8000
```

**Indicators:**
- ✅ **PID 1**: Usually the main process in a container
- ✅ **COMMAND**: Shows uvicorn/python running
- ✅ Limited process list (only container processes)

---

## ✅ Method 5: Check Environment Inside Container

### Command:
```powershell
docker compose exec api env | Select-String "PATH|HOSTNAME|API"
```

### What to look for:
```
HOSTNAME=abc123def456
PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
API_HOST=0.0.0.0
API_PORT=8000
DATA_PATH=/app/data/transactions_data.csv
```

**Indicators:**
- ✅ **HOSTNAME**: Shows container ID
- ✅ **PATH**: Linux-style paths (even on Windows)
- ✅ **API_* variables**: Docker environment variables

---

## ✅ Method 6: Check File System Inside Container

### Command:
```powershell
docker compose exec api ls -la /app
```

### What to look for:
```
total 48
drwxr-xr-x    1 root root  4096 Feb 15 12:00 .
drwxr-xr-x    1 root root  4096 Feb 15 12:00 ..
drwxr-xr-x    2 root root  4096 Feb 15 12:00 data
-rw-r--r--    1 root root  1234 Feb 15 12:00 pyproject.toml
-rw-r--r--    1 root root   567 Feb 15 12:00 setup.py
drwxr-xr-x    3 root root  4096 Feb 15 12:00 src
```

**Indicators:**
- ✅ Linux-style file permissions
- ✅ Files are in `/app` directory (container workspace)
- ✅ Owner is `root` (container user)

---

## ✅ Method 7: Check API Metadata Response

### Command:
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/system/metadata" | ConvertTo-Json
```

### What to look for:
```json
{
  "api_version": "1.0.0",
  "python_version": "3.12.x",
  "environment": {
    "DATA_PATH": "/app/data/transactions_data.csv",
    "API_HOST": "0.0.0.0",
    "API_PORT": "8000"
  }
}
```

**Indicators:**
- ✅ **DATA_PATH**: Shows `/app/data/...` (container path)
- ✅ **API_HOST**: `0.0.0.0` (Docker listens on all interfaces)

---

## ✅ Method 8: Check Network Connections

### Command:
```powershell
docker compose exec api netstat -tlnp
```

### What to look for:
```
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:8000            0.0.0.0:*               LISTEN      7/python
```

**Indicators:**
- ✅ Listening on `0.0.0.0:8000` inside container
- ✅ Process is Python/uvicorn

---

## ✅ Method 9: Check Docker Stats

### Command:
```powershell
docker stats banking-api --no-stream
```

### What to look for:
```
CONTAINER ID   NAME          CPU %     MEM USAGE / LIMIT     MEM %     NET I/O           BLOCK I/O
abc123def456   banking-api   0.50%     250MiB / 8GiB         3.05%     1.2MB / 850kB     10MB / 0B
```

**Indicators:**
- ✅ Shows real-time resource usage
- ✅ Container name matches
- ✅ Memory/CPU usage visible

---

## ✅ Method 10: Compare Local vs Docker Process

### Check Local Processes:
```powershell
# Windows - check if uvicorn running locally
Get-Process | Where-Object {$_.ProcessName -like "*python*" -or $_.ProcessName -like "*uvicorn*"}
```

### Check Docker Processes:
```powershell
docker compose top api
```

**In Docker:**
```
UID     PID     PPID    C    STIME   TTY   TIME       CMD
root    12345   12344   0    12:00   ?     00:00:03   python -m uvicorn banking_api.main:app
```

---

## 🎯 Quick Verification Checklist

Run these commands to confirm Docker execution:

```powershell
# 1. Is container running?
docker ps | Select-String "banking-api"

# 2. What's the container hostname?
docker compose exec api hostname

# 3. Where are the files?
docker compose exec api pwd

# 4. What's the environment?
docker compose exec api env | Select-String "API_HOST"

# 5. Check API response
Invoke-RestMethod http://localhost:8000/api/system/health
```

### Expected Results (Running in Docker):
```
✅ Container "banking-api" is listed in docker ps
✅ Hostname is a container ID (like abc123def456)
✅ Working directory is /app
✅ API_HOST=0.0.0.0
✅ API responds on http://localhost:8000
```

### If Running Locally (Not Docker):
```
❌ No containers in docker ps
❌ Hostname is your computer name
❌ Working directory is your local path (C:\Users\...)
❌ No Docker environment variables
❌ Process running in your Windows task manager
```

---

## 🔍 Visual Differences

### When Running in Docker:

1. **Container appears in Docker Desktop**
   - Open Docker Desktop → Containers
   - See "banking-api" container running

2. **Docker icon shows activity**
   - Docker Desktop system tray icon
   - Shows container is running

3. **Logs in Docker Desktop**
   - Click on container in Docker Desktop
   - View logs in UI

### When Running Locally:

1. **Terminal shows direct output**
   - Logs appear in your PowerShell window
   - No "banking-api |" prefix

2. **Process in Task Manager**
   - Open Task Manager
   - See python.exe process

3. **No Docker containers**
   - Docker Desktop shows no containers
   - `docker ps` returns empty

---

## 🚀 Complete Verification Script

Run this PowerShell script to verify Docker execution:

```powershell
Write-Host "`n=== DOCKER VERIFICATION REPORT ===`n" -ForegroundColor Cyan

# Check 1: Container exists
Write-Host "1. Container Status:" -ForegroundColor Yellow
$container = docker ps --filter "name=banking-api" --format "{{.Names}}" 2>$null
if ($container) {
    Write-Host "   ✓ Container 'banking-api' is running" -ForegroundColor Green
} else {
    Write-Host "   ✗ No container found - API NOT running in Docker" -ForegroundColor Red
}

# Check 2: Container hostname
Write-Host "`n2. Hostname Check:" -ForegroundColor Yellow
$hostname = docker compose exec api hostname 2>$null
if ($hostname) {
    Write-Host "   ✓ Container hostname: $hostname" -ForegroundColor Green
} else {
    Write-Host "   ✗ Cannot get container hostname" -ForegroundColor Red
}

# Check 3: Working directory
Write-Host "`n3. Working Directory:" -ForegroundColor Yellow
$workdir = docker compose exec api pwd 2>$null
if ($workdir -match "/app") {
    Write-Host "   ✓ Working in container: $workdir" -ForegroundColor Green
} else {
    Write-Host "   ✗ Not in container directory" -ForegroundColor Red
}

# Check 4: Environment variables
Write-Host "`n4. Environment Variables:" -ForegroundColor Yellow
$env_check = docker compose exec api env 2>$null | Select-String "API_HOST"
if ($env_check) {
    Write-Host "   ✓ Docker environment detected" -ForegroundColor Green
    Write-Host "   $env_check" -ForegroundColor Gray
} else {
    Write-Host "   ✗ No Docker environment variables" -ForegroundColor Red
}

# Check 5: API Response
Write-Host "`n5. API Response:" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod http://localhost:8000/api/system/health -ErrorAction Stop
    Write-Host "   ✓ API is responding" -ForegroundColor Green
    Write-Host "   Status: $($response.status)" -ForegroundColor Gray
} catch {
    Write-Host "   ✗ API not responding" -ForegroundColor Red
}

Write-Host "`n=== END OF REPORT ===`n" -ForegroundColor Cyan
```

---

## 📝 Summary

To know your API is running in Docker:

| Indicator | Docker | Local |
|-----------|--------|-------|
| **docker ps** | Shows container | Empty |
| **hostname** | Container ID | Computer name |
| **Working dir** | `/app` | `C:\Users\...` |
| **Logs** | Prefixed with container name | Direct output |
| **Process** | Inside container | Windows process |
| **Environment** | Docker variables | Windows variables |

**Easiest way:** Run `docker ps` - if you see `banking-api` container, it's running in Docker! 🐳✅

