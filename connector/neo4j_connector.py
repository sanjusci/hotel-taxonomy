
__author__ = "Sanjeev Kumar"
__email__ = "sanjeev.k@srijan.net"
__copyright__ = "Copyright 2019, Srijan Technologies Pvt. Ltd."

from connector.connector import Connector
from neo4j import GraphDatabase


class Neo4jConnector(Connector):

    def __init__(self, uri, user, password):
        """

        :param uri:
        :param user:
        :param password:
        """
        self.uri = uri
        self.user = user
        self.password = password

    def connect(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        return GraphDatabase.driver(
            self.uri,
            auth=(self.user, self.password)
        )

    def close(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        pass
