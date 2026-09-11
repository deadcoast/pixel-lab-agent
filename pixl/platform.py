"""Offline PixelLab preparation and caller-supplied observation journals.

``prepare`` accepts the exact MCP ``inputSchema`` object, not a tool descriptor.
No function here discovers a server, transmits a request, fetches a URL, or polls.
Schema provenance and remote receipts are supplied by the caller and cannot be
authenticated locally. The returned journal records those claims explicitly.
"""

import base64
import binascii
import copy
import hashlib
import io
import json
import math
import os
import re
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator
from PIL import Image
from referencing import Registry
from referencing.exceptions import NoSuchResource

from .codec import PixlError

_SECRET_KEYS = {"apikey", "apitoken", "authorization", "auth", "accesstoken",
                "refreshtoken", "bearertoken", "password", "secret", "clientsecret",
                "credentials", "token"}
_DIRECTIONS = {"south", "north", "east", "west", "south-east", "south-west",
               "north-east", "north-west"}
_TRANSITIONS = {"prepared": {"submitted", "unknown", "failed"},
                "submitted": {"running", "succeeded", "failed", "unknown"},
                "running": {"running", "succeeded", "failed", "unknown"},
                "unknown": {"submitted", "running", "succeeded", "failed"},
                "succeeded": set(), "failed": set()}


def _fail(detail, code="platform_constraint"):
    raise PixlError(code, detail)


def _json_bytes(value):
    def visit(item, depth=0):
        if depth > 64:
            _fail("JSON nesting exceeds 64", "platform_json")
        if isinstance(item, dict):
            if any(not isinstance(k, str) for k in item):
                _fail("JSON keys must be strings", "platform_json")
            for child in item.values():
                visit(child, depth + 1)
        elif isinstance(item, list):
            for child in item:
                visit(child, depth + 1)
        elif item is None or type(item) in (str, bool, int) or type(item) is float and math.isfinite(item):
            return
        else:
            _fail("expected finite JSON values", "platform_json")

    try:
        visit(value)
        data = json.dumps(value, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (RecursionError, ValueError, TypeError) as error:
        if isinstance(error, PixlError):
            raise
        _fail("invalid JSON encoding", "platform_json")
    if len(data) > 16 * 1024 * 1024:
        _fail("JSON exceeds 16 MiB", "platform_json")
    return data


def _sha(value):
    return hashlib.sha256(_json_bytes(value)).hexdigest()


def _no_secrets(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if re.sub(r"[^a-z0-9]", "", key.lower()) in _SECRET_KEYS:
                _fail("credential fields must remain outside PIXL requests and receipts", "platform_secret")
            _no_secrets(child)
    elif isinstance(value, list):
        for child in value:
            _no_secrets(child)


def capabilities(name=None):
    """Read the source or bundled catalog, without implying live availability."""
    plugin = os.environ.get("PIXL_PLUGIN_ROOT")
    packaged = Path(__file__).resolve().with_name("resources")
    root = (Path(plugin) / "resources" if plugin else packaged if packaged.is_dir()
            else Path(__file__).resolve().parent.parent)
    path = root / "knowledge" / "pixellab-capabilities.json"
    try:
        catalog = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(catalog, dict) or not isinstance(catalog.get("tools"), list):
            raise ValueError("invalid catalog")
    except (OSError, ValueError) as error:
        raise PixlError("platform_catalog", "cannot read the PixelLab capability catalog") from error
    if name is None:
        return catalog
    if not isinstance(name, str):
        _fail("tool name must be a string", "platform_tool")
    for item in catalog["tools"]:
        if isinstance(item, dict) and item.get("name") == name:
            return item
    _fail("tool is absent from the catalog; refresh or select a documented tool", "platform_tool")


def _validate_schema(arguments, schema):
    if not isinstance(schema, dict) or "inputSchema" in schema:
        _fail("supply the exact inputSchema object, not a tool descriptor", "platform_schema")

    def references(value):
        if isinstance(value, dict):
            for key, child in value.items():
                if key in ("$ref", "$dynamicRef") and (not isinstance(child, str) or not child.startswith("#")):
                    _fail("only fragment-local schema references are allowed", "platform_schema")
                references(child)
        elif isinstance(value, list):
            for child in value:
                references(child)

    references(schema)

    def unavailable(uri):
        # An explicit registry prevents jsonschema's historical network fallback.
        raise NoSuchResource(ref=uri)

    try:
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, registry=Registry(retrieve=unavailable))
        error = next(validator.iter_errors(arguments), None)
        if error is not None:
            # jsonschema's message may echo instance data; emit only its keyword.
            _fail(f"arguments violate inputSchema ({error.validator})", "platform_arguments")
    except PixlError:
        raise
    except Exception as error:
        raise PixlError("platform_schema", "invalid, unresolved, or recursive inputSchema") from error


def _range(value, low, high, field, integer=True):
    valid = type(value) is int if integer else type(value) in (int, float)
    if not valid or not low <= value <= high:
        _fail(f"{field} must be {'an integer ' if integer else ''}between {low} and {high}")


def _present(arguments, key):
    return key in arguments and arguments[key] is not None


def _exclusive(arguments, *keys, required=False):
    count = sum(_present(arguments, k) for k in keys)
    if count > 1 or (required and count != 1):
        _fail(f"supply {'exactly one' if required else 'at most one'} of {', '.join(keys)}")


def _require(arguments, *keys):
    for key in keys:
        if not _present(arguments, key) or arguments[key] in ("", []):
            _fail(f"{key} is required for this operation")


def _decoded_image(encoded):
    try:
        if not isinstance(encoded, str):
            raise ValueError("not encoded text")
        data = base64.b64decode(encoded, validate=True)
        with Image.open(io.BytesIO(data)) as image:
            if image.format not in ("PNG", "JPEG") or image.width * image.height > 16_777_216:
                raise ValueError("unsupported image")
            size = image.size
            image.verify()
        return size
    except (ValueError, binascii.Error, OSError, Image.DecompressionBombError) as error:
        raise PixlError("platform_image", "image base64 must contain a complete PNG or JPEG") from error


def _images(tool, arguments):
    """Validate supplied bytes/URL syntax without resolving remote URLs."""
    sizes = {}
    for field in arguments:
        if field.endswith("_base64"):
            _exclusive(arguments, field, f"{field[:-7]}_url")
    _exclusive(arguments, "images_base64", "image_urls")
    if tool == "create_portrait_character":
        _exclusive(arguments, "image", "image_url", required=True)

    def walk(value, path=""):
        if isinstance(value, dict):
            for key, child in value.items():
                name = f"{path}.{key}" if path else key
                if child is None:
                    continue
                if key.endswith("_base64") or key == "base64" or (key == "image" and isinstance(child, str)):
                    if isinstance(child, list):
                        for i, encoded in enumerate(child):
                            sizes[f"{name}.{i}"] = _decoded_image(encoded)
                    else:
                        sizes[name] = _decoded_image(child)
                elif key.endswith("_url") or key == "url" or key == "image_urls":
                    urls = child if isinstance(child, list) else [child]
                    for i, url in enumerate(urls):
                        if not isinstance(url, str):
                            _fail("image URLs must be strings", "platform_image")
                        try:
                            parsed = urlsplit(url)
                            https = parsed.scheme == "https" and parsed.hostname and not parsed.username and not parsed.password
                        except ValueError:
                            https = False
                        if not https:
                            allow_data = tool not in ("create_character", "animate_character") and key != "url"
                            match = re.fullmatch(r"data:image/(?:png|jpeg);base64,(.+)", url) if allow_data else None
                            if match is None:
                                _fail("image URL must use supported HTTPS or image data transport", "platform_image")
                            sizes[f"{name}.{i}" if isinstance(child, list) else name] = _decoded_image(match[1])
                else:
                    walk(child, name)
        elif isinstance(value, list):
            for i, child in enumerate(value):
                walk(child, f"{path}.{i}")

    walk(arguments)
    return sizes


def _rules(tool, a, schema, authorization, entry):
    def value(field, fallback=None):
        if _present(a, field):
            return a[field]
        definition = schema.get("properties", {}).get(field, {})
        if isinstance(definition, dict) and definition.get("default") is not None:
            return definition["default"]
        return fallback

    def reject_fields(*fields):
        if any(_present(a, field) for field in fields):
            _fail("requested mode ignores or excludes: " + ", ".join(f for f in fields if _present(a, f)))

    def dimension_pair(width="width", height="height", defaults=(128, 128)):
        w, h = value(width, defaults[0]), value(height, defaults[1])
        _range(w, 1, 1_000_000, width)
        _range(h, 1, 1_000_000, height)
        return w, h

    sizes = _images(tool, a)

    if tool == "create_character":
        mode = value("mode", "standard")
        size = value("size", 48)
        _range(size, 1, 256 if mode == "v3" else 128, "size")
        if mode in ("pro", "v3"):
            if value("n_directions", 8) != 8:
                _fail("pro and v3 characters always have eight directions")
            reject_fields("shading", "proportions", "text_guidance_scale")
        if mode == "pro":
            reject_fields("outline", "detail")
        if value("view") == "oblique" and (mode != "standard" or value("n_directions", 8) != 4):
            _fail("oblique requires standard mode and four directions")
        if value("body_type", "humanoid") == "quadruped" and a.get("template") not in {"bear", "cat", "dog", "horse", "lion"}:
            _fail("quadruped characters require a supported template")
        if _present(a, "style_character_id") and mode != "pro":
            _fail("style_character_id requires pro mode")
        if any(_present(a, k) for k in ("reference_image_base64", "reference_image_url")):
            if mode != "v3":
                _fail("character sprite references require v3 mode")
            reject_fields("outline", "detail")
            if any(max(dim) > 256 for dim in sizes.values()):
                _fail("v3 character references are at most 256x256")

    if tool == "create_character_state":
        if _present(a, "override_width") != _present(a, "override_height"):
            _fail("state canvas overrides must be paired")
        for key in ("override_width", "override_height"):
            if _present(a, key):
                _range(a[key], 4, 1_000_000, key)
                if a[key] % 4:
                    _fail("state canvas overrides must be multiples of four")

    if tool in ("animate_character", "animate_object"):
        character = tool == "animate_character"
        mode = value("mode", "template" if character and a.get("template_animation_id") else "v3")
        if mode == "template":
            _require(a, "template_animation_id")
            reject_fields("frame_count")
        elif character or not a.get("animation_group_id"):
            _require(a, "action_description" if character else "animation_description")
        if mode == "v3":
            frames = value("frame_count", 8)
            _range(frames, 4, 16, "frame_count")
            if frames % 2:
                _fail("v3 frame_count must be even")
        elif character and mode == "pro":
            reject_fields("frame_count")
        elif mode == "pro" and _present(a, "frame_count") and a["frame_count"] not in (4, 9, 16):
            _fail("object pro frame_count must be 4, 9, or 16, subject to source canvas")
        pose_keys = ("custom_start_frame_base64", "custom_start_frame_url", "end_frame_base64", "end_frame_url")
        if any(_present(a, k) for k in pose_keys):
            if mode != "v3":
                _fail("custom poses require v3 mode")
            # Object direction cardinality depends on the source; no source lookup is performed.
            directions = a.get("directions")
            if (character or directions is not None) and (not isinstance(directions, list) or len(directions) != 1 or directions[0] not in _DIRECTIONS):
                _fail("a custom character pose requires one explicit direction")
            poses = [dim for key, dim in sizes.items() if any(key.startswith(p) for p in pose_keys)]
            if any(max(dim) > 256 for dim in poses) or len(set(poses)) > 1:
                _fail("custom start/end canvases must match and be at most 256x256")
        if mode != "v3":
            reject_fields("keep_first_frame")
        if character and a.get("animation_group_id"):
            _require(a, "animation_name")
        if mode == "pro" and a.get("confirm_cost") is True:
            quote = authorization.get("cost_quote") if isinstance(authorization, dict) else None
            approval = authorization.get("approval") if isinstance(authorization, dict) else None
            if not isinstance(quote, dict) or not quote or not isinstance(approval, dict) or approval.get("explicit") is not True:
                _fail("pro confirmation requires cost_quote and explicit approval evidence", "platform_authorization")
            if not isinstance(approval.get("evidence"), dict) or not approval["evidence"]:
                _fail("pro confirmation requires nonempty user approval evidence", "platform_authorization")

    if tool in ("create_1_direction_object", "create_8_direction_object"):
        single = tool == "create_1_direction_object"
        if single:
            if "style_images" not in a or not isinstance(a["style_images"], list):
                _fail("style_images is required; use an empty list when no references are intended")
            style = a["style_images"]
            if style and _present(a, "size"):
                _fail("style_images determine size; omit explicit size")
            dims = [dim for key, dim in sizes.items() if key.startswith("style_images.")]
            size = max((max(dim) for dim in dims), default=value("size", 64))
            _range(size, 16, 256, "effective size")
            count = 64 if size <= 42 else 16 if size <= 85 else 4 if size <= 170 else 1
            max_refs = 8 if size <= 85 else 4 if size <= 170 else 1
            if len(style) > max_refs or len(a.get("item_descriptions") or []) > count:
                _fail("reference or item-description count exceeds the size-dependent grid")
        else:
            _range(value("size", 64), 24, 168, "size")
            _exclusive(a, "reference_image_base64", "style_image_base64")
            if _present(a, "size") and any(_present(a, k) for k in ("reference_image_base64", "style_image_base64")):
                _fail("reference images determine eight-direction object size")

    if tool in ("create_topdown_tileset", "create_sidescroller_tileset"):
        topdown = tool == "create_topdown_tileset"
        mode = value("mode", "standard")
        tile = value("tile_size", 16)
        if isinstance(tile, dict):
            w, h = tile.get("width"), tile.get("height")
            if w != h:
                _fail("terrain tiles must be square")
            tile = w
        allowed = (16, 32, 64) if topdown and mode == "pro" else (16, 32)
        if type(tile) is not int or tile not in allowed:
            _fail("tile_size is unsupported for this terrain mode")
        if mode == "pro" and a.get("shape_style") is not None:
            _fail("pro terrain rejects shape_style")
        if mode != "pro":
            reject_fields("spread_x", "slope_size", "raggedness")
        transition = value("transition_size", 0.0)
        _range(transition, 0, 1, "transition_size", integer=False)
        if not a.get("shape_style") and transition not in ((0, .25, .5, 1) if topdown else (0, .25, .5)):
            _fail("this terrain mode requires a discrete transition_size")

    if tool in ("create_path_tiles", "create_building_kit", "create_tiles_pro"):
        tile_type = value("tile_type", "square_topdown" if tool == "create_path_tiles" else "isometric")
        size = value("tile_size", 32)
        if tool == "create_path_tiles":
            if tile_type == "square_topdown" and size != 32:
                _fail("square top-down paths require size 32")
            if tile_type == "isometric":
                _range(size, 48, 96, "tile_size")
        elif tool == "create_building_kit":
            _range(size, 32 if tile_type == "isometric" else 16, 96, "tile_size")
            _range(value("wall_tiles", 2), 1, 3, "wall_tiles")
        else:
            _range(size, 16, 128, "tile_size")
            if a.get("tile_feature") not in (None, "tileset"):
                _fail("MCP create_tiles_pro supports only tile_feature=tileset; use dedicated path/building tools")
            if a.get("style_images"):
                reject_fields("tile_feature", "tile_type", "tile_size", "tile_height", "tile_view",
                              "tile_view_angle", "tile_depth_ratio", "tile_flat_top_px")

    image_inputs = {"edit_image": ("images_base64", "image_urls"),
                    "correct_pixelart": ("images_base64", "image_urls"),
                    "reduce_colors": ("images_base64", "image_urls"),
                    "edit_image_pixen": ("image_base64", "image_url"),
                    "image_to_pixelart": ("image_base64", "image_url"),
                    "unzoom_image": ("image_base64", "image_url"),
                    "inpaint_image": ("image_base64", "image_url"),
                    "animate_image": ("first_frame_base64", "first_frame_url"),
                    "animate_image_pixminimax": ("first_frame_base64", "first_frame_url")}
    if tool in image_inputs:
        keys = image_inputs[tool]
        _exclusive(a, *keys, required=True)
        _require(a, next(k for k in keys if _present(a, k)))
    if tool in ("correct_pixelart", "reduce_colors"):
        dims = [dim for key, dim in sizes.items() if key.startswith(("images_base64.", "image_urls."))]
        if len(set(dims)) > 1:
            _fail("input frames must have identical dimensions")
    if tool == "reduce_colors" and _present(a, "num_colors") and any(_present(a, k) for k in ("palette_image_base64", "palette_image_url")):
        _fail("num_colors excludes a supplied palette image")
    if tool == "edit_image" and not any(_present(a, k) for k in ("description", "reference_image_base64", "reference_image_url")):
        _fail("edit_image needs an edit description or reference")
    if tool == "edit_image_pixen":
        description = a.get("description")
        if not isinstance(description, str) or not 1 <= len(description) <= 500:
            _fail("edit_image_pixen description length must be 1-500")
        source = sizes.get("image_base64", sizes.get("image_url"))
        if source and max(source) > 256:
            _fail("Pixen edit input is at most 256 pixels per side")
        if source or (_present(a, "width") and _present(a, "height")):
            w, h = dimension_pair(defaults=source or (128, 128))
            if w * h > 65536:
                _fail("Pixen edit output area exceeds 65536 pixels")
    if tool in ("create_image_pixflux", "create_image_pixen"):
        source = sizes.get("init_image_base64", sizes.get("init_image_url"))
        w, h = dimension_pair(defaults=source or (128, 128))
        if tool == "create_image_pixflux":
            if min(w, h) < 16 or w * h < 1024:
                _fail("pixflux needs axes >=16 and area >=1024 pixels")
            if source and source != (w, h):
                _fail("pixflux init image must match output dimensions")
        elif w % 4 or h % 4 or (min(w, h) < 32 and w != h):
            _fail("pixen dimensions must be multiples of four and small canvases square")
    if tool in ("create_ui_asset", "create_image_pro"):
        w, h = dimension_pair(defaults=(256, 256) if tool == "create_ui_asset" else (128, 128))
        limits = ((512, 512), (688, 384), (384, 688), (600, 448), (448, 600))
        if (tool == "create_ui_asset" and min(w, h) < 192) or not any(w <= mw and h <= mh for mw, mh in limits):
            _fail("dimensions exceed the published aspect-dependent canvas bounds")
        if len(a.get("reference_images") or []) > 4:
            _fail("pro images accept at most four labelled references")
    if tool == "inpaint_image":
        rect = ("mask_x", "mask_y", "mask_width", "mask_height")
        supplied = sum(_present(a, k) for k in rect)
        mask = any(_present(a, k) for k in ("mask_image_base64", "mask_image_url"))
        if supplied not in (0, 4) or (supplied and mask) or not (supplied or mask):
            _fail("inpainting requires one complete rectangle or one mask image")
        source = sizes.get("image_base64", sizes.get("image_url"))
        if source and (min(source) < 32 or max(source) > 512):
            _fail("inpaint input must be between 32x32 and 512x512")
        if supplied:
            for key in rect:
                _range(a[key], 0 if key in ("mask_x", "mask_y") else 1, 1_000_000, key)
            if source and (a["mask_x"] + a["mask_width"] > source[0] or a["mask_y"] + a["mask_height"] > source[1]):
                _fail("mask rectangle extends outside the input image")
        mask_size = sizes.get("mask_image_base64", sizes.get("mask_image_url"))
        if source and mask_size and source != mask_size:
            _fail("mask image must match the input canvas")
    if tool in ("animate_image", "animate_image_pixminimax"):
        minimax = tool == "animate_image_pixminimax"
        frames = value("frame_count", 8)
        _range(frames, 4, 40 if minimax else 16, "frame_count")
        if frames % (4 if minimax else 2):
            _fail("frame_count has the wrong multiple for the selected animation engine")
        dims = [dim for key, dim in sizes.items() if key.startswith(("first_frame", "last_frame"))]
        if any(max(dim) > 256 for dim in dims) or len(set(dims)) > 1:
            _fail("animation start/end canvases must match and be at most 256x256")


def prepare(tool: str, arguments: dict, schema: dict, authorization: dict | None = None) -> dict:
    """Validate a caller-supplied inputSchema and return an unsubmitted intent.

    For confirmed pro animation, authorization must contain a nonempty
    ``cost_quote`` receipt and ``approval={explicit:true,evidence:{...}}``.
    Those receipts remain caller assertions, not authenticated remote evidence.
    No argument is removed, coerced, default-inserted, or sent to PixelLab.
    """
    if not isinstance(arguments, dict) or (authorization is not None and not isinstance(authorization, dict)):
        _fail("arguments and optional authorization must be JSON objects", "platform_arguments")
    _json_bytes(arguments)
    _json_bytes(schema)
    _json_bytes(authorization)
    _no_secrets(arguments)
    _no_secrets(authorization)
    entry = capabilities(tool)
    _validate_schema(arguments, schema)
    try:
        _rules(tool, arguments, schema, authorization, entry)
    except PixlError:
        raise
    except (TypeError, ValueError, KeyError) as error:
        raise PixlError("platform_constraint", "invalid value for a documented PixelLab constraint") from error
    return {"tool": tool, "arguments": copy.deepcopy(arguments), "schema_sha256": _sha(schema),
            "intent_sha256": _sha({"tool": tool, "arguments": arguments, "schema": schema}),
            "schema_source": "caller_supplied", "discovery_verified": False,
            "remote_executed": False, "state": "prepared", "remote_id": None, "observations": [],
            "approval_receipts": copy.deepcopy(authorization), "effect": entry.get("effect"),
            "poll_tool": entry.get("poll_tool"),
            "unverified": ["server availability and acceptance", "source asset state and remote URL image contents",
                           "source-dependent canvas/frame rules", "current pricing and account entitlement",
                           "generated output, visual quality, and engine import"]}


def _evidence_required(event, evidence):
    if event in ("submitted", "running", "succeeded", "failed") and (not isinstance(evidence, dict) or not evidence):
        _fail("this observation requires a nonempty evidence object", "platform_journal")


def _remote_id(value):
    if value is not None and (not isinstance(value, str) or not value.strip() or value != value.strip()):
        _fail("remote_id must be a nonempty, unmodified server identifier", "platform_journal")


def _journal(job):
    if not isinstance(job, dict) or not re.fullmatch(r"[0-9a-f]{64}", str(job.get("intent_sha256", ""))):
        _fail("journal needs a canonical intent_sha256", "platform_journal")
    if not isinstance(job.get("tool"), str) or not job["tool"] or not isinstance(job.get("observations"), list):
        _fail("journal needs tool and observations", "platform_journal")
    state, remote = "prepared", None
    for index, observation in enumerate(job["observations"], 1):
        if not isinstance(observation, dict):
            _fail("malformed observation history", "platform_journal")
        target = observation.get("event")
        if observation.get("sequence") != index or observation.get("from_state") != state or target not in _TRANSITIONS[state]:
            _fail("observation history has an invalid transition", "platform_journal")
        if observation.get("intent_sha256") != job["intent_sha256"] or observation.get("tool") != job["tool"]:
            _fail("journal intent and tool identity cannot be rebound", "platform_journal")
        next_remote = observation.get("remote_id")
        _remote_id(next_remote)
        if remote is not None and next_remote != remote:
            _fail("journal remote identity cannot change", "platform_journal")
        if target in ("submitted", "running", "succeeded") and next_remote is None:
            _fail("accepted outcomes require the observed remote identifier", "platform_journal")
        _evidence_required(target, observation.get("evidence"))
        state, remote = target, next_remote
    if job.get("state") != state or job.get("remote_id") != remote:
        _fail("journal state or remote identity disagrees with observation history", "platform_journal")


def job_update(job: dict, event: str, remote_id: str | None = None, evidence: dict | None = None) -> dict:
    """Append one caller-supplied observation; never submit, poll, or retry.

    Event names are target states: submitted, running, succeeded, failed, unknown.
    A lost response can be recorded as unknown without an ID. Identity recovery
    requires a supplied server ID and evidence. Succeeded and failed are terminal.
    The journal detects inconsistent history, not malicious replacement of the
    entire file; callers must persist it with the store's concurrency protection.
    ``remote_executed=False`` describes this local function, not job history.
    """
    _json_bytes(job)
    _json_bytes(evidence)
    _no_secrets(job)
    _no_secrets(evidence)
    if evidence is not None and not isinstance(evidence, dict):
        _fail("evidence must be a JSON object", "platform_journal")
    _journal(job)
    if not isinstance(event, str) or event not in _TRANSITIONS[job["state"]]:
        _fail("invalid or terminal job transition; recreation is not a journal event", "platform_journal")
    _remote_id(remote_id)
    identity = job["remote_id"] if remote_id is None else remote_id
    if job["remote_id"] is not None and identity != job["remote_id"]:
        _fail("remote identity is immutable once recorded", "platform_journal")
    if event in {"submitted", "running", "succeeded"} and identity is None:
        _fail("accepted outcomes require a real identifier from the remote response", "platform_journal")
    _evidence_required(event, evidence)
    result = copy.deepcopy(job)
    result["observations"].append({"sequence": len(result["observations"]) + 1,
                                   "from_state": job["state"], "event": event,
                                   "intent_sha256": job["intent_sha256"], "tool": job["tool"],
                                   "remote_id": identity, "evidence": copy.deepcopy(evidence),
                                   "evidence_origin": "caller_supplied",
                                   "recorded_at": datetime.now(UTC).isoformat()})
    result.update(state=event, remote_id=identity, remote_executed=False)
    return result
