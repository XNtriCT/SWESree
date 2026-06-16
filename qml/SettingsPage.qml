import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

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
        
        // Header
        ColumnLayout {
            spacing: 4
            Text {
                text: "SYSTEM SETTINGS & TECHNICAL INFO"
                font.family: "Consolas"
                font.bold: true
                font.pixelSize: 20
                color: "#FFFFFF"
                font.letterSpacing: 0.5
            }
            Text {
                text: "Manage binary environment dependencies and view system parameters."
                font.family: "Consolas"
                font.pixelSize: 12
                color: "#8E8E93"
            }
        }
        
        // FFmpeg Card
        Rectangle {
            Layout.fillWidth: true
            implicitHeight: ffmpegLayout.implicitHeight + 30
            color: "#181818"
            border.color: "#242424"
            border.width: 1
            radius: 4
            
            ColumnLayout {
                id: ffmpegLayout
                anchors.fill: parent
                anchors.margins: 15
                spacing: 12
                
                Text {
                    text: "FFMPEG VIDEO PIPELINE BINARY"
                    font.family: "Consolas"
                    font.bold: true
                    font.pixelSize: 12
                    color: "#FFFFFF"
                    font.letterSpacing: 0.5
                }
                
                Text {
                    text: backend.ffmpegStatus
                    font.family: "Consolas"
                    font.pixelSize: 11
                    font.bold: true
                    color: backend.ffmpegStatus.indexOf("✓") !== -1 ? "#30D158" : "#FF453A"
                }
                
                RowLayout {
                    spacing: 15
                    Layout.fillWidth: true
                    
                    Text {
                        text: "CUSTOM PATH"
                        font.family: "Consolas"
                        font.bold: true
                        font.pixelSize: 11
                        color: "#8E8E93"
                        Layout.preferredWidth: 100
                    }
                    
                    TextField {
                        id: ffmpegPathInput
                        text: backend.customFfmpegPath
                        placeholderText: "Leave blank to resolve automatically using PATH"
                        placeholderTextColor: "#48484A"
                        font.family: "Consolas"
                        font.pixelSize: 11
                        color: "#FFFFFF"
                        Layout.fillWidth: true
                        background: Rectangle { color: "#1C1C1E"; border.color: "#2C2C2E"; radius: 3 }
                        onTextChanged: backend.saveFfmpegPath(ffmpegPathInput.text)
                    }
                    
                    Button {
                        text: "LOCATE"
                        font.family: "Consolas"
                        font.pixelSize: 10
                        font.bold: true
                        background: Rectangle {
                            implicitWidth: 80
                            implicitHeight: 28
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
                        onClicked: binDialog.open()
                    }
                }
                
                RowLayout {
                    Layout.fillWidth: true
                    Item { Layout.fillWidth: true }
                    Button {
                        text: "TEST & VERIFY PATHWAY"
                        font.family: "Consolas"
                        font.pixelSize: 10
                        font.bold: true
                        background: Rectangle {
                            implicitWidth: 160
                            implicitHeight: 28
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
                        onClicked: backend.verifyFfmpeg(false)
                    }
                }
            }
        }
        
        // Reset Dashboard stats
        Rectangle {
            Layout.fillWidth: true
            implicitHeight: statsResetLayout.implicitHeight + 30
            color: "#181818"
            border.color: "#242424"
            border.width: 1
            radius: 4
            
            ColumnLayout {
                id: statsResetLayout
                anchors.fill: parent
                anchors.margins: 15
                spacing: 12
                
                Text {
                    text: "RESET PIPELINE TELEMETRY"
                    font.family: "Consolas"
                    font.bold: true
                    font.pixelSize: 12
                    color: "#FFFFFF"
                    font.letterSpacing: 0.5
                }
                
                Text {
                    text: "Erase telemetry logs, space reduction and conversion counters from the Dashboard page."
                    font.family: "Consolas"
                    font.pixelSize: 11
                    color: "#8E8E93"
                }
                
                Button {
                    text: "RESET STATS MATRIX"
                    font.family: "Consolas"
                    font.pixelSize: 10
                    font.bold: true
                    background: Rectangle {
                        implicitWidth: 160
                        implicitHeight: 28
                        color: parent.hovered ? "#FF453A" : "#1C1C1E"
                        border.color: parent.hovered ? "#FF453A" : "#3A3A3C"
                        radius: 3
                    }
                    contentItem: Text {
                        text: parent.text
                        font: parent.font
                        color: parent.hovered ? "#FFFFFF" : "#FF453A"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    onClicked: backend.resetStats()
                }
            }
        }
        
        // About Card (Teenage Engineering Industrial Style)
        Rectangle {
            Layout.fillWidth: true
            implicitHeight: aboutLayout.implicitHeight + 30
            color: "#181818"
            border.color: "#242424"
            border.width: 1
            radius: 4
            
            ColumnLayout {
                id: aboutLayout
                anchors.fill: parent
                anchors.margins: 15
                spacing: 15
                
                Text {
                    text: "TECHNICAL SPECIFICATIONS"
                    font.family: "Consolas"
                    font.bold: true
                    font.pixelSize: 12
                    color: "#FFFFFF"
                    font.letterSpacing: 0.5
                }
                
                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: "#242424"
                }
                
                Text {
                    text: "SWESree is a modular personal productivity wrapper specifically designed to compile optimized web assets using GPU acceleration.\n\n" +
                          "Core System Components:\n" +
                          "  • GUI Layer: PySide6 QML (Qt Quick) GPU Engine\n" +
                          "  • Image Core: Pillow (PIL) WebP Encoder\n" +
                          "  • Video Core: FFmpeg Custom VP9 Compressor\n" +
                          "  • Frame Core: OpenCV (cv2) Lanczos4 Scaler"
                    font.family: "Consolas"
                    font.pixelSize: 12
                    color: "#8E8E93"
                    wrapMode: Text.Wrap
                    Layout.fillWidth: true
                }
                
                Text {
                    text: "© 2026 SWESree. All rights reserved. Industrial config layout."
                    font.family: "Consolas"
                    font.pixelSize: 9
                    color: "#48484A"
                }
            }
        }
    }
    
    // Binary Selector Dialog
    FileDialog {
        id: binDialog
        title: "Locate ffmpeg.exe"
        currentFolder: backend.documentsFolder
        fileMode: FileDialog.OpenFile
        onAccepted: {
            ffmpegPathInput.text = binDialog.selectedFile.toString()
            backend.saveFfmpegPath(ffmpegPathInput.text)
        }
    }
}