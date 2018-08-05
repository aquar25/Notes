###Mobile Game Dev

#####Android
* skia/canvas
* OpenGL ES
* NDK

#####Mac & IOS
* Quartz2D 
* OpenGL ES 卡马克 地图算法

#####Linux
* OpenGL

#####WP7 & WP8 & WIN8
* DirectX
* XNA 游戏框架（Microsoft supply）

* HTML5: Canvas/WebGL
* Unity3D: OpenGL
* Cocos2d-x: OpenGL ES/DirectX/Canvas

cocos2d 最早是用Python编写,因此是cocos2d-python，首先cocos2d-iPhone版本非常受欢迎,随后开发了cocos2d-android,但是效果不是很好，最终开发了cocos2d-x,实现了多个平台。

cocos2d-x的组件：
* 主体：OpenGL ES/DirectX/Canvas/pthread
* 2D物理引擎：Box2D/Chipmunk
* 网络库：libcurl/BSD Socket/SimpleAudioEngine

cocos2d-x的数据结构
* CCCopying // 接口，用来复制对象，类似java中的clone()
* CCObject  // 所有类的基类
* CCZone    // 只是保存了CCObject的一个对象指针
* CCData    // 有个byte的字节数组，用来保存数据
* CCGeometry// 几何图形相关CCPoint/CCRect
* CCSet     // 类似java中的set
* CCArray   // 类似java的数组
* CCString  // 字符串的封装
* CCTypes.h // 定义的常量、结构体


