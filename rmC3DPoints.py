# Harald Penasso Aug. 7, 2024
# Functions and Cleaned by Chat GPT-4o

from ezc3d import c3d
import numpy as np
import sys

def find_indices(lst, markers):
    """
    Find indices in a list where elements either start with '*' or match specified markers.
    
    Parameters:
    lst (list of str): List of labels to search through.
    markers (list of str): List of marker names to match.
    
    Returns:
    tuple: Two lists containing indices where elements start with '*' and match the markers, respectively.
    """
    indices_star = [i for i, s in enumerate(lst) if s.startswith('*')]
    indices_marker = [i for i, s in enumerate(lst) if s in markers]
    return indices_star, indices_marker

def remove_indices(lst, indices):
    """
    Remove elements from a list at specified indices.
    
    Parameters:
    lst (list): Original list.
    indices (list of int): Indices of elements to remove.
    
    Returns:
    list: Updated list with specified elements removed.
    """
    return [i for j, i in enumerate(lst) if j not in indices]

# Path to the C3D file passed as a command-line argument
path = sys.argv[1]

# Direct path for testing 
# path = "path\\to\\your\\file.c3d"

# Print the filename being processed
print("Processing: " + path)

# Load the C3D file
c3d_file = c3d(path)

# Extract existing labels from the C3D file
label_list = c3d_file['parameters']['POINT']['LABELS']['value']
label_list2 = c3d_file['parameters']['POINT']['LABELS2']['value']

# Define lists of virtual markers and other labels to remove
virtual_markers = ["PELO","PELA","PELL","PELP","SACO","SACA","SACL","SACP",
                   "LFEO","LFEA","LFEL","LFEP","RFEO","RFEA","RFEL","RFEP",
                   "LTIO","LTIA","LTIL","LTIP","RTIO","RTIA","RTIL","RTIP",
                   "LFOO","LFOA","LFOL","LFOP","RFOO","RFOA","RFOL","RFOP",
                   "LTOO","LTOA","LTOL","LTOP","RTOO","RTOA","RTOL","RTOP",
                   "HEDO","HEDA","HEDL","HEDP","LCLO","LCLA","LCLL","LCLP",
                   "RCLO","RCLA","RCLL","RCLP","TRXO","TRXA","TRXL","TRXP",
                   "LHUO","LHUA","LHUL","LHUP","LRAO","LRAA","LRAL","LRAP",
                   "LHNO","LHNA","LHNL","LHNP","RHUO","RHUA","RHUL","RHUP",
                   "RRAO","RRAA","RRAL","RRAP","RHNO","RHNA","RHNL","RHNP",
                   "CentreOfMass","CentreOfMassFloor"]

remove_also = ["LPelvisAngles","RPelvisAngles","LFootProgressAngles","RFootProgressAngles",
               "LHipAngles","RHipAngles","LKneeAngles","RKneeAngles","LAnkleAngles","RAnkleAngles",
               "LFFootAngles","RFFootAngles","RShankAngles","LShankAngles","RThighAngles","LThighAngles",
               "LAbsAnkleAngle","RAbsAnkleAngle","RNeckAngles","LNeckAngles","RSpineAngles","LSpineAngles",
               "LShoulderAngles","LElbowAngles","LWristAngles","RShoulderAngles","RElbowAngles","RWristAngles",
               "RThoraxAngles","LThoraxAngles","RHeadAngles","LHeadAngles","RSpineModel_L3T12","RSpineModel_SACR",
               "RSpineModel_L3","RSpineModel_T12","RSpineModel_T8","RSpineModel_T4","LSpineModel_SACR","LSpineModel_L3",
               "LSpineModel_T12","LSpineModel_T8","LSpineModel_T4","LSpineModel_L3T12","LAnklePower","RAnklePower",
               "LKneePower","RKneePower","LHipPower","RHipPower","LWaistPower","RWaistPower","LNeckPower","RNeckPower",
               "LShoulderPower","RShoulderPower","LElbowPower","RElbowPower","LWristPower","RWristPower","F_ForcePlate1",
               "F_ForcePlate2","F_ForcePlate3","F_ForcePlate4","F_ForcePlate5","F_ForcePlate6","F_ForcePlate7",
               "F_ForcePlate8","F_ForcePlate9","LKneeForce","RKneeForce","LAnkleForce","RAnkleForce","LNormalisedGRF",
               "RNormalisedGRF","LGroundReactionForce","RGroundReactionForce","LGRF","RGRF","LHipForce","RHipForce",
               "LWaistForce","RWaistForce","LNeckForce","RNeckForce","LShoulderForce","RShoulderForce","LElbowForce",
               "RElbowForce","LWristForce","RWristForce","LKneeMoment","RKneeMoment","LAnkleMoment",
               "RAnkleMoment","LHipMoment","RHipMoment","LGroundReactionMoment","RGroundReactionMoment","LWaistMoment",
               "RWaistMoment","LNeckMoment","RNeckMoment","LShoulderMoment","RShoulderMoment","LElbowMoment","RElbowMoment",
               "LWristMoment","RWristMoment","LGroundReactionMoment","RGroundReactionMoment",
               "LWaistMoment","RWaistMoment","LNeckMoment","RNeckMoment","LShoulderMoment","RShoulderMoment","LElbowMoment",
               "RElbowMoment","LWristMoment","RWristMoment"]

# Find indices of labels to remove in label_list and label_list2
# (remove all labels in the lists virtual_markers and remove_also but also all labels starting with a star '*')
indices_star1, indices_marker1 = find_indices(label_list, virtual_markers + remove_also)
indices_labels = indices_star1 + indices_marker1
label_list_upd = remove_indices(label_list, indices_labels)

indices_star2, indices_marker2 = find_indices(label_list2, virtual_markers + remove_also)
indices_labels2 = indices_star2 + indices_marker2
label_list2_upd = remove_indices(label_list2, indices_labels2)

# Remove data points corresponding to the labels to remove
remove_data_indices = indices_labels + [int(i) + 255 for i in indices_labels2]
data = c3d_file['data']['points'][:, :, :]
data_upd = np.delete(data, remove_data_indices, axis=1)

# Delete 'meta_points' from C3D file to let ezc3d recreate it
del c3d_file['data']['meta_points']

# Update the labels in the C3D file
c3d_file['parameters']['POINT']['LABELS']['value'] = label_list_upd
c3d_file['parameters']['POINT']['LABELS2']['value'] = label_list2_upd

# Update the data in the C3D file
c3d_file['data']['points'] = data_upd

# Save the patched C3D file with a new name
c3d_file.write(path[0:-4] + '_patched.c3d')

# Final message
print("    ... File patched (*_patched.c3d)")
