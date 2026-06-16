import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "CustomControls"

ScrollView {
    id: root
    anchors.fill: parent
    contentWidth: -1
    contentHeight: contentColumn.implicitHeight + 40
    clip: true
    
    property var selectedPaths: []
    
    ColumnLayout {
        id: contentColumn
        width: root.width - 40
        anchors.top: parent.top
        anchors.topMargin: 20
        anchors.horizontalCenter: parent.horizontalCenter
        spacing: 20
        
        // Header
        ColumnLayout {
            spacing: 4
            Text {
                text: "VIDEO → FRAMES SEQUENCE EXTRACTOR"
                font.family: "Consolas"
                font.bold: true
                font.pixelSize: 20
                color: "#FFFFFF"
                font.letterSpacing: 0.5
            }
            Text {
                text: "Extract video frames to lossless scaled PNG sequences."
                font.family: "Consolas"
                font.pixelSize: 12
                color: "#8E8E93"
            }
        }
        
        // Drag-and-drop
        DropZone {
            Layout.fillWidth: true
            supported_extensions: [".mov", ".mp4", ".mkv", ".avi", ".webm"]
            onPathsDropped: (paths) => root.addPaths(paths)
            onPathsSelected: (paths) => root.addPaths(paths)
        }
        
        // Queue List
        QueueList {
            Layout.fillWidth: true
            model: root.selectedPaths
            onItemRemoved: (path) => {
                var idx = root.selectedPaths.indexOf(path)
                if (idx !== -1) {
                    var arr = root.selectedPaths.slice()
                    arr.splice(idx, 1)
                    root.selectedPaths = arr
                }
            }
        }
        
        // Destination Card
        Rectangle {
            Layout.fillWidth: true
            height: 45
            color: "#181818"
            border.color: "#242424"
            border.width: 1
            radius: 4
            
            RowLayout {
                anchors.fill: parent
                anchors.margins: 12
                spacing: 10
                
                Text {
                    text: "OUTPUT DESTINATION:"
                    font.family: "Consolas"
                    font.bold: true
                    font.pixelSize: 11
                    color: "#8E8E93"
                    font.letterSpacing: 0.5
                }
                Text {
                    text: "Frames will be saved in folders named after each video alongside the sources."
                    font.family: "Consolas"
                    font.pixelSize: 11
                    color: "#8E8E93"
                    font.italic: true
                }
            }
        }
        
        // Collapsible Advanced Settings
        Rectangle {
            id: advSettings
            Layout.fillWidth: true
            Layout.preferredHeight: expanded ? (advLayout.implicitHeight + 24) : 42
            clip: true
            color: "#181818"
            border.color: "#242424"
            border.width: 1
            radius: 4
            
            property bool expanded: false
            
            Behavior on Layout.preferredHeight {
                NumberAnimation { duration: 250; easing.type: Easing.OutQuint }
            }
            
            ColumnLayout {
                id: advLayout
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.margins: 12
                spacing: 15
                
                RowLayout {
                    Layout.fillWidth: true
                    
                    Text {
                        text: advSettings.expanded ? "▼ ADVANCED CONFIGURATION" : "▶ ADVANCED CONFIGURATION"
                        font.family: "Consolas"
                        font.bold: true
                        font.pixelSize: 11
                        color: "#FFFFFF"
                        font.letterSpacing: 0.5
                    }
                    Item { Layout.fillWidth: true }
                    Button {
                        text: "RESET"
                        font.family: "Consolas"
                        font.pixelSize: 9
                        font.bold: true
                        background: Rectangle {
                            implicitWidth: 60
                            implicitHeight: 22
                            color: parent.hovered ? "#2C2C2E" : "#1C1C1E"
                            border.color: "#3A3A3C"
                            radius: 3
                        }
                        contentItem: Text {
                            text: parent.text
                            font: parent.font
                            color: parent.hovered ? "#FF4F00" : "#8E8E93"
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                        onClicked: root.resetDefaults()
                    }
                    MouseArea {
                        anchors.fill: parent
                        anchors.rightMargin: 70
                        cursorShape: Qt.PointingHandCursor
                        onClicked: advSettings.expanded = !advSettings.expanded
                    }
                }
                
                // Fields
                ColumnLayout {
                    Layout.fillWidth: true
                    Layout.topMargin: 10
                    spacing: 12
                    
                    RowLayout {
                        spacing: 15
                        Text { text: "TARGET HEIGHT (PX)"; font.family: "Consolas"; font.bold: true; font.pixelSize: 11; color: "#8E8E93"; Layout.preferredWidth: 140 }
                        TextField {
                            id: heightInput
                            text: "1080"
                            font.family: "Consolas"
                            font.pixelSize: 11
                            color: "#FFFFFF"
                            Layout.fillWidth: true
                            background: Rectangle { color: "#1C1C1E"; border.color: "#2C2C2E"; radius: 3 }
                        }
                    }
                    
                    CustomSlider {
                        id: pngSlider
                        label: "PNG COMPRESSION LEVEL"
                        from: 0
                        to: 9
                        value: 3
                        stepSize: 1
                        Layout.fillWidth: true
                    }
                    
                    RowLayout {
                        spacing: 15
                        Text { text: "FRAME NAMING PATTERN"; font.family: "Consolas"; font.bold: true; font.pixelSize: 11; color: "#8E8E93"; Layout.preferredWidth: 140 }
                        TextField {
                            id: namingInput
                            text: "frame_%06d.png"
                            font.family: "Consolas"
                            font.pixelSize: 11
                            color: "#FFFFFF"
                            Layout.fillWidth: true
                            background: Rectangle { color: "#1C1C1E"; border.color: "#2C2C2E"; radius: 3 }
                        }
                    }
                    
                    CheckBox {
                        id: recursiveCheck
                        text: "PROCESS DIRECTORIES RECURSIVELY"
                        font.family: "Consolas"
                        font.pixelSize: 10
                        checked: false
                    }
                }
            }
        }
        
        // Output Execution Log Panel
        Rectangle {
            Layout.fillWidth: true
            height: 250
            color: "#161616"
            border.color: "#242424"
            border.width: 1
            radius: 4
            
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 12
                spacing: 10
                
                RowLayout {
                    Layout.fillWidth: true
                    Text {
                        text: "LOG MATRIX ACTIVITY"
                        font.family: "Consolas"
                        font.bold: true
                        font.pixelSize: 11
                        color: "#8E8E93"
                        font.letterSpacing: 0.5
                    }
                    Item { Layout.fillWidth: true }
                    Text {
                        text: "STATUS: " + backend.framesStatus.toUpperCase()
                        font.family: "Consolas"
                        font.bold: true
                        font.pixelSize: 10
                        color: backend.framesStatus === "idle" ? "#8E8E93" : (backend.framesStatus === "success" ? "#30D158" : "#FF9F0A")
                    }
                }
                
                ProgressBar {
                    id: progressBar
                    Layout.fillWidth: true
                    height: 4
                    value: backend.framesProgress / 100.0
                    
                    background: Rectangle {
                        color: "#2D2D2D"
                        radius: 2
                    }
                    
                    contentItem: Item {
                        Rectangle {
                            width: progressBar.visualPosition * parent.width
                            height: parent.height
                            color: "#FF4F00"
                            radius: 2
                        }
                    }
                }
                
                ScrollView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true
                    
                    TextArea {
                        id: logArea
                        readOnly: true
                        font.family: "Consolas"
                        font.pixelSize: 11
                        color: "#D4D4D6"
                        placeholderText: "Live pipeline execution trace will stream here..."
                        placeholderTextColor: "#48484A"
                        background: Rectangle { color: "transparent" }
                    }
                }
            }
        }
        
        // Actions
        RowLayout {
            Layout.fillWidth: true
            spacing: 15
            
            Button {
                text: "CANCEL PIPELINE"
                font.family: "Consolas"
                font.pixelSize: 11
                font.bold: true
                enabled: backend.framesStatus === "running"
                
                background: Rectangle {
                    implicitWidth: 150
                    implicitHeight: 38
                    color: parent.down ? "#2C2C2E" : (parent.hovered ? "#3A3A3C" : "#1C1C1E")
                    border.color: parent.enabled ? "#FF453A" : "#242424"
                    border.width: 1
                    radius: 4
                }
                
                contentItem: Text {
                    text: parent.text
                    font: parent.font
                    color: parent.enabled ? (parent.hovered ? "#FF453A" : "#8E8E93") : "#48484A"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                
                onClicked: backend.cancelFramesWorkflow()
            }
            
            Item { Layout.fillWidth: true }
            
            GlowButton {
                text: "RUN EXTRACTION"
                enabled: root.selectedPaths.length > 0 && backend.framesStatus !== "running"
                onClicked: {
                    logArea.clear()
                    backend.startFramesWorkflow(
                        root.selectedPaths,
                        parseInt(heightInput.text),
                        pngSlider.value,
                        namingInput.text,
                        recursiveCheck.checked
                    )
                }
            }
        }
    }
    
    function addPaths(paths) {
        var cleaned = backend.validatePaths(paths, "frames")
        var temp = root.selectedPaths.slice()
        var added = false
        for (var i = 0; i < cleaned.length; i++) {
            if (temp.indexOf(cleaned[i]) === -1) {
                temp.push(cleaned[i])
                added = true
            }
        }
        if (added) {
            root.selectedPaths = temp
        }
    }
    
    function resetDefaults() {
        heightInput.text = "1080"
        pngSlider.value = 3
        namingInput.text = "frame_%06d.png"
        recursiveCheck.checked = false
        logArea.append("Configuration reset to tuned script defaults.")
    }
    
    Connections {
        target: backend
        function onLogReceived(tool, msg) {
            if (tool === "frames") {
                logArea.append(msg)
            }
        }
    }
}