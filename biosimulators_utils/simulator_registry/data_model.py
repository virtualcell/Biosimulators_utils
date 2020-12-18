""" Data model for submitting simulators to the BioSimulators registry

:Author: Jonathan Karr <karr@mssm.edu>
:Date: 2020-12-06
:Copyright: 2020, Center for Reproducible Biomedical Modeling
:License: MIT
"""

import enum


class IssueLabel(str, enum.Enum):
    validated = 'Validated'
    invalid = 'Invalid'
    approved = 'Approved'
    action_error = 'Action error'


class SimulatorSubmission(object):
    """ Submission of a simulator to the BioSimulators registry

    Attributes:
        id (:obj:`str`): id of simulator (e.g., `tellurium` or `vcell`)
        version (:obj:`str`): version of simulator (e.g., `2.1.6`)
        specifications_url (:obj:`str`): URL for the specifications of the version of the simulator
            (e.g., `https://raw.githubusercontent.com/biosimulators/Biosimulators_tellurium/2.1.6/biosimulators.json`)
        validate_image (:obj:`bool`): if :obj:`True`, validate Docker image
        commit_simulator (:obj:`bool`): if :obj:`True`, commit simulator to database
    """

    def __init__(self, id=None, version=None, specifications_url=None,
                 validate_image=False, commit_simulator=False,
                 validated=False, approved=False, committed=False):
        """
        Args:
            id (:obj:`str`, optional): id of simulator
            version (:obj:`str`, optional): version of simulator
            specifications_url (:obj:`str`, optional): URL for the specifications of the version of the simulator
            validate_image (:obj:`bool`, optional): if :obj:`True`, validate Docker image
            commit_simulator (:obj:`bool`, optional): if :obj:`True`, commit simulator to database
            validated (:obj:`bool`, optional): :obj:`True`, if the simulator has been validated
            approved (:obj:`bool`, optional): :obj:`True`, if the simulator has been approved for committment to the BioSimulators registry
            committed (:obj:`bool`, optional): :obj:`True`, if the simulator has been committed to the BioSimulators registry
        """
        self.id = id
        self.version = version
        self.specifications_url = specifications_url
        self.validate_image = validate_image
        self.commit_simulator = commit_simulator
        self.validated = validated
        self.approved = approved
        self.committed = committed

    def to_tuple(self):
        """ Tuple representation of a person

        Returns:
            :obj:`tuple` of :obj:`str`: tuple representation of a person
        """
        return (self.id, self.version, self.specifications_url, self.validate_image, self.commit_simulator,
                self.validated, self.approved, self.committed)

    def is_equal(self, other):
        """ Determine if two submissions are equal

        Args:
            other (:obj:`SimulatorSubmission`): another submission

        Returns:
            :obj:`bool`: :obj:`True`, if two submissions are equal
        """
        return self.__class__ == other.__class__ \
            and self.id == other.id \
            and self.version == other.version \
            and self.specifications_url == other.specifications_url \
            and self.validate_image == other.validate_image \
            and self.commit_simulator == other.commit_simulator \
            and self.validated == other.validated \
            and self.approved == other.approved \
            and self.committed == other.committed
