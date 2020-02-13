#!/usr/bin/env python
# encoding: utf-8

# Imports
import random
from typing import Sequence, List, Dict, Optional, TypeVar

from dotmap import DotMap

from . import probabilities as prob
from .agent import Agent, Agent_set


def get_partner(
    agent: Agent, all_agent_set: Agent_set, params: DotMap
) -> Optional[Agent]:
    """
    :Purpose:
        Get partner for agent.

    :Input:
        agent : Agent

        all_agent_set: AgentSet of partners to pair with

    :Output:
        partner: new partner
    """
    agent_drug_type = agent._DU
    RandomPartner = None

    if agent_drug_type == "IDU":
        if random.random() < 0.8:
            # choose from IDU agents
            RandomPartner = get_random_IDU_partner(agent, all_agent_set)

        # either didn't try to get IDU partner, or failed to get IDU partner
        if RandomPartner is None:
            get_random_sex_partner(agent, all_agent_set, params)
    elif agent_drug_type in ("NDU", "NIDU"):
        if params.features.assort_mix and (
            random.random()
            < params.demographics[agent._race].assort_mix.coefficient
        ):
            RandomPartner = get_assort_sex_partner(agent, all_agent_set, params)

            # try again with random sex partner is assort mix percent not 100%
            if RandomPartner is None and params.assort_mix.coefficient <= 1.0:
                RandomPartner = get_random_sex_partner(agent, all_agent_set, params)
        else:
            RandomPartner = get_random_sex_partner(agent, all_agent_set, params)
    else:
        raise ValueError("Check method _get_partners(). Agent not caught!")

    if RandomPartner == agent:
        return None
    else:
        return RandomPartner


def get_random_IDU_partner(agent: Agent, all_agent_set: Agent_set) -> Optional[Agent]:
    """
    :Purpose:
        Get a random partner which is sex compatible

    :Input:
        agent: Agent
        all_agent_set: AgentSet of partners to pair with

    :Output:
        partner : Agent or None

    """
    agent_drug_type = agent._DU
    assert agent_drug_type == "IDU", "Agent's drug type must be IDU"

    RandomPartner = None

    RandomPartner = safe_random_choice(
        [
            ptn
            for ptn in all_agent_set._subset["DU"]._subset["IDU"]._members
            if ptn not in agent._partners and ptn != agent
        ]
    )

    return RandomPartner


def get_assort_sex_partner(
    agent: Agent, all_agent_set: Agent_set, params: DotMap
) -> Optional[Agent]:
    """
    :Purpose:
        Get a random partner which is sex compatible and fits assortativity constraints

    :Input:
        agent: int
        all_agent_set: AgentSet of partners to pair with

    :Output:
        partner : Agent or None

    """
    RandomPartner = None

    assert agent._SO in params.classes.sex_types

    eligPartnerType = params.demographics[agent._race][
        agent._SO
    ]  # TO_REVIEW elgsepartnertype gone self-partnering for now?
    eligible_partners = all_agent_set._subset["SO"]._subset[eligPartnerType]._members

    if params.assort_mix.type == "Race":
        samplePop = [
            tmpA
            for tmpA in eligible_partners
            if (tmpA._race == agent._race and tmpA not in agent._partners)
        ]

    elif params.assort_mix.type == "Client":
        if agent._race == "WHITE":
            samplePop = [
                tmpA
                for tmpA in eligible_partners
                if (tmpA._race == "WHITE" and tmpA not in agent._partners)
            ]
        else:
            samplePop = [
                tmpA
                for tmpA in eligible_partners
                if (
                    tmpA._race == "WHITE"
                    and tmpA._everhighrisk_bool
                    and tmpA not in agent._partners
                )
            ]

    elif params.assort_mix.type == "HR":
        samplePop = [
            tmpA
            for tmpA in eligible_partners
            if (tmpA._everhighrisk_bool and tmpA not in agent._partners)
        ]

    RandomPartner = safe_random_choice(samplePop)

    # partner can't be existing parter or agent themself
    if RandomPartner in agent._partners or RandomPartner == agent:
        RandomPartner = None

    return RandomPartner


def get_random_sex_partner(
    agent: Agent, all_agent_set: Agent_set, params: DotMap
) -> Optional[Agent]:
    """
    :Purpose:
        Get a random partner which is sex compatible

    :Input:
        agent: Agent
        all_agent_set: list of available partners (Agent_set)

    :Output:
        partner : Agent or None

    """
    random_partner = None

    # eligPtnType = params.demographics[agent._race][
    #     agent._SO
    # ]  # TO_REVIEW what to do here
    elig_partner_pool = [partner for partner in all_agent_set._members if sex_possible(agent._SO, partner._SO, params)]

    random_partner = safe_random_choice(elig_partner_pool)

    if (random_partner in agent._partners) or (random_partner == agent):
        random_partner = None

    return random_partner


def sex_possible(agent_sex_type: str, partner_sex_type: str, params: DotMap) -> bool:
    """
    :Purpose:
    Determine if sex is possible.

    :Input:
    agent_sex_type : str

    partner_sex_type : str

    :Output:
    SexPossible : bool
    """

    # dictionary defining which sex types each sex type is compatible with
    # TO_REVIEW these definitions should probably be reviewed
    st = {
        "HM": ["HF", "WSW", "MTF"],
        "MSM": ["MSM", "WSW", "HF", "MTF"],
        "WSW": ["MSM", "WSW", "HM"],
        "HF": ["HM", "MSM"],
        "MTF": ["HM", "MSM"],
    }

    # Check input
    if agent_sex_type not in params.classes.sex_types:
        raise ValueError("Invalid agent_sex_type! %s" % str(agent_sex_type))
    if partner_sex_type not in params.classes.sex_types:
        raise ValueError("Invalid partner_sex_type! %s" % str(partner_sex_type))

    return (agent_sex_type in st[partner_sex_type]) and (
        partner_sex_type in st[agent_sex_type]
    )


def get_partnership_duration(agent: Agent, params: DotMap) -> int:
    """
    :Purpose:
        Get duration of a relationship
        Drawn from Poisson distribution.

    :Input:
        agent : Agent

    :Output:
        NumPartners : int
        Zero partners possible.
    """
    # Check input
    agent_drug_type = agent._DU
    agent_sex_type = agent._SO
    agent_race_type = agent._race

    # Drug type
    if agent_drug_type not in ["IDU", "NIDU", "NDU"]:
        raise ValueError("Invalid drug type! %s" % str(agent_drug_type))
    # Sex type
    if agent_sex_type not in params.classes.sex_types:
        raise ValueError("Invalid sex type! %s" % str(agent_sex_type))

    diceroll = random.random()

    # Length of relationship (months)a
    # <1 1,679 32.3% 566 17.7 1,113 55.8
    # 1–6 1,359 26.2% 929 29.0 430 21.6
    # 7–12 604 11.6% 459 14.4 145 7.3
    # 13–24 628 12.1% 480 15.0 148 7.4
    # 25–36 309 6.0% 264 8.3 45 2.3
    # >37 614 11.8% 501 15.7 113 5.7
    if agent_race_type == "BLACK" and params.model == "MSW":
        dur_bin = 5
        for i in range(1, 5):
            if diceroll < prob.MSWsexualDurations[i]["p_value"]:
                dur_bin = i
                break

        duration = random.randrange(
            prob.MSWsexualDurations[dur_bin]["min"],
            prob.MSWsexualDurations[dur_bin]["max"],
            1,
        )

    else:
        dur_bin = 5
        for i in range(1, 5):
            if diceroll < params.partnership.sex.duration[i].prob:
                dur_bin = i
                break

        duration = random.randrange(
            params.partnership.sex.duration[dur_bin].min,
            params.partnership.sex.duration[dur_bin].max,
            1,
        )

    return duration


T = TypeVar("T")


def safe_random_choice(seq: Sequence[T]) -> Optional[T]:
    """
    Return None or a random choice
    """
    if seq:
        return random.choice(seq)
    else:
        return None
