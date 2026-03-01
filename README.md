#  Mutual Fund Framework Analyzer

An interactive web application for comparing mutual fund selection frameworks, built on research from IIM Indore.

##  What This Tool Does

- **Compares** different fund selection frameworks (IIM Framework vs Value Research)
- **Simulates** investor outcomes with different strategies
- **Visualizes** wealth paths, success probabilities, and risk metrics
- **Educates** investors on framework differences

##  Live Demo

##  Local Development

### Prerequisites
- Python 3.8 or higher
- pip

### Installation

1. Clone or download this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

4. Open your browser to `http://localhost:8501`

##  Deploy to Streamlit Cloud (FREE)

### Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and create a new repository
2. Name it something like `fund-framework-analyzer`
3. Make it **Public** (required for free Streamlit hosting)

### Step 2: Upload Your Code

Upload these files to your GitHub repository:
```
fund-framework-analyzer/
├── app.py
├── requirements.txt
└── README.md
```

You can either:
- Use GitHub's web interface to upload files
- Or use git command line:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/fund-framework-analyzer.git
git push -u origin main
```

### Step 3: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **"New app"**
4. Select:
   - **Repository**: `YOUR_USERNAME/fund-framework-analyzer`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click **"Deploy!"**

That's it! Your app will be live at:
`https://YOUR_USERNAME-fund-framework-analyzer-app-xxxxx.streamlit.app`

### Step 4: Share Your App

Once deployed, you can:
- Share the URL with anyone
- Embed it in presentations
- Add it to your resume/portfolio

##  Features

### Current Features (v1.0)
-  Framework comparison (FW4 vs Value Research)
-  Custom framework builder with weight sliders
-  Interactive wealth growth visualizations
-  Benchmark beating probability analysis
-  Risk avoidance metrics
-  Multi-horizon evaluation (1Y, 3Y, 5Y, 7Y)
-  Responsive design

### Coming Soon (v2.0)
-  SIP simulation (monthly/quarterly)
-  Multiple start date testing
-  Distribution analysis (best/median/worst outcomes)
-  Regret probability maps
-  PDF report export
-  Framework stability tracking

##  Methodology

This tool implements a novel **Outcome Reliability Framework** developed through research at IIM Indore. 

Key differences from traditional rating systems:
- Focuses on **forward outcome probability** instead of backward performance
- Uses **rolling window analysis** to simulate real investor experiences
- Implements a **reliability gate** based on 7-year win probability
- Evaluates **multi-horizon strength** across different time periods

For full methodology, see the "Methodology" tab in the app.

##  Project Structure

```
.
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

##  Customization

### Adding Your Own Framework Results

To add results from your own framework testing:

1. Open `app.py`
2. Find the `load_framework_results()` function
3. Add your framework data in the same format:

```python
'YourFramework': {
    'name': 'Your Framework Name',
    'weights': {...},
    'results': {
        '1Y': {'terminal_wealth': ..., 'cagr': ..., ...},
        # ... more horizons
    }
}
```

### Changing Colors/Theme

Edit the CSS in the `st.markdown()` section at the top of `app.py`

### Adding More Metrics

Add new calculations in each tab section of the code.

##  Tips for Best Results

1. **Use wide mode**: Set `layout="wide"` in page config (already done)
2. **Cache data**: Use `@st.cache_data` for expensive computations (already implemented)
3. **Mobile friendly**: Test on mobile devices - Streamlit is responsive by default

##  Troubleshooting

### App won't load
- Check that all files are uploaded to GitHub
- Verify `requirements.txt` has no typos
- Check Streamlit Cloud logs for errors

### Slow performance
- Enable caching with `@st.cache_data`
- Reduce number of data points in visualizations
- Use Streamlit's built-in profiler: `streamlit run app.py --server.runOnSave false`

### Chart not displaying
- Check browser console for JavaScript errors
- Try a different browser
- Clear browser cache

##  License

This is a research project created for educational purposes. Feel free to use and modify for academic or personal projects.

##  Contributing

This is a research project, but suggestions are welcome! Open an issue or reach out.

##  Contact

For questions about the methodology or collaboration opportunities, please reach out through:
- GitHub Issues
- [Your email if you want to share]

##  Acknowledgments

- **IIM Indore** for research support
- **AMFI** for mutual fund data
- **NSE** for benchmark indices
- **Streamlit** for the amazing framework

##  Disclaimer

This tool is for **educational and research purposes only**. It is not investment advice. 

- Past performance does not guarantee future results
- All investments carry risk
- Consult a qualified financial advisor before making investment decisions
- The creators assume no liability for investment decisions made using this tool

---

Built with ❤️ using Streamlit | Research Project @ IIM Indore
