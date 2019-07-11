from colorama import init, Fore, Back, Style
import textwrap
import sys
from wcwidth import wcswidth
from common.env.env import env

percentage_significant_figures = 1
init()

margin = '  '
line_width = 150

simple_mode = env['app_settings']['simple_unicode_output']

error_symbol = u'\u274c' if not simple_mode else 'E'

warn_symbol = u'\u26A0' if not simple_mode else '!'

info_symbol = u'\u2139' if not simple_mode else 'i'

step_symbol = u'\u25CF' if not simple_mode else '*'

success_symbol = u'\u2714'  # this seems to be supported by most environments

not_done_symbol = u'\u25CB' if not simple_mode else 'x'


def is_double_width_char(c: str) -> bool:
    return wcswidth(c) == 2 or c in [u'\u26A0',
                                     u'\u2139']

def error(message, carriage_return=False, wrap_text=True, new_line=True):
    print_line(error_symbol,
               Fore.RED,
               message,
               Fore.RED,
               carriage_return=carriage_return,
               wrap_text=wrap_text,
               new_line=new_line)


def warn(message, wrap_text=True, new_line=True):
    print_line(warn_symbol,
               Fore.YELLOW,
               message,
               Fore.YELLOW,
               wrap_text=wrap_text,
               new_line=new_line)


def info(message, carriage_return=False, wrap_text=True, new_line=True):
    print_line(info_symbol,
               Fore.WHITE,
               message,
               Fore.WHITE,
               carriage_return=carriage_return,
               wrap_text=wrap_text,
               new_line=new_line)


def step(message, wrap_text=True, new_line=True):
    print_line(step_symbol,
               Fore.BLUE,
               message,
               Fore.WHITE,
               wrap_text=wrap_text,
               new_line=new_line)


def success(message, carriage_return=False, wrap_text=True, new_line=True):
    print_line(success_symbol,
               Fore.GREEN,
               message,
               Fore.GREEN,
               carriage_return=carriage_return,
               wrap_text=wrap_text,
               new_line=new_line)


def success_only_green_tick(message, carriage_return=False, wrap_text=True, new_line=True):
    print_line(success_symbol,
               Fore.GREEN,
               message,
               Fore.WHITE,
               carriage_return=carriage_return,
               wrap_text=wrap_text,
               new_line=new_line)


def not_done(message, wrap_text=True, new_line=True):
    print_line(not_done_symbol,
               Fore.YELLOW,
               message,
               Fore.WHITE,
               wrap_text=wrap_text,
               new_line=new_line)


def print_line(symbol_char, symbol_color, message, message_color, carriage_return=False, wrap_text=True, new_line=True):
    _margin = margin[:len(margin)-1] \
        if is_double_width_char(symbol_char) and env['app_settings']['fix_double_width_unicode_symbols'] \
        else margin

    text_raw = (('\r' if carriage_return else '')
                + symbol_color
                + symbol_char
                + Style.RESET_ALL
                + _margin
                + message_color
                + message
                + Style.RESET_ALL)

    text = text_raw
    if wrap_text and not carriage_return:
        text = textwrap.fill(text_raw,
                             line_width,
                             subsequent_indent=' '*(len(margin)+1),
                             replace_whitespace=False)
    elif not wrap_text and not carriage_return:
        # indentation on subsequent lines
        text_raw = text_raw.replace('\n', '\n' + '  '*(len(margin)+1))
        text = textwrap.fill(text_raw,
                             400,
                             subsequent_indent=' '*(len(margin)+1),
                             replace_whitespace=False)

    sys.stdout.write(text + ('\n' if new_line else ''))


def rounded_percentage_integers(a, b):
    return round((float(a)/float(b)) * 100, percentage_significant_figures)


def integer_progress(a, b):
    return f'{a}/{b} [{rounded_percentage_integers(a, b)}%]'


def print_http_progress(
        n_current,
        n_total,
        n_success,
        post_action_msg,
        error_code_counts,
        suffix=''):
    sys.stdout.write(
        f'\r{integer_progress(n_current, n_total)} processed | {n_success}/{n_total} {post_action_msg} | HTTP codes: {error_code_counts} {suffix}')
    sys.stdout.flush()
