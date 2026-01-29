import streamlit as st
import google.generativeai as genai

# Page configuration
st.set_page_config(
    page_title="JCL Optimization Analyzer",
    page_icon="🚀",
    layout="wide"
)

# Title and description
st.title("🚀 JCL Optimization Analyzer")
st.markdown("**AI-Powered Mainframe Batch Performance Optimization**")
st.markdown("*Built by Biswarup Chakraborty - Proof of Concept*")
st.markdown("---")

# Sidebar with information
with st.sidebar:
    st.markdown("### About This Tool")
    st.markdown("""
    This analyzer uses Google Gemini AI to identify optimization opportunities in JCL procedures:
    
    ✅ Parallelization opportunities  
    ✅ Resource optimization  
    ✅ I/O efficiency improvements  
    ✅ Unnecessary dependencies  
    ✅ Job step consolidation  
    """)
    
    st.markdown("### Sample Use Cases")
    st.markdown("""
    **Financial Services:**
    - Daily annuity processing (AIG experience)
    - End-of-day settlement
    - Regulatory reporting
    
    **Automotive:**
    - Manufacturing batch jobs
    - Supply chain processing
    - Quality control reporting
    """)
    
    # API Key input
    st.markdown("---")
    st.markdown("### ⚙️ Configuration")
 # Trying to get API key from secrets first (for deployed version)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    st.success("✅ API Key configured (from StreamLit)")
except:
    # If not in secrets, ask user to input
    api_key = st.text_input(
        "Google Gemini API Key",
        type="password",
        #help="Get free key from: https://makersuite.google.com/app/apikey"
    )
    
    if api_key:
        st.success("API Key configured ✅")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📝 Input JCL")
    
    # Sample JCL selector
    sample_option = st.selectbox(
        "Choose JCL Sample:",
        [
            "⚠️ Select a sample to load...",
            "🏦 Daily Annuity Processing (AIG - Financial)",
            "🏭 Manufacturing Batch (Automotive)",
            "✏️ Enter Custom JCL"
        ]
    )
    
    # Sample JCL procedures
    samples = {
        "🏦 Daily Annuity Processing (AIG - Financial)": """//DAILYPRC JOB (ACCT),'DAILY ANNUITY PROCESS',CLASS=A,MSGCLASS=X
//********************************************************************
//* DAILY ANNUITY PROCESSING - AIG USA
//* BASELINE: 6 HOUR BATCH WINDOW (BEFORE OPTIMIZATION)
//* PROCESSES: Premium calculations, Policy validations, Reports
//********************************************************************
//STEP01   EXEC PGM=SORT,REGION=8M
//SORTIN   DD DSN=ANNUITY.TRANS.DAILY,DISP=SHR
//SORTOUT  DD DSN=&&SORTED,DISP=(NEW,PASS),
//            SPACE=(CYL,(10,5)),UNIT=SYSDA
//SYSIN    DD *
  SORT FIELDS=(1,10,CH,A)
/*
//*
//STEP02   EXEC PGM=VALPROG,REGION=8M,COND=(0,NE,STEP01)
//INPUT    DD DSN=&&SORTED,DISP=(OLD,DELETE)
//OUTPUT   DD DSN=&&VALID,DISP=(NEW,PASS),
//            SPACE=(CYL,(10,5)),UNIT=SYSDA
//SYSOUT   DD SYSOUT=*
//*
//STEP03   EXEC PGM=CALCPREM,REGION=8M,COND=(0,NE,STEP02)
//INPUT    DD DSN=&&VALID,DISP=(OLD,DELETE)
//PREMIUM  DD DSN=PREMIUM.CALC.OUTPUT,DISP=(NEW,CATLG),
//            SPACE=(CYL,(20,10)),UNIT=SYSDA
//SYSOUT   DD SYSOUT=*
//*
//STEP04   EXEC PGM=INTEREST,REGION=8M,COND=(0,NE,STEP03)
//INPUT    DD DSN=PREMIUM.CALC.OUTPUT,DISP=SHR
//OUTPUT   DD DSN=INTEREST.CALC.OUTPUT,DISP=(NEW,CATLG),
//            SPACE=(CYL,(15,8)),UNIT=SYSDA
//*
//STEP05   EXEC PGM=RPTGEN,REGION=8M,COND=(0,NE,STEP04)
//INPUT1   DD DSN=PREMIUM.CALC.OUTPUT,DISP=SHR
//INPUT2   DD DSN=INTEREST.CALC.OUTPUT,DISP=SHR
//REPORT   DD SYSOUT=*
//SUMMARY  DD DSN=DAILY.SUMMARY.REPORT,DISP=(NEW,CATLG),
//            SPACE=(CYL,(5,2)),UNIT=SYSDA""",
        
        "🏭 Manufacturing Batch (Automotive)": """//MFGBATCH JOB (MFG),'MANUFACTURING DAILY',CLASS=A,MSGCLASS=X
//********************************************************************
//* DAILY MANUFACTURING BATCH - AUTOMOTIVE
//* PROCESSES: Parts inventory, Quality checks, Defect tracking
//********************************************************************
//STEP01   EXEC PGM=SORT,REGION=8M
//SORTIN   DD DSN=MFG.PARTS.DAILY,DISP=SHR
//SORTOUT  DD DSN=&&SORTED1,DISP=(NEW,PASS),
//            SPACE=(CYL,(15,5)),UNIT=SYSDA
//SYSIN    DD *
  SORT FIELDS=(1,8,CH,A)
/*
//*
//STEP02   EXEC PGM=SORT,REGION=8M
//SORTIN   DD DSN=MFG.QUALITY.DAILY,DISP=SHR
//SORTOUT  DD DSN=&&SORTED2,DISP=(NEW,PASS),
//            SPACE=(CYL,(15,5)),UNIT=SYSDA
//SYSIN    DD *
  SORT FIELDS=(1,8,CH,A)
/*
//*
//STEP03   EXEC PGM=QCCHECK,REGION=8M,COND=(0,NE,STEP01)
//INPUT    DD DSN=&&SORTED1,DISP=(OLD,DELETE)
//OUTPUT   DD DSN=&&QCPASS,DISP=(NEW,PASS),
//            SPACE=(CYL,(10,5)),UNIT=SYSDA
//FAILED   DD DSN=QC.FAILED.PARTS,DISP=(NEW,CATLG),
//            SPACE=(CYL,(5,2)),UNIT=SYSDA
//*
//STEP04   EXEC PGM=DEFECT,REGION=8M,COND=(0,NE,STEP02)
//INPUT    DD DSN=&&SORTED2,DISP=(OLD,DELETE)
//OUTPUT   DD DSN=&&DEFECTS,DISP=(NEW,PASS),
//            SPACE=(CYL,(10,5)),UNIT=SYSDA
//*
//STEP05   EXEC PGM=INVUPD,REGION=8M,COND=(0,NE,STEP03)
//QCPASS   DD DSN=&&QCPASS,DISP=(OLD,DELETE)
//INVENTORY DD DSN=MFG.MASTER.INVENTORY,DISP=SHR
//OUTPUT   DD DSN=MFG.INVENTORY.UPDATED,DISP=(NEW,CATLG),
//            SPACE=(CYL,(20,10)),UNIT=SYSDA
//*
//STEP06   EXEC PGM=RPTGEN,REGION=8M,COND=(0,NE,STEP04)
//DEFECTS  DD DSN=&&DEFECTS,DISP=(OLD,DELETE)
//REPORT   DD SYSOUT=*
//SUMMARY  DD DSN=MFG.DAILY.SUMMARY,DISP=(NEW,CATLG),
//            SPACE=(CYL,(5,2)),UNIT=SYSDA"""
    }
    
    # Set default text based on selection
    if sample_option == "⚠️ Select a sample to load...":
        default_jcl = "// Select a sample from the dropdown above or choose 'Enter Custom JCL'"
        jcl_disabled = True
    elif sample_option == "✏️ Enter Custom JCL":
        default_jcl = "// Paste your JCL here..."
        jcl_disabled = False
    else:
        default_jcl = samples[sample_option]
        jcl_disabled = False
    
    jcl_input = st.text_area(
        "JCL Code:",
        value=default_jcl,
        height=450,
        disabled=jcl_disabled,
        help="Load a sample above or enter custom JCL"
    )

with col2:
    st.markdown("### 🔍 Optimization Analysis")
    
    # Info box
    st.info("""
    👨‍💻 **About the Analysis:**
    
    This tool uses Google's Gemini AI (free) to analyze JCL procedures the same way I manually optimized batch jobs at AIG—but in seconds instead of weeks.
    
    **At AIG, I achieved:**
    - 40% batch window reduction (6hrs → 3.6hrs)
    - Through parallelization and resource tuning
    - Took weeks of manual analysis
    
    **This tool automates that process.**
    """)
    
    if st.button("🚀 Analyze & Optimize", type="primary", use_container_width=True):
        if not api_key:
            st.error("⚠️ Please enter your Google Gemini API key in the left sidebar")
            st.info("💡 Get a free key from: https://makersuite.google.com/app/apikey")
        elif not jcl_input.strip() or "Select a sample" in jcl_input:
            st.error("⚠️ Please select a JCL sample from the dropdown above")
        else:
            with st.spinner("🤖 Google Gemini AI is analyzing your JCL... (15-30 seconds)"):
                try:
                    # Configure Gemini
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    # Optimization analysis prompt
                    prompt = f"""You are a senior mainframe performance optimization expert with 25+ years of experience at major financial services and automotive companies. You've personally optimized batch processing for companies like AIG, Citibank, and major automotive manufacturers.

Analyze this JCL procedure and provide a COMPREHENSIVE, DETAILED optimization analysis.

JCL CODE TO ANALYZE:
{jcl_input}

Provide your analysis in this EXACT markdown format:

# 📊 JCL OPTIMIZATION ANALYSIS REPORT

## 1. EXECUTIVE SUMMARY
- **Current estimated runtime:** [estimate in hours/minutes]
- **Optimized estimated runtime:** [estimate in hours/minutes]  
- **Potential time savings:** [percentage]
- **Annual cost savings:** [calculate: hours saved × 365 days × $500/hour]
- **Implementation effort:** [Low/Medium/High]

## 2. 🔄 PARALLELIZATION OPPORTUNITIES (HIGHEST IMPACT)

### Current Execution Flow:
```
[Show current serial execution as ASCII diagram]
STEP01 (1.5hrs) → STEP02 (1.5hrs) → STEP03 (1.5hrs) → STEP04 (1.5hrs)
Total: 6 hours
```

### Optimized Execution Flow:
```
[Show parallel execution as ASCII diagram]
STEP01 (1.5hrs) ────┐
                     ├──→ STEP03 (1.5hrs)
STEP02 (1.5hrs) ────┘
                     
STEP04 can also run parallel to STEP03
Total: 3 hours
```

### Specific Recommendations:
1. **STEP01 and STEP02 can run in parallel**
   - No data dependencies between them
   - Currently running serial due to COND parameter
   - Remove: `COND=(0,NE,STEP01)` from STEP02
   
2. [Continue with more specific recommendations...]

## 3. 💾 RESOURCE OPTIMIZATION

### REGION Parameter Analysis:
| Step | Current | Recommended | Savings |
|------|---------|-------------|---------|
| STEP01 | 8M | 2M | 6M saved |
| STEP02 | 8M | 4M | 4M saved |
[Continue for all steps...]

**Rationale:** SORT programs typically need 2-4M, not 8M. Oversized REGION wastes memory.

### Buffer Optimization:
[Provide specific BUFNO/BUFSIZE recommendations for large files]

## 4. 📁 I/O OPTIMIZATION

### Temporary Dataset Elimination:
- **STEP02:** Currently uses `&&SORTED,DISP=(NEW,PASS)` 
  - Can be replaced with pipe if steps combined
  - Saves 1 disk I/O operation
  
### SPACE Allocation Improvements:
[Provide specific recommendations]

## 5. 🔗 DEPENDENCY ANALYSIS

### Unnecessary COND Parameters:
- **STEP02:** `COND=(0,NE,STEP01)` - Remove for parallelization
- **STEP03:** `COND=(0,NE,STEP02)` - Necessary, keep

### Job Step Consolidation:
[Identify steps that could be combined]

## 6. 💻 CODE IMPROVEMENTS (BEFORE/AFTER)

### Change #1: Parallelize STEP01 and STEP02

**BEFORE:**
```jcl
//STEP01   EXEC PGM=SORT,REGION=8M
[current code]
//STEP02   EXEC PGM=XXX,REGION=8M,COND=(0,NE,STEP01)
```

**AFTER:**
```jcl
//STEP01   EXEC PGM=SORT,REGION=2M
[optimized code]
//STEP02   EXEC PGM=XXX,REGION=4M
// Remove COND to allow parallel execution
```

[Continue with more changes...]

## 7. 📈 IMPLEMENTATION ROADMAP

### Phase 1: Quick Wins (Low Risk, High Impact)
1. ✅ Adjust REGION parameters (1 day, test in DEV)
2. ✅ Add buffer optimization (1 day)
   
### Phase 2: Parallelization (Medium Risk, Highest Impact)
1. Remove unnecessary COND parameters (3 days with testing)
2. Restructure job dependencies

### Phase 3: Advanced (Higher Risk)
1. Job step consolidation
2. [Additional items]

## 8. ⚠️ RISK ASSESSMENT

### LOW RISK (Implement immediately):
- ✅ REGION parameter adjustments
- ✅ SPACE parameter tuning

### MEDIUM RISK (Test in DEV first):
- ⚠️ Parallelization changes
- ⚠️ Buffer optimizations

### HIGH RISK (Thorough testing required):
- 🔴 Job step consolidation
- 🔴 Major flow restructuring

## 9. 💰 BUSINESS IMPACT

**For Financial Services (Annuity Processing):**
- Faster nightly batch = earlier reporting
- Reduced batch window risk
- $438K annual savings (typical)

**For Automotive (Manufacturing):**
- Faster quality reports = quicker defect response
- Improved production planning
- Similar cost savings

## 10. 🎯 RECOMMENDED NEXT STEPS

1. **Immediate (This Week):**
   - Implement REGION optimizations
   - Test in development environment
   
2. **Short-term (Next 2 Weeks):**
   - Implement parallelization
   - Conduct thorough testing
   
3. **Long-term (Next Month):**
   - Monitor performance improvements
   - Document lessons learned

---

**SUMMARY:** This JCL has significant optimization potential. Conservative estimate: **40% runtime reduction** with low implementation risk. Recommend starting with Phase 1 quick wins.

*Analysis completed by AI (Google Gemini) - Verify recommendations in test environment before production implementation.*"""

                    # Generate analysis
                    response = model.generate_content(
                        prompt,
                        generation_config=genai.types.GenerationConfig(
                            temperature=0.3,
                            max_output_tokens=8000,
                        )
                    )
                    
                    # Display analysis
                    analysis_text = response.text
                    st.markdown(analysis_text)
                    
                    st.markdown("---")
                    
                    # Success metrics visualization
                    st.markdown("### 📊 Typical Optimization Impact")
                    st.caption("Based on my experience at AIG optimizing similar batch jobs")
                    
                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                    
                    with metric_col1:
                        st.metric(
                            label="⏱️ Time Savings",
                            value="40%",
                            delta="2.4 hrs/day",
                            help="Typical parallelization + resource tuning gains"
                        )
                    
                    with metric_col2:
                        st.metric(
                            label="💰 Annual Savings",
                            value="$438K",
                            delta="Positive ROI",
                            help="2.4 hrs × 365 days × $500/hr mainframe cost"
                        )
                    
                    with metric_col3:
                        st.metric(
                            label="📅 Implementation",
                            value="1-2 weeks",
                            delta="Fast deployment",
                            help="Most changes are configuration, not code"
                        )
                    
                    with metric_col4:
                        st.metric(
                            label="🎯 Risk Level",
                            value="Low",
                            delta="Safe changes",
                            help="Phase 1 changes are low-risk configuration"
                        )
                    
                    # Download button
                    st.markdown("---")
                    st.download_button(
                        label="📥 Download Full Optimization Report",
                        data=analysis_text,
                        file_name="jcl_optimization_report.md",
                        mime="text/markdown",
                        use_container_width=True,
                        type="primary"
                    )
                    
                    st.success("✅ Analysis complete! Review recommendations above and download the full report.")
                    
                except Exception as e:
                    st.error(f"❌ Error occurred: {str(e)}")
                    st.info("""
                    **Troubleshooting:**
                    - ✅ Check your API key is correct
                    - ✅ Verify you have internet connection  
                    - ✅ Make sure API key has free quota remaining
                    - 💡 Get a new key from: https://makersuite.google.com/app/apikey
                    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p style='font-size: 18px; font-weight: bold; margin-bottom: 10px;'>🚀 JCL Optimization Analyzer</p>
    <p style='margin: 5px 0;'>Proof of Concept - Built by <strong>Biswarup Chakraborty</strong></p>
    <p style='margin: 5px 0;'>For <strong>Living Mainframe</strong> Professional Consultant Interview</p>
    <p style='margin: 5px 0; font-size: 14px;'>Technologies: Python • Streamlit • Google Gemini AI (Free Tier)</p>
    <p style='margin-top: 15px; font-size: 12px; color: #999;'>
        Based on real experience optimizing mainframe batch jobs at AIG USA<br>
        Achieved 40% reduction in batch window (6 hours → 3.6 hours)
    </p>
</div>
""", unsafe_allow_html=True)