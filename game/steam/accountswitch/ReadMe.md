## Steam 帐号切换

### 工作原理

参考 https://steamcn.com/t367536-1-1

1. 用各个帐号正常登录一次，且记住密码
2. 修改注册表中当前自动登录的帐号
3. 执行steam主程序

```bat
::对应有4个地方需要写账号并且一致，各位自行修改核对或者添加（最好用记事本的全部替换）。以下3个分别是我的主号码、小号。
@echo off 
color 9E 
echo 请steam选择账号 
echo 1、        account1 
echo 2、        account2 
echo 3、        退出   

set /p choice2=

:Step1_Next   
if %choice2%==1 goto account1 
if %choice2%==2 goto account2 
if %choice2%==3 goto end   

:account1 
reg add "HKEY_CURRENT_USER\Software\Valve\Steam" /v AutoLoginUser /t REG_SZ /d account1 /f 
goto Step2

:account2 
reg add "HKEY_CURRENT_USER\Software\Valve\Steam" /v AutoLoginUser /t REG_SZ /d account2 /f 
goto Step2

:end 
exit
::steam路径设置 
:Step2 
echo 强制结束当前的所有steam进程
echo taskkill /im steam.exe /f
start D:\Steam\Steam.exe 
exit
```

作者的C#实现简单调整了一些，使用应用程序配置文件，增加用户名设置

```c#
public MainDialog()
{
	InitializeComponent();
	InitControlValues();
}

private void OnStartClick(object sender, EventArgs e)
{
	// get the user name
	string user = AccountCombobox.Text.Trim();

	// add in register
	AddAutoLoginRegister(user);

	// start steam
	StartSteamApp();
}
// 使用配置文件需要在工程--添加--引用--程序集--框架中选择Configuration
private void InitControlValues()
{
	AccountCombobox.Items.Clear();
	if (ConfigurationManager.AppSettings.HasKeys())
	{
		foreach (string theKey in ConfigurationManager.AppSettings.Keys)
		{
			string usr = ConfigurationManager.AppSettings[theKey];
			AccountCombobox.Items.Add(usr);
		}
	}            
}

private void AddAutoLoginRegister(string user)
{
	RegistryKey hklm = Registry.CurrentUser;
	RegistryKey software = hklm.OpenSubKey("SOFTWARE", true);
	RegistryKey value = software.OpenSubKey("Valve", true);
	RegistryKey steam = value.OpenSubKey("Steam", true);
	steam.SetValue("AutoLoginUser", user);
}

private void StartSteamApp()
{
	KillCurrentSteamApp();

	RegistryKey steam = Registry.CurrentUser.OpenSubKey("SOFTWARE", true).OpenSubKey("Valve", true).OpenSubKey("Steam", true);
	string steamExe = steam.GetValue("SteamExe").ToString();
	// @ is for not \ parse
	System.Diagnostics.Process.Start(@steamExe);
}

private void KillCurrentSteamApp()
{
	Process[] ps = Process.GetProcesses();
	foreach (Process item in ps)
	{
		if (item.ProcessName == "Steam")
		{
			item.Kill();
		}
	}
}
```

#### 其他补充

在steam的安装目录`D:\Program Files (x86)\Steam\config`下有`loginusers.vdf`配置文件，其中可以获取当前可以自动登录的用户列表以及用户上次登录时间信息，从而不需要配置文件中设置登录用户名。