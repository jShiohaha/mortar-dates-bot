import random

from ..constants.constants import MEMBERS


def groupings_to_str(groupings, excluded_member):
    response = "Mortar Dates 🤟🏼\n\n"
    for idx, group in enumerate(groupings):
        response += "{}: {} & {}\n".format((idx+1), group[0], group[1])
        if excluded_member is not None:
            response += ("\n{} was left out this week 🙁 Join another date or "
                        "wait until next week.").format(excluded_member)
    return response


def generate_excluded_member(existing_groups):
    excluded_member = None
    if len(MEMBERS) % 2 == 0:
        return excluded_member
    # get previously excluded members so that the same member is not excluded >1 time
    previously_excluded_members = {
        member for pairing in existing_groups for member in pairing['excluded'] if member is not None}
    while excluded_member is None or excluded_member in previously_excluded_members:
        excluded_member = random.choice(MEMBERS)
    return excluded_member


def generate_new_groups(graph, existing_groups, n=2):
    print("num members: {}".format(len(MEMBERS)))
    groups = []
    members = [member for member in MEMBERS]
    # if a single person will be left out, we will generate a new excluded member
    if len(members) % n == 1:
        excluded_member = generate_excluded_member(existing_groups)
        groups.append([excluded_member])
        members.remove(excluded_member)

    while len(members) > n:
        group_size = 0
        group = []
        member = None
        while group_size < n:
            if group_size == 0:
                member = random.choice(members)
            else:
                # possible partners are members that have not been chosen for another group
                # and have never been paired with the current member
                possible_partners = list(set(members) & set(graph[member]))
                print("Looking for partners for {}".format(member))
                print(possible_partners)
                print("\n")

                if possible_partners is None:
                    print("No possilbe partners for {}".format(member))
                    # could generate an infinite loop? we might need to
                    # remove this person from the list of members
                    member = random.choice(members)
                    continue
    
                partner = random.choice(possible_partners)
                # update edges in graph for both member and partner
                graph[member].remove(partner)
                graph[partner].remove(member)
                member = partner
            # member should be removed from future consideration in these groups
            members.remove(member)
            group.append(member)
            group_size += 1
        groups.append(group)
    # the number of left over members will be >1 and should be considered as their own group
    if len(members) > 0:
        groups.append(members)
    return groups, graph
