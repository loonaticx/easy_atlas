import maya.cmds as cmds
import subprocess, os
import socket
import threading
from .EAGlobals import ResamplingModeValues

# This is the JS script that will be sent to Photoshop to be executed.
with open('%s/ps_scripts/PalettizeImages.js' % os.path.dirname(__file__), 'r') as file:
    PSScript = file.read()


def getFreeSocket():
    """Get a free socket."""
    TCP_IP = '127.0.0.1'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, 0))
    TCP_PORT = s.getsockname()[1]
    s.listen(1)
    return s, TCP_PORT


def waitForPSConfirmation(s, TCP_PORT):
    """
    Method that will be added to a thread that waits for Photoshop connection.

    :param s: socket
    """
    BUFFER_SIZE = 1024

    conn, addr = s.accept()
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            break
        if data == str(TCP_PORT):
            refreshTextures = """string $fileNodes[]  = `ls -type file`;for($f in $fileNodes) {string $attrName = $f 
            + ".fileTextureName";string $fileName = `getAttr $attrName`;setAttr -type "string" $attrName $fileName;}"""
            cmds.evalDeferred('import maya.mel as mel;mel.eval(\'%s\')' % refreshTextures)

        # conn.send(data)
    conn.close()


def createAtlas(aItems, txtFinalFilename, sizeX, sizeY, photoshopPath, resamplingMode):
    """Send information to Photoshop to create texture atlas."""

    if not os.path.exists(photoshopPath):
        cmds.confirmDialog(message = "Photoshop path does not exist.", button = ["ok"])
        return

    if not resamplingMode:
        resamplingMode = 'automatic'
    resampleMode = ResamplingModeValues.index(resamplingMode) + 1

    commandList = [txtFinalFilename, sizeX, sizeY, resampleMode]

    for k in aItems:
        kPosX = int(sizeX * k.posX)
        kPosY = int(sizeY * k.posY)
        kSizeX = int(sizeX * k.sizeX)
        kSizeY = int(sizeY * k.sizeY)

        commandList.extend([k.file, kPosX, kPosY, kSizeX, kSizeY])

    # Setup thread to wait for Photoshop response - STEP 1
    s, TCP_PORT = getFreeSocket()
    commandList.insert(0, TCP_PORT)

    t = threading.Thread(target = waitForPSConfirmation, args = (s, TCP_PORT))
    threads = []
    threads.append(t)
    t.start()

    # Send job to Photoshop
    commandString = (','.join(map(str, commandList))).replace("\\", "/")
    PSscriptOutput = PSScript.replace("ITEMLIST", commandString)

    scriptFile = (os.path.dirname(__file__) + "/EAscript.jsx").replace("/", "\\")
    with open(scriptFile, "w") as script:
        script.write("/* GENERATED JAVASCRIPT FILE. DO NOT EDIT. */")
        script.write(PSscriptOutput)

    subprocess.Popen((photoshopPath, scriptFile))
