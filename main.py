from pulp import LpProblem, lpSum, LpMaximize, LpVariable, LpInteger, LpStatus, value


def main(graph, source, destination,  printResult=True):

    prob = LpProblem("Maximum Flow", LpMaximize)

    edgeVarsStartIn = {}
    edgeVarsEndIn = {}
    allVars = []
    for edge in graph:
        edgeVariable = LpVariable(
            "edge_"+str(edge[0])+"_"+str(edge[1]), 0, edge[2], LpInteger)

        if edge[0] not in edgeVarsStartIn.keys():
            edgeVarsStartIn[edge[0]] = [edgeVariable]
        else:
            edgeVarsStartIn[edge[0]].append(edgeVariable)

        if edge[1] not in edgeVarsEndIn.keys():
            edgeVarsEndIn[edge[1]] = [edgeVariable]
        else:
            edgeVarsEndIn[edge[1]].append(edgeVariable)

        allVars.append(edgeVariable)

    prob += sum(edgeVarsEndIn[destination])

    for i in edgeVarsEndIn:
        if i != destination:
            print(i)
            prob += sum(edgeVarsEndIn[i]) == sum(edgeVarsStartIn[i])

    prob.solve()

    if printResult:
        print("Status:", LpStatus[prob.status])

        if LpStatus[prob.status] == "Optimal":
            for v in prob.variables():
                print(v.name, "=", v.varValue)
            print("OBJECTIVE = ", value(prob.objective))


if __name__ == "__main__":
    graph = [[0, 1, 16], [0, 2, 13], [1, 2, 10], [2, 1, 4], [1, 3, 12], [
        3, 2, 9], [2, 4, 14], [4, 3, 7], [3, 5, 20], [4, 5, 4]]

    main(graph, source=0, destination=5)
