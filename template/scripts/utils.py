###########################################
# Logging setup
###########################################
import logging
import logging.config
import logging.handlers
import datetime

# logging setup info
today = datetime.date.today().strftime('%Y%m%d')
log_file = 'tmp_{}.log'.format(today)

# email info
fromaddr = 'galion.lidar@protonmail.com'
toaddrs = ['galion.lidar@protonmail.com', 'nicholas.hamilton@nrel.gov']
emailsubject = 'testing email handler'
email_pass = 'at6g1s_g'

log_format = (
    "%(asctime)s [%(levelname)s]: %(message)s in %(pathname)s:%(lineno)d")
log_level = logging.INFO


class data_logger(logging.Logger):
    '''
    data_logger subclass of logging.Logger() specifically records the relevant information produced during reception of CL51 atmospheric data.
    '''
    import logging

    def __init__(
            self,
            name,
            log_file,
            log_format=None,
            date_format=None,
            log_level='INFO',
    ):
        # provide defualt log_format and date_format strings
        if log_format is None:
            log_format = '%(asctime)s\n%(name)s\n%(levelname)s\n%(funcName)s %(lineno)d\n%(message)s \n'
        if date_format is None:
            date_format = '%Y/%m/%d %H:%M:%S'

        # make parameters accessible as part of the object interface
        self.name = name
        self.log_file = log_file
        self.log_format = log_format
        self.date_format = date_format
        self.log_level = log_level

        # inherit from logging.Logger class
        logging.Logger.__init__(self, name=name)

        # setup formatter
        data_logging_formatter = logging.Formatter(log_format, date_format)

        # setup logging handler
        data_logging_handler = logging.FileHandler(
            log_file,
            mode='a',
        )
        data_logging_handler.setLevel(log_level)
        data_logging_handler.setFormatter(data_logging_formatter)

        # instantiate logger
        self.setLevel(log_level)
        self.addHandler(data_logging_handler)


###########################################
# color info functions
###########################################


###########################################
def get_colors(ncolors, basecolor='cycle', reverse=False):
    """make a gradient of colors for use in plotting"""

    # nrel official colors
    nrelcolors = get_nrelcolors()

    if isinstance(basecolor, list):
        colors = basecolor  #[ nrelcolors[basecolor[x]][1] for x in range(len(basecolor))]
        cdict = polylinear_gradient(colors, ncolors + 2)
        colors = cdict['hex']

    elif basecolor in nrelcolors:
        nc = ncolors + 2
        colors = []
        while len(colors) < ncolors:
            nc += 1
            colors = [
                '#D1D5D8', nrelcolors[basecolor][1], nrelcolors[basecolor][0]
            ]
            cdict = polylinear_gradient(colors, nc)
            colors = cdict['hex']
            del colors[2]

    elif basecolor is 'cycle':
        nc = ncolors + 2
        colors = []
        while len(colors) < ncolors:
            nc += 1
            colors = ['#0079C2', '#D1D5D8', '#D9531E', '#00A4E4']
            cdict = polylinear_gradient(colors, nc)
            colors = cdict['hex']
            del colors[2]

    elif basecolor is 'span':
        colors = [nrelcolors['blue'][0], '#a1a5a7', nrelcolors['red'][0]]
        cdict = polylinear_gradient(colors, ncolors + 2)
        colors = cdict['hex']

    if reverse is True:
        colors = colors[-1::-1]

    return colors


def get_nrelcolors():
    nrelcolors = {
        'blue': ['#0079C2', '#00A4E4'],
        'red': ['#933C06', '#D9531E'],
        'green': ['#3D6321', '#5D9732'],
        'gray': ['#3A4246', '#5E6A71']
    }
    return nrelcolors


def hex_to_RGB(hex):
    ''' "#FFFFFF" -> [255,255,255] '''
    # Pass 16 to the integer function for change of base
    return [int(hex[i:i + 2], 16) for i in range(1, 6, 2)]


def RGB_to_hex(RGB):
    ''' [255,255,255] -> "#FFFFFF" '''
    # Components need to be integers for hex to make sense
    RGB = [int(x) for x in RGB]
    return "#" + "".join(
        ["0{0:x}".format(v) if v < 16 else "{0:x}".format(v) for v in RGB])


def linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
    ''' returns a gradient list of (n) colors between
    two hex colors. start_hex and finish_hex
    should be the full six-digit color string,
    inlcuding the number sign ("#FFFFFF") '''
    # Starting and ending colors in RGB form
    s = hex_to_RGB(start_hex)
    f = hex_to_RGB(finish_hex)
    # Initilize a list of the output colors with the starting color
    RGB_list = [s]
    # Calcuate a color at each evenly spaced value of t from 1 to n
    for t in range(1, n):
        # Interpolate RGB vector for color at the current value of t
        curr_vector = [
            int(s[j] + (float(t) / (n - 1)) * (f[j] - s[j])) for j in range(3)
        ]
        # Add it to our list of output colors
        RGB_list.append(curr_vector)

    return color_dict(RGB_list)


def color_dict(gradient):
    ''' Takes in a list of RGB sub-lists and returns dictionary of
    colors in RGB and hex form for use in a graphing function
    defined later on '''
    return {
        "hex": [RGB_to_hex(RGB) for RGB in gradient],
        "r": [RGB[0] for RGB in gradient],
        "g": [RGB[1] for RGB in gradient],
        "b": [RGB[2] for RGB in gradient]
    }


def polylinear_gradient(colors, n):
    """
    returns a list of colors forming linear gradients between
    all sequential pairs of colors. n specifies the total
    number of desired output colors
    """
    # The number of colors per individual linear gradient
    n_out = int(float(n) / (len(colors) - 1))
    # returns dictionary defined by color_dict()
    gradient_dict = linear_gradient(colors[0], colors[1], n_out)

    if len(colors) > 1:
        for col in range(1, len(colors) - 1):
            next = linear_gradient(colors[col], colors[col + 1], n_out)
            for k in ("hex", "r", "g", "b"):
                # Exclude first point to avoid duplicates
                gradient_dict[k] += next[k][1:]

    return gradient_dict


###########################################
