
###shadowsocksR
网上下载的windows程序运行时会提示“Fatal Error Can't bind to 127.0.0.1:xxxx (error number 10106)”,经过在stackoverflow上查，原因是winsock的错误
```
Service provider failed to initialize. This error is returned if either a service provider's DLL could not be loaded(LoadLibrary failed)or the provider's WSPStartup or NSPStartup function failed.
```
To fix it, open cmd as admin, type the following and hit Enter. `netsh winsock reset`