"""Cold retained source aggregate rejection precedes renderer invocation."""

import hashlib
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from pixl import codec, inspection, inspection_views, store
from pixl.codec import PixlError
from tests.inspection_support import options, project

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    project(root)
    folder = root / ".pixl"
    inspection.prepare(
        folder, codec.digest(store.load(folder)), "candidate", "packet", options(), root
    )
    doc = store.load(folder)
    total = sum(
        (root / name).stat().st_size for name in ("candidate.png", "reference.png")
    )
    with (
        patch.object(inspection_views, "MAX_TOTAL_SOURCE_BYTES", total - 1),
        patch.object(
            inspection_views,
            "render",
            side_effect=AssertionError("renderer must not run"),
        ) as renderer,
    ):
        try:
            inspection.report(doc, root, "packet")
        except PixlError as error:
            assert "retained source byte limits exceeded" in str(error)
            renderer.assert_not_called()
            print(
                json.dumps(
                    {
                        "result": "aggregate capture rejected before renderer",
                        "limit": total - 1,
                        "source_bytes": total,
                        "error": str(error),
                        "source_sha256": hashlib.sha256(
                            Path("pixl/inspection.py").read_bytes()
                        ).hexdigest(),
                    },
                    indent=2,
                )
            )
        else:
            raise AssertionError("aggregate read bound bypassed")
