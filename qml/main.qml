import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Window

ApplicationWindow {
    id: window
    width: 1024
    height: 768
    visible: true
    title: "SWESree"
    flags: Qt.Window
    color: "#0F0F11"
    
    // Background Volumetric Lighting (Ambient Orbs moving slowly)
    Item {
        anchors.fill: parent
        z: -1
        
        // Dark Obsidian Base
        Rectangle {
            anchors.fill: parent
            color: "#121212"
        }
        
        // Volumetric Orb 1 (Orange Tint)
        Rectangle {
            id: orb1
            width: 500
            height: 500
            radius: 250
            color: "#FF4F00"
            opacity: 0.04
            
            x: 0
            y: 0
            
            SequentialAnimation on x {
                loops: Animation.Infinite
                NumberAnimation { to: 400; duration: 18000; easing.type: Easing.InOutSine }
                NumberAnimation { to: 0; duration: 18000; easing.type: Easing.InOutSine }
            }
            SequentialAnimation on y {
                loops: Animation.Infinite
                NumberAnimation { to: 300; duration: 22000; easing.type: Easing.InOutSine }
                NumberAnimation { to: 0; duration: 22000; easing.type: Easing.InOutSine }
            }
        }
        
        // Volumetric Orb 2 (Titanium Grey Tint)
        Rectangle {
            id: orb2
            width: 400
            height: 400
            radius: 200
            color: "#8E8E93"
            opacity: 0.05
            
            x: 600
            y: 400
            
            SequentialAnimation on x {
                loops: Animation.Infinite
                NumberAnimation { to: 200; duration: 20000; easing.type: Easing.InOutSine }
                NumberAnimation { to: 600; duration: 20000; easing.type: Easing.InOutSine }
            }
            SequentialAnimation on y {
                loops: Animation.Infinite
                NumberAnimation { to: 100; duration: 16000; easing.type: Easing.InOutSine }
                NumberAnimation { to: 400; duration: 16000; easing.type: Easing.InOutSine }
            }
        }
    }
    
    // Main App Container (Sidebar + Content)
    ColumnLayout {
        anchors.fill: parent
        spacing: 0
        
        // Custom Titlebar
        Rectangle {
            id: titlebar
            Layout.fillWidth: true
            height: 40
            color: "#181818"
            border.color: "#242424"
            border.width: 1
            

            RowLayout {
                anchors.fill: parent
                anchors.leftMargin: 15
                anchors.rightMargin: 15
                spacing: 12
                
                Text {
                    text: "SWESree"
                    font.family: "Consolas"
                    font.bold: true
                    font.pixelSize: 12
                    color: "#FF4F00"
                    font.letterSpacing: 1.0
                }
                
                Text {
                    text: "PRODUCTION KIT"
                    font.family: "Consolas"
                    font.pixelSize: 9
                    color: "#8E8E93"
                    font.letterSpacing: 1.5
                }
                
                Item { Layout.fillWidth: true }
                
                // Minimize
                Button {
                    text: "—"
                    font.bold: true
                    font.pixelSize: 10
                    Layout.preferredWidth: 26
                    Layout.preferredHeight: 20
                    background: Rectangle {
                        color: parent.hovered ? "#2C2C2E" : "transparent"
                        radius: 3
                    }
                    contentItem: Text {
                        text: parent.text
                        color: "#FFFFFF"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    onClicked: window.showMinimized()
                }
                
                // Maximize
                Button {
                    text: window.visibility === Window.Maximized ? "❐" : "⬜"
                    font.pixelSize: 9
                    Layout.preferredWidth: 26
                    Layout.preferredHeight: 20
                    background: Rectangle {
                        color: parent.hovered ? "#2C2C2E" : "transparent"
                        radius: 3
                    }
                    contentItem: Text {
                        text: parent.text
                        color: "#FFFFFF"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    onClicked: {
                        if (window.visibility === Window.Maximized) {
                            window.showNormal()
                        } else {
                            window.showMaximized()
                        }
                    }
                }
                
                // Close
                Button {
                    text: "×"
                    font.bold: true
                    font.pixelSize: 16
                    Layout.preferredWidth: 26
                    Layout.preferredHeight: 20
                    background: Rectangle {
                        color: parent.hovered ? "#FF453A" : "transparent"
                        radius: 3
                    }
                    contentItem: Text {
                        text: parent.text
                        color: parent.hovered ? "#FFFFFF" : "#8E8E93"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    onClicked: window.close()
                }
            }
        }
        
        // Sidebar & Page content Layout
        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 0
            
            // Sidebar Navigation
            Rectangle {
                id: sidebar
                Layout.fillHeight: true
                width: 200
                color: "#181818"
                border.color: "#242424"
                border.width: 1
                
                ColumnLayout {
                    anchors.fill: parent
                    anchors.topMargin: 20
                    anchors.bottomMargin: 20
                    spacing: 4
                    
                    // Helper function to define nav buttons
                    Component {
                        id: navButtonComponent
                        Button {
                            id: navBtn
                            property string pageUrl: parent ? parent.pageUrl : ""
                            property string pageName: parent ? parent.pageName : ""
                            property int indexID: parent ? parent.indexID : -1
                            
                            Layout.fillWidth: true
                            Layout.leftMargin: 12
                            Layout.rightMargin: 12
                            Layout.preferredHeight: 38
                            
                            background: Rectangle {
                                color: (pageLoader.currentIndex === indexID) ? "#2D2D2D" : (navBtn.hovered ? "#242424" : "transparent")
                                radius: 4
                                border.color: (pageLoader.currentIndex === indexID) ? "#FF4F00" : "transparent"
                                border.width: 1
                            }
                            
                            contentItem: Text {
                                text: navBtn.pageName
                                font.family: "Consolas"
                                font.bold: true
                                font.pixelSize: 11
                                color: (pageLoader.currentIndex === indexID) ? "#FFFFFF" : "#8E8E93"
                                verticalAlignment: Text.AlignVCenter
                                anchors.left: parent.left
                                anchors.leftMargin: 15
                            }
                            
                            onClicked: {
                                pageLoader.currentIndex = indexID
                                pageLoader.source = navBtn.pageUrl
                            }
                        }
                    }
                    
                    Loader {
                        Layout.fillWidth: true
                        sourceComponent: navButtonComponent
                        property string pageName: "📊 DASHBOARD"
                        property string pageUrl: "DashboardPage.qml"
                        property int indexID: 0
                    }
                    
                    Loader {
                        Layout.fillWidth: true
                        sourceComponent: navButtonComponent
                        property string pageName: "🖼️ IMAGE → WEBP"
                        property string pageUrl: "ImageToolPage.qml"
                        property int indexID: 1
                    }
                    
                    Loader {
                        Layout.fillWidth: true
                        sourceComponent: navButtonComponent
                        property string pageName: "⚡ VIDEO → WEBM"
                        property string pageUrl: "WebmToolPage.qml"
                        property int indexID: 2
                    }
                    
                    Loader {
                        Layout.fillWidth: true
                        sourceComponent: navButtonComponent
                        property string pageName: "🎞️ VIDEO → FRAMES"
                        property string pageUrl: "FramesToolPage.qml"
                        property int indexID: 3
                    }
                    
                    Loader {
                        Layout.fillWidth: true
                        sourceComponent: navButtonComponent
                        property string pageName: "⚙️ SETTINGS"
                        property string pageUrl: "SettingsPage.qml"
                        property int indexID: 4
                    }
                    
                    Item { Layout.fillHeight: true }
                    
                    Text {
                        text: "SWESree v1.0.0"
                        font.family: "Consolas"
                        font.pixelSize: 9
                        color: "#48484A"
                        Layout.alignment: Qt.AlignHCenter
                    }
                }
            }
            
            // Dynamic Content Loader Area (Smooth fade-in transition)
            Item {
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true
                
                Loader {
                    id: pageLoader
                    anchors.fill: parent
                    source: "DashboardPage.qml"
                    
                    property int currentIndex: 0
                    
                    onSourceChanged: {
                        fadeInAnimation.restart()
                    }
                    
                    opacity: 0
                    
                    NumberAnimation on opacity {
                        id: fadeInAnimation
                        from: 0
                        to: 1
                        duration: 300
                        easing.type: Easing.OutQuad
                    }
                }
            }
        }
    }
}