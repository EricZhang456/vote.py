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
        from .tf2.types import VOTE_PASS_DEFAULT_REASONS
        from events.manager import game_event_manager
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
            vote_controller = BaseEntity.find("vote_controller")
            return vote_controller.get_network_property_int("m_iActiveIssueIndex") != -1
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
        """Method for sending the vote. Must be implemented in subclass.
        
        :raises NotImplementedError: Method not implemented in subclass.
        """
        raise NotImplementedError("Must be implemented in subclass.")

    def send_pass_custom(self, pass_reason: VotePassTypes | None = None,
                         detail: str = "", index: int | None = None):
        """Display a vote pass panel.
        
        :param VotePassTypes or None pass_reason: Optional reason for vote pass for
                                                    a custom vote pass type.
        :param str detail: Optional detail paramater for supported vote pass types.
        :param int or None index: Optional client index to send to vote menu to.
                                Will send vote to every client if not specified.
        :raises RuntimeError: Game not supported.
        """
        if pass_reason is None:
            default_reason = VOTE_PASS_DEFAULT_REASONS.get(self.vote_type)
            if default_reason is None:
                pass_reason = getattr(VotePassTypes, self.vote_type.name)
            else:
                pass_reason = default_reason
        match GAME_NAME:
            case "tf":
                vote_pass = VotePass(pass_reason.value, detail, 0)
            case _:
                raise RuntimeError("Game not supported.")
        if index is None:
            vote_pass.send()
        else:
            vote_pass.send(index)

    def send_fail(self, fail_reason: VoteFailedReason = VoteFailedReason.VOTE_FAILED_GENERIC,
                  index: int | None = None):
        """Display a vote fail panel.
        
        :param VoteFailedReason fail_reason: Reason for vote fail. Defaults to 
                                            VoteFailedReason.VOTE_FAILED_GENERIC.
        :param int or None index: Optional client index to send to vote menu to.
                                Will send vote to every client if not specified.
        :raises RuntimeError: Game not supported.
        """
        match GAME_NAME:
            case "tf":
                fail = VoteFailed(0, fail_reason.value)
            case _:
                raise RuntimeError("Game not supported.")
        if index is None:
            fail.send()
        else:
            fail.send(index)

    def _send(self, is_yes_no_vote: bool, index: int | None = None):
        """Base method for sending the vote.
        
        :param bool is_yes_no_vote: True if the vote is a yes/no vote. False otherwise.
        :param int or None index: Optional client index to send to vote menu to.
                                Will send vote to every client if not specified.
        :raises RuntimeError: Game not supported.
        """
        match GAME_NAME:
            case "tf":
                vote = VoteStart(self.vote_type.value, self.detail,
                                 is_yes_no_vote, 0, self.initiator)
            case _:
                raise RuntimeError("Game not supported.")
        if index is None:
            vote.send()
        else:
            vote.send(index)

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
        :raises ValueError: Vote type not supported.
        :raises RuntimeError: Game not supported.
        """
        if vote_type not in multi_vote_types:
            raise ValueError("Vote type not supported.")
        if GAME_NAME not in ("tf", "csgo"):
            raise RuntimeError("Game not supported.")
        super().__init__(vote_type, initiator, detail)
        if len(items) > 5:
            items = items[:5]
        self.items = items

    def send(self, index: int | None = None):
        vote_options_event = game_event_manager.create_event("vote_options", True)
        vote_options_event.set_int("count", len(self.items))
        for item in self.items:
            vote_options_event.set_string(f"option{self.items.index(item) + 1}", item.display)
        game_event_manager.fire_event(vote_options_event, True)
        super()._send(False, index)
