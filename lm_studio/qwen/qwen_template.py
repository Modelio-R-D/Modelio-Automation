# Load helper library (CHANGE PATH TO MATCH YOUR SYSTEM)
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

def createMyProcess(parentPackage):
    # 1. Process
    process = modelingSession.getModel().createBpmnProcess()
    process.setName("ProcessName")
    process.setOwner(parentPackage)
    
    # 2. Lanes
    laneSet = modelingSession.getModel().createBpmnLaneSet()
    laneSet.setProcess(process)
    
    lane1 = createLane(laneSet, "Lane1")
    lane2 = createLane(laneSet, "Lane2")
    
    lanes = {"Lane1": lane1, "Lane2": lane2}
    
    # 3. Elements
    start = createStartEvent(process, "Start")
    addToLane(start, lane1)
    
    task1 = createUserTask(process, "Task 1")
    addToLane(task1, lane1)
    
    end = createEndEvent(process, "End")
    addToLane(end, lane2)
    
    # 4. References
    elements = [start, task1, end]
    elementRefs = {"Start": start, "Task 1": task1, "End": end}
    
    # 5. Layout: (column, lane)
    elementLayout = {
        "Start": (0, "Lane1"),
        "Task 1": (1, "Lane1"),
        "End": (2, "Lane2"),
    }
    
    # 6. Flows: (source, target, guard)
    flowDefs = [
        ("Start", "Task 1", ""),
        ("Task 1", "End", ""),
    ]
    
    # 7. Build
    buildDiagram(process, elements, elementRefs, lanes, elementLayout, flowDefs, "Diagram")
    print "Done!"

if (selectedElements.size > 0):
    if (isinstance(selectedElements.get(0), Package)):
        createMyProcess(selectedElements.get(0))