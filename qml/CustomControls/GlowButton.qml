import QtQuick
import QtQuick.Controls

Button {
    id: control
    implicitWidth: 160
    implicitHeight: 38
    
    // Spring physics scale transition on hover
    scale: control.hovered ? 1.04 : 1.0
    Behavior on scale {
        SpringAnimation { spring: 3.5; damping: 0.25; epsilon: 0.005 }
    }
    
    contentItem: Text {
        text: control.text
        font.family: "Consolas"
        font.bold: true
        font.pixelSize: 12
        color: "#FFFFFF"
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }
    
    background: Rectangle {
        color: control.down ? "#C83E00" : (control.hovered ? "#FF5F15" : "#FF4F00")
        radius: 4
        border.color: "#33FFFFFF"
        border.width: 1
        
        // Dynamic Outer Glow Ring
        Rectangle {
            anchors.fill: parent
            anchors.margins: -5
            color: "transparent"
            border.color: "#FF4F00"
            border.width: 1.5
            opacity: control.hovered ? 0.5 : 0.0
            radius: 9
            
            Behavior on opacity {
                NumberAnimation { duration: 180 }
            }
        }
    }
}
