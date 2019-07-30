__author__ = "Sanjeev Kumar"
__email__ = "sanjeev.k@srijan.net"
__copyright__ = "Copyright 2019, Srijan Technologies Pvt. Ltd."


class Connector(object):

    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        """
        pass

    def connect(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        pass

    @classmethod
    def setup(cls, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        return cls(*args, **kwargs)

    def close(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        pass



