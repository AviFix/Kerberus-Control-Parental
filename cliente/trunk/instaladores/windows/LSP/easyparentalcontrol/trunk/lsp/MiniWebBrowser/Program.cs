using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Forms;

namespace MiniWebBrowser
{
    static class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new WebBrowserForm());
            /*
            var lspInstaller1 = new LspInstaller();
            try
            {
                lspInstaller1.Install();
                Application.Run(new WebBrowserForm());
            }
            finally
            {
                lspInstaller1.Uninstall();
            }
             */
        }
    }
}
