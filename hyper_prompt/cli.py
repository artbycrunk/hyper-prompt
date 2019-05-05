
import argparse
import sys

from . import config, helpers, prompt


def parser():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--shell', action='store', default='bash',
                            help='Set this to your shell type',
                            choices=['bash', 'tcsh', 'zsh', 'bare'])
    arg_parser.add_argument('prev_error', nargs='?', type=int, default=0,
                            help='Error code returned by the last command')
    return arg_parser.parse_args()


def main():
    args = parser()
    valid_config = config.get()

    _importer = helpers.Importer()

    theme_conf = valid_config.get("theme", "default")
    theme_conf = helpers.ensure_dict(theme_conf, conf_type="theme")
    theme_module = theme_conf.get("module")

    theme = _importer.import_theme(theme_module)

    hyper_prompt = prompt.Prompt(args, valid_config, theme)

    segment_threads = list()
    for seg_conf in valid_config.get("segments", []):
        seg_conf = helpers.ensure_dict(seg_conf)
        seg_module = seg_conf.get("module")
        _segment = _importer.import_segment(seg_module)

        segment = _segment(hyper_prompt, seg_conf)
        segment.start()
        segment.join()
        segment_threads.append(segment)

    hyper_prompt.add_segments(segment_threads)

    sys.stdout.write(hyper_prompt.draw())
    return 0
