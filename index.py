import csv

from PlanNode import PlanNode
from ZipNode import ZipNode


def find_matching_rate_area(state_plan_arr, rate_area):
    # returns a list of results
    # where rate_area matches items in arr
    results = []
    for item in state_plan_arr:
        if item.rate_area == rate_area:
            results.append(item)

    results.sort(key=lambda x: x.rate, reverse=False)

    lowest = results[0].rate
    for r in results:
        if r.rate > lowest:
            return r

    return None


plans = {}
plansHeader = None
with open("./data/plans.csv") as csvPlans:
    readCSVplans = csv.reader(csvPlans, delimiter=",")
    plansHeader = next(readCSVplans)

    for row in readCSVplans:
        if row[2].lower() == "silver":
            newPlanNode = PlanNode(row[0], row[1], row[2], row[3], row[4])

            # store by state
            if row[1] not in plans.keys():
                plans[row[1]] = newPlanNode
            else:
                if isinstance(plans[row[1]], PlanNode):
                    temp = plans[row[1]]
                    plans[row[1]] = []
                    plans[row[1]].append(temp)
                plans[row[1]].append(newPlanNode)
            # plans.append({
            #     plansHeader[0]: row[0],
            #     plansHeader[1]: row[1],
            #     plansHeader[2]: row[2],
            #     plansHeader[3]: row[3],
            #     plansHeader[4]: row[4]
            # })

zips = {}
zipsHeader = None
with open("./data/zips.csv") as csvZips:
    readCSVzips = csv.reader(csvZips, delimiter=",")
    zipsHeader = next(readCSVzips)

    for row in readCSVzips:
        newZipNode = ZipNode(row[0], row[1], row[2], row[3], row[4])

        # store by zipcode
        if row[0] not in zips.keys():
            zips[row[0]] = newZipNode
        else:
            if isinstance(zips[row[0]], ZipNode):
                temp = zips[row[0]]
                zips[row[0]] = []
                zips[row[0]].append(temp)
            zips[row[0]].append(newZipNode)
        # print(zips[row[0]])

slcsp = []
slcspHeader = None

with open("./data/slcsp.csv") as csvslcsp:
    readCSVslcsp = csv.reader(csvslcsp, delimiter=",")
    slcspHeader = next(readCSVslcsp)
    slcsp.append(f"{slcspHeader[0]},{slcspHeader[1]}")
    for row in readCSVslcsp:

        if row[0] in zips.keys():
            if isinstance(zips[row[0]], ZipNode):
                if zips[row[0]].state not in plans.keys():
                    # no plans in matching state - entries will be left blank
                    slcsp.append(f"{row[0]},")
                else:
                    if isinstance(plans[zips[row[0]].state], PlanNode):
                        # if only one plan is available, there is no 2nd cheapest & should be left blank
                        slcsp.append(f"{row[0]},")
                    else:
                        matchList = find_matching_rate_area(plans[zips[row[0]].state], zips[row[0]].rate_area)
                        if matchList is not None:
                            slcsp.append(f"{row[0]},{matchList.rate}")
                        else:
                            # blank if match is None due to all being the same rate
                            slcsp.append(f"{row[0]},")

            else:
                # check if zips in the list are able to be determined
                isSame = True
                state = zips[row[0]][0].state
                rate_area = zips[row[0]][0].rate_area

                for z in zips[row[0]]:
                    if z.state != state or z.rate_area != rate_area:
                        isSame = False

                if (isSame):
                    matchList = find_matching_rate_area(plans[state], rate_area)
                    if matchList is not None:
                        slcsp.append(f"{row[0]},{matchList.rate}")
                    else:
                        # blank if match is None due to all being the same rate
                        slcsp.append(f"{row[0]},")
                else:
                    # if the answer is ambiguous it should be left blank.
                    slcsp.append(f"{row[0]},")
        else:
            slcsp.append(f"{row[0]},")

with open("output.csv", 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_NONE, delimiter='\n')
    wr.writerow(slcsp)
