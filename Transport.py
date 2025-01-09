A = [60.0,70.0,20.0]
B = [40.0,30.0,30.0,50.0]

C = [
    [2,4,5,1],
    [2,3,9,4],
    [3,4,2,5]
]

C1 = [
    [2,4,5,1],
    [2,3,9,4],
    [3,4,2,5]
]

def first_plan(suppliers, consumers):
    i=0
    j=0
    #
    plan = []
    for k in range(len(suppliers)):
        plan.append([])
    while i<len(suppliers) and j<len(consumers):
        #
        plan[i].append(min(suppliers[i], consumers[j]))
        difference = max(suppliers[i], consumers[j]) - min(suppliers[i], consumers[j])
        #
        if suppliers[i] > consumers[j]:
            for line in range(i+1,len(plan)):
                plan[line].append(0)
            j+=1
            suppliers[i] = difference
        else:
            for element in range(j+1,len(consumers)):
                plan[i].append(0)
            i+=1
            consumers[j] = difference
    return plan

def first_costs(costs,plan):
    u = [0]; v = []
    i=0; j=0
    while i<len(costs):
        # print(f"i={i} j={j}")
        if plan[i][j] != 0:
            if j >= len(v):
                v.append(costs[i][j] + u[i])
            if i>= len(u):
                u.append(v[j] - costs[i][j])
            if j<len(plan[i])-1:
                # print('branch 1')
                j+=1
            else:
                j=0
                i+=1
        else:
            if j<len(plan[i])-1:
                # print('branch 2')
                j+=1
            else:
                j=0
                i+=1
    c = costs.copy()
    for i in range(len(c)):
        for j in range(len(c[i])):
            c[i][j] = costs[i][j] - (v[j] - u[i])
    return c

def min_cost(costs):
    mins = []
    for line in costs:
        mins.append(min(line))
    min_val = min(mins)
    for i in range(len(costs)):
        for j in range(len(costs[i])):
            if costs[i][j] == min_val:
                return i,j

def new_plan(plan,index):
    i_lead = index[0]; j_lead = index[1]
    elems = [plan[i_lead][j_lead]]
    indexex = [index]
    for i in range(len(plan)):
        for j in range(len(plan[i])):
            if j == j_lead or i == i_lead:
                continue
            if plan[i][j] != 0 and plan[i_lead][j] != 0 and plan[i][j_lead] != 0:
                elems.append(plan[i][j])
                elems.append(plan[i_lead][j])
                elems.append(plan[i][j_lead])
                indexex.append((i,j))
                indexex.append((i_lead,j))
                indexex.append((i,j_lead))
                # elems.sort()
                break
    elems.pop(0)
    elems.pop(0)
    # print("elems=",elems)
    min_plan_val = min(elems)
    # print("indexex=",indexex)
    for temp_index in indexex:
        # print(indexex.index(temp_index))
        i = temp_index[0]
        j = temp_index[1]
        if indexex.index(temp_index) < 2:
            plan[i][j] += min_plan_val
        else:
            plan[i][j] -= min_plan_val
        """
        if (index[0]+index[1])%2==0:
            i = indexex[temp_index][0]
            j = indexex[temp_index][1]
            if (i+j) % 2 == 0:
                plan[i][j] += min_plan_val
            else:
                plan[i][j] -= min_plan_val
        else:
            i = indexex[temp_index][0]
            j = indexex[temp_index][1]
            if (i+j) % 2 == 0:
                plan[i][j] -= min_plan_val
            else:
                plan[i][j] += min_plan_val"""
    return plan

def new_costs(plan,costs,index):
    i = index[0]; j = index[1]
    rows = [i]; ex_rows =[]
    columns = []; ex_columns = [j]
    here_i_am = abs(costs[index[0]][index[1]])
    while len(rows)>0 or len(columns)>0:
        for i in rows:
            for j in range(len(plan[i])):
                if plan[i][j] != 0 and not(j in ex_columns):
                    columns.append(j)
                costs[i][j] += here_i_am
            ex_rows.append(i)
        rows.clear()
        for j in columns:
            for i in range(len(plan)):
                if plan[i][j] != 0 and not(i in ex_rows):
                    rows.append(i)
                costs[i][j] -= here_i_am
            ex_columns.append(j)
        columns.clear()
    # napishi tozhe samoe dlya strok
    return costs

def costs_zreomore(costs):
    for line in costs:
        for element in line:
            if element < 0:
                return False
    return True

def get_values(costs,plan):
    kaioken = 0
    for i in range(len(plan)):
        for j in range(len(plan[i])):
            kaioken += (costs[i][j] * plan[i][j])
    return kaioken

PN = first_plan(A,B)
print(PN)
CN = first_costs(C,PN)
print(CN)

while not costs_zreomore(CN):
    m = min_cost(CN)
    PN = new_plan(PN, m)
    print(PN)
    CN = new_costs(PN, CN, m)
    print()
    print(CN)

print("\nОптимальный план")
for i in range(len(PN)):
    print(PN[i])
print(f"затраты составляют {get_values(C1,PN)}")