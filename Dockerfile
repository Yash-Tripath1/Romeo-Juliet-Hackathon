# Round 2 policy image - The One Introduction Problem (Vouchsafe hackathon).
# Assessed limits: 2 CPU cores, 1 GiB RAM, 64 processes, 10 s per invocation,
# 1 MiB for request/response/carried memory, 2 GiB image, no network.
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=0 \
    # Arm to ship; see policy.py ARMS. Override at build or run time.
    ROUND2_ARM=waitfloor

WORKDIR /app

# Pinned runtime dependency (pure-Python, keeps the image small).
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# The organisers' public kit (eligibility + observation contract) and our policy.
COPY kit.py policy.py ./
COPY LICENSE.kit LICENSE.kit

# Read-only image, unprivileged user (the harness runs --user=65534:65534).
RUN chmod -R a+rX /app

# One JSON request on stdin, one JSON response on stdout, exit 0. No arguments.
ENTRYPOINT ["python3", "/app/policy.py"]
