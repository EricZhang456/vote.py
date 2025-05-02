"""Provides voting functionality."""

# pylint: disable = global-statement

from abc import abstractmethod
from dataclasses import dataclass

from core import GAME_NAME
from entities.entity import BaseEntity

multi_vote_types = []
current_vote: object | None = None

match GAME_NAME:
    case "tf":
        from .tf2.messages import VoteStart, VotePass, VoteFailed, CallVoteFailed
        from .tf2.types import VoteTypes, VotePassTypes, VoteFailedReason, CallVoteFailedReason
        multi_vote_types.append(VoteTypes.NEXT_LEVEL, VoteTypes.CUSTOM)
    case _:
        raise RuntimeError("Game not supported.")

def show_call_vote_fail(player_index: int, vote_fail_type: CallVoteFailedReason,
                        time: int = 0):
    """Send a call vote fail panel to client.
    
    :param int player_index: Client index of the target client.
    :param CallVoteFailedReason vote_fail_type: Reason of the call vote failure.
    :param int time: Optional time paramater for certian types of failure, defaults to 0.
    """
    CallVoteFailed(vote_fail_type.value, time).send(player_index)

def get_game_vote_in_progress() -> bool:
    """Check if a vote is in progress.
    
    :return: True if a vote is in progress, False otherwise.
    :rtype: bool
    :raises RuntimeError: Game not supported.
    """
    match GAME_NAME:
        case "tf" | "csgo":
            return BaseEntity.find("vote_controller").get_network_property_int("m_iActiveIssueIndex") != -1
        case _:
            raise RuntimeError("Game not supported.")

def get_current_vote() -> object | None:
    """Get the ongoing vote object.
    
    :return: Object of the ongoing vote, None if there are no votes ongoing.
    :rtype: object or None
    """
    return current_vote

class _Vote():
    """Base vote class."""

    def __init__(self, vote_type: VoteTypes, initiator: int, detail: str = ""):
        """Initialize a vote.

        :param VoteTypes vote_type: Type of the vote.
        :param int initiator: Client index of the initator of the vote.
        :param str detail: Optional detail paramater for supported vote types.
        """
        self.vote_type = vote_type
        self.initiator = initiator
        self.detail = detail
        global current_vote
        current_vote = self

    @abstractmethod
    def send(self):
        """Method for sending the vote. Must be implemented in subclass."""
        raise NotImplementedError("Must be implemented in subclass.")

    def _send(self, is_yes_no_vote: bool, index: int | None = None):
        """Base method for sending the vote.
        
        :param bool is_yes_no_vote: True if the vote is a yes/no vote. False otherwise.
        :param int or None index: Optional client index to send to vote menu to.
                                Will send vote to every client if not specified.
        :raises RuntimeError: Game not supported.
        """
        match GAME_NAME:
            case "tf2":
                VoteStart(self.vote_type.value, self.detail, is_yes_no_vote, 0,
                          self.initiator).send(index)
            case _:
                raise RuntimeError("Game not supported.")

@dataclass
class MultiVoteOption():
    """An item for a multiple choices vote.
        
    :param str info: Item information string.
    :param str display: Text to display for the item on the vote menu.
    """
    info: str
    display: str

class MultiVote(_Vote):
    """Create a multiple choices vote."""

    def __init__(self, vote_type: VoteTypes, initiator: int,
                 items: list[MultiVoteOption], detail: str = ""):
        """Initialize a multiple choices vote.

        :param VoteTypes vote_type: Type of the vote.
        :param int initiator: Client index of the initator of the vote.
        :param list[MultiVoteOption] items: A list of items to be included in the vote.
        :param str detail: Optional detail paramater for supported vote types.
        """
        if vote_type not in multi_vote_types:
            raise ValueError("Vote type not supported.")
        super().__init__(vote_type, initiator, detail)
        self.items = items

    def send(self, index: int | None = None):
        # TODO: Set vote_options entity before sending
        super()._send(False, index)
