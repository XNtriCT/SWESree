import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: root
    implicitWidth: 400
    implicitHeight: 180
    
    property alias model: listView.model
    signal itemRemoved(string path)
    
    ColumnLayout {
        anchors.fill: parent
        spacing: 8
        
        Text {
            text: "QUEUED ASSETS (" + listView.count + ")"
            font.family: "Consolas"
            font.bold: true
            font.pixelSize: 11
            color: "#8E8E93"
            font.letterSpacing: 0.5
        }
        
        ListView {
            id: listView
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            spacing: 4
            
            ScrollBar.vertical: ScrollBar {
                policy: ScrollBar.AsNeeded
            }
            
            // 120fps fluid adding and removing transition curves
            add: Transition {
                NumberAnimation { properties: "x"; from: -30; duration: 250; easing.type: Easing.OutQuint }
                NumberAnimation { properties: "opacity"; from: 0.0; duration: 250; easing.type: Easing.OutQuint }
            }
            
            remove: Transition {
                NumberAnimation { properties: "x"; to: 30; duration: 200; easing.type: Easing.OutQuint }
                NumberAnimation { properties: "opacity"; to: 0.0; duration: 200; easing.type: Easing.OutQuint }
            }
            
            displaced: Transition {
                NumberAnimation { properties: "y"; duration: 200; easing.type: Easing.OutQuint }
            }
            
            delegate: Rectangle {
                width: listView.width
                height: 36
                color: "#1C1C1E"
                radius: 3
                border.color: hoverArea.containsMouse ? "#FF4F00" : "#2C2C2E"
                border.width: 1
                
                MouseArea {
                    id: hoverArea
                    anchors.fill: parent
                    hoverEnabled: true
                }
                
                Behavior on border.color {
                    ColorAnimation { duration: 120 }
                }
                
                RowLayout {
                    anchors.fill: parent
                    anchors.leftMargin: 12
                    anchors.rightMargin: 12
                    spacing: 12
                    
                    Text {
                        text: (modelData && modelData.indexOf(".") !== -1) ? "📄" : "📁"
                        font.pixelSize: 14
                        color: "#FF4F00"
                    }
                    
                    Text {
                        text: {
                            if (!modelData) return ""
                            var parts = modelData.split(/[/\\]/)
                            return parts[parts.length - 1]
                        }
                        font.family: "Consolas"
                        font.bold: true
                        font.pixelSize: 12
                        color: "#FFFFFF"
                    }
                    
                    Text {
                        text: {
                            if (!modelData) return ""
                            var parts = modelData.split(/[/\\]/)
                            parts.pop()
                            return parts.join("/")
                        }
                        font.family: "Consolas"
                        font.pixelSize: 10
                        color: "#636366"
                        Layout.fillWidth: true
                        elide: Text.ElideLeft
                    }
                    
                    Button {
                        text: "×"
                        font.bold: true
                        font.pixelSize: 18
                        Layout.preferredWidth: 20
                        Layout.preferredHeight: 20
                        
                        background: Rectangle {
                            color: parent.hovered ? "#26FF453A" : "transparent"
                            radius: 10
                        }
                        
                        contentItem: Text {
                            text: parent.text
                            font: parent.font
                            color: parent.hovered ? "#FF453A" : "#8E8E93"
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                        
                        onClicked: root.itemRemoved(modelData)
                    }
                }
            }
        }
    }
}