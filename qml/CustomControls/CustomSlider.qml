import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: root
    implicitWidth: 350
    implicitHeight: 40
    
    property alias label: labelText.text
    property alias value: slider.value
    property alias from: slider.from
    property alias to: slider.to
    property alias stepSize: slider.stepSize
    property string valueSuffix: ""
    
    RowLayout {
        anchors.fill: parent
        spacing: 15
        
        Text {
            id: labelText
            Layout.preferredWidth: 140
            font.family: "Consolas"
            font.bold: true
            font.pixelSize: 12
            color: "#8E8E93"
            elide: Text.ElideRight
        }
        
        Slider {
            id: slider
            Layout.fillWidth: true
            value: 0
            from: 0
            to: 100
            
            background: Rectangle {
                x: slider.leftPadding
                y: slider.topPadding + slider.availableHeight / 2 - height / 2
                width: slider.availableWidth
                height: 4
                radius: 2
                color: "#2C2C2E"
                
                Rectangle {
                    width: slider.visualPosition * parent.width
                    height: parent.height
                    color: "#FF4F00"
                    radius: 2
                }
            }
            
            handle: Rectangle {
                x: slider.leftPadding + slider.visualPosition * (slider.availableWidth - width)
                y: slider.topPadding + slider.availableHeight / 2 - height / 2
                width: 14
                height: 14
                radius: 7
                color: "#FFFFFF"
                border.color: "#FF4F00"
                border.width: 1.5
                
                // Spring handle scale on hover
                scale: slider.hovered ? 1.35 : 1.0
                Behavior on scale {
                    SpringAnimation { spring: 4.5; damping: 0.22; epsilon: 0.005 }
                }
            }
        }
        
        Text {
            text: {
                if (slider.stepSize === 1.0) {
                    return Math.round(slider.value) + root.valueSuffix
                }
                return slider.value.toFixed(0) + root.valueSuffix
            }
            font.family: "Consolas"
            font.bold: true
            font.pixelSize: 12
            color: "#FFFFFF"
            Layout.preferredWidth: 60
            horizontalAlignment: Text.AlignRight
        }
    }
}