"""Attachments: files a run stores with a step or with the run itself.

The container holds no MIMICK credential, so a file goes to mimickd's
RunReportService, which needs the run token and stores the file for the run.
The attach record then places it under its step.
"""

from __future__ import annotations

import codecs
import mimetypes
import os
from collections.abc import Iterator
from typing import TYPE_CHECKING

from mimick import env as _env, events
from mimick.appliance.v1 import run_report_pb2, run_report_pb2_grpc

if TYPE_CHECKING:
    from mimick.run import Run

CHUNK = 256 << 10


def _chunks(path: str, name: str, media_type: str) -> Iterator[run_report_pb2.FileChunk]:
    first = True
    with open(path, "rb") as f:
        while True:
            data = f.read(CHUNK)
            if first or data:
                yield run_report_pb2.FileChunk(
                    name=name if first else "", media_type=media_type if first else "", data=data)
                first = False
            if not data:
                return


def media_type_of(path: str, name: str) -> str:
    """The type the extension says, else text when the start of the file reads
    as UTF-8, as the Go CLI sniffs it."""
    if guessed := mimetypes.guess_type(name)[0]:
        return guessed
    with open(path, "rb") as f:
        head = f.read(512)
    try:
        # Incremental, so a character the 512-byte cut splits is not an error.
        codecs.getincrementaldecoder("utf-8")().decode(head, final=False)
    except UnicodeDecodeError:
        return "application/octet-stream"
    return "text/plain; charset=utf-8" if b"\x00" not in head else "application/octet-stream"


def attach_bytes(run: Run, task_id: str, name: str, data: bytes, media_type: str = "") -> str:
    """Uploads data held in memory under name, and writes the attach record."""
    import tempfile

    with tempfile.NamedTemporaryFile(prefix="mimick-attach-") as f:
        f.write(data)
        f.flush()
        return attach(run, task_id, f.name, name, media_type)


def attach(run: Run, task_id: str, path: str, name: str = "", media_type: str = "") -> str:
    """Uploads path and writes the attach record. Returns the file id."""
    name = name or os.path.basename(path)
    media_type = media_type or media_type_of(path, name)
    stub = run_report_pb2_grpc.RunReportServiceStub(_env.channel(run.env))
    resp = stub.UploadFile(_chunks(path, name, media_type))
    run.emitter.emit(events.Event(
        events.ATTACH, f"Attached {name}", task_id=task_id,
        attrs={
            "mimick.file.id": resp.file_id,
            "mimick.file.name": name,
            "mimick.file.size": str(resp.size),
            "mimick.file.media_type": media_type,
        }))
    return resp.file_id
