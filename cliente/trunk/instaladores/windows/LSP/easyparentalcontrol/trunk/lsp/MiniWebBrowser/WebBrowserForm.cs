using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace MiniWebBrowser
{
    public partial class WebBrowserForm : Form
    {
        public WebBrowserForm()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            toolStripButton1_Click(sender, e);
        }

        private void toolStripButton1_Click(object sender, EventArgs e)
        {
            webBrowser1.Url = new Uri(toolStripTextBox1.Text);
        }

        private void webBrowser1_Navigating(object sender, WebBrowserNavigatingEventArgs e)
        {
            string url = e.Url.ToString();
            if (url != "about:blank")
            {
                toolStripTextBox1.Text = url;
            }
            toolStripStatusLabel1.Text = "Loading...";
        }

        private void webBrowser1_Navigated(object sender, WebBrowserNavigatedEventArgs e)
        {
            toolStripStatusLabel1.Text = "Ready";
        }

        private void toolStripButton2_Click(object sender, EventArgs e)
        {
            webBrowser1.GoBack();
        }
    }
}
