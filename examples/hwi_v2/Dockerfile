# A runbook image for the HWI v2 test. Push it to your organization's registry
# and set it as the runbook's image; runbook.sh is the runbook's script.
FROM python:3.13-slim
RUN pip install --no-cache-dir \
    "mimick-sdk[openhtf] @ https://github.com/CriticalShift/MIMICK-sdk/archive/refs/tags/v0.10.7.tar.gz"
COPY hwi_plug.py hwi_test.py /opt/hwi/
WORKDIR /opt/hwi
