from enum import Enum
class Confidentiality(Enum):
    LOW = 1
    HIGH = 2
class Role(Enum):
    UNREGISTERED = 1  
    BUYER = 2  
    SELLER = 3 

def can_flow(from_conf:Confidentiality, from_role:Role, to_conf:Confidentiality, to_role:Role) -> bool:
    # data flow from the same role
    if from_role == to_role:
        # data flow from low to high
        if from_conf == Confidentiality.LOW and to_conf == Confidentiality.HIGH:
            return True
        # data flow from high to low
        return False  
    # if data comes from unregistered
    if from_role == Role.UNREGISTERED:
        # deny date from high to low 
        if from_conf == Confidentiality.HIGH and to_conf == Confidentiality.LOW:
            return False
        # return true otherwise 
        return True
    # base case
    return False

def declassify(owner_conf:Confidentiality, owner_role:Role, new_state_conf:Confidentiality, new_state_role:Role)-> bool:
    # no change in state
    if owner_conf == new_state_conf and owner_role == new_state_role:
        return True
    # confidentialty declassification
    if owner_conf != new_state_conf and owner_role == new_state_role:
        # trying to go from low to high
        if owner_conf == Confidentiality.LOW and new_state_conf == Confidentiality.HIGH:
            return False
        return True
    # role declassification
    if owner_role != new_state_role:
        # trying to go from unregistered to buyer or seller
        if owner_role == Role.UNREGISTERED and new_state_role == (Role.SELLER or Role.BUYER):
            return False
        # declassify to unregistered
        if new_state_role == Role.UNREGISTERED:
            return True
        # trying to go from seller to buyer or the other way
        return False
    return False