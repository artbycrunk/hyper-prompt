import argparse
import signal
import sys
import os

from . import config, helpers, prompt, defaults


def parser():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--version", action="store_true", help="Output the version"
    )
    arg_parser.add_argument(
        "--separator",
        action="store",
        default=None,
        help="Override the segment separator",
        choices=defaults.SEPARATORS.keys(),
    )
    arg_parser.add_argument(
        "--showall",
        action="store",
        default=None,
        help="Test different aspects of hyperprompt",
        choices=["separator"],
    )
    arg_parser.add_argument(
        "--shell",
        action="store",
        default="",
        help="Set this to your shell type",
        choices=defaults.SHELLS.keys(),
    )
    arg_parser.add_argument(
        "--fallback",
        action="store",
        default="",
        help="Fallback to this value in cases of disaster",
    )
    arg_parser.add_argument(
        "--debug",
        action="store_true",
        help="Show more debug information",
    )
    arg_parser.add_argument(
        "prev_error",
        nargs="?",
        type=int,
        default=0,
        help="Error code returned by the last command",
    )
    args = arg_parser.parse_args()
    args.shell = detect_shell(args)
    return args


def detect_shell(args):
    """
    If a shell is not provided by the user,
    use the shell currently installed user shell
    """
    if args.shell:
        return args.shell

    current_shell = os.getenv("SHELL")
    if current_shell:
        current_shell = os.path.basename(current_shell)
    else:
        current_shell = "bash"
    return current_shell


def build_prompt(
    args, valid_config, theme, importer=None, draw=True, newline=False
):
    hyper_prompt = prompt.Prompt(args, valid_config, theme)

    segment_threads = list()
    segments = valid_config.get("segments", [])
    if segments and newline:
        segments = segments[:] + ["newline"]
    for seg_conf in segments:
        seg_conf = helpers.ensure_dict(seg_conf)
        seg_module = seg_conf.get("module")
        if args.debug:
            print("Processing: %s" % seg_module)
        try:
            _segment = importer.import_segment(seg_module)

            segment = _segment(hyper_prompt, seg_conf)
            segment.start()
            segment.join()
            segment_threads.append(segment)
        except helpers.ModuleNotFoundException as e:
            if args.debug:
                print("ERROR: %s" % str(e))

    hyper_prompt.add_segments(segment_threads)

    if draw:
        prompt_draw = hyper_prompt.draw()
        sys.stdout.write(prompt_draw)
        return prompt_draw
    return hyper_prompt


def process(args):
    valid_config = config.get(args)
    _importer = helpers.Importer()

    theme_conf = valid_config.get("theme", "default") or "default"
    theme_conf = helpers.ensure_dict(theme_conf, conf_type="theme")
    theme_module = theme_conf.get("module")

    _theme = _importer.import_theme(theme_module)
    theme = _theme(theme_conf)

    if args.showall == "separator":
        for sep in defaults.SEPARATORS.keys():
            args.separator = sep
            build_prompt(
                args, valid_config, theme, importer=_importer, newline=True
            )
        return True
    return build_prompt(args, valid_config, theme, importer=_importer)


def get_fallback_prompt(args):
    active_prompt = str(os.environ.get("PROMPT"))
    if args.fallback:
        active_prompt = args.fallback
    sys.stdout.write(active_prompt)


def main():
    args = parser()

    if args.version:
        import hyper_prompt

        print(hyper_prompt.__version__)
        return 0

    s = signal.signal(signal.SIGINT, signal.SIG_IGN)
    try:
        if not os.environ.get("HYPER_PROMPT_DISABLE", None) == "1":
            process(args)
        else:
            get_fallback_prompt(args)
    except Exception as e:
        if args.debug:
            print("ERROR: %s" % str(e))
        get_fallback_prompt(args)
    signal.signal(signal.SIGINT, s)
    return 0
