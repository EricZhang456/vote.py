"""Voting types for Team Fortress 2."""

from enum import Enum

class VoteTypes(Enum):
    """Vote types available when starting a vote."""
    KICK = "#TF_vote_kick_player_other"
    """Generic kick vote."""
    KICK_IDLE = "#TF_vote_kick_player_idle"
    """Idler kick vote."""
    KICK_CHEATING = "#TF_vote_kick_player_cheating"
    """Cheater kick vote."""
    KICK_SCAMMING = "#TF_vote_kick_player_scamming"
    """Scammer kick vote."""
    RESTART_GAME = "#TF_vote_restart_game"
    """Restart map vote."""
    CHANGE_LEVEL = "#TF_vote_changelevel"
    """Change map vote."""
    NEXT_LEVEL = "#TF_vote_nextlevel"
    """Set next map vote."""
    NEXT_LEVEL_CHOICES = "#TF_vote_nextlevel_choices"
    """End of map vote. This vote is not in the user vote menu."""
    SCRAMBLE_TEAMS = "#TF_vote_scramble_teams"
    """Scramble teams vote."""
    SCRAMBLE_TEAMS_AT_ROUND_END = "#TF_vote_should_scramble_round"
    """Scramble teams at round end vote. This vote is not in the user vote menu."""
    START_ROUND = "#TF_vote_td_start_round"
    """Start round vote. This vote is not in the user vote menu."""
    CHANGE_MVM_MISSION = "#TF_vote_changechallenge"
    """Change MVM mission vote."""
    ETERNAWEEN = "#TF_vote_eternaween"
    """Activate Halloween mode vote."""
    AUTOBALANCE_ENABLE = "#TF_vote_autobalance_enable"
    """Activate autobalance vote."""
    AUTOBALANCE_DISABLE = "#TF_vote_autobalance_disable"
    """Disable autobalance vote."""
    CLASSLIMIT_ENABLE = "#TF_vote_passed_classlimits_enable"
    """Activate class limit vote."""
    CLASSLIMIT_DISABLE = "#TF_vote_passed_classlimits_disable"
    """Disable class limit vote."""
    CUSTOM = "#TF_playerid_noteam"
    """Custom vote."""

class VotePassTypes(Enum):
    """Vote success types."""
    KICK = "#TF_vote_passed_kick_player"
    """Vote kick passed."""
    RESTART_GAME = "#TF_vote_passed_restart_game"
    """Restart vote passed."""
    CHANGE_LEVEL = "#TF_vote_passed_changelevel"
    """Change level vote passed."""
    NEXT_LEVEL = "#TF_vote_passed_nextlevel"
    """Set next level vote passed."""
    NEXT_LEVEL_EXTEND = "#TF_vote_passed_nextlevel_extend"
    """Current map has been extended."""
    SCRAMBLE_TEAMS = "#TF_vote_passed_scramble_teams"
    """Scramble teams vote passed."""
    START_ROUND = "#TF_vote_passed_td_start_round"
    """Start round vote passed."""
    CHANGE_MVM_MISSION = "#TF_vote_passed_changechallenge"
    """Change MVM mission vote passed."""
    ETERNAWEEN = "#TF_vote_passed_eternaween"
    """Halloween mode vote passed."""
    AUTOBALANCE_ENABLE = "#TF_vote_passed_autobalance_enable"
    """Activate autobalance vote passed."""
    AUTOBALANCE_DISABLE = "#TF_vote_passed_autobalance_disable"
    """Disable autobalance vote passed."""
    CLASSLIMIT_ENABLE = "#TF_vote_passed_classlimits_enable"
    """Activate class limit vote passed."""
    CLASSLIMIT_DISABLE = "#TF_vote_passed_classlimits_disable"
    """Disable class limit vote passed."""
    CUSTOM = "#TF_playerid_noteam"
    """Custom vote passed."""

class VoteFailedReason(Enum):
    """Vote failed reasons."""
    VOTE_FAILED_GENERIC = 0
    """Generic Vote Failed message"""
    VOTE_FAILED_YES_MUST_EXCEED_NO = 3
    """Yes votes must outnumber No votes"""
    VOTE_FAILED_QUORUM_FAILURE = 4
    """Not enough votes"""

class CallVoteFailedReason(Enum):
    """Call vote failed reasons."""
    VOTE_FAILED_TRANSITIONING_PLAYERS = 1
    """Cannot call vote while other players are still loading. This appears to be a 
    holdover from L4D2; use code 10 instead."""
    VOTE_FAILED_RATE_EXCEEDED = 2
    """You called a vote recently and cannot call another one for X seconds."""
    VOTE_FAILED_ISSUE_DISABLED = 5
    """Server has disabled that issue."""
    VOTE_FAILED_MAP_NOT_FOUND = 6
    """That map does not exist."""
    VOTE_FAILED_MAP_NAME_REQUIRED = 7
    """You must specify a map name."""
    VOTE_FAILED_FAILED_RECENTLY = 8
    """This vote failed recently."""
    VOTE_FAILED_TEAM_CANT_CALL = 9
    """Your team cannot call this vote."""
    VOTE_FAILED_WAITINGFORPLAYERS = 10
    """Voting not allowed while Waiting for Players."""
    VOTE_FAILED_CANNOT_KICK_ADMIN = 12
    """Can't Kick Server Admin."""
    VOTE_FAILED_SCRAMBLE_IN_PROGRESS = 13
    """Vote Scramble is pending."""
    VOTE_FAILED_SPECTATOR = 14
    """Spectators can't vote."""
    VOTE_FAILED_NEXTLEVEL_SET = 15
    """Next level already set."""
    VOTE_FAILED_MAP_NOT_VALID = 16
    """Map is not in the map list."""
    VOTE_FAILED_CANNOT_KICK_FOR_TIME = 17
    """Cannot kick yet. Used for MVM."""
    VOTE_FAILED_CANNOT_KICK_DURING_ROUND = 18
    """Cannot kick during round. Used for MVM."""
    VOTE_FAILED_MODIFICATION_ALREADY_ACTIVE = 19
    """Modification is already active. Used by Eternaween."""

VOTE_PASS_DEFAULT_REASONS = {
    VoteTypes.KICK_IDLE: VotePassTypes.KICK,
    VoteTypes.KICK_CHEATING: VotePassTypes.KICK,
    VoteTypes.KICK_SCAMMING: VotePassTypes.KICK,
    VoteTypes.NEXT_LEVEL_CHOICES: VotePassTypes.NEXT_LEVEL,
    VoteTypes.SCRAMBLE_TEAMS_AT_ROUND_END: VotePassTypes.SCRAMBLE_TEAMS
}
