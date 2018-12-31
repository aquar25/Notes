using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Configuration;
using Microsoft.Win32;
using System.Diagnostics;

namespace SteamAccountSwitch
{
    public partial class MainDialog : Form
    {
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

    }
}
