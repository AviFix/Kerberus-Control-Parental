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
    public partial class LspProvidersForm : Form
    {
        public LspProvidersForm()
        {
            InitializeComponent();
        }

        private void LspProvidersForm_Load(object sender, EventArgs e)
        {

        }

        private void btnRefresh_Click(object sender, EventArgs e)
        {
            var providers = new lsputils.Providers();
        }
    }
}
