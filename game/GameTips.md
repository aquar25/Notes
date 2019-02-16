### NBA 2K14

软件自动去连接服务器，设置host屏蔽一下，不然太卡顿

```bash
# for nba2k14
127.0.0.1 ns.take2games.com
127.0.0.1 nba2k14.pc.2ksports.com
127.0.0.1 hostmaster.take2games.com
```



### Steam

#### 导入已经下载好的游戏

steam客户端根据acf文件来判断一个库中的游戏的下载进度和配置情况。

**没有游戏对应的acf文件时，一定确保要安装的目录磁盘剩余空间足够steam安装时分配，即磁盘空间在拷贝了已经下载好的文件后，还可以有足够的空间再让steam下载一份游戏**

1. steam支持多个库目录，以古墓丽影为例，把其他电脑上steam库目录A里的`F:\SteamLibrary\steamapps\common\Tomb Raider`目录拷贝到本机的steam对应库目录B
2. 在保证剩余磁盘空间足够的前提下，在steam客户端中安装游戏`Tomb Raider`，此时steam会开始准备下载文件，选则安装的库目录为刚刚拷贝的那个库目录B
3. 开始安装后，steam会为游戏分配磁盘空间，它首先会发现库里面已经有了这个游戏，开始检测现有文件的有效性，对于缺少的文件则会下载到downloading目录下的`203160`目录中，这个数字是古墓9的steam编号。如果拷贝过来的文件本来就是完整的，检测完成后不会下载其他的文件

* 对于有游戏对应的acf文件的时，只要把acf文件和游戏原始文件放到对应的目录下，steam在启动后，自动会发现库里面的acf文件，并根据acf文件中的状态来决定是否需要更新游戏。所以，拷贝游戏时最好把游戏文件和acf文件都要拷贝了，不然容易出现不匹配的情况。

以下为古墓丽影9在2019-02-16时的appmanifest_203160.acf文件，其中`"StateFlags"		"4"`表示游戏下载完成

```json
"AppState"
{
	"appid"		"203160"
	"Universe"		"1"
	"name"		"Tomb Raider"
	"StateFlags"		"4"
	"installdir"		"Tomb Raider"
	"LastUpdated"		"1550322713"
	"UpdateResult"		"0"
	"SizeOnDisk"		"11739736619"
	"buildid"		"2306640"
	"LastOwner"		"76561198099917059"
	"BytesToDownload"		"0"
	"BytesDownloaded"		"0"
	"AutoUpdateBehavior"		"0"
	"AllowOtherDownloadsWhileRunning"		"0"
	"ScheduledAutoUpdate"		"0"
	"UserConfig"
	{
		"language"		"english"
	}
	"InstalledDepots"
	{
		"203161"
		{
			"manifest"		"5485481450200467014"
		}
		"203162"
		{
			"manifest"		"2490011264789018002"
		}
		"203163"
		{
			"manifest"		"6372322314347314780"
		}
		"203179"
		{
			"manifest"		"1235174477397814857"
		}
		"208810"
		{
			"manifest"		"3849166016491976395"
			"dlcappid"		"208810"
		}
		"208811"
		{
			"manifest"		"4516305040932421733"
			"dlcappid"		"208811"
		}
		"208812"
		{
			"manifest"		"2242108116796868778"
			"dlcappid"		"208812"
		}
		"208813"
		{
			"manifest"		"9089747663761388950"
			"dlcappid"		"208813"
		}
		"208814"
		{
			"manifest"		"3065129487810682314"
			"dlcappid"		"208814"
		}
	}
	"MountedDepots"
	{
		"203161"		"5485481450200467014"
		"203162"		"2490011264789018002"
		"203163"		"6372322314347314780"
		"203179"		"1235174477397814857"
		"208810"		"3849166016491976395"
		"208811"		"4516305040932421733"
		"208812"		"2242108116796868778"
		"208813"		"9089747663761388950"
		"208814"		"3065129487810682314"
	}
	"DlcDownloads"
	{
		"208810"
		{
			"BytesDownloaded"		"62800416"
			"BytesToDownload"		"62800416"
		}
		"208811"
		{
			"BytesDownloaded"		"286248768"
			"BytesToDownload"		"286248768"
		}
		"208812"
		{
			"BytesDownloaded"		"34445744"
			"BytesToDownload"		"34445744"
		}
		"208813"
		{
			"BytesDownloaded"		"181159200"
			"BytesToDownload"		"181159200"
		}
		"208814"
		{
			"BytesDownloaded"		"89924624"
			"BytesToDownload"		"89924624"
		}
	}
}
```

