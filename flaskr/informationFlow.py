from enum import Enum

class Confidentiality(Enum):
    LOW = 1
    HIGH = 2

class Role(Enum):
    UNREGISTERED = 1  
    BUYER = 2  
    SELLER = 3 


def can_flow(src_conf:Confidentiality, src_role:Role, dst_conf:Confidentiality, dst_role:Role) -> bool:
    # Confidentiality check
    if src_conf == Confidentiality.HIGH and dst_conf == Confidentiality.LOW:
        return False  
    # Role hierarchy: Unregistered ≤ Buyer, Unregistered ≤ Seller, Buyer ≰ Seller
    if src_role == dst_role:
        return True  
    if src_role == Role.UNREGISTERED:
        return True  
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
        #trying to go from unregistered to buyer or seller
        if owner_role == Role.UNREGISTERED and new_state_role == (Role.SELLER or Role.BUYER):
            return False
        # declassify to unregistered
        if new_state_role == Role.UNREGISTERED:
            return True
        
        # trying to go from seller to buyer or the other way
        return False

    return False
