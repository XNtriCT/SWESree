import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ScrollView {
    id: root
    anchors.fill: parent
    contentWidth: -1
    contentHeight: contentColumn.implicitHeight + 40
    clip: true
    
    ColumnLayout {
        id: contentColumn
        width: root.width - 40
        anchors.top: parent.top
        anchors.topMargin: 20
        anchors.horizontalCenter: parent.horizontalCenter
        spacing: 25
        
        // Title block
        ColumnLayout {
            spacing: 4
            Text {
                text: "CREATIVE PRODUCTION HUB"
                font.family: "Consolas"
                font.bold: true
                font.pixelSize: 20
                color: "#FFFFFF"
                font.letterSpacing: 0.5
            }
            Text {
                text: "Optimize, compress, and extract production-grade web assets at 120fps GPU speeds."
                font.family: "Consolas"
                font.pixelSize: 12
                color: "#8E8E93"
            }
        }
        
        // Stats Cards Row
        RowLayout {
            Layout.fillWidth: true
            spacing: 15
            
            // Image Stats
            Rectangle {
                id: statImages
                Layout.fillWidth: true
                height: 90
                color: "#181818"
                border.color: hoverImages.containsMouse ? "#FF4F00" : "#242424"
                border.width: 1
                radius: 4
                
                scale: hoverImages.containsMouse ? 1.02 : 1.0
                Behavior on scale { SpringAnimation { spring: 3.5; damping: 0.2 } }
                
                MouseArea { id: hoverImages; anchors.fill: parent; hoverEnabled: true }
                
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 15
                    spacing: 4
                    Text {
                        text: backend.statsImages
                        font.family: "Consolas"
                        font.bold: true
                        font.pixelSize: 26
                        color: "#FF4F00"
                    }
                    Text {
                        text: "IMAGES OPTIMIZED"
                        font.family: "Consolas"
                        font.pixelSize: 9
                        font.bold: true
                        color: "#8E8E93"
                        font.letterSpacing: 1.0
                    }
                }
            }
            
            // Video Stats
            Rectangle {
                id: statVideos
                Layout.fillWidth: true
                height: 90
                color: "#181818"
                border.color: hoverVideos.containsMouse ? "#FF4F00" : "#242424"
                border.width: 1
                radius: 4
                
                scale: hoverVideos.containsMouse ? 1.02 : 1.0
                Behavior on scale { SpringAnimation { spring: 3.5; damping: 0.2 } }
                
                MouseArea { id: hoverVideos; anchors.fill: parent; hoverEnabled: true }
                
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 15
                    spacing: 4
                    Text {
                        text: backend.statsVideos
                        font.family: "Consolas"
                        font.bold: true
                        font.pixelSize: 26
                        color: "#FF9F0A"
                    }
                    Text {
                        text: "VIDEOS COMPRESSED"
                        font.family: "Consolas"
                        font.pixelSize: 9
                        font.bold: true
                        color: "#8E8E93"
                        font.letterSpacing: 1.0
                    }
                }
            }
            
            // Savings Stats
            Rectangle {
                id: statSavings
                Layout.fillWidth: true
                height: 90
                color: "#181818"
                border.color: hoverSavings.containsMouse ? "#FF4F00" : "#242424"
                border.width: 1
                radius: 4
                
                scale: hoverSavings.containsMouse ? 1.02 : 1.0
                Behavior on scale { SpringAnimation { spring: 3.5; damping: 0.2 } }
                
                MouseArea { id: hoverSavings; anchors.fill: parent; hoverEnabled: true }
                
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 15
                    spacing: 4
                    Text {
                        text: backend.statsMbSaved.toFixed(1) + " MB"
                        font.family: "Consolas"
                        font.bold: true
                        font.pixelSize: 26
                        color: "#30D158"
                    }
                    Text {
                        text: "SPACE REDUCTION"
                        font.family: "Consolas"
                        font.pixelSize: 9
                        font.bold: true
                        color: "#8E8E93"
                        font.letterSpacing: 1.0
                    }
                }
            }
        }
        
        Text {
            text: "SELECT WORKFLOW CONFIGURATOR"
            font.family: "Consolas"
            font.bold: true
            font.pixelSize: 11
            color: "#636366"
            font.letterSpacing: 1.0
            Layout.topMargin: 15
        }
        
        // Tool Configurator Cards Layout
        RowLayout {
            Layout.fillWidth: true
            spacing: 15
            
            // Card 1
            Rectangle {
                id: card1
                Layout.fillWidth: true
                Layout.preferredHeight: 190
                color: "#181818"
                border.color: mouse1.containsMouse ? "#FF4F00" : "#242424"
                border.width: 1
                radius: 4
                
                scale: mouse1.containsMouse ? 1.03 : 1.0
                Behavior on scale { SpringAnimation { spring: 3.5; damping: 0.2 } }
                
                MouseArea {
                    id: mouse1
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        pageLoader.currentIndex = 1
                        pageLoader.source = "ImageToolPage.qml"
                    }
                }
                
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 20
                    spacing: 8
                    
                    Text { text: "🖼️"; font.pixelSize: 22 }
                    Text { text: "Image → WebP"; font.family: "Consolas"; font.bold: true; font.pixelSize: 14; color: "#FFFFFF" }
                    Text {
                        text: "Optimize PNG/JPG files to WebP. Toggles lossy or lossless compression engines."
                        font.family: "Consolas"; font.pixelSize: 11; color: "#8E8E93"; elide: Text.ElideRight; wrapMode: Text.Wrap
                        Layout.fillWidth: true; Layout.fillHeight: true
                    }
                    Text {
                        text: "LAUNCH →"
                        font.family: "Consolas"; font.bold: true; font.pixelSize: 9
                        color: mouse1.containsMouse ? "#FF4F00" : "#636366"
                        font.letterSpacing: 0.5
                    }
                }
            }
            
            // Card 2
            Rectangle {
                id: card2
                Layout.fillWidth: true
                Layout.preferredHeight: 190
                color: "#181818"
                border.color: mouse2.containsMouse ? "#FF4F00" : "#242424"
                border.width: 1
                radius: 4
                
                scale: mouse2.containsMouse ? 1.03 : 1.0
                Behavior on scale { SpringAnimation { spring: 3.5; damping: 0.2 } }
                
                MouseArea {
                    id: mouse2
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        pageLoader.currentIndex = 2
                        pageLoader.source = "WebmToolPage.qml"
                    }
                }
                
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 20
                    spacing: 8
                    
                    Text { text: "⚡"; font.pixelSize: 22 }
                    Text { text: "Video → WebM"; font.family: "Consolas"; font.bold: true; font.pixelSize: 14; color: "#FFFFFF" }
                    Text {
                        text: "Compress MOV/MP4 streams to mobile WebM targets using FFmpeg codecs."
                        font.family: "Consolas"; font.pixelSize: 11; color: "#8E8E93"; elide: Text.ElideRight; wrapMode: Text.Wrap
                        Layout.fillWidth: true; Layout.fillHeight: true
                    }
                    Text {
                        text: "LAUNCH →"
                        font.family: "Consolas"; font.bold: true; font.pixelSize: 9
                        color: mouse2.containsMouse ? "#FF4F00" : "#636366"
                        font.letterSpacing: 0.5
                    }
                }
            }
            
            // Card 3
            Rectangle {
                id: card3
                Layout.fillWidth: true
                Layout.preferredHeight: 190
                color: "#181818"
                border.color: mouse3.containsMouse ? "#FF4F00" : "#242424"
                border.width: 1
                radius: 4
                
                scale: mouse3.containsMouse ? 1.03 : 1.0
                Behavior on scale { SpringAnimation { spring: 3.5; damping: 0.2 } }
                
                MouseArea {
                    id: mouse3
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        pageLoader.currentIndex = 3
                        pageLoader.source = "FramesToolPage.qml"
                    }
                }
                
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 20
                    spacing: 8
                    
                    Text { text: "🎞️"; font.pixelSize: 22 }
                    Text { text: "Video → Frames"; font.family: "Consolas"; font.bold: true; font.pixelSize: 14; color: "#FFFFFF" }
                    Text {
                        text: "Extract video sequence frames to high-fidelity, scaled PNG images."
                        font.family: "Consolas"; font.pixelSize: 11; color: "#8E8E93"; elide: Text.ElideRight; wrapMode: Text.Wrap
                        Layout.fillWidth: true; Layout.fillHeight: true
                    }
                    Text {
                        text: "LAUNCH →"
                        font.family: "Consolas"; font.bold: true; font.pixelSize: 9
                        color: mouse3.containsMouse ? "#FF4F00" : "#636366"
                        font.letterSpacing: 0.5
                    }
                }
            }
        }
    }
}