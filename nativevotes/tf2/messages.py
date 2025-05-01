"""Voting user messages for Team Fortress 2."""

from messages.base import UserMessageCreator

class VoteStart(UserMessageCreator):
    """Create a VoteStart."""

    message_name = "VoteStart"
    translatable_fields = ["details_str"]
    reliable = True

    def __init__(self, disp_str: str, details_str: str, is_yes_no_vote: bool,
                 team: int, ent_idx: int):
        """Show a vote start panel.

        :param str disp_str: Vote issue translation string.
        :param str details_str: Vote issue text.
        :param bool is_yes_no_vote: True for Yes/No vote, False for multiple choice
        :param int team: Team index or 0 for all
        :param int ent_idx: Client index of person who started the vote, or 99 for the server.
        """
        super().__init__(disp_str=disp_str, details_str=details_str,
                         is_yes_no_vote=is_yes_no_vote, team=team, ent_idx=ent_idx)

    def bitbuf(self, buffer, translated_kwargs):
        """Send the VoteStart with bitbuf."""
        buffer.write_byte(translated_kwargs.team)
        buffer.write_byte(translated_kwargs.ent_idx)
        buffer.write_string(translated_kwargs.disp_str)
        buffer.write_string(translated_kwargs.details.str)
        buffer.write_byte(translated_kwargs.is_yes_no_vote)

    protobuf = None

class VotePass(UserMessageCreator):
    """Create a VotePass."""

    message_name = "VotePass"
    translatable_fields = ["details_str"]

    def __init__(self, disp_str: str, details_str: str, team: int):
        """Show a vote pass panel.
        
        :param str disp_str: Vote success translation string.
        :param str details_str: Vote winner.
        :param int team: Team index or 0 for all.
        """
        super().__init__(disp_str=disp_str, details_str=details_str, team=team)

    def bitbuf(self, buffer, translated_kwargs):
        """Send the VotePass with bitbuf."""
        buffer.write_byte(translated_kwargs.team)
        buffer.write_string(translated_kwargs.disp_str)
        buffer.write_string(translated_kwargs.details_str)

    protobuf = None

class VoteFailed(UserMessageCreator):
    """Create a VoteFailed."""

    message_name = "VoteFailed"
    translatable_fields = []

    def __init__(self, team: int, reason: int):
        """Show a vote failed panel.

        :param int team: Team index or 0 for all.
        :param int reason: Failure reason code (0, 3-4).
        """
        super().__init__(team=team, reason=reason)

    def bitbuf(self, buffer, translated_kwargs):
        """Send the VoteFailed with bitbuf."""
        buffer.write_byte(translated_kwargs.team)
        buffer.write_byte(translated_kwargs.reason)

    protobuf = None

class CallVoteFailed(UserMessageCreator):
    """Create a CallVoteFailed."""

    message_name = "CallVoteFailed"
    translatable_fields = []

    def __init__(self, reason: int, time: int):
        """Show a call vote failed panel.
        
        :param int reason: Failure reason (1-2, 5-10, 12-19).
        :param int time: For failure reasons 2 and 8, time in seconds until client
                can start another vote. 2 is per user, 8 is per vote type.
        """
        super().__init__(reason=reason, time=time)

    def bitbuf(self, buffer, translated_kwargs):
        """Send the CallVoteFailed with bitbuf."""
        buffer.write_byte(translated_kwargs.reason)
        buffer.write_short(translated_kwargs.time)

    protobuf = None
