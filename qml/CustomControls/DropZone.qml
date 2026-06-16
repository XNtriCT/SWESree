import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

Item {
    id: root
    implicitWidth: 500
    implicitHeight: 150
    
    signal pathsDropped(var paths)
    signal pathsSelected(var paths)
    
    property bool dragActive: false
    property var supported_extensions: []
    
    // Spring physics scale transition on drag hover
    scale: dragActive ? 0.97 : 1.0
    Behavior on scale {
        SpringAnimation { spring: 3.5; damping: 0.22; epsilon: 0.005 }
    }
    
    Rectangle {
        anchors.fill: parent
        color: dragActive ? "#08FF4F00" : "#161616"
        radius: 6
        border.color: dragActive ? "#FF4F00" : "#2E2E2E"
        border.width: dragActive ? 1.5 : 1
        
        // Dashed lines simulated by canvas or nice opacity border
        opacity: dragActive ? 1.0 : 0.85
        
        ColumnLayout {
            anchors.centerIn: parent
            spacing: 12
            
            Text {
                text: "📥"
                font.pixelSize: 26
                Layout.alignment: Qt.AlignHCenter
                color: "#FF4F00"
            }
            
            Text {
                text: "DROP PRODUCTION ASSETS OR DIRECTORIES"
                font.family: "Consolas"
                font.bold: true
                font.pixelSize: 11
                color: "#FFFFFF"
                Layout.alignment: Qt.AlignHCenter
                font.letterSpacing: 1.0
            }
            
            RowLayout {
                spacing: 12
                Layout.alignment: Qt.AlignHCenter
                
                Button {
                    text: "SELECT FILES"
                    font.family: "Consolas"
                    font.pixelSize: 10
                    font.bold: true
                    
                    background: Rectangle {
                        implicitWidth: 100
                        implicitHeight: 28
                        color: parent.down ? "#1F1F24" : (parent.hovered ? "#2C2C2E" : "#1C1C1E")
                        border.color: "#3A3A3C"
                        border.width: 1
                        radius: 3
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        font: parent.font
                        color: parent.hovered ? "#FF4F00" : "#8E8E93"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: fileDialog.open()
                }
                
                Button {
                    text: "SELECT FOLDER"
                    font.family: "Consolas"
                    font.pixelSize: 10
                    font.bold: true
                    
                    background: Rectangle {
                        implicitWidth: 100
                        implicitHeight: 28
                        color: parent.down ? "#1F1F24" : (parent.hovered ? "#2C2C2E" : "#1C1C1E")
                        border.color: "#3A3A3C"
                        border.width: 1
                        radius: 3
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        font: parent.font
                        color: parent.hovered ? "#FF4F00" : "#8E8E93"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: folderDialog.open()
                }
            }
        }
        
        DropArea {
            id: dropArea
            anchors.fill: parent
            onEntered: (drag) => {
                root.dragActive = true
                drag.acceptProposedAction()
            }
            onPositionChanged: (drag) => {
                drag.acceptProposedAction()
            }
            onExited: root.dragActive = false
            onDropped: (drag) => {
                root.dragActive = false
                if (drag.hasUrls) {
                    var pathsList = []
                    for (var i = 0; i < drag.urls.length; i++) {
                        pathsList.push(drag.urls[i].toString())
                    }
                    root.pathsDropped(pathsList)
                    drag.acceptProposedAction()
                }
            }
        }
    }
    
    // Qt 6 standard file dialogs using backend.documentsFolder
    FileDialog {
        id: fileDialog
        title: "Select Assets"
        currentFolder: backend.documentsFolder
        fileMode: FileDialog.OpenFiles
        onAccepted: {
            var selected = []
            for (var i = 0; i < selectedFiles.length; i++) {
                selected.push(selectedFiles[i].toString())
            }
            root.pathsSelected(selected)
        }
    }
    
    FolderDialog {
        id: folderDialog
        title: "Select Folder"
        currentFolder: backend.documentsFolder
        onAccepted: {
            root.pathsSelected([selectedFolder.toString()])
        }
    }
}