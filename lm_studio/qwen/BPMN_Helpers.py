#
# BPMN_Helpers.py
#
# Modelio BPMN Helper Library
# Place this file in your Modelio macros folder
#
# Usage in scripts:
#   execfile("/path/to/BPMN_Helpers.py")
#

from org.modelio.metamodel.bpmn.processCollaboration import BpmnProcess
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLane
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLaneSet
from org.modelio.metamodel.bpmn.activities import BpmnUserTask
from org.modelio.metamodel.bpmn.activities import BpmnServiceTask
from org.modelio.metamodel.bpmn.activities import BpmnManualTask
from org.modelio.metamodel.bpmn.events import BpmnStartEvent
from org.modelio.metamodel.bpmn.events import BpmnEndEvent
from org.modelio.metamodel.bpmn.gateways import BpmnExclusiveGateway
from org.modelio.metamodel.bpmn.gateways import BpmnParallelGateway
from org.modelio.metamodel.bpmn.flows import BpmnSequenceFlow
from org.modelio.metamodel.uml.statik import Package
from org.eclipse.draw2d.geometry import Rectangle as Draw2DRectangle
import time

# ============================================================================
# GET MODELIO GLOBALS
# ============================================================================
# These are normally available as globals in Modelio scripts
# We get them explicitly so the library works when loaded via execfile()
modelingSession = Modelio.getInstance().getModelingSession()
diagramService = Modelio.getInstance().getDiagramService()

# ============================================================================
# CONFIGURATION
# ============================================================================
WAIT_TIME_MS = 50
MAX_ATTEMPTS = 3
SPACING = 120
START_X = 80

# ============================================================================
# ELEMENT CREATION
# ============================================================================

def createLane(laneSet, name):
    lane = modelingSession.getModel().createBpmnLane()
    lane.setName(name)
    lane.setLaneSet(laneSet)
    return lane

def addToLane(element, lane):
    try:
        lane.getFlowElementRef().add(element)
    except:
        pass

def createStartEvent(process, name):
    event = modelingSession.getModel().createBpmnStartEvent()
    event.setName(name)
    event.setContainer(process)
    return event

def createEndEvent(process, name):
    event = modelingSession.getModel().createBpmnEndEvent()
    event.setName(name)
    event.setContainer(process)
    return event

def createUserTask(process, name):
    task = modelingSession.getModel().createBpmnUserTask()
    task.setName(name)
    task.setContainer(process)
    return task

def createServiceTask(process, name):
    task = modelingSession.getModel().createBpmnServiceTask()
    task.setName(name)
    task.setContainer(process)
    return task

def createManualTask(process, name):
    task = modelingSession.getModel().createBpmnManualTask()
    task.setName(name)
    task.setContainer(process)
    return task

def createExclusiveGateway(process, name):
    gateway = modelingSession.getModel().createBpmnExclusiveGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway

def createParallelGateway(process, name):
    gateway = modelingSession.getModel().createBpmnParallelGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway

def createSequenceFlow(process, source, target, label=""):
    flow = modelingSession.getModel().createBpmnSequenceFlow()
    flow.setName(label)
    flow.setSourceRef(source)
    flow.setTargetRef(target)
    flow.setContainer(process)
    if label:
        try:
            flow.setConditionExpression(label)
        except:
            pass
    return flow

# ============================================================================
# DIAGRAM UTILITIES
# ============================================================================

def parseBounds(boundsStr):
    try:
        startIdx = boundsStr.find("(")
        endIdx = boundsStr.rfind(")")
        if startIdx == -1 or endIdx == -1:
            return None
        inner = boundsStr[startIdx + 1:endIdx]
        parts = inner.split(",")
        if len(parts) == 4:
            return {
                "x": float(parts[0].strip()),
                "y": float(parts[1].strip()),
                "w": float(parts[2].strip()),
                "h": float(parts[3].strip())
            }
    except:
        pass
    return None

def getGraphics(diagramHandle, element):
    try:
        graphics = diagramHandle.getDiagramGraphics(element)
        if graphics is not None and graphics.size() > 0:
            return graphics.get(0)
    except:
        pass
    return None

def getBounds(diagramHandle, element):
    dg = getGraphics(diagramHandle, element)
    if dg:
        return parseBounds(str(dg.getBounds()))
    return None

def getLaneCenterY(diagramHandle, lane):
    bounds = getBounds(diagramHandle, lane)
    if bounds:
        return bounds["y"] + bounds["h"] / 2 - 23
    return None

def waitForElements(diagramHandle, elements):
    elementGraphics = {}
    attempt = 0
    while attempt < MAX_ATTEMPTS:
        attempt += 1
        for elem in elements:
            name = elem.getName()
            if name not in elementGraphics:
                dg = getGraphics(diagramHandle, elem)
                if dg:
                    elementGraphics[name] = dg
        if len(elementGraphics) == len(elements):
            return elementGraphics, attempt
        time.sleep(WAIT_TIME_MS / 1000.0)
    return elementGraphics, attempt

def unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout):
    unmaskedCount = 0
    laneY = {}
    for laneName, lane in lanes.items():
        bounds = getBounds(diagramHandle, lane)
        if bounds:
            laneY[laneName] = int(bounds["y"] + bounds["h"] / 2)
    for elem in elements:
        name = elem.getName()
        if name not in elementGraphics:
            laneName = elementLayout.get(name, (0, ""))[1]
            targetY = laneY.get(laneName, 100)
            try:
                result = diagramHandle.unmask(elem, 100, targetY)
                if result and result.size() > 0:
                    elementGraphics[name] = result.get(0)
                    unmaskedCount += 1
            except:
                pass
    return unmaskedCount

# ============================================================================
# HIGH-LEVEL DIAGRAM BUILDER
# ============================================================================

def buildDiagram(process, elements, elementRefs, lanes, elementLayout, flowDefs, diagramName):
    """
    Build complete BPMN diagram with positioning and flows.
    
    Args:
        process: BpmnProcess object
        elements: List of all BPMN elements
        elementRefs: Dict {name: element}
        lanes: Dict {laneName: lane}
        elementLayout: Dict {elementName: (column, laneName)}
        flowDefs: List of (source, target, label) tuples
        diagramName: Name for the diagram
    """
    # Create diagram
    diagram = modelingSession.getModel().createBpmnProcessDesignDiagram()
    diagram.setName(diagramName)
    diagram.setOrigin(process)
    
    diagramService = Modelio.getInstance().getDiagramService()
    diagramHandle = diagramService.getDiagramHandle(diagram)
    diagramHandle.save()
    
    # Wait for elements
    elementGraphics, attempts = waitForElements(diagramHandle, elements)
    
    if len(elementGraphics) < len(elements):
        unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout)
        diagramHandle.save()
    
    # Get lane Y positions
    laneY = {}
    for laneName, lane in lanes.items():
        y = getLaneCenterY(diagramHandle, lane)
        if y:
            laneY[laneName] = y
    
    # Reposition elements
    for elem in elements:
        name = elem.getName()
        if name in elementLayout and name in elementGraphics:
            col, laneName = elementLayout[name]
            dg = elementGraphics[name]
            bounds = getBounds(diagramHandle, elem)
            if bounds:
                targetX = START_X + SPACING * col
                targetY = laneY.get(laneName, 100)
                newBounds = Draw2DRectangle(int(targetX), int(targetY), int(bounds["w"]), int(bounds["h"]))
                dg.setBounds(newBounds)
                diagramHandle.save()
    
    # Create flows
    for srcName, tgtName, label in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            createSequenceFlow(process, src, tgt, label)
    
    diagramHandle.save()
    diagramHandle.close()
    
    return diagram
