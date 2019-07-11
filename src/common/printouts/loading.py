import itertools
import threading
import time
import sys
from .general import info

class Enum(object):
    def __init__(self):
        # the subclasses declare class attributes which are numbers.
        # Upon instantiation we define instance attributes, which are the same
        # as the class attributes but wrapped with the ANSI escape sequence
        for name in dir(self):
            if not name.startswith('_'):
                value = getattr(self, name)
                setattr(self, name, value)

class _Animations(Enum):
    SPINNER = ['| ', '/ ', '--', '\\ ']
    BUILDING_TOWER = [u'\u2581', u'\u2582', u'\u2583', u'\u2584', u'\u2585', u'\u2586', u'\u2587']
    HORIZONTAL_MORPHING_BARS = ['▉', '▊', '▋', '▌', '▍', '▎', '▏', '▎', '▍', '▌', '▋', '▊', '▉']
    VERTICAL_MORPHING_CIRCLE = ['◡', '⊙', '◠', '⊙']
    FILLING_DIAMOND = ['◇', '◈', '◆']
    ELLIPSIS = ['.  ', '.. ', '...', '.. ']

# BUG: Changing the name of this to something like "LoadingDisplay" causes an error
# relating to "self._target". Can't seem to reproduce it consistently. Very strange...
class Spinner(threading.Thread):
    """
    Class that displays a loading animation, utilising threading.Thread.
    
    Initiatation example:
    ```
    spinner = Spinner(...attributes)
    spinner.start()
    # Long running task...
    spinner.stop(failed=bool)
    ```

    Attributes:
        suffix (str): Text displayed after the animated loading characters during loading
        done_message_prefix (str): Text displayed before the time-taken display when done
        animation (list): One of the animations, i.e. Animations.ELLIPSIS. Can be any list of characters.
    """

    t = None
    i = 0
    dt_s = None
    done = False
    suffix = None
    start_time = None
    done_message_prefix = None
    done_message = None
    frames = None
    
    def __init__(self,
                 suffix='Loading',
                 done_message_prefix='Done',
                 animation=_Animations.ELLIPSIS) -> bool:
        self.frames = animation
        self.suffix = suffix
        self.done_message_prefix = done_message_prefix

    def start(self):
        """Start the animation."""
        self.t = threading.Thread(target=self._animate)
        self.t.start()
        self.start_time=time.time()

    def stop(self, failed=False):
        """Stop the animation. failed=True causes "Failed" instead of standard done message."""
        self.i = 0
        dt_s = time.time() - self.start_time
        prefix = self.done_message_prefix if not failed else 'Failed'
        self.done_message = f'{prefix} ({round(dt_s, 2)}s)     '
        self.done = True
        self.t.join()

    def _animate(self):
        for c in itertools.cycle(self.frames):
            if self.done:
                break
            if self.i == 0 or self.i % 10 == 0:
                if self.start_time:
                    self.dt_s = time.time() - self.start_time
                else:
                    self.dt_s = 0
            sys.stdout.write(f'\r{c}  {self.suffix} [{round(self.dt_s, 1)}s]')

            self.i = self.i + 1
            
            sys.stdout.flush()
            time.sleep(0.2)
        info(self.done_message, carriage_return=True)


Animations = _Animations()