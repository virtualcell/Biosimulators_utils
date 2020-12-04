from ..data_model import Person
from ..utils.core import are_lists_equal

__all__ = [
    'Metadata',
    'ExternalReferences',
    'Citation',
    'Identifier',
    'OntologyTerm',
]


class Metadata(object):
    """ Metadata about an object

    Attributes:
        description (:obj:`str`): description
        tags (:obj:`list` of :obj:`str`): tags
        authors (:obj:`list` of :obj:`Person`): authors
        references (:obj:`ExternalReferences`): identifiers and citations
        license (:obj:`OntologyTerm`): license
    """

    def __init__(self, description=None, tags=None, authors=None, references=None, license=None):
        """
        Args:
            description (:obj:`str`, optional): description
            tags (:obj:`list` of :obj:`str`, optional): tags
            authors (:obj:`list` of :obj:`Person`, optional): authors
            references (:obj:`ExternalReferences`, optional): identifiers and citations
            license (:obj:`OntologyTerm`, optional): license
        """
        self.description = description
        self.tags = tags or []
        self.authors = authors or []
        self.references = references
        self.license = license

    def to_tuple(self):
        """ Get a tuple representation

        Returns:
            :obj:`tuple` of :obj:`str`: tuple representation
        """
        return (self.description, tuple(self.tags),
                tuple(sorted(author.to_tuple() for author in self.authors)),
                self.references.to_tuple() if self.references else None,
                self.license.to_tuple() if self.license else None)

    def is_equal(self, other):
        """ Determine if metadata are equal

        Args:
            other (:obj:`Metadata`): another metadata

        Returns:
            :obj:`bool`: :obj:`True`, if two metadata are equal
        """
        return self.__class__ == other.__class__ \
            and self.description == other.description \
            and sorted(self.tags) == sorted(other.tags) \
            and are_lists_equal(self.authors, other.authors) \
            and ((self.references is None and self.references == other.references)
                 or (self.references is not None and self.references.is_equal(other.references))) \
            and ((self.license is None and self.license == other.license)
                 or (self.license is not None and self.license.is_equal(other.license)))


class ExternalReferences(object):
    """ Identifiers and citations of an object

    Attributes:
        identifiers (:obj:`list` of :obj:`Identifier`): identifiers
        citations (:obj:`list` of :obj:`Citation`): citations
    """

    def __init__(self, identifiers=None, citations=None):
        """
        Args:
            identifiers (:obj:`list` of :obj:`Identifier`, optional): identifiers
            citations (:obj:`list` of :obj:`Citation`, optional): citations
        """
        self.identifiers = identifiers or []
        self.citations = citations or []

    def to_tuple(self):
        """ Get a tuple representation

        Returns:
            :obj:`tuple` of :obj:`str`: tuple representation
        """
        return (
            tuple(sorted(identifier.to_tuple() for identifier in self.identifiers)),
            tuple(sorted(citation.to_tuple() for citation in self.citations)),
        )

    def is_equal(self, other):
        """ Determine if collections of external references are equal

        Args:
            other (:obj:`ExternalReferences`): another collection of external referencse

        Returns:
            :obj:`bool`: :obj:`True`, if two collections of external references are equal
        """
        return self.__class__ == other.__class__ \
            and are_lists_equal(self.identifiers, other.identifiers) \
            and are_lists_equal(self.citations, other.citations)


class Citation(object):
    """ A citation

    Attributes:
        title (:obj:`str`): title
        authors (:obj:`str`): authors
        journal (:obj:`str`): journal
        volume (:obj:`str`): volume
        issue (:obj:`str`): issue
        pages (:obj:`str`): pages
        year (:obj:`int`): year
        identifiers (:obj:`list` of :obj:`Identifier`): identifiers
    """

    def __init__(self, title=None, authors=None, journal=None, volume=None, issue=None, pages=None, year=None, identifiers=None):
        """
        Args:
            title (:obj:`str`, optional): title
            authors (:obj:`str`, optional): authors
            journal (:obj:`str`, optional): journal
            volume (:obj:`str`, optional): volume
            issue (:obj:`str`, optional): issue
            pages (:obj:`str`, optional): pages
            year (:obj:`int`, optional): year
            identifiers (:obj:`list` of :obj:`Identifier`, optional): identifiers
        """
        self.title = title
        self.authors = authors
        self.journal = journal
        self.volume = volume
        self.issue = issue
        self.pages = pages
        self.year = year
        self.identifiers = identifiers or []

    def to_tuple(self):
        """ Get a tuple representation

        Returns:
            :obj:`tuple` of :obj:`str`: tuple representation
        """
        return (
            self.title,
            self.authors,
            self.journal,
            self.volume,
            self.issue,
            self.pages,
            self.year,
            tuple(sorted(identifier.to_tuple() for identifier in self.identifiers)),
        )

    def is_equal(self, other):
        """ Determine if citations are equal

        Args:
            other (:obj:`Citation`): another citation

        Returns:
            :obj:`bool`: :obj:`True`, if two citations are equal
        """
        return self.__class__ == other.__class__ \
            and self.title == other.title \
            and self.authors == other.authors \
            and self.journal == other.journal \
            and self.volume == other.volume \
            and self.issue == other.issue \
            and self.pages == other.pages \
            and self.year == other.year \
            and are_lists_equal(self.identifiers, other.identifiers)


class Identifier(object):
    """ An identifier

    Attributes:
        namespace (:obj:`str`): namespace
        id (:obj:`str`): id
        url (:obj:`str`): URL
    """

    def __init__(self, namespace=None, id=None, url=None):
        """
        Args:
            namespace (:obj:`str`, optional): namespace
            id (:obj:`str`, optional): id
            url (:obj:`str`, optional): URL
        """
        self.namespace = namespace
        self.id = id
        self.url = url

    def to_tuple(self):
        """ Get a tuple representation

        Returns:
            :obj:`tuple` of :obj:`str`: tuple representation
        """
        return (self.namespace, self.id, self.url)

    def is_equal(self, other):
        """ Determine if identifiers are equal

        Args:
            other (:obj:`Identifier`): another identifier

        Returns:
            :obj:`bool`: :obj:`True`, if two identifiers are equal
        """
        return self.__class__ == other.__class__ \
            and self.namespace == other.namespace \
            and self.id == other.id \
            and self.url == other.url


class OntologyTerm(Identifier):
    """ Term in an ontology """
    pass
